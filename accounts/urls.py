from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('log_in/', views.log_in, name='log-in'),
    path('sign_up/', views.sign_up, name='sign-up'),
    path('log_out/', views.log_out, name='log-out'),
]
