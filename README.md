# DonDominio-AuthHook
El Auth Hook para obtenter Wildcard de Let's Encrypt mediante Certbot


### Un pequeño script para ayudar a obtener certificado tipo WildCard de Let's Encrypt mediante método de verificación DNS del programa Certbot. Ya que no tiene soporte para DonDominio, pues se crea su Auth-Hook con los cretidenciales del API de DonDominio.

#### Para obtener por primera vez el certificado:
`
certbot certonly --logs-dir $HOME/DonDominio/ --work-dir $HOME/DonDominio/ --config-dir $HOME/DonDominio/ --manual --manual-auth-hook $HOME/DonDominio/auth-hook.py --deploy-hook $HOME/DonDominio/deploy-hook.sh -d ***.dominio.com*** --preferred-challenges=dns --agree-tos --no-eff-email -m register@disframed.com
`

### Para obtener la renovación del certificado:
`
certbot renew --logs-dir $HOME/DonDominio/ --work-dir $HOME/DonDominio/ --config-dir $HOME/DonDominio/ --manual --manual-auth-hook $HOME/DonDominio/auth-hook.py --deploy-hook $HOME/DonDominio/deploy-hook.sh --preferred-challenges=dns
`
### Para revocar y borrar el certificado:
`
certbot revoke --delete-after-revoke --non-interactive --cert-path $HOME/DonDominio/archive/***dominio.com***/cert1.pem --key-path $HOME/DonDominio/archive/***dominio.com***/privkey1.pem --logs-dir $HOME/DonDominio/ --work-dir $HOME/DonDominio/ --config-dir $HOME/DonDominio/ -m register@disframed.com && rm -vrf accounts/ archive/ backups/ csr/ keys/ letsencrypt.* live/ renewal* *.pem
`
