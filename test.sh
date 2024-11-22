clear
docker container run \
-it \
--rm \
-v $(pwd)/template.json:/home/template.json \
-v $(pwd)/listener.py:/home/listener.py \
-v $(pwd)/app.py:/home/app.py \
-v $(pwd)/debug.py:/home/debug.py \
--network="host" \
wiregrass:dynamic-mapper-edge \
/bin/bash