cd "$(dirname "${BASH_SOURCE[0]}")"

 ./createContextUsecaseKube.sh PowerGridContext $1
 ./createContextUsecaseKube.sh ATMContext $1
 ./createContextUsecaseKube.sh RailwayContext $1
 