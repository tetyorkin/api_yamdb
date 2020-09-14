from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .models import Category, Genre, Review, Title, User
from .permissions import (AdminPermission, IsAdminOrModeratorOrReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          EmailSerializer, GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenGainSerializer, UserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(Avg('review__score'))
    filter_class = TitleFilter
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleReadSerializer
        return TitleWriteSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminOrModeratorOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        return review.comment.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        author = self.request.user
        serializer.save(author=author, review=review)


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', )


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly)
    filter_backends = [filters.SearchFilter]
    search_fields = ('=name',)
    lookup_field = 'slug'


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)
    email = request.data['email']
    serializer.is_valid(raise_exception=True)
    user = User.objects.filter(email=email).exists()
    if not user:
        User.objects.create_user(email=email)
    user = get_object_or_404(User, email=email)
    confirmation_code = default_token_generator.make_token(user)
    mail_subject = 'Confirmation code'
    message = f'Your code: {confirmation_code}'
    send_mail(mail_subject, message, '<admin@admin.ru>',
              (request.data.get('email'),), fail_silently=False)
    return Response(f'Code send to {email}')


@api_view(['POST'])
def get_jwt_token(request):
    serializer = TokenGainSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': f'{token}'})
    return Response({'confirmation_code': 'Wrong confirmation code'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    pagination_class = PageNumberPagination

    @action(detail=False, url_path='me', permission_classes=(IsAuthenticated,))
    def user_info(self, request):
        serializers = UserSerializer(self.request.user)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @user_info.mapping.patch
    def new_user_info(self, request):
        serializers = UserSerializer(
            self.request.user, data=self.request.data, partial=True
        )
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminOrModeratorOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title).all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
