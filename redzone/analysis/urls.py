from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

# app_name='rooms'

urlpatterns = [
    # path('<str:param>/', views.APITestView.as_view(), name='api_test_view'),
    path('create_user/', views.UserCreationView.as_view(), name='user_creation_view'),
    path('user_list/', views.UserListView.as_view(), name='user_list_view'),
    path('user_detail/', views.UserDetailView.as_view(), name='user_detail_view'),
    path('get_auth_token/', obtain_auth_token, name='api_token_auth'),
]