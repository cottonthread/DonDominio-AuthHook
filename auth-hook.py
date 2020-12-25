#!/usr/bin/python3
import os, json, requests, time, smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formatdate

# Colección de datos preparativos
apiconf = open("api.conf")
apiconf = apiconf.readlines()
apiuser = apiconf[0].strip()
apipasswd = apiconf[1].strip()
emailserver = apiconf[2].strip()
emailport = apiconf[3].strip()
emailuser = apiconf[4].strip()
emailpasswd = apiconf[5].strip()
url1 = "https://simple-api.dondominio.net/service/dnslist/"
url2 = "https://simple-api.dondominio.net/service/dnsupdate/"
url3 = "https://simple-api.dondominio.net/service/dnscreate/"
certbot_domain = str(os.getenv('CERTBOT_DOMAIN'))
certbot_validation = str(os.getenv('CERTBOT_VALIDATION'))
certbot_token = os.getenv('CERTBOT_TOKEN')
certbot_remaining_challenges = str(os.getenv('CERTBOT_REMAINING_CHALLENGES'))
certbot_all_domains = str(os.getenv('CERTBOT_ALL_DOMAINS'))
name = "_acme-challenge." + certbot_domain
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

# Mostrar información recibida de Certbot
print("Reciveced from Certbot:\nDomain: ", certbot_domain, "\tValidation:", certbot_validation, "\nToken:", certbot_token, "\tRemaining Challenges:", certbot_remaining_challenges, "\tAll Domains:", certbot_all_domains, "\n" + "*" * 20)

# Comienza la comunicación con DonDominio
print("Comunicating with DonDominio:")

# Ensamblar los datos de petición para la lista de DNS
dataurl1 = {'apiuser': apiuser, 'apipasswd': apipasswd, 'name': name, 'serviceName': certbot_domain}

# Obtención de resultados
response = json.loads(requests.post(url1, data=dataurl1).text)

if response.get('success') is True:
	for key, value in response.items():
		if key == "responseData":
			pass
		else:
			print(key, value)
	keys = response.get('responseData').get('dns')
	for key in keys:
		if name in key.values():
		# Positivo en capturar el entityID del "_acme-challenge."+certbot_domain
			print(key.get('name'), "has entityID", key.get('entityID'))
			entityID = key.get('entityID')
			print ("*" * 20)
			if key.get('value') == certbot_validation:
			# Si el valor del registro certbot_validation es el mismo que la pre-existencia
				print("Value you going to update is the same as you recived from Certbot, look:")
				for item, value in key.items():
					print(item + ":", value)
				print ("*" * 20)
			else:
			# Si el valor del registro certbot_validation NO es el mismo que la pre-existencia
				print("Update", key.get('value'), "to", certbot_validation)
				print ("*" * 20)
				# Ensamblar los datos de petición para la actualización del registro certbot_validation
				dataurl2 = {'apiuser': apiuser, 'apipasswd': apipasswd, 'name': name, 'serviceName': certbot_domain, 'entityID': entityID, 'value': certbot_validation}
				# Obtención de resultados
				response = json.loads(requests.post(url2, data=dataurl2).text)
				print("Done, results:")
				if response.get('success') is True:
					for key, value in response.items():
						if key == "responseData":
							pass
						else:
							print(key, value)
				else:
					for key, value in response.items():
						print(key, value)
						# Se envía un correo electrónico con el resultado de error en la respuesta del API de DonDominio
						email("Error modificating DNS TXT in DonDominio!", json.dumps(response, indent = 2))
			print ("*" * 20)
			break
		else:
		# Negativo en capturar el entityID del "_acme-challenge."+certbot_domain
			print(name, "is not in", certbot_domain, "so creating...")
			# Ensamblar los datos de petición para la creación del registro certbot_validation
			dataurl3 = {'apiuser': apiuser, 'apipasswd': apipasswd, 'name': name, 'serviceName': certbot_domain, 'type': "TXT", 'value': certbot_validation, "ttl": 600}
			# Obtención de resultados
			response = json.loads(requests.post(url3, data=dataurl3).text)
			print("Done, results:")
			if response.get('success') is True:
				for key, value in response.items():
					if key == "responseData":
						pass
					else:
						print(key, value)
			else:
				for key, value in response.items():
					print(key, value)
				# Se envía un correo electrónico con el resultado de error en la respuesta del API de DonDominio
				email("Error creating DNS Zone in DonDominio!", json.dumps(response, indent = 2))
		print ("*" * 20)
	time.sleep(25)
else:
	for key, value in response.items():
		print(key, value)
	# Se envía un correo electrónico con el resultado de error en la respuesta del API de DonDominio
	email("Error getting DNS list from DonDominio!", json.dumps(response, indent = 2))
	
