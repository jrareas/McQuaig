#!/bin/bash
docker exec -it mcquaig-mcquaig-1 /bin/sh -c "alembic -c development.ini upgrade head"
