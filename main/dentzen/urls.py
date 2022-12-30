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
    path('clinics/', views.ClinicIndexView.as_view()),
    path('clinics/<int:id>/', views.ClinicShowView.as_view()),
    path('clinics/<int:clinic_id>/dentists/', views.ClinicDentistsView.as_view()),
    path('clinics/<int:clinic_id>/suppliers/', views.ClinicSuppliersView.as_view()),

    path('supplier-contracts/', views.SupplierClinicContractIndexView.as_view()),
    path('supplier-contracts/<int:id>/', views.SupplierClinicContractShowView.as_view()),

    path('suppliers/', views.SupplierIndexView.as_view()),
    path('suppliers/<int:id>/', views.SupplierShowView.as_view()),
    path('suppliers/<int:supplier_id>/products/', views.SupplierProductsIndexView.as_view()),
    path('suppliers/<int:supplier_id>/products/<str:type>', views.SupplierProductsIndexView.as_view()),
    path('suppliers/<int:supplier_id>/products/<int:id>/', views.SupplierProductsIndexView.as_view()),
    path('suppliers/<int:supplier_id>/products/<int:id>/<str:type>/', views.SupplierProductsIndexView.as_view()),

    path('dentist-contracts/', views.DentistClinicContractIndexView.as_view()),
    path('dentist-contracts/<int:id>/', views.DentistClinicContractShowView.as_view()),

    path('dentists/', views.DentistIndexView.as_view()),
    path('dentists/<int:id>/', views.DentistShowView.as_view()),
    path('dentists/<int:dentist_id>/appointments/', views.DentistAppointmentView.as_view()),

    path('appointments/', views.AppointmentIndexView.as_view()),
    path('appointments/<int:id>/', views.AppointmentShowView.as_view()),

    path('patients/', views.PatientIndexView.as_view()),
    path('patients/<int:id>/', views.PatientShowView.as_view()),
    path('patients/<int:patient_id>/diseases/', views.DiseaseIndexView.as_view()),
    path('patients/<int:patient_id>/diseases/<int:id>', views.DiseaseShowView.as_view()),
    path('patients/<int:patient_id>/appointments/', views.PatientAppointmentView.as_view()),
]
