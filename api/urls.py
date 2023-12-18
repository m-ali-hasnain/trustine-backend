
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView,
    UserLoginView,
    CourseViewSet,
    CourseRegistrationViewSet,
    UserView
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'registrations', CourseRegistrationViewSet)

urlpatterns = [
    path('token/obtain', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('users/<int:pk>/courses', UserView.as_view(), name='registered_courses' ),
    path('', include(router.urls))
]