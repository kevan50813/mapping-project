#!  /bin/bash

PRIVATE_TOKEN='glpat-LFvBvfu78QjuxwnY9sWr'

curl -s -L --header "PRIVATE-TOKEN: $PRIVATE_TOKEN" "https://gitlab.com/api/v4/projects/31237418/jobs/artifacts/main/download?job=build-maps-job" -o temp.zip && unzip temp.zip -d maps_new && rm -rf temp.zip maps && mv maps_new maps