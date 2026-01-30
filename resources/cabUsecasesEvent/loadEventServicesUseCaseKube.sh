cd "$(dirname "${BASH_SOURCE[0]}")"

 ./createEventUsecaseKube.sh ATMEvent $1
 ./createEventUsecaseKube.sh PowerGridEvent $1
 ./createEventUsecaseKube.sh RailwayEvent $1