#!/bin/bash

# Copyright (c) 2022, RTE (http://www.rte-france.com)
# See AUTHORS.txt
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
# This file is part of the OperatorFabric project.

# This starts by moving to the directory where the script is located so the paths below still work even if the script
# is called from another folder
cd "$(dirname "${BASH_SOURCE[0]}")"

url=$2
if [ -z $url ]
then
	url="https://demo.interactiveai.irt-systemx.fr" #urt="https://frontend.cab-dev.irtsystemx.org"
fi
if [ -z $1 ]
then
    echo "Usage : loadRealTimeScreens file_name opfab_url"
else
	echo "Will load realTimeScreens $1 on $url"
	source ../getTokenKube.sh admin $url
	
    response=$(curl -s -X POST "$url/businessconfig/realtimescreens" -w "%{http_code}\n%{response_code}" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -H "Authorization:Bearer $token" -F "file=@$1")

    # Extract the status code
    status_code=$(echo "$response" | head -n 1)
    
    # Extract the response body
    response_body=$(echo "$response" | tail -n 1)
    
    # Print the status code and response body
    echo "real time screens Status Code: $status_code"
    echo "real time screens Response Body: $response_body"
fi
