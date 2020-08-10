# Employee time punch app
An employee clock on/off app created with Python.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [Project Status](#project-status)
* [Sources](#sources)

<a name="general-info"></a>
## General info 
A simple time punch app used to track employee clock on/off times. It can also display the data in a timesheet grid
that totals weekly hours worked. <br/>
I created this app for a small business to replace and automate employees needing to write down their hours at the end 
of the day.

<a name="technologies"></a>
## Technologies
Project is created with:
* Python 3.8
* Sqlite3 
* Tkinter 8.6

<a name="setup"></a>
## Setup
To run this project, install it locally by git cloning https://github.com/baileo02/Clock_timestamp_2.git or 
alternatively by downloading the ZIP. <br/>
You will need to run 'pipenv install' to install the packages required. If you don't have pipenv, install it by 'pip install pipenv' <br/>
Then run 'pipenv run start' <br/>
Default access password for admin control is: 'admin' and this can be changed in alter_hour_page.py. <br/>

<a name="features"></a>
## Features
* Simple intuitive clock on and off system
* Easy to visualise hours worked grid, counting total hours for each employee.
* Admin can add employees as well as amend clock on/off times

<a name="project-status"></a>
## Project Status
This project is primarily for personal learning and as such, it is still in development and not applicable for all business types.
Currently, all data is stored locally but for future iterations, I plan to implement server based database

<a name="sources"></a>
## Sources 
http://effbot.org/tkinterbook/ - For documentation and examples on tkinter's GUI <br/>
https://docs.python.org/3/library/ - Standard Python reference and guides <br/>
https://stackoverflow.com/ - Helped immensely in guiding me to problem solutions
