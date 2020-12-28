#!/usr/bin/bash
cp -vf $RENEWED_LINEAGE/fullchain.pem $HOME/DonDominio-AuthHook/"$CERTBOT_DOMAIN"_fullchain.pem
cp -vf $RENEWED_LINEAGE/privkey.pem $HOME/DonDominio-AuthHook/"$CERTBOT_DOMAIN"_privkey.pem
