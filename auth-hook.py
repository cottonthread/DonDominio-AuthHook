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
url2 = "https://simple-api.dondominio.net/service/dnsupdate/"
url3 = "https://simple-api.dondominio.net/service/dnscreate/"
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

def verification(name, array):
	# Verificar si el dominio en cuestión está dentro de la tabla recibida.
	for value in array:
		if name in value.values():
			return True, value
		else:
			pass
	return False, "Not Found!"

def updatedns(url, data):
	# Actualizar/Crear el registro de DNS
	dnsresult = json.loads(requests.post(url, data=data).text)
	return dnsresult

# Mostrar información recibida de Certbot
print("Reciveced from Certbot:\nDomain: ", certbot_domain, "\tValidation:", certbot_validation, "\nToken:", certbot_token, "\tRemaining Challenges:", certbot_remaining_challenges, "\tAll Domains:", certbot_all_domains, "\n" + "*" * 20)

# Comienza la comunicación con DonDominio
print("Comunicating with DonDominio:")

# Ensamblar los datos de petición para la lista de DNS
dataurl1 = {'apiuser': apiuser, 'apipasswd': apipasswd, 'serviceName': serviceName}

# Obtención de resultados
response = json.loads(requests.post(url1, data=dataurl1).text)

if response.get('success') is True:
# Si se ha podido comunicar con DonDominio
	for key, value in response.items():
		if key == "responseData":
			pass
		else:
			print(key, value)
	keys = response.get('responseData').get('dns')
	if verification(name, keys)[0] is True:
	# Positivo en capturar el entityID del "_acme-challenge." + certbot_domain
		verificationresult = verification(name, keys)[1]
		entityID = verificationresult.get('entityID')
		print(name, "has entityID", entityID)
		if verificationresult.get('value') == certbot_validation:
		# Si el valor de Value es lo mismo que ya pre-existe, salir de la aplicación directamente
			print("Same value of", name + ":", verificationresult.get('value'))
			quit()
		else:
		# Si el valor de Value NO es lo que pre-existe, proceder a la actualización
			print("Updating", certbot_validation, "to", name)
			dataurl2 = {'apiuser': apiuser, 'apipasswd': apipasswd, 'serviceName': serviceName, 'entityID': entityID, 'value': certbot_validation}
			# Ensamblar los datos de petición para la actualización del registro certbot_validation
			dnsresult = updatedns(url2, dataurl2)
			if dnsresult.get('success') is True:
			# Si el valor de Value se ha podido actualizar
				print("Done, results:", dnsresult)
			else:
			# Si el valor de Value NO se ha podido actualizar, aunque si por reazones que sea, hubiese sido el mismo Value, el programa acaba mucho antes en donde la verificación de pre-existencia
				print("Error, results (will be send by mail too):", dnsresult)
				email("Error updating DNS TXT in DonDominio!", json.dumps(response, indent = 2))
				quit()
	else:
	# Negativo en capturar el entityID del "_acme-challenge." + certbot_domain
		print(name, "is not in", serviceName, "so creating...")
		dataurl3 = {'apiuser': apiuser, 'apipasswd': apipasswd, 'name': name, 'serviceName': serviceName, 'type': "TXT", 'value': certbot_validation, "ttl": 600}
		dnsresult = updatedns(url3, dataurl3)
		if dnsresult.get('success') is True:
		# Si el valor de Value se ha podido crear
			print("Done, results:", dnsresult)
		else:
		# Si el valor de Value NO se ha podido crear
			print("Error, results (will be send by mail too):", dnsresult)
			email("Error creating DNS TXT in DonDominio!", json.dumps(response, indent = 2))
			quit()
	time.sleep(60)
	# Esperar un tiempo si todo va bien para que Certbot tenga tiempo en verificar el certbot_validation
else:
# Si no se ha podido comunicar con DonDominio
	for key, value in response.items():
		print(key, value)
	# Se envía un correo electrónico con el resultado de error en la respuesta del API de DonDominio
	email("Error getting DNS list from DonDominio!", json.dumps(response, indent = 2))
