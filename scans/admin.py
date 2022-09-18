from django.contrib import admin
from .models import Vulnerability, Analysis
# Register your models here.
admin.site.register(Vulnerability)
admin.site.register(Analysis)