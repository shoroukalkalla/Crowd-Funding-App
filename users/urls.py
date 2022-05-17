from django.urls import path, re_path

from .views import SignIn, signup, home, activate, profile, EditProfile, DeleteUser, PasswordChange, PasswordReset, PasswordResetSet ,get_top_latest_projects

urlpatterns = [
    # path("signup/", SignUpView.as_view(), name="signup"),
    path('', get_top_latest_projects,name="home"),
    path("register/", signup, name="signup"),
    path('login/', SignIn.as_view(), name='login'),
    path('password_change/', PasswordChange.as_view(), name="password_change"),
    path('password_reset/', PasswordReset.as_view(), name="password_reset"),
    path('reset/<uidb64>/<token>/', PasswordResetSet.as_view(), name="set_password"),
    path('profile/<pk>', EditProfile.as_view(), name='profile'),
    path('profile/delete/<pk>', DeleteUser.as_view(), name='delete_user'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate'),
    # path('activate/<uidb64>/<token>/', activate, name='activate'),
]
