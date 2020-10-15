from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('create-user/', views.CreateUserView.as_view(), name='create'),
    path('get-token/', views.CreateTokenView.as_view(), name='token'),
    path('current-user/', views.ManageUserView.as_view(), name='me'),
]
