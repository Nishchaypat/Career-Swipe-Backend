"""
URL configuration for cpanel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from mypy_extensions import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.info, name='info'),
    path('firstspage/', views.firstspage, name='firstspage'),
    path('signin/', views.signin, name='signin'),
    path('signup/',views.signup,name='signup'),
    path('Rsignin/', views.Rsignin, name='Rsignin'),
    path('Rsignup/', views.Rsignup, name='Rsignup'),
    path('postRsignin/', views.postRsignin, name='/postRsignin/'),
    path('postRsignup/', views.postRsignup, name='/postRsignup/'),
    path('postsignin/', views.postsignin, name='/postsignin/'),
    path('logout/',views.logout,name='log'),
    path('Rforgotpassword/',views.Rforgotpassword,name='Rforgotpassword'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    path('search/',views.search,name='search/'),
    path('favStudent/', views.favStudent, name='favStudent'),
    path('results/',views.results,name='results'),
    #path('favourite/',views.favourite,name='favourite'),
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('reupload/',views.reupload,name='reupload'),
    path('postsignup/', views.postsignup, name='/postsignup/'),
    path('uploadfile/', views.uploadfile, name='/uploadfile/'),
    path('postfilter/', views.postfilter, name='postfilter'),
    path('postforgotpassword/', views.postforgotpassword, name='/postforgotpassword/'),
    path('remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    path('postRforgotpassword/', views.postRforgotpassword, name='/postRforgotpassword/')
    #path('microsoft-login/', views.microsoft_login, name='microsoft_login')
]