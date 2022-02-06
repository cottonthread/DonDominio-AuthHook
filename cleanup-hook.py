#!/usr/bin/python3
import os, json, requests, time, smtplib
from tld import get_fld
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formatdate

# Colección de datos preparativos
home = os.path.expanduser("~")
apiconf = open(home + "/DonDominio-AuthHook/api.conf")
apiconf = apiconf.readlines()
apiuser = apiconf[0].strip()
apipasswd = apiconf[1].strip()
emailserver = apiconf[2].strip()
emailport = apiconf[3].strip()
emailuser = apiconf[4].strip()
emailpasswd = apiconf[5].strip()
url1 = "https://simple-api.dondominio.net/service/dnslist/"
url2 = "https://simple-api.dondominio.net/service/dnsdelete/"
certbot_domain = str(os.getenv('CERTBOT_DOMAIN'))
certbot_validation = str(os.getenv('CERTBOT_VALIDATION'))
certbot_token = os.getenv('CERTBOT_TOKEN')
certbot_remaining_challenges = str(os.getenv('CERTBOT_REMAINING_CHALLENGES'))
certbot_all_domains = str(os.getenv('CERTBOT_ALL_DOMAINS'))
name = "_acme-challenge." + certbot_domain
serviceName = get_fld("http://" + certbot_domain)
entityID=""

def email(title, msg):
	msg = MIMEText(msg, 'plain', 'utf-8')
	msg['Date'] = formatdate()
	msg['From'] = emailuser
	msg['To'] = emailuser
	msg['Subject'] = Header(title, 'utf-8').encode()
	smtp = smtplib.SMTP(emailserver, emailport)
	smtp.set_debuglevel(1)
	smtp.starttls()
	smtp.login(emailuser, emailpasswd)
	smtp.sendmail(emailuser, emailuser, msg.as_string())
	smtp.quit()

def updatedns(url, data):
	dnsresult = json.loads(requests.post(url, data=data).text)
	return dnsresult

dataurl1 = {'apiuser': apiuser, 'apipasswd': apipasswd, 'serviceName': serviceName, 'filter': '_acme-challenge'}
response = json.loads(requests.post(url1, data=dataurl1).text)

for record in response.get('responseData')['dns']:
	dataurl2 = {'apiuser': apiuser, 'apipasswd': apipasswd, 'serviceName': serviceName, 'entityID': record['entityID']}
	dnsresult = updatedns(url2, dataurl2)
