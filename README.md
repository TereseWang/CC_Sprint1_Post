# F22-Starter-Microservice

## Introduction

This is a simple Flask based starter microservice for F22 Columbia classes.


## Setup

- For the purposes of E6156 and W4111, please install PyCharm Professional.
- University students can register for a free, one year license.
- Also, please make sure that your system has already installed:
  - Python (3.9 or greater)
  - MySQL Community Server

Open the project in PyCharm and create a new virtual environment for the project. You can find the instructions
online in the PyCharm documentation. After creating the virtual environment, open a terminal window using the bottom
pane (open the terminal within PyCharm). In the root of the directory, execute the command

```pip install -r requirements.txt```

This should install the necessary Python requirements.

## Executing the Program

Select the file ```application.py``` in the directory ```./src``` in the file explorer. Right click on the file and
select "run." In the execution panel at the bottom of the screen, you should see messages about "running on ... ..."
This indicates that the web application has started.

Select the file ```tts.py``` and run it. The message will determine if your end-to-end test worked.


## Connecting to the Database

The file ```columbia_student_resource.py``` is a simple, starter REST resource.


