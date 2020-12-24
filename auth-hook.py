#!/usr/bin/python3

# DonDominio的DNS验证方法，这样可以直接走通配符放行域名了！

# certbot certonly --logs-dir $HOME/DonDominio/ --work-dir $HOME/DonDominio/ --config-dir $HOME/DonDominio/ --manual --manual-auth-hook $HOME/DonDominio/auth-hook.py --deploy-hook $HOME/DonDominio/deploy-hook.sh -d *.enlace.com.es --preferred-challenges=dns --agree-tos --no-eff-email -m register@disframed.com

# 如果是做更新的话，其实不用加很多参数，因为它会直接读取你在获取证书时的原始配置，也就意味着如果你更换了配置，最好重新走申请新证书的流程，而不是单纯地更新它
# certbot renew --logs-dir $HOME/DonDominio/ --work-dir $HOME/DonDominio/ --config-dir $HOME/DonDominio/ --manual --manual-auth-hook $HOME/DonDominio/auth-hook.py --deploy-hook $HOME/DonDominio/deploy-hook.sh --preferred-challenges=dns

# certbot revoke --test-cert --delete-after-revoke --non-interactive --cert-path $HOME/DonDominio/archive/enlace.com.es/cert1.pem --key-path $HOME/DonDominio/archive/enlace.com.es/privkey1.pem --logs-dir $HOME/DonDominio/ --work-dir $HOME/DonDominio/ --config-dir $HOME/DonDominio/ -m register@disframed.com && rm -vrf accounts/ archive/ backups/ csr/ keys/ letsencrypt.* live/ renewal* *.pem

import os, json, requests, time
# 首先把所有的变量收集齐
apiconf = open("api.conf")
apiconf = apiconf.readlines()
apiuser = apiconf[0].strip()
apipasswd = apiconf[1].strip()
url1 = "https://simple-api.dondominio.net/service/dnslist/"
url2 = "https://simple-api.dondominio.net/service/dnsupdate/"
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
count = 0
for key, value in response.items():
	count = count + 1
	# 只需要回复的前5条记录
	if count <= 5:
		print (key + ":", value)
	else:
		pass
if response.get('success') is False:
	print("Error Ocurred!\n" + "*" * 20)
	# 这里是不是要发封邮件啊？
else:
	# 获取结果中符合 certbot_domain 的 entityID
	keys = response.get('responseData').get('dns')
	for key in keys:
		# 其实每个key都是一个字典
		if key.get('name') == name:
			entityID = key.get('entityID')
			print(key.get('name'), "has entityID", entityID)
			print ("*" * 20)
			if key.get('value') == certbot_validation:
				# 如果要更新的值和已有的值一样，那就别管了
				print("Value you going to update is the same as you recived from Certbot, look:")
				for dict, value in key.items():
					print(dict + ":", value)
				break
				print ("*" * 20)
			else:
				print("Update", key.get('value'), "to", certbot_validation)
				print ("*" * 20)
				# 组装修改申请
				dataurl2 = {'apiuser': apiuser, 'apipasswd': apipasswd, 'name': name, 'serviceName': certbot_domain, 'entityID': entityID, 'value': certbot_validation}
				count = 0
				# 获取修改结果
				response = json.loads(requests.post(url2, data=dataurl2).text)
				print("Done, results:")
				for key, value in response.items():
					count = count + 1
					# 只需要回复的前5条记录
					if count <= 5:
						print (key + ":", value)
					else:
						pass
				if response.get('success') is False:
					print("Error Ocurred!\n" + "*" * 20)
					# 这里是不是要发封邮件啊？
			print ("*" * 20)
			break
		else:
			pass
	# 如果数据都遍历完了，还是找不到_acme-challenge.怎么办？应该有个创建用的语法：
	# if (name in key.values()) 拿着DonDominio的数据验证一下
	time.sleep(25)