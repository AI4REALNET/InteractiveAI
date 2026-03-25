#!/bin/bash

# Copyright (c) 2022, RTE (http://www.rte-france.com)
# See AUTHORS.txt
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
# This file is part of the OperatorFabric project.

url=$4
if [ -z $url ]
then
	url="https://demo.interactiveai.irt-systemx.fr" #urt="https://frontend.cab-dev.irtsystemx.org"
fi
if [ "$#" -lt 3 ]
then
    echo "Usage : sendAckForCard user card_uid entitiesAcks opfab_url"
else
    source ../getTokenKube.sh admin $url
    curl -X POST $url/cards/userAcknowledgement/$2 -H "Authorization: Bearer $token" -H "Content-type:application/json" --data $3
fi
