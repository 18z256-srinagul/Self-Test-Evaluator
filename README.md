# Self-Test-Evaluator
	An application to test yourself

There are times we used to learn some concepts but requires mentor to test our learnings. Sometimes we make use of flashcards wasting paper and ink.
Presenting Self_Test_Evaluator - an self testing application that allows you to take test on questions entered by you on Multiple choice question format. 

The application is developed using kivy package available in python. It also includes material design version of kivy package called kivymd that pleases look. It also makes use of sqlite3 for database requirements.

The list of packages that are used for development of this application are as follows:

Packages for question application:

1) Kivy
2) kivy-deps.angle - https://github.com/Microsoft/angle
3) kivy-deps.glew - http://glew.sourceforge.net/
4) kivy-deps.gstreamer - https://gstreamer.freedesktop.org/
5) kivy-deps.sdl2 - https://libsdl.org/

Packages for answer application:

6) kivymd - https://github.com/HeaTTheatR/KivyMD

To make use of this application, 
1) User has to provide his username and password for identification purposes.
2) User first has to enter questions in one applications (Question.py) that saves questions and corresponding answers in database file. The questions has to be given a unique title and domain name. With the help of this unique title and domain name user can refer these questions from database.
3) To answer these questions or in other words to take self test user has to open another application (Play.py) and enter corresponding question title and domain name.
4) At the end of the test, user is presented with scores and mistakes. This score is taken to leaderboard and provided with rank

Note: The application is not developed completely ( not present in .exe or .apk format ). To make use of this application , the user can install the above packages and run using python interpreter
