from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'titles', views.TitleViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

auth = [
    path('email/', views.send_confirmation_code),
    path('token/', views.get_jwt_token),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth)),
]
