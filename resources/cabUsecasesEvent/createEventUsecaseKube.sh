cd "$(dirname "${BASH_SOURCE[0]}")"

url=$2
if [ -z $url ] 
then
	url="https://demo.interactiveai.irt-systemx.fr" #urt="https://frontend.cab-dev.irtsystemx.org"
fi
if [ -z $1 ]
then
    echo "Usage : createEventUsecase use_case_name cab_url"
else
    source ../getTokenKube.sh "admin" $url/auth/token
    echo "Create event usecase $1 on $url"
    curl -X POST $url/cab_event/api/v1/usecases -H "Content-type:application/json" -H "Authorization:Bearer $token" --data @$1.json -v
    echo ""
fi
