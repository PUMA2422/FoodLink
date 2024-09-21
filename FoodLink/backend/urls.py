from django.urls import path
from .views import RegisterView, ObtainTokenView,login_view,signup_view, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', ObtainTokenView.as_view(), name='token_obtain'),
]
