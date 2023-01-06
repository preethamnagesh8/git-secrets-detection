from django.urls import path

from . import views

urlpatterns = [
    path('newscan', views.new_scan, name='new_scan'),
    path('listscans/', views.list_scans, name='list_scan'),
    path('errorpage/', views.list_scans, name='list_scan'),
    path('triggerscan/<scanid>', views.trigger_scan, name='trigger_scan'),
    path('detailedscan/<scanid>/', views.detailed_scan, name='detailed_scan'),
    path('detailedscan/<scanid>/verifyvulnerability/<vulnerabilityid>/', views.verify_vulnerability, name='verify_vulnerability'),
]