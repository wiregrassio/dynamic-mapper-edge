clear
docker container run \
-it \
--rm \
-v $(pwd)/template.json:/home/template.json \
-e INBOUND_TOPIC="/c8y/inbound/topic" \
--network="host" \
wiregrass:dynamic-mapper-edge