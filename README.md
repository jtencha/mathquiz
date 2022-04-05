I developed this repo last summer as my summer project. I do not think I will make any major improvements/changes to this, barring some unforseen idea I might have. As of April 5th 2022, the program is still completely functional. 

# Configuration and Running
Install package requirements if not using Anaconda

`pip install -r requirements.txt`

Set up Math Quiz database (don't skip this step)

`python initialize_sqlite_db.py`

To Run Math Quiz Web Server:

`python run_mathquiz_server.py`

Then open browser and navigate to http://0.0.0.0:5000/


If you prefer to run this program in a terminal environment instead of on the web, there is a built in function for this, although I will warn you that it is *extremely* outdated. 

`python legacy.py`
