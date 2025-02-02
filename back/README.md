# InsAccess
A web app created for the INSA of Rouen Normandie.

# Table of content
- [Installation](#installation)
- [Development](#dev)
- [Models](#models)

# Installation <div id='installation'/>
- create the database (we used mariadb, but others should work fine)
- create a `config.json` file for the flask app by using the  `config-template.json`
- create a python `venv` and install requirement (`pip install -r requirements.txt`)
- launch the `test_insertion.py` file for initializing the app (this file is only temporary)

# Development <div id='dev'/>
-  launch the flask server
```
flask run --debug
```
-  if you're using mariadb you can access the tables by doing the following
```
sudo mariadb
>>> USE app;
```
## Code Structure
- `app/blueprints` contain the different modules that define the available routes organized by `blueprint` (https://flask.palletsprojects.com/en/stable/blueprints/)
	- `main.py` define the main routes.
	- `api.py` define the route for the application apis, used between the front and the back to retrieve or post values to the server.
	- `auth.py` code for handling authentication - code is fully generic and should not really be modified. Function requiring authentication should take the decorator `@login_required`
	- `admin.py` define the managing route for the admin of the website (used mainly to add association or to handle error)
	- `parameters.py` define the settings route.
	

# Models <div id='models'/>



## how to fetch
> for day, simply put the day (ex : 20250123 for 2025/01/23)
> for week, must be the sunday previous to the week you wanna fetch (for the 12 to 16 then fetch at 11)
> for month, simply fetch at the first day of the month

