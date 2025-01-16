# to launch the database and use it

systemctl start mariadb
systemctl status mariadb
systemctl stop mariadb
 
> to get to the mariadb terminal and use it :
> - sudo mariadb
> - USE app
#if not installed do this
sudo apt update
sudo apt install mariadb-server
sudo mysql_secure_installation
look into config.json for database connection
default pwd for user is toto
if first time then you need to initialize the database app using:
create database app;
show databases;

