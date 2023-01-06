import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
import subprocess, logging, json
from .models import Vulnerability, Analysis
from celeryapp.tasks import run_scan_repository, verify_vulnerability_task
from django.contrib.auth.decorators import login_required

@login_required
def new_scan(request):
    if request.method == "GET":
        context = {}
        return render(request, 'scans/newscan.html', context)
    elif request.method == "POST":
        scan_obj = Analysis.objects.create(userid=request.user,repositoryurl=request.POST['repositoryurl'],name=request.POST['analysisname'],state="New")
        return redirect("/scans/detailedscan/" + str(scan_obj.analysisid) + "/")

@login_required
def trigger_scan(request, scanid):
    scan_details = Analysis.objects.get(analysisid=scanid)
    Vulnerability.objects.filter(analysisid=scanid).delete()
    scan_details.state = "In Progress"
    scan_details.save()
    run_scan_repository.delay(scanid)
    return redirect("/scans/detailedscan/" + str(scanid))

@login_required
def list_scans(request):
    scans_list = Analysis.objects.filter(userid=request.user)

    name_filter = "None"
    status_filter = "None"

    if 'name' in request.GET and request.GET['name'] != "None":
        name_filter = request.GET['name']
        scans_list = scans_list.filter(name__contains=request.GET['name'])

    if 'status' in request.GET and request.GET['status'] != "None":
        status_filter = request.GET['status']
        scans_list = scans_list.filter(state=status_filter)

    context = {'scans_list': scans_list}
    return render(request, "scans/listscans.html", context)

@login_required
def detailed_scan(request, scanid):
    try:
        scan_details = Analysis.objects.get(analysisid=scanid, userid=request.user)
    except Analysis.DoesNotExist:
        context = {'error_msg': "Unauthorized Access Detected. This action will be reported."}
        return render(request, "scans/error.html", context)
    scan_vulns = Vulnerability.objects.filter(analysisid=scanid)
    context = {'scan_details': scan_details, 'scan_vulns': scan_vulns, 'error': False}
    return render(request, "scans/detailedscan.html", context)

@login_required
def verify_vulnerability(request, scanid, vulnerabilityid):
    vuln_details = Vulnerability.objects.get(vulnerabilityid=vulnerabilityid)
    verify_vulnerability_task.delay(vulnerabilityid)
    return redirect("/scans/detailedscan/" + str(scanid))


def error_page(request):
    return render(request, "scans/error.html")