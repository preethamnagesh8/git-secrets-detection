from django.db import models
import uuid

# Create your models here.

class Vulnerability(models.Model):
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


class Analysis(models.Model):
    analysisid = models.CharField(max_length=40, primary_key=True, default=uuid.uuid4)
    userid = models.CharField(max_length=50)
    startedat = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    repositoryurl = models.TextField()
    name = models.CharField(max_length=250)
    state = models.CharField(max_length=100)
