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

# CAB fix ":2100" to localhost url directly to allow use on kube ingress systems

url=$2 
if [ -z $url ] 
then
	url="https://demo.interactiveai.irt-systemx.fr" #urt="https://frontend.cab-dev.irtsystemx.org"
fi
if [ -z $1 ]
then
    echo "Usage : deleteBundle bundle_name opfab_url"
else
	echo "Will delete bundle $1 on $url"
	source ../getTokenKube.sh admin $url
	curl -s -X DELETE "$url/businessconfig/processes/$1" -H "Authorization:Bearer $token"
	echo ""
fi


