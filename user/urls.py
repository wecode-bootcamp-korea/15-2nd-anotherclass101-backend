from django.urls import path

from user.views import (
                            SignUpView,
                            SignInView,
                            SMSVerificationView,
                            SMSVerificationConfirmView,
                            KakaoSignInView,
                            ProfileView,
                            ProfileImageView,
                            ProfileDataView,
                        )

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/sms', SMSVerificationView.as_view()),
    path('/sms_verification', SMSVerificationConfirmView.as_view()),
    path('/kakao', KakaoSignInView.as_view()),
    path('/profile', ProfileView.as_view()),
    path('/profileimage', ProfileImageView.as_view()),
    path('/profiledata', ProfileDataView.as_view()),
]