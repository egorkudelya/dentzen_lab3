"""dentzen URL Configuration

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
from dentzen_app import views


urlpatterns = [
    path('dentists/<int:id>/', views.DentistShowView.as_view()),
    path('dentists/', views.DentistIndexView.as_view()),
    path('clinics/<int:id>/', views.ClinicShowView.as_view()),
    path('clinics/', views.ClinicIndexView.as_view()),
    path('dentist-contracts/<int:id>/', views.DentistClinicContractShowView.as_view()),
    path('dentist-contracts/', views.DentistClinicContractIndexView.as_view()),
    path('patients/<int:id>/', views.PatientShowView.as_view()),
    path('patients/', views.PatientIndexView.as_view()),
    path('patients/<int:patient_id>/diseases/<int:id>', views.DiseaseShowView.as_view()),
    path('patients/<int:patient_id>/diseases/', views.DiseaseIndexView.as_view()),
]
