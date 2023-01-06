from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.auth.models import User, Group
from django.conf import settings

# Create your models here.

class Vulnerability(models.Model):

    class VulnerabilityVerificationStatus(models.TextChoices):
        UNVERIFIED = 'UV', _('Unverified')
        VERIFIEDVULNERABILITY = 'VV', _('Verified Vulnerable')
        VERIFIEDFALSEPOSITIVE = 'VF', _('Verified False Positive')
        VERIFICATIONERROR = 'VE', _('Verification Error')

    vulnerabilityid = models.CharField(max_length=30, primary_key=True, default=uuid.uuid4)
    userid = models.CharField(max_length=50)
    analysisid = models.CharField(max_length=50)
    vulnerabilitytitle = models.CharField(max_length=100)
    vulnerabilitydescription = models.CharField(max_length=250)
    category = models.CharField(max_length=30)
    severity = models.CharField(max_length=30)
    filename = models.CharField(max_length=500)
    lineofcode = models.PositiveIntegerField()
    commitid = models.CharField(max_length=100)
    snippet = models.TextField()
    falsepositive = models.BooleanField()
    verificationstatus = models.CharField(max_length=2, choices=VulnerabilityVerificationStatus.choices, default=VulnerabilityVerificationStatus.UNVERIFIED)


class Analysis(models.Model):
    analysisid = models.CharField(max_length=40, primary_key=True, default=uuid.uuid4)
    startedat = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    repositoryurl = models.TextField()
    name = models.CharField(max_length=250)
    state = models.CharField(max_length=100)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)