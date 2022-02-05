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

## Running the app for development
running the App on your phone in devloper mode:

1) follow the instectuins on this link : https://reactnative.dev/docs/running-on-device for instal set up with phone etc..
    EACH TIME YOU WISH TO RUN THE APP AFTER STEP 1 DO THE FOLLOWING
2) open 2 sperate terminals
3) form terminal 1. run npm start and form 2. run react-native run-android ENSURE YOUR PHONE IS PLUGGED INTO YOUR PC AND IS IN DEVELOPER MODE
4) allow the app to install 
5) run the app 
