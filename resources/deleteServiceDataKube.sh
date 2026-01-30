#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")"

servicename=$1
url=$2

if [ -z $url ]; then
    url="https://demo.interactiveai.irt-systemx.fr" #urt="https://frontend.cab-dev.irtsystemx.org"
fi

if [ -z $servicename ]; then
    echo "Usage : deleteServiceData servicename cab_url"
else
    source ./getTokenKube.sh "admin" $url
    echo "Sending delete request to $url/$servicename/api/v1/delete_all_data"
    curl -X DELETE $url/$servicename/api/v1/delete_all_data -H "Content-type:application/json" -H "Authorization:Bearer $token" -v
    echo ""
fi
