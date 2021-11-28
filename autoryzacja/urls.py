from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from autoryzacja.views import RegisterView, LoginView, UserView

urlpatterns = [
    path('rejestracja/', RegisterView.as_view(), name='rejestracja'),
    path('login/', LoginView.as_view(), name='login'),
    path('profil/', UserView.as_view(), name='profil'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
