This is a Python Django App and requires a MySQL connection

Installation Steps:
	In the database, create a new database with following command:
	mysql> create database my_app;


	Run following commands to install required packages:
	pCrypto: sudo easy_install pycrypto 
	django: sudo pip install django

	After installing above packages, go to project home and run migrations using following command:
	python manage.py migrate

	This should create the required table.

	Start Django server using following command:
	python manage.py runserver

	go to localhost:8000 and upload page should appear

	Make sure your user has access to /tmp directory as the system uses this directory to store encrypted files.
	Unencrypted files are never saved on filesystem or anywhere else.


