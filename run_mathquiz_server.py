from flask import Flask,render_template,request,redirect, make_response, url_for, abort, send_file
import sqlite3
import os
import sys
import time
from datetime import datetime, timedelta
import csv
from itertools import permutations
import random

# Local import
from multiplication import generate_question

# Standard initializion of Flask object
app = Flask(__name__)

DB_NAME = "mathquiz.db"

# Function run_sql_query
# Routine to execute SQL queries on Database. Makes new connection on each call to avoid multi-user write conflicts.
# Inputs
# sql = Text string of valid SQL text; required
# query = If True, sql input text contains a SQL query. If False, sql input text contains a SQL executable statement
# return_as_dict = If True, results are returned in dictionary form. If False, results are returned as a list
# Output 1 is Boolean indicating success of query
# Output 2 is results from database, if applicable
def run_sql_query(sql, query=True, return_as_dict=True):

    try:
        # Open db connection
        with sqlite3.connect(DB_NAME) as sqlite_connection:
            # Returns results as dict
            if return_as_dict:
                sqlite_connection.row_factory = sqlite3.Row
            # Set up connection cursor
            sqlite_cursor = sqlite_connection.cursor()

            # Run the provided SQL text
            sqlite_cursor.execute(sql)
            if query:
                results = sqlite_cursor.fetchall()
                print("Successful SQL Query")
                return True, results
            else:
                sqlite_connection.commit()
                print("Successful SQL Execution")
                return True, None
    except:
        print("Error connecting to database:", sys.exc_info())
        return False, None


# Function getResults
# Routine to retrieve a full (non-archived) list of results
# Inputs = None
# Output = List of quiz results
def getResults(UserName=None, QuizType=None, DaysAgo=365, OrderedBy=None):
    sql = "SELECT ResultID, UserName, NumQuestions, NumCorrect, \
                        NumWrong, RunDate, RunDuration, QuizType FROM RESULTS"

    # TODO - Need to calculate minimum requested RunDate from DaysAgo

    # TODO - Need to add WHERE statements based on inputs

    completed, queryResults = run_sql_query(sql)
    if completed:
        return True, queryResults
    else:
        return False, None


# Handles requests to main web site address "/"
# Attempts a database connection and routes to first_time.html is unsuccessful
@app.route('/' , methods = ['GET','POST'])
def landing():
    return render_template('home.html')


# Handles requests to main web site address "/startquiz/"
@app.route('/startquiz/', methods = ['GET', 'POST'])
def startingQuiz():

    # Handle user-submitted form elements: quiz_type,num_questions,time_per,curr_ques
    quiz_parameters = request.form
    print(quiz_parameters)

    if "user-answer" in quiz_parameters:
        if quiz_parameters["solution"] == quiz_parameters["user-answer"]:
            feedback = random.choice(["Amazing!", "Great Job!", "Keep it up!", "Correct!", "Excellent!", "Awesome!"])
            print("Correct!")
        else:
            feedback = random.choice(["Sorry! ", "Almost! ", "Not quite! ", "Oof! ", "*Disappointing Trombone Music* "])
            print("Incorrect")

    # Check if done with quiz
    if int(quiz_parameters['curr_ques']) + 1 > int(quiz_parameters['num_questions']):
        return render_template('scoreboard.html')
    else:
        # Set next question
        ques_type, num_one, sign, num_two, solution = generate_question(quiz_parameters['quiz_type'])
        return render_template('doquiz.html', ques_type = ques_type, num_one = num_one, sign = sign, num_two = num_two, solution = solution, quiz_parameters = quiz_parameters)



# Handles requests to main web site address "/contact", which is a simple contact page
@app.route('/contact', methods = ['GET','POST'])
def contacting():
    return render_template('contact.html')


# Handles requests to main web site address "/scoreboard", which is a results scoreboard page
@app.route('/scoreboard', methods = ['GET','POST'])
def scoring():
    # TODO - lots of work here once quizzes are working and being recorded in db
    return render_template('scoreboard.html')


# Handles requests to main web site address "/export", which is how results can be exported from the database to a csv file
@app.route('/export', methods = ['GET','POST'])
def exporting():

    sql = "SELECT ResultID, UserName, NumQuestions, NumCorrect, NumWrong, RunDate, RunDuration, QuizType FROM RESULTS ORDER BY ResultID"
    status, searchResults = run_sql_query(sql, return_as_dict=False)
    if status is False or searchResults is None:
        return "Failed"
    with open('static/mathquiz_export.csv','w') as fout:
        fnames = ["ResultID", "UserName", "NumQuestions", "NumCorrect", \
                            "NumWrong", "RunDate", "RunDuration", "QuizType"]
        writer = csv.writer(fout)
        #writer = csv.DictWriter(fout, fieldnames=fnames)
        #writer.writeheader()
        writer.writerow(fnames)
        for record in searchResults:
            #print(record)
            writer.writerow(record)

    try:
        return send_file('static/mathquiz_export.csv', attachment_filename='mathquiz_export.csv')
    except Exception as e:
        return str(e)


# Kick off app locally on port 5000
app.run(host='localhost', port=5000)
