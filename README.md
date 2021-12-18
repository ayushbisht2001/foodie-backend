# Setup Guide for foodie-backend

## Getting Project
    git clone https://github.com/ayushbisht2001/foodie-backend.git


## Creating virtual environment

    pip install virtualenv

    virtualenv hacker-env

    source hacker-env/Scripts/activate

## Installing Dependencies

    pip install django

    pip install -r requirements.txt

## Database setup

    For MySql
        - CREATE USER 'hacker'@'localhost' IDENTIFIED BY 'Hacker@123';
        - GRANT SELECT ON * . * TO 'test'@'localhost';
        - Permissions - All
        - create database  hackerearth

    if facing any issue with MySQL DB setup, then uncomment the line    
    DB_TYPE = "sqlite"  ( backend/backend/settings.py )


## Database Migration and seeding

    python manage.py makemigrations
    
    python manage.py migrate

    python manage.py createsuperuser

    python manage.py seed


## Start server

    python manage.py runserver