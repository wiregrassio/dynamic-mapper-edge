docker container run \
-it \
--rm \
-v $(pwd)/listener.py:/home/listener.py \
-v $(pwd)/template.json:/home/template.json \
-v $(pwd)/mapper.py:/home/mapper.py \
wiregrass:dynamic-mapper-edge \
/bin/bash