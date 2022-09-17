from django.shortcuts import render
from django.http import HttpResponse
import subprocess, logging, json


def new_scan(request):
    context = {}
    return render(request, 'scans/newscan.html', context)


def trigger_scan(request):
    logging.warning("Starting Scan")
    repositoryurl = "https://github.com/preethamnagesh8/DevSecOps1"
    process = subprocess.run(['trufflehog', 'git', repositoryurl, '--json'], stdout=subprocess.PIPE)
    scan_results = json.loads(process.stdout.strip())
    logging.warning(scan_results)
    return HttpResponse('Scan Started')


def view_scans(request):
    context = {}
    return None