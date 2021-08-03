import random
import time
from datetime import datetime

from send_as_email import send_as_email
email_results_to_overlord = False
overlord_email = ""

print("Multiplication Quiz!")
print("Last Updated: 8/2/2020")

def generate_question(ques_type, max_number = 13):

    numbers = [x for x in range(2,max_number)]
    num_one = random.choice(numbers)
    num_two = random.choice(numbers)


    # Handled Mixed/Random Choice first
    if ques_type == "4":
        ques_type = random.choice(["0","1","2","3"])
    print(ques_type, type(ques_type))

    # Multiplication
    if ques_type == "0":
        sign = "*"
        return ques_type,num_one, sign, num_two, num_one * num_two
    # Division
    elif ques_type == "1":
        sign = "/"
        return ques_type,num_one * num_two, sign, num_two, num_one
    # Addition
    elif ques_type == "2":
        sign = "+"
        return ques_type,num_one, sign, num_two, num_one + num_two
    # Subtraction
    elif ques_type == "3":
        sign = "-"
        return ques_type,num_one + num_two, sign, num_one, num_two
    # Unexpected input; default to multiplication

    else:
        print("Question type provided is not supported; Doing multiplication")
        sign = "*"
        return ques_type, num_one, sign, num_two, num_one * num_two


def mathquiz_legacy():

    points = 0

    numbers = [x for x in range(2,13)]

    number_of_questions = num_questions

    #Legacy
    proceed = False

    while not proceed:
        type = input("\nAvalible functions: \n1-Mulitplication\n2-Division\n3-Mixed\nWhat function would you like to do today? ")
        try:
            if (type in ["1"]):
                print("\nMultiplication it is!")
                proceed = True
            elif (type in ["2"]):
                print("\nDivision it is!\n")
                proceed = True
            elif (type in ["3"]):
                print("This function isn't avalible at this time.")
                continue
        except:
            print("\Put the number for which function you would like to practice.")

    num_correct = 0
    missed = list()
    times = list()
    incorrect = list()
    feedback_list = ["Amazing!", "Great Job!", "Keep it up!", "Correct!", "Excellent!", "Awesome!"]
    neg_list = ["Sorry! ", "Almost! ", "Not quite! ", "Oof! ", "*Disappointing Trombone Music* "]

    if (type in ["1"]):
        for question_number in range(1,number_of_questions+1):
            print("\nQuestion " + str(question_number) + " of " + str(number_of_questions) + ":")
            num_one = random.choice(numbers)
            num_two = random.choice(numbers)

            proceed = False

            while not proceed:
                start = time.time()
                print (str(num_one) + " * " + str(num_two))
                answer = input("What is the answer? ")
                correct_answer = num_one * num_two
                try:
                    answer = float(answer)
                    proceed = True
                except ValueError:
                    print("\nYour answer contained something other than a number.\n ")
                    continue

            ans_time = time.time()
            time_to_answer = ans_time - start
            final = int(time_to_answer)
            print("You took " + str(final) + " seconds")

            neg_feed = random.choice(neg_list)
            feedback = random.choice(feedback_list)
            if correct_answer == answer:
                print (str(feedback))
                num_correct += 1
                if final >= 10:
                    print ("Error: This question has been flagged because you took more than ten seconds\n")
                    times.append("{0} * {1}; Took {2} seconds".format(num_one,num_two,final))
                    points += 1
                    print("You gained one point!")
                    print("You have {0} points.".format(points))
                else:
                    points += 2
                    print("You gained two points!")
                    print("You have {0} points".format(points))
            else:
                if final >= 10:
                    print ("Error: This question has been flagged because you took more than ten seconds\n")
                    times.append("{0} * {1}; Took {2} seconds".format(num_one,num_two,final))

                print (str(neg_feed) + "The correct answer was: " + str(correct_answer))
                missed.append("{0} * {1}; Submitted {2}".format(num_one,num_two,answer))
                incorrect.append((num_one,num_two))
                points -= 2
                print("You lost two points!")

        proceed = False

        while not proceed:
            if len(incorrect) == 0:
                proceed = True
                print ("\nYou got no questions wrong. Congratulations!")
            else:
                print ("\nWhoops, you missed some. Lets's review...\n")
                for entry in incorrect:
                    print ("Redo:")
                    num_one, num_two = entry
                    correct_redo = num_one * num_two
                    redo = -1
                    while str(redo) != str(correct_redo):
                        print (str(num_one) + " * " + str(num_two))
                        redo = input("What is the answer? ")
                        if str(redo) == str(correct_redo):
                            print (str(feedback))
                            print ("You took " + str(final) + " seconds\n")
                        else:
                            print("Not Quite! \n")
                proceed = True

        print("\nYou Finished!")
        print("Your total number of points was {0}!".format(points))

        if email_results_to_overlord:
            email_text = "{0} of {1} correct\n\n{2}\n\n".format(num_correct, number_of_questions, "\n".join(missed))
            email_text += "\n".join(times)
            email_result = send_as_email(overlord_email,email_text)
            if email_result:
                print("\nSending results to {0}".format(overlord_email))
            else:
                print("Email failed,",email_text)
        else:
            print("Email has been disabled. Enable it to send the results.")

    elif (type in ["2"]):
        for question_number in range(1,number_of_questions+1):
            print("\nQuestion " + str(question_number) + " of " + str(number_of_questions) + ":")
            num_one = random.choice(numbers)
            num_two = random.choice(numbers)
            product = num_one * num_two
            proceed = False

            while not proceed:
                start = time.time()
                print (str(product) + " / " + str(num_one))
                answer = input("What is the answer? ")
                correct_answer = product / num_one
                try:
                    answer = float(answer)
                    proceed = True
                except ValueError:
                    print("\nYour answer contained something other than a number.\n ")
                    continue

            ans_time = time.time()
            time_to_answer = ans_time - start
            final = int(time_to_answer)
            print("You took " + str(final) + " seconds")

            neg_feed = random.choice(neg_list)
            feedback = random.choice(feedback_list)
            if correct_answer == answer:
                print (str(feedback))
                num_correct += 1
                if final >= 15:
                    print ("Error: This question has been flagged because you took more than fifteen seconds\n")
                    times.append("{0} / {1}; Took {2} seconds".format(product,num_one,final))
                    points += 1
                    print("You gained one point!")
                    print("You have {0} points.".format(points))
                else:
                    points += 2
                    print("You gained two points!")
                    print("You have {0} points".format(points))
            else:
                if final >= 15:
                    print ("Error: This question has been flagged because you took more than fifteen seconds\n")
                    times.append("{0} / {1}; Took {2} seconds".format(product,num_one,final))

                print (str(neg_feed) + "The correct answer was: " + str(correct_answer))
                missed.append("{0} / {1}; Submitted {2}".format(product,num_one,answer))
                incorrect.append((product,num_one))
                points -= 2
                print("You lost two points!")

        proceed = False
        while not proceed:
            if len(incorrect) == 0:
                proceed = True
                print ("\nYou got no questions wrong. Congratulations!")
            else:
                print ("\nWhoops, you missed some. Lets's review...\n")
                for entry in incorrect:
                    print ("Redo:")
                    product, num_one = entry
                    correct_redo = product / num_one
                    redo = -1
                    while redo != correct_redo:
                        print (str(product) + " / " + str(num_one))
                        redo = input("What is the answer? ")
                        proceed = False
                        try:
                            redo = float(redo)
                            proceed = True
                        except ValueError:
                            print("\nYour answer contained something other than a number.\n ")
                            continue
                        if redo == correct_redo:
                            print (str(feedback))
                            print ("You took " + str(final) + " seconds\n")
                        else:
                            print("Not Quite! \n")
                    proceed = True

        print("\nYou Finished!")
        print("Your total number of points was {0}!".format(points))

        if email_results_to_overlord:
            email_text = "{0} of {1} correct\n\n{2}\n\n".format(num_correct, number_of_questions, "\n".join(missed))
            email_text += "\n".join(times)
            email_result = send_as_email(overlord_email,email_text)
            if email_result:
                print("\nSending results to {0}".format(overlord_email))
            else:
                print("Email failed,",email_text)
        else:
            print("Email has been disabled. Enable it to send the results.")
