#!/bin/bash

screen -X -S flask kill

cd ./backend/

screen -dmS flask flask run --debug


cd ../front/ && npm start
