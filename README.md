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
	
	Run this command in shell prompt to create symlink for mysql client libraries
	sudo ln -s /usr/local/mysql/lib/libmysqlclient.18.dylib /usr/lib/libmysqlclient.18.dylib

	Start Django server using following command:
	python manage.py runserver

	go to localhost:8000 and upload page should appear

	Make sure your user has access to /tmp directory as the system uses this directory to store encrypted files.
	Unencrypted files are never saved on filesystem or anywhere else.



This application in its current form is very basic and saves files in local storage which is not scalable at all

Scalability:
1. Using a third party service like S3 as storage will allow more storage and also make it secure.
2. While decrypting the files, system writes all decrypted contents into memory and then sends it as response. This can be improved by writing to response in batches and freeing up the memory.
3. Same can be done for encryption step as well.

Resiliency:
1. Use a reliable storage system like S3. If there is an error while uploading, user needs to be asked to upload again. If there is an error while decryption/downloading, restart the decryption process and generate a new file in the same request scope so it appears seamless to user.


Enhancemenets:
	1. Add SHA1 hash for oneway password encryption.
	2. The encryption key is currently hardcoded, but users password should be used for it.
	3. Improve UI
	4. Collect users email addresses so that user can be communicated in event of compromise of security
