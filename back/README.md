# InsAccess
---
A web app created for the INSA of Rouen Normandie




# My Table of content
- [Section 1](#id-section1)
- [Section 2](#id-section2)

<div id='id-section1'/>
## Section 1
<div id='id-section2'/>
## Section 2



systemctl start mariadb
systemctl status mariadb
systemctl stop mariadb
 
> to get to the mariadb terminal and use it :
> - sudo mariadb
> - USE app
# if not installed do this
sudo apt update
sudo apt install mariadb-server
sudo mysql_secure_installation
look into config.json for database connection
default pwd for user is toto
if first time then you need to initialize the database app using:
create database app;
show databases;

## how to fetch
> for day, simply put the day (ex : 20250123 for 2025/01/23)
> for week, must be the sunday previous to the week you wanna fetch (for the 12 to 16 then fetch at 11)
> for month, simply fetch at the first day of the month

