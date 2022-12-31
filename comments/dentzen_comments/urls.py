"""dentzen_comments URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from comments_app import views

urlpatterns = [
    path('clinics/<int:parent_id>/comments/', views.ClinicCommentsIndexView.as_view()),
    path('clinics/<int:parent_id>/comments/<str:comment_id>/', views.ClinicCommentsShowView.as_view()),
    path('suppliers/<int:parent_id>/comments/', views.SupplierCommentsIndexView.as_view()),
    path('suppliers/<int:parent_id>/comments/<str:comment_id>/', views.SupplierCommentsShowView.as_view()),
]
