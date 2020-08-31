from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


router = DefaultRouter()
router.register(r'titles', views.TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/genres/', views.GenreList.as_view()),
    path('v1/genres/<slug:slug>/', views.GenreDestroy.as_view()),
    path('v1/categories/', views.CategoryList.as_view()),
    path('v1/categories/<slug:slug>/', views.CategoryDestroy.as_view()),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
