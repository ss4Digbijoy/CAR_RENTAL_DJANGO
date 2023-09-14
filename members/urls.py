from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('account/', views.acc, name='acc'),
    path('logout/', views.logout, name='logout'),
    path('rent/', views.rent, name='rent'),
    path('history/', views.history, name='history'),
    path('pay/', views.pay, name='pay'),
    path('payhistory/', views.payhistory, name='payhistory'),








]
