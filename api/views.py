from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, generics, filters, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .models import Category, Genre, Title, User, Review, Comment
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, EmailSerializer, TokenGainSerializer, \
    UserSerializer, ReviewSerializer, CommentSerializer
from .permissions import AdminPermission, IsAdminOrReadOnly, IsAuthenticatedRole


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre__slug', 'name', 'year')

    def perform_create(self, serializer):
        category = get_object_or_404(Category, slug=self.request.data.get('category'))
        geners = []
        for slug in self.request.data.getlist('genre'):
            genre = get_object_or_404(Genre, slug=slug)
            geners.append(genre)
        serializer.save(category=category, genre=geners)


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    permission_classes = (IsAdminOrReadOnly,)


class CategoryDestroy(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (AdminPermission,)


class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    permission_classes = (IsAdminOrReadOnly,)


class GenreDestroy(generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (AdminPermission,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedRole,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        reviews = get_object_or_404(Title, pk=title_id).reviews
        return reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        reviews = get_object_or_404(Title, pk=title_id).reviews.all()
        review_id = self.kwargs.get('review_id')
        comment = get_object_or_404(reviews, pk=review_id).comments
        return comment.all()

    def perform_create(self, serializer):
        #title_id = self.kwargs.get('title_id')
        #reviews = get_object_or_404(Title, pk=title_id).reviews.all()
        review_id = self.kwargs.get('review_id')
        serializer.save(author=self.request.user)

@api_view(['POST'])
def send_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)
    email = request.data['email']
    if serializer.is_valid():
        user = User.objects.filter(email=email).exists()
        if not user:
            User.objects.create_user(email=email)
        user = get_object_or_404(User, email=email)
        confirmation_code = default_token_generator.make_token(user)
        mail_subject = 'Confirmation code'
        message = f'Your code: {confirmation_code}'
        send_mail(mail_subject, message, '<admin@yamdb.ru>', (request.data.get('email'),), fail_silently=False)
        return Response(f'Code send to {email}', status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = TokenGainSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, email=email)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Wrong confirmation code'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]


class UserInfo(APIView):
    def get(self, request):
        queryset = User.objects.get(username=request.user.username)
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
