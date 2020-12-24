#!/usr/bin/python3
import os, json, requests, time
# 首先把所有的变量收集齐
apiconf = open("api.conf")
apiconf = apiconf.readlines()
apiuser = apiconf[0].strip()
apipasswd = apiconf[1].strip()
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

# 展示从Certbot获取的数据
print("Reciveced from Certbot:\nDomain: ", certbot_domain, "\tValidation:", certbot_validation, "\nToken:", certbot_token, "\tRemaining Challenges:", certbot_remaining_challenges, "\tAll Domains:", certbot_all_domains, "\n" + "*" * 20)

# 开始和DonDominio联系
print("Comunicating with DonDominio:")
# 组装申请数据
dataurl1 = {'apiuser': apiuser, 'apipasswd': apipasswd, 'name': name, 'serviceName': certbot_domain}

# 获取数据申请结果
response = json.loads(requests.post(url1, data=dataurl1).text)
if response.get('success') is True:
	for key, value in response.items():
		if key == "responseData":
			pass
		else:
			print(key, value)
	# 获取结果中符合 certbot_domain 的 entityID
	keys = response.get('responseData').get('dns')
	for key in keys:
		# 假如已经存在相应的TXT项，只需要更新相关内容的话
		if name in key.values():
			print(key.get('name'), "has entityID", key.get('entityID'))
			entityID = key.get('entityID')
			print ("*" * 20)
			if key.get('value') == certbot_validation:
				# 如果要更新的值和已有的值一样，那就别管了
				print("Value you going to update is the same as you recived from Certbot, look:")
				for item, value in key.items():
					print(item + ":", value)
				print ("*" * 20)
			else:
				print("Update", key.get('value'), "to", certbot_validation)
				print ("*" * 20)
				# 组装修改申请
				dataurl2 = {'apiuser': apiuser, 'apipasswd': apipasswd, 'name': name, 'serviceName': certbot_domain, 'entityID': entityID, 'value': certbot_validation}
				# 获取修改结果
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
						# 这里是不是要发封邮件啊？
			print ("*" * 20)
			break
		# 假如没有相应的TXT项，需要创建的话
		else:
			print(name, "is not in", certbot_domain, "so creating...")
			# 组装修改申请
			dataurl3 = {'apiuser': apiuser, 'apipasswd': apipasswd, 'name': name, 'serviceName': certbot_domain, 'type': "TXT", 'value': certbot_validation, "ttl": 600}
			# 获取修改结果
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
				# 这里是不是要发封邮件啊？
		print ("*" * 20)
	time.sleep(25)
else:
	for key, value in response.items():
		print(key, value)
	# 这里是不是要发封邮件啊？
