from flask import Flask,render_template,request,redirect, make_response, url_for, abort, send_file
import sqlite3
import os
import sys
import time
from datetime import datetime, timedelta, date
import csv
from itertools import permutations
import random
import json
import time

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
@app.route('/' , methods = ['GET','POST'])
def landing():
    return render_template('home.html')


# Handles requests to main web site address "/startquiz/"
@app.route('/startquiz/', methods = ['GET', 'POST'])
def startingQuiz():

    # Handle user-submitted form elements: quiz_type,num_questions,time_per,curr_ques
    quiz_parameters = dict(request.form)
    print(quiz_parameters, type(quiz_parameters))
    quiz_cookie = dict()

    # TODO - Fix these hidden field hacks on doquiz.html
    #<input type="hidden" id="solution" name="solution" value="{{quiz_parameters["solution"]}}">
    #<input type="hidden" id="quiz_type" name="quiz_type" value="{{quiz_parameters["quiz_type"]}}">
    #<input type="hidden" id="curr_ques" name="curr_ques" value="{{quiz_parameters["curr_ques"]|int + 1}}">
    #<input type="hidden" id="num_questions" name="num_questions" value="{{quiz_parameters["num_questions"]}}">
    #<input type="hidden" id="correct" name="correct" value="{{quiz_parameters["correct"]}}">

    # Coming from home page / new quiz
    if "user_answer" not in quiz_parameters:
        quiz_cookie["user_results"] = ""
        quiz_cookie["user_answers"] = ""
        #username = quiz_parameters['username']
        if 'username' not in quiz_parameters:
            return redirect(url_for('landing'))
        elif quiz_parameters['username'] == "":
            quiz_cookie['username'] = "Guest"
        elif quiz_parameters['username'] == "40314":
            quiz_cookie['username'] = "Guest"
            quiz_parameters['num_questions'] = 3
        else:
            quiz_cookie['username'] = quiz_parameters['username']
        print(quiz_parameters['username'])

    # Coming from quiz answer page in quiz
    else:
        quiz_cookie = json.loads(request.cookies.get('quiz_cookie'))
        quiz_cookie["user_answers"] += quiz_parameters["user_answer"] + ";"
        print(quiz_cookie["user_answers"])

        if quiz_parameters["solution"] == quiz_parameters["user_answer"]:
            print("Correct!")
            #print(type(quiz_parameters["correct"]))
            quiz_cookie["user_results"]+="1;"
            print(quiz_cookie["user_results"])
        else:
            print("Incorrect")
            quiz_cookie["user_results"]+="0;"
            print(quiz_cookie["user_results"])

    # Check if done with quiz
    if int(quiz_parameters['curr_ques']) + 1 > int(quiz_parameters['num_questions']):
        raw_answers = quiz_cookie["user_results"].split(";", int(quiz_parameters['num_questions']))
        correct = 0
        for answer in raw_answers:
            print(answer)
            if answer == '1':
                correct += 1
                print(correct)
                #Safety check to see if something went wrong
                #You should never get to this line
                if int(correct) > int(quiz_parameters["num_questions"]):
                    correct = int(quiz_parameters["num_questions"])

        if quiz_parameters['quiz_type'] == "0":
            translated_type = "Multiplication"
        elif quiz_parameters['quiz_type'] == "1":
            translated_type = "Division"
        elif quiz_parameters['quiz_type'] == "2":
            translated_type = "Addition"
        elif quiz_parameters['quiz_type'] == "3":
            translated_type = "Subtraction"
        else:
            translated_type = "Mixed"

        # Add user results to database
        '''
        TABLE RESULTS (ResultID integer PRIMARY KEY AUTOINCREMENT, \
                            UserName text, NumQuestions integer, NumCorrect integer, \
                            NumWrong integer, PercentageRight real, RunDate date, RunDuration integer, QuizType text)
        '''
        num_questions = int(quiz_parameters["num_questions"])
        wrong = num_questions - correct
        results_insert_sql = "INSERT INTO RESULTS (UserName,NumQuestions,NumCorrect,NumWrong,RunDate,RunDuration,QuizType,PercentageRight) VALUES ('{0}',{1},{2},{3},'{4}',{5},'{6}',{7})".format(quiz_cookie['username'],num_questions,correct,wrong,date.today(),0,translated_type, 100 * (round(float(correct)/num_questions,2)))
        print(results_insert_sql)
        run_sql_query(results_insert_sql, query=False)
        resp = make_response(render_template('summary.html', correct = correct, question_total = quiz_parameters["num_questions"], username = quiz_cookie['username'], translated_type = translated_type))
        resp.delete_cookie('quiz_cookie')
        return resp

    else:
        # Set next question
        # Map all of these into quiz_parameters so you don't have to pass in a resp with a million single variables
        quiz_parameters["ques_type"], quiz_parameters["num_one"], quiz_parameters["sign"], quiz_parameters["num_two"], quiz_parameters["solution"] = generate_question(quiz_parameters['quiz_type'])
        resp = make_response(render_template('doquiz.html', quiz_parameters = quiz_parameters, username = quiz_cookie['username']))
        resp.set_cookie('quiz_cookie', json.dumps(quiz_cookie))
        return resp


@app.route('/summary', methods = ['GET', 'POST'])
def end():
    return render_template('summary.html')

# Handles requests to main web site address "/contact", which is a simple contact page
@app.route('/contact', methods = ['GET','POST'])
def contacting():
    return render_template('contact.html')


# Handles requests to main web site address "/scoreboard", which is a results scoreboard page
@app.route('/scoreboard', methods = ['GET','POST'])
def scoring():

    # Pull user results from database
    '''
    TABLE RESULTS (ResultID integer PRIMARY KEY AUTOINCREMENT, \
                        UserName text, NumQuestions integer, NumCorrect integer, \
                        NumWrong integer, PercentageRight real, RunDate date, RunDuration integer, QuizType text)
    '''
    results_retrieve_sql = "SELECT UserName,NumQuestions,NumCorrect,NumWrong,PercentageRight,RunDate,RunDuration,QuizType FROM RESULTS WHERE NumQuestions=$$$ ORDER BY PercentageRight DESC, RunDuration ASC"
    ques_options = ["50","40","30","20"] 
    top_n_limit = 20
    top_n_quiz_results = []
    for option in ques_options:
        run_sql = results_retrieve_sql.replace("$$$",option)
        success,results = run_sql_query(run_sql)[:top_n_limit]
        if success:
            top_n_quiz_results.append(results)
        else:
            top_n_quiz_results.append([])
    
    return render_template('scoreboard.html', top_n_quiz_results=top_n_quiz_results)


# Handles requests to main web site address "/export", which is how results can be exported from the database to a csv file
@app.route('/export', methods = ['GET','POST'])
def exporting():

    sql = "SELECT ResultID, UserName, NumQuestions, NumCorrect, NumWrong, PercentageRight, RunDate, RunDuration, QuizType FROM RESULTS ORDER BY ResultID"
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
app.run(host='0.0.0.0', port=5000)
