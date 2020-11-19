from account import views

from django.urls import path

app_name = 'account'

urlpatterns = [
    # path('my-profile/<int:pk>/', views.MyProfile.as_view(), name='my_profile'),
    path('my-profile/', views.MyProfile.as_view(), name='my_profile'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('activate/<str:username>', views.ActivateUser.as_view(), name='activate'),
    path('password_change/', views.ChangePasswordUserView.as_view(), name='password-change'),
    path('password_change_done/', views.ChangePasswordUserDoneView.as_view(), name='password-change-done'),

]
