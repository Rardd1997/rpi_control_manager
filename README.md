# rpi_control_manager
Raspberry Pi3 Control System for I/O
***
In order to get started with the controller, you need to install the operating system Raspian. 
How to do this is described in detail [HERE](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).
***
Now when it is necessary to set up remote access, because programming on the raspberry is not very convenient, but it is more convenient to write code on a local machine, and testing it on raspberries. Access to raspberry can be done using samsung or nss. How to do this with SSH is described [HERE](https://www.raspberrypi.org/documentation/remote-access/ssh/README.md), how to work with VNС is described [HERE](https://www.raspberrypi.org/documentation/remote-access/vnc/README.md) | [RU-lang](http://wiki.amperka.ru/rpi:vnc-server).
***
Now that the system is installed, you can connect to raspberry by ssh or other interfaces, by default the user has the name of the pi, and the password - raspberry. How to find out the ip address of raspberries is described in detail [HERE](https://www.raspberrypi.org/documentation/remote-access/ip-address.md).
***
Then you need to configure the GPIO. Details [HERE](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-gpio).
***
After installation, you need to enable and configure the I2C. Details [HERE](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c).
***
Next you need to configure the RTC. Details [HERE](https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-rtc-time).
***
Now that the system is configured, you can start installing the controller. To get started, copy the project into the working directory of the previously configured raspberry server. In order to clone a project, run the following command:
>git clone https://github.com/Rardd1997/rpi_control_manager.git [your_folder_name]
***
Now you need to set up a database. I used MASKL but you can use whatever you like and which supports alchemy glass (everything is configured in the config file).
The installation of the database is accessible through the command:
>sudo apt-get update && sudo apt-get upgrade

>sudo apt-get install mysql-server --fix-missing

>sudo apt-get install mysql-client

After installation, we can launch the command console by the command:
>sudo mysql

After that, you will need to enter the password you set for the user root when installing the mysql server. So, then we need to create new user for our controller. Run mysql and execute the following commands:
>CREATE USER 'rpi3'@'localhost' IDENTIFIED BY 'rpi3';

where 'rpi3' is the username, 'localhost' - host, and IDENTIFIED BY 'rpi3' - password
Now we grant all available privileges to our user

>GRANT ALL PRIVILEGES ON * . * TO 'rpi3'@'localhost';

>FLUSH PRIVILEGES;
***
Now we create a database which we fill in later using the migration package for the Flask
>CREATE DATABASE rpi3;
***
As you have already understood, the controller is written in the Python, so you need to install all the necessary packages for work, also need to install the python version 3 if it is not already installed. Package list:
* pigpio 
* python-pigpio 
* python3-pigpio
* flask
* Flask-SQLAlchemy
* itsdangerous
* click
* Werkzeug
* Jinja2
* MarkupSafe
* flask-migrate
* Mako
* alembic
* python-dateutil
* python-editor
* six
* flask-login
* flask-mail
* WTForms
* flask-wtf
* flask-mysqldb
* flask-moment
* flask-bootstrap

Command for executing for installed all this package:
>sudo apt-get update

>sudo pip3 install pigpio python-pigpio python3-pigpio flask flask-sqlalchemy flask-migrate flask-login flask-mail flask-wtf flask-bootstrap flask-moment

>sudo apt-get install python-mysqldb

>sudo pip3 install flask-mysqldb
***
Now you need to create the structure of the created database. For this you need to execute the following commands:
>export FLASK_APP=contol.py

>flask db init

>flask db migrate -m "comment"
***
Now that everything is ready, we can launch the pigpio deamon and our controller.But before that, go to the controller folder using the cd command.
>sudo pigpiod

>sudo python3 control.py
