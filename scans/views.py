import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
import subprocess, logging, json
from .models import Vulnerability, Analysis


def new_scan(request):
    if request.method == "GET":
        context = {}
        return render(request, 'scans/newscan.html', context)
    elif request.method == "POST":
        scan_obj = Analysis.objects.create(userid="",repositoryurl=request.POST['repositoryurl'],name=request.POST['analysisname'],state="New")
        return redirect("/scans/detailedscan/" + str(scan_obj.analysisid) + "/")


def trigger_scan(request, scanid):
    scan_details = Analysis.objects.get(analysisid=scanid)
    process = subprocess.Popen('trufflehog git ' + scan_details.repositoryurl + ' --json', stdout=subprocess.PIPE, shell=True)
    scan_string = '[' + process.stdout.read().decode().strip().replace("}\n{", "},{") + ']'
    json_data = json.loads(scan_string)
    scan_details.state = "Done"
    scan_details.save()
    for jd in json_data:
        Vulnerability.objects.create(userid="",analysisid=scan_details.analysisid,vulnerabilitytitle="",vulnerabilitydescription="",category=jd['DetectorName'],severity="High",filename=jd['SourceMetadata']['Data']['Git']['file'],lineofcode=jd['SourceMetadata']['Data']['Git']['line'],commitid=jd['SourceMetadata']['Data']['Git']['commit'],falsepositive=False,snippet=jd['Redacted'])
    return redirect("/scans/detailedscan/" + str(scanid))


def list_scans(request):
    scans_list = Analysis.objects.all()

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


def detailed_scan(request, scanid):
    scan_details = Analysis.objects.get(analysisid=scanid)
    scan_vulns = Vulnerability.objects.filter(analysisid=scanid)
    context = {'scan_details': scan_details, 'scan_vulns': scan_vulns}
    return render(request, "scans/detailedscan.html", context)