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

url=$1 
if [[ -z $url ]]
then
	url="https://demo.interactiveai.irt-systemx.fr" #urt="https://frontend.cab-dev.irtsystemx.org"
fi
echo "URL: $url"

(
	cd bundles
	./deleteAllBundlesKube.sh $url
	./loadAllBundlesKube.sh $url
	cd ../processGroups
	./loadProcessGroupsKube.sh cabProcessGroup.json $url
	#TODO Clear perimeters first?
	cd ../perimeters
	./createAllPerimeterKube.sh $url
	cd ../realTimeScreens
	./loadRealTimeScreensKube.sh realTimeScreens.json $url
	cd ../cabUsecasesEvent
	./loadEventServicesUseCaseKube.sh $url
	cd ../cabUsecasesContext
	./loadContextServicesUseCaseKube.sh $url
	cd ../cabUsecasesRecommendation
	./loadRecommendationServicesUseCaseKube.sh $url
)
