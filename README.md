README

Files involved:

    /Python Project/newfile.py             #main file to be executed, contains contents of entire Application
    /Python Project/testing.py             #secondary file to be executed before newfile.py in a separate terminal to facilitate ChatPage
    /Python Project/connectivity_file.py   #functions related to MySQL connectivity
    /Python Project/Mail_functions.py      #functions related to sending mail for OTP and Hire/Apply
    /Python Project/templates/index.html   #web browser facilitating ChatPage

    /Python Project/JS_Login.png           #images used as Background in GUI
    /Python Project/Login_BG.png           #images used as Background in GUI
    /Python Project/Recruiter_Login.png    #images used as Background in GUI
    /Python Project/UP_JobSeeker.png       #images used as Background in GUI
    /Python Project/UP_Recruiter.png       #images used as Background in GUI

    /Python Project/pfps                   #directory containing profile pictures of accounts

Usage:

    Run testing.py in a terminal using the command "python testing.py"
    Run newfile.py in another terminal using the command "python newfile.py"
    Interact with GUI of newfile.py

Dependencies and Installation:

    To run the project, Python and MySQL are required
    They can be properly installed by visiting their official websites
        Python: https://www.python.org/downloads/
        MySQL: https://dev.mysql.com/downloads/mysql/

    The following modules are used in the project and need to be installed if not already installed:
        tkinter
        os
        mysql.connector
        kivy
        threading
        functools
        reportlab
        PIL
        socketio
        smtplib
        flask
        flask_socketio

    To install the above modules, 
    Create a file called requirements.txt with these contents
        mysql-connector-python
        kivy
        reportlab
        pillow
        python-socketio
        Flask
        flask-socketio
    Then run "pip install -r requirements.txt"(bash) in the terminal or its equivalent depending on the shell
    The other modules are built in along with Python and need not be installed separately

