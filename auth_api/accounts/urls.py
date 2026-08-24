from django.urls import path,include
from . import views

urlpatterns = [
    path('register',views.UserRegistrationView.as_view(),name="register"),
    path('login',views.UserLoginView.as_view(),name="login"),
    path('profile',views.UserProfileView.as_view(),name="profile"),
    path('changepassword',views.UserChangePasswordView.as_view(),name="changepassword"),
    path('send-reset-password',views.UserResetPasswordView.as_view(),name="resetpassword"),
    path('reset-password-done/<uid>/<token>',views.UserResetPasswordDoneView.as_view(),name="resetpassworddone"),
]
