Python Version：Python 3.6.8 (tags/v3.6.8:3c6b436a57, Dec 24 2018, 00:16:47) [MSC v.1916 64 bit (AMD64)] on win32

Dependencies：

	# framework.py:
		from flask import Flask, render_template, jsonify, session, request
		from flask_session import Session
		from werkzeug.utils import secure_filename

		import shutil
		import os
	
		import pymysql
		import redis

	This script using Flask, Flask_Session, and Werkzeug to handle web requests.
	Also, Shutil and OS are used to handle file OS.

	MySQL and Redis are used for zip file uploading.
	Configuration:
		Redis: 127.0.0.1:6379
		MySQL: localhost:3306(self-defined username and password needed)

	To change default config, you can find lines of code like below in "framework.py":
		app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
		db = pymysql.connect(host="localhost", user="root", db="maxWang", password="sinocbd", port=3306)

	You can run the script without the fore-mentioned DBs. Just make sure that you are not using the zip 	file 	upload API(single file upload would be the only API you can use in this case).

	# algEngine.py
	## no new dependency

	The actual computation happens in the following function:
		def normalize_chance(self, chances)

Hot to run:
	1. Make sure you installed all needed dependent libraries.

	2. Open a console and in the root directory("FYP"), type this:
		 python .\backend\framework.py

	then, the output would have something like the following:
		* Running on http://192.168.1.231:8001/ (Press CTRL+C to quit)
	Remember the IP and port.

	Now, it is up and running.


