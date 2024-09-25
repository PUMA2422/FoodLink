from django.urls import path
from .views import RegisterView, ObtainTokenView,login_view,signup_view, home_view, dashboard_view, check_email,check_username, new_order_view

urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/new-order/', new_order_view, name='add_order'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', ObtainTokenView.as_view(), name='token_obtain'),
    path('api/check-username/', check_username, name='check_username'),
    path('api/check-email/', check_email, name='check_email'),
]
