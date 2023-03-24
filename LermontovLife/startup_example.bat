@echo on
call ..\Anaconda\Scripts\activate.bat
call activate FlaskEnv
set FLASK_APP=app.py
set FLASK_DEBUG=0
flask run