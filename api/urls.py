from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'titles', views.TitleViewSet)

urlpatterns = [
    path('v1/users/me/', views.UserInfo.as_view()),
    path('v1/', include(router.urls)),
    path('v1/genres/', views.GenreList.as_view()),
    path('v1/genres/<slug:slug>/', views.GenreDestroy.as_view()),
    path('v1/categories/', views.CategoryList.as_view()),
    path('v1/categories/<slug:slug>/', views.CategoryDestroy.as_view()),
    path('v1/auth/email/', views.send_confirmation_code),
    path('v1/auth/token/', views.get_jwt_token),
]
