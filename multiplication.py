import random
import time
from datetime import datetime
#run this as a python3 program in terminal

from send_as_email import send_as_email
email_results_to_overlord = False
#overlord_email = "" Put your email here where you want it sent.

print("Benjamin's Mulitplication Quiz!")

points = 0
proceed = False

while not proceed:
    max_inq = input("Enter max range for numbers: ")
    try:
        max = int(max_inq)
        if int(max) >= 100 or int(max) <= 10:
            print("You need to pick between 10-100! \n")
        elif int(max_inq) == max:
            proceed = True
        else:
            print("Sorry, I didn't catch that\n")
    except:
        print("Sorry, I didn't catch that.\n")

numbers = [x for x in range(2,max)]

proceed = False

while not proceed:
    questions = input("How many questions would you like to do today? ")
    try:
        number_of_questions = int(questions)
        if number_of_questions <= 29 or number_of_questions >= 101:
            print("Error: Pick between 30 and 100")
            #Note: I designed this for my sister so that is why there is a limit.
        else:
            proceed = True
    except:
        print("Error: Do not include letters/symbols")

num_correct = 0
missed = list()
times = list()
incorrect = list()
for question_number in range(1,number_of_questions+1):
    print("\nQuestion " + str(question_number) + " of " + str(number_of_questions) + ":")
    num_one = random.choice(numbers)
    num_two = random.choice(numbers)
    print (str(num_one) + " * " + str(num_two))

    start = time.time()
    answer = input("What is the answer? ")
    correct_answer = num_one * num_two
    ans_time = time.time()
    time_to_answer = ans_time - start
    final = int(time_to_answer)
    print ("You took " + str(final) + " seconds")

    proceed = False
    while not proceed:
        try:
            if (answer in [" ", ""]):
                print ("Well that can't be right. Try again.")
                print ("\n" + str(num_one) + " * " + str(num_two))
                answer = input("What is the answer? ")
            else:
                proceed = True
        except:
            print("Internal Error")
            quit()

    feedback_list = ["Amazing!", "Great Job!", "Keep it up!", "Correct!", "Excellent!", "Awesome!"]
    neg_list = ["Sorry! ", "Almost! ", "Not quite! ", "Oof! ", "*Disappointing Trombone Music* "]
    neg_feed = random.choice(neg_list)
    feedback = random.choice(feedback_list)
    if str(correct_answer) == str(answer.strip()):
        print (str(feedback))
        num_correct += 1
        if final >= 10:
            print ("Error: This question has been flagged because you took more than ten seconds\n")
            times.append("{0} * {1}; Took {2} seconds".format(num_one,num_two,final))
            points -= 1
            print("You lost one point!")
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
    if number_of_questions == 2:
        proceed = True
    elif len(incorrect) == 0:
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
    email_text = "User finished with {0} points".format(points)
    email_result = send_as_email(overlord_email,email_text)
    if email_result:
        print("\nSending results to {0}".format(overlord_email))
    else:
        print("Email failed,",email_text)
else:
    print("Email has been disabled. Enable it to send the results.")
