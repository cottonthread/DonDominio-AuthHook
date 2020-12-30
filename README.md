# DonDominio-AuthHook
El Auth Hook para obtenter Wildcard de Let's Encrypt mediante Certbot

### Un pequeño script para ayudar a obtener certificado tipo WildCard de Let's Encrypt mediante método de verificación DNS del programa Certbot. Ya que no tiene soporte para DonDominio, pues se crea su Auth-Hook con los cretidenciales del API de DonDominio.
#### No apto. para obtención de certificado de dominios del CNAME.

### Preparación

1. Obtener el acceso del API en [La web oficial de DonDominio](https://www.dondominio.com/products/api/#requestaccess)
2. Esperar que DonDominio te aprueba y te hagan firmar los papeles antes de concederte el acceso.
3. Introducir el IP que vaya a utilizar el API en [El panel de control de "IPs permitida"](https://www.dondominio.com/admin/account/api)
4. Apuntar/Crear los datos de usuario y contraseña del API en [El panel de control de "Configuración"](https://www.dondominio.com/admin/account/api)
5. Apuntar los datos de servidor, puerto, usuario y contraseña de tu servidor de correos electrónicos, así para poder de así posibilitar que el script pueda mandarte un mail en caso de error directamente.


### Instalación

CentOS:
`
sudo yum install -y epel-release yum-utils certbot.noarch python3 git
`
```
git clone https://github.com/cottonthread/DonDominio-AuthHook.git
cd DonDominio-AuthHook
vim api.conf *Con los datos preparados*
```


###

#### Para obtener por primera vez el certificado:
```
certbot certonly --logs-dir $HOME/DonDominio-AuthHook/ --work-dir $HOME/DonDominio-AuthHook/ --config-dir $HOME/DonDominio-AuthHook/ \
--manual --manual-auth-hook $HOME/DonDominio-AuthHook/auth-hook.py --deploy-hook $HOME/DonDominio-AuthHook/deploy-hook.sh \
-d ***.dominio.com*** --preferred-challenges=dns --agree-tos --no-eff-email --manual-public-ip-logging-ok -m register@dominio.com
```
### Para obtener la renovación del certificado:
```
certbot renew --logs-dir $HOME/DonDominio-AuthHook/ --work-dir $HOME/DonDominio-AuthHook/ --config-dir $HOME/DonDominio-AuthHook/ \
--manual --manual-auth-hook $HOME/DonDominio-AuthHook/auth-hook.py --deploy-hook $HOME/DonDominio-AuthHook/deploy-hook.sh --preferred-challenges=dns
```
### Para revocar y borrar el certificado:
```
certbot revoke --delete-after-revoke --non-interactive --logs-dir $HOME/DonDominio-AuthHook/ --work-dir $HOME/DonDominio-AuthHook/ --config-dir $HOME/DonDominio-AuthHook/ \
--cert-path $HOME/DonDominio-AuthHook/archive/***dominio.com***/cert1.pem --key-path $HOME/DonDominio-AuthHook/archive/***dominio.com***/privkey1.pem \
-m register@dominio.com && rm -vrf accounts/ archive/ backups/ csr/ keys/ letsencrypt.* live/ renewal* *.pem
```
