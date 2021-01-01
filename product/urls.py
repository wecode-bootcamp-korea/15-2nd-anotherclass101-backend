from django.urls import path,include
from .views import CourseListView,ProductLikeView,EarlybirdView,OrderByLikeView

urlpatterns = [
    path('/category/<int:category_pk>', CourseListView.as_view()),  
    path('/status', EarlybirdView.as_view()),
    path('/orderbylike', OrderByLikeView.as_view()),
    path('/like', ProductLikeView.as_view())
]
