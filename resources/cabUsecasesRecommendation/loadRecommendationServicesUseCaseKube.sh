cd "$(dirname "${BASH_SOURCE[0]}")"
echo "Load recommendation usecases on Kube cluster##########################################"
 ./createRecommendationUsecaseKube.sh PowerGridRecommendationUC $1
 ./createRecommendationUsecaseKube.sh ATMRecommendationUC $1
 ./createRecommendationUsecaseKube.sh RailwayRecommendationUC $1