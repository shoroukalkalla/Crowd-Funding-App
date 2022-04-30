from django.urls import path, re_path

from .views import SignIn, signup, home, activate

urlpatterns = [
    # path("signup/", SignUpView.as_view(), name="signup"),
    path("signup/", signup, name="signup"),
    path('home', home, name='home'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate'),
    # path('activate/<uidb64>/<token>/', activate, name='activate'),
]
