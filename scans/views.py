from django.shortcuts import render
from django.http import HttpResponse
import subprocess, logging


def new_scan(request):
    context = {}
    return render(request, 'scans/newscan.html', context)


def trigger_scan(request):
    logging.warning("Starting Scan")
    repositoryurl = "https://github.com/preethamnagesh8/DevSecOps1"
    process = subprocess.run(['trufflehog', 'git', repositoryurl, '--json'], stdout=subprocess.PIPE)
    logging.warning(process.stdout)
    return HttpResponse('Scan Started')


def view_scans(request):
    context = {}
    return None