"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from myapi import views
from mainApp.urls import schema_view
urlpatterns = [
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.RegisterAPI.as_view(), name="register"),
    path("login/", views.LoginAPI.as_view(), name="login"),
    path("is-logged-in/", views.isLoggedin, name="is-logged-in"),
    path("getUser/",views.getUser),
    path("addExpense/",views.AddExpense.as_view(),name="addExpense"),
    path("getExpense/<int:id>",views.getExpense),
    path("getUserExpenses/<str:username>",views.getUserExpenses),
    path("getOverallExpenses/",views.getOverallExpenses),
    path("getBalanceSheet/<str:username>",views.getBalanceSheet),
    path("downloadBalanceSheet/<str:username>",views.downloadBalanceSheet)
]
