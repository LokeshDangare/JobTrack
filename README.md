# JobTrack

A professional mini application for managing your job search.

## Features:
- Dashboard
- Company management
- Job application management
- Interview tracking
- Search/filter
- Edit/delete
- MySQL relational database
- SQL JOINs
- Analytics
- Plotly charts

## Project Structure

JobTrack/
│
├── app.py
├── database.py
├── models.py
├── requirements.txt
├── .env
├── .gitignore
│
├── pages/
│   ├── 1_Companies.py
│   ├── 2_Applications.py
│   ├── 3_Interviews.py
│   └── 4_Analytics.py
│
└── utils/
    ├── __init__.py
    └── queries.py

## Create SQL Database

CREATE DATABASE JobTrackDB;
SHOW DATABASES;
USE JobTrackDB;

## Create Python environment

py -3.11 -m venv jobtrack

Activate it: jobtrack\Scripts\activate

## Run requirements.txt

## Create .env file to add the secret credential

DB_USER=root

DB_PASSWORD=your_mysql_password

DB_HOST=localhost

DB_PORT=3306

DB_NAME=JobTrackDB

Replace: 'your_mysql_password' with the password you created for MySQL.

## Create .gitignore

Add all this:

jobtrack/
.env
__pycache__/
*.pyc
.streamlit/

This prevents your password and virtual environment from being uploaded to GitHub.


## Start MySQL

Before running Streamlit, make sure MySQL Server is running.
You can verify through MySQL Workbench.

Run:

USE JobTrackDB;
SHOW TABLES;

## Run the application

streamlit run app.py

## So the actual architecture is:

                 JOBTRACK
                     │
                     ↓
               STREAMLIT UI
                     │
                     ↓
                 Python
                     │
                     ↓
                SQLAlchemy
                     │
                     ↓
          mysql-connector-python
                     │
                     ↓
              MYSQL SERVER
                     │
                     ↓
               JobTrackDB
              /     |      \
             /      |       \
            ↓       ↓        ↓
       companies applications interviews
