#!/bin/bash
docker exec -it mcquaig-mcquaig-1 /bin/sh -c "pip install -Ur /app/tests/requirements.txt; pytest"
