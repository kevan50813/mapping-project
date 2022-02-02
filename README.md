# COMP5530M_Mapping_Project

# Build instructions
To build server locally either as
## PEX Binary (python binary with requirements)
Run `./pants package server/src/main.py` with a python 3.8 interpreter.

## Docker Image
Run `./pants package Dockerfile` with the `BUILD_TAG` environment variable set.
I would suggest setting this to something unique like the git commit you are
currently on `git rev-parse --short HEAD`

Use the docker-compose.yml file as a template to run this image with your own
tag. You will have to login `docker login registry.gitlab.com` if you want to
use the CI builds.
