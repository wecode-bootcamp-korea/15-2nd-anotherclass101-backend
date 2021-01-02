from django.urls import path

from request.views import CategoryListView, SingleRequestCreateView, RequestView, RequestBasicInfoView, RequestTitleView, RequestIntroView

urlpatterns= [
    path('/main', RequestView.as_view()),
    path('/basicinfo', RequestBasicInfoView.as_view()),
    path('/title', RequestTitleView.as_view()),
    path('/intro', RequestIntroView.as_view()),
    path('/create', SingleRequestCreateView.as_view()),
    path('/category', CategoryListView.as_view()),
]
