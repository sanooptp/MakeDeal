from django.urls import path
from restframework import views
from rest_framework_simplejwt.views import TokenRefreshView
from .api import RegistrationAPI,LoginAPI,UserAPI
from knox import views as knox_views



urlpatterns = [
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path("",views.ListTodoAPIView.as_view(),name="todo_list"),
    path("create/", views.CreateTodoAPIView.as_view(),name="todo_create"),
    path("update/<int:pk>/",views.UpdateTodoAPIView.as_view(),name="update_todo"),
    path("delete/<int:pk>/",views.DeleteTodoAPIView.as_view(),name="delete_todo"),
    path('testapi',views.ApitestView.as_view(), name='testapi'),
    path('loginapi/', views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('loginapi/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('user/', UserAPI.as_view()),
]