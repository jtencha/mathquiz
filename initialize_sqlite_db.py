'''
This module should be run once to initialize a new sqlite3 database file for the mathquiz program.
WARNING - Running this module will result in the loss of an existing mathquiz database of the same name.

Execute this file on a python command line by supplying the full path to a new database file.
---
python initialize_sqlite_db.py /full/path/to/db/file.db
---
'''

import sqlite3
import sys
import os
import time

DB_NAME = "mathquiz.db"

# Initializes Orion SQLITE database file based on user-provided file path input
def initialize_db(db_name):

    # Create and connect to database
    print("Creating database...")

    try:
        # Open db connection
        with sqlite3.connect(db_name) as sqlite_connection:
            # Set up connection cursor
            sqlite_cursor = sqlite_connection.cursor()

            # Create COUNTRY table
            sqlite_cursor.execute("DROP TABLE IF EXISTS RESULTS")
            sqlite_connection.commit()
            sqlite_cursor.execute("CREATE TABLE RESULTS (ResultID integer PRIMARY KEY AUTOINCREMENT, \
                                UserName text, NumQuestions integer, NumCorrect integer, \
                                NumWrong integer, PercentageRight real, RunDate date, RunDuration integer, QuizType text)")
            sqlite_connection.commit()
            print("Created RESULTS table")

    except:
        print("Fatal Error:", sys.exc_info())
        quit()


# Run this when called from CLI
if __name__ == "__main__":

    initialize_db(DB_NAME)
    print("Done!")
