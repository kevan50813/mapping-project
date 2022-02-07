# How to Run Server

# Install Docker

Install `docker` and `docker-compose`

[Install Docker Engine](https://docs.docker.com/engine/install/)

Run `sudo systemctl enable --now docker`

This link shows how you can run without sudo

[Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)

Run `docker login registry.gitlab.com`

# Run docker-compose file

`docker-compose up` to see the console or `docker-compose up -d` to daemonise it (`docker-compose down` after you’re done).

This will pull the latest image from the `main` branch and run it with a redis server on port `80` and `6379` respectively.

# Load Data into the Database

Currently there is no API endpoint for loading GeoJSON so you will have to run a python script to load data in

Run the `get_json.sh` script from the git root

```bash
#!/bin/bash
PRIVATE_TOKEN="PLEASE GENERATE YOUR OWN OR MAYBE SEE #SERVER FOR MINE"
curl -s -L --header "PRIVATE-TOKEN: $PRIVATE_TOKEN" "https://gitlab.com/api/v4/projects/31237418/jobs/artifacts/main/download?job=build-maps-job" -o temp.zip
unzip -d maps_new temp.zip
rm -rf temp.zip maps 
mv maps_new maps
```

Then make a file in `server/src/` called `test.py`

```python
import asyncio
import logging
from src.parser.map_data import MapData
from src.parser.graph_parser import Parser
from src.database.controller import Controller

async def test():
    d = MapData("../../maps/bragg-osm-floors", graph_name="test_bragg")
    p = Parser(d.graph_name, d.polygons, d.linestring, d.points)

    db = Controller("127.0.0.1")
    db.redis_db.flushall()

    tasks = []
    tasks.append(asyncio.create_task(
        db.save_graph(d.graph_name, p.nodes, p.edges)))
    tasks.append(asyncio.create_task(
        db.add_entries(d.graph_name, p.polygons)))
    tasks.append(asyncio.create_task(
        db.add_entries(d.graph_name, p.pois)))

    return await asyncio.wait(tasks)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(test())
    print("done")
```

Run `export PYTHONPATH="$PWD/server"` in the git root and then `pip install -r requirements.txt`

Then `cd server/src` and run `python test.py` you should see a lot of DEBUG messages, this is good.

# Test Server

Navigate to [http://127.0.0.1](http://127.0.0.1), you should see the 'graphql playground'

Try the query:

```graphql
query {
  nodes (graph:"test_bragg") {
    id
    tags
  }
}
```

Click the 'play button'. If the `"nodes"` object isn’t an empty list it’s worked!

You can click ‘schema’ to view the GQL schema and mess around with it.
