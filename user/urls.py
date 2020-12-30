from django.urls import path

from user.views import (
                            SignUpView,
                            SignInView,
                            SMSVerificationView,
                            SMSVerificationConfirmView,
                            KakaoSignInView,
                        )

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/sms', SMSVerificationView.as_view()),
    path('/sms_verification', SMSVerificationConfirmView.as_view()),
    path('/kakao', KakaoSignInView.as_view()),
]