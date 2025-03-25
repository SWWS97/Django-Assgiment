from django.contrib.auth.views import LogoutView
from django.urls import path
from member import cb_views as member_cb_views

urlpatterns = [
    path('signup/', member_cb_views.SignupView.as_view(), name='signup'),
    path('login/', member_cb_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/', member_cb_views.verify_email, name='verify_email'),
]