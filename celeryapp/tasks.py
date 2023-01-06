from celery import shared_task
import requests
import os
import subprocess, logging, json
from scans.models import Vulnerability, Analysis
from django.db import transaction

@shared_task()
def run_scan_repository(scanid):
    with transaction.atomic():
        scan_details = Analysis.objects.get(analysisid=scanid)
        process = subprocess.Popen('trufflehog git ' + scan_details.repositoryurl + ' --json --entropy', stdout=subprocess.PIPE, shell=True)
        scan_string = '[' + process.stdout.read().decode().strip().replace("}\n{", "},{") + ']'
        json_data = json.loads(scan_string)
        for jd in json_data:
            vulnverifiedstatus = ''
            match jd['Verified']:
                case True:
                    vulnverifiedstatus = Vulnerability.VulnerabilityVerificationStatus.VERIFIEDVULNERABILITY
                case _:
                    vulnverifiedstatus = Vulnerability.VulnerabilityVerificationStatus.UNVERIFIED
            Vulnerability.objects.create(userid="",analysisid=scan_details.analysisid,vulnerabilitytitle="",vulnerabilitydescription="",category=jd['DetectorName'],severity="High",filename=jd['SourceMetadata']['Data']['Git']['file'],lineofcode=jd['SourceMetadata']['Data']['Git']['line'],commitid=jd['SourceMetadata']['Data']['Git']['commit'],falsepositive=False,snippet=jd['Raw'],verificationstatus=vulnverifiedstatus)
        scan_details.state = "Done"
        scan_details.save()

@shared_task()
def verify_vulnerability_task(vulnerabilityid):
    with transaction.atomic():
        vuln_details = Vulnerability.objects.get(vulnerabilityid=vulnerabilityid)

        match vuln_details.category:
            case "Github":
                headers = {'Authorization': 'Bearer ' + vuln_details.snippet}
                res = requests.get('https://api.github.com/user', headers=headers)
                if res.status_code == 200:
                    vuln_details.verificationstatus = Vulnerability.VulnerabilityVerificationStatus.VERIFIEDVULNERABILITY
                    vuln_details.save()
                elif res.status_code == 401:
                    vuln_details.verificationstatus = Vulnerability.VulnerabilityVerificationStatus.VERIFIEDFALSEPOSITIVE
                    vuln_details.save()
            case "Gitlab":
                res = requests.get('https://gitlab.com/api/v4/projects?private_token=' + vuln_details.snippet)
                if res.status_code == 200:
                    vuln_details.verificationstatus = Vulnerability.VulnerabilityVerificationStatus.VERIFIEDVULNERABILITY
                    vuln_details.save()
                elif res.status_code == 401:
                    vuln_details.verificationstatus = Vulnerability.VulnerabilityVerificationStatus.VERIFIEDFALSEPOSITIVE
                    vuln_details.save()
            case "Slack":
                res = requests.post('https://slack.com/api/auth.test?token=' + vuln_details.snippet)
                if res.status_code == 200:
                    rdata = res.json()
                    if rdata['ok'] != False:
                        vuln_details.verificationstatus = Vulnerability.VulnerabilityVerificationStatus.VERIFIEDVULNERABILITY
                        vuln_details.save()
                    else:
                        vuln_details.verificationstatus = Vulnerability.VulnerabilityVerificationStatus.VERIFIEDFALSEPOSITIVE
                        vuln_details.save()
                elif res.status_code == 401:
                    vuln_details.verificationstatus = Vulnerability.VulnerabilityVerificationStatus.VERIFIEDFALSEPOSITIVE
                    vuln_details.save()
            case "SlackWebhook":
                headers = {'Content-type': 'application/json'}
                data = {'text':''}
                res = requests.post(vuln_details.snippet, headers=headers, data=data)
                if res.status_code == 200:
                    vuln_details.verificationstatus = Vulnerability.VulnerabilityVerificationStatus.VERIFIEDVULNERABILITY
                    vuln_details.save()
                elif res.status_code in [401,403]:
                    vuln_details.verificationstatus = Vulnerability.VulnerabilityVerificationStatus.VERIFIEDFALSEPOSITIVE
                    vuln_details.save()