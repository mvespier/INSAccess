#!/bin/bash

screen -X -S flask kill

screen -dmS flask flask run --debug

cd ./front/ && npm start
