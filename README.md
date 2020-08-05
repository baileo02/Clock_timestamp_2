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
* Tkinter 3.8.5

<a name="setup"></a>
## Setup
To run this project, install it locally by git cloning https://github.com/baileo02/Clock_timestamp_2.git or 
alternatively by downloading the ZIP. <br/>
Open the project and run clock_timestamp_controller.py, this will create a new local database file when run for 
the first time. <br/>
Default access password for admin control is: 'admin' and this can be changed in alter_hour_page.py. <br/>

<a name="features"></a>
## Features
* Admin has the ability to fix incorrect clock on/off times for employees
* Easy to visualise hours worked grid, counting total hours for each employee.
* Adjustable default break time allocated for employees accounted for.

<a name="project-status"></a>
## Project Status
This project is primarily for personal learning and as such, it is still in development and not applicable for all business types.
Currently, all data is stored locally but for future iterations, I plan to implement server based database

<a name="sources"></a>
## Sources 
http://effbot.org/tkinterbook/ - For documentation and examples on tkinter's GUI <br/>
https://docs.python.org/3/library/ - Standard Python reference and guides <br/>
https://stackoverflow.com/ - Helped immensely in guiding me to solutions 
