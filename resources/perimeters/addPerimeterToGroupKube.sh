#!/bin/bash

# Copyright (c) 2021, RTE (http://www.rte-france.com)
# See AUTHORS.txt
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
# This file is part of the OperatorFabric project.

# This starts by moving to the directory where the script is located so the paths below still work even if the script
# is called from another folder
cd "$(dirname "${BASH_SOURCE[0]}")"

url=$3 
if [ -z $url ] 
then
	url="https://demo.interactiveai.irt-systemx.fr" #urt="https://frontend.cab-dev.irtsystemx.org"
fi
if [ -z $1 ] || [ -z $2 ]
then
    echo "Usage : addPerimeterToGroup perimeter_id group_id opfab_url"
else
    source ../getTokenKube.sh admin $url
    echo "Add perimeter $1 to group $2"
    response=$(curl -X PATCH $url/users/groups/$2/perimeters -w "%{http_code}\n%{response_code}" -H "Content-type:application/json" -H "Authorization:Bearer $token" --data "[\"$1\"]")

    # Extract the status code
    status_code=$(echo "$response" | head -n 1)
    
    # Extract the response body
    response_body=$(echo "$response" | tail -n 1)
    
    # Print the status code and response body
    echo "Add permiter to group Status Code: $status_code"
    echo "Add Permiter to group Response Body: $response_body"
fi
