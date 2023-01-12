"""
Title: Python Quiz
Description: Script for python quiz game with email functionality to send results to any recipient
Author: Albin Anthony (Ibha-X)
Date: 22-12-2022
Credits: Tutorials Point (Questions scraped from tutorialspoint.com)
"""

# Standard Imports
from sys import platform
from os import system
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
from random import shuffle
import json

# Specific Imports
from requests import get
from bs4 import BeautifulSoup

# Constants
AUTHOR = "Albin Anthony"
CREDITS = "Tutorials Point"

# Checking platform for using system functionalities
if platform in ["linux", "linux2"]:
    # clears the screen for linux machines
    clear = lambda: system("clear")
       
elif platform == "win32":
    # clears the screen for windows machines
    clear = lambda: system("cls")


def Print(string, speed=4) -> None:
    """
    A simple script for displaying typewriter effect on screen
    """
    if speed > 10: speed = 10
    elif speed < 0: speed = 0
    for i in string:
        print(i, flush=True, end="")
        sleep((10-speed) * 0.005)

def python_qa() -> dict:
    """Generator script for scraping questions and answers from the website tutorialspoint.com """
    url = "https://www.tutorialspoint.com/python/python_mock_test.htm?min=1&max=100"
    res = get(url).content
    soup = BeautifulSoup(res, "lxml")
    
    # Fetching Questions
    questions = soup.find_all("div", class_="QA")
    for i in questions:
        ques = i.find("p").text.split('-')[1].strip()
        options = [" ".join(a.text.split('-')[1:]).strip() for a in i.find_all("a")]
        ans = i.find("h3").text.split(':')[1].strip()
        explanation = i.find_all("h3")[1].find_next_sibling("p").text
        
        # compiling results as a dictionary object
        data = {
            "question": ques,
            "options": options,
            "ans": ans,
            "explanation": explanation
        }
        yield data

def save_questions(filepath) -> None:
    """ A simple script for saving scraped data"""
    questions = list(python_qa())
    shuffle(questions)
    
    with open(f"{filepath}.json", "w") as file:
        # converts the data into json format
        data = json.dumps(questions, indent=4)
        file.write(data)
        
def quiz() -> tuple:
    """ Quiz Game """
    Print("\t\tPython Quiz\n")
    Print("\t\t-----------\n")
    questions = list(python_qa())
    shuffle(questions)
    Print("Enter your Name: ")
    name = input().title()
    clear() # clears the screen
    correct_answers = 0 # calculates correct answers
    wrong_answers = 0 # calculates wrong answers
    question_attended = 0 # calculates total questions attended
    skipped = 0 # calculates skipped questions
    
    # looping over questions
    for idx, i in enumerate(questions):
        print("\t\tPython Quiz")
        print("\t\t-----------\n")
        print(f"Question {idx+1} of {len(questions)}")
        Print(f"{i['question']}\n", speed=6)
        print()
        
        # looping over answers
        options = i['options']
        for idx, option in enumerate(options):
            Print(f"{'ABCD'[idx]}. {option}\n", speed=8)
        
        user = input("\nYour answer (A, B, C, D, skip): ").lower()
        ans = i['ans'].lower()
        
        # checks if the user inputs a valid answer
        options = "abcdskip"
        while user not in options:
            Print("Invalid input, Choose one of (A, B, C, D): ")
            user = input().lower()
        
        # skips the current question
        if user in ['s', 'skip']:
            skipped += 1
            clear() # clears the screen
            continue
        
        # checks if the answer provided by the user is correct ir not
        if user == ans:
            correct_answers += 1
            Print("Correct Answer..\n\n")
            Print("Need Explanation? (yes, no): ")
            exp = input()
            
            # checks if the user inputs a valid answer
            v_ans = "yesno"
            while exp not in v_ans:
                Print("Invalid input, Choose one of (yes, no): ")
                exp = input().lower()
                
            if exp in ['yes', 'y']:
                Print(i['explanation'], speed=5)
           
        elif user != ans:
            wrong_answers += 1
            Print("Wrong Answer..\n\n")
            Print("Show Answer? (yes, no): ")
            show = input()
            
            # checks if the user inputs a valid answer
            v_ans = "yesno"
            while show not in v_ans:
                Print("Invalid input, Choose one of (yes, no): ")
                show = input().lower()
                
            if show in ['yes', 'y']:
                Print(f"\nCorrect Answer is {ans.upper()}\n")
                print("\nExplanation:")
                print("------------")
                Print(i['explanation'], speed=6)
        
        question_attended += 1
        Print("\nNext Question? (yes, no): ")
        action = input()
        if action in ['yes', 'y']:
            clear() # clears the screen
            continue
        break
    clear() # clears the screen
    avg = (correct_answers/len(questions))*100
    completion = f"{name} has completed the quiz!" \
                    if question_attended == 100 else \
                    f"{name} has attended {question_attended} questions"
    Print(completion)
    
    data = f"""\n\t\tResults\n\t\t-------\n{'Student Name': <20}: {name}\n{'Questions Attended': <20}: {question_attended} out of {len(questions)}\n{'Correct Answers': <20}: {correct_answers}\n{'Wrong Answers': <20}: {wrong_answers}\n{'Questions Skipped': <20}: {skipped}\n{'Average score': <20}: {avg}%\n{'Author': <20}: {AUTHOR}\n{'Credits': <20}: {CREDITS}\n"""
    Print(data, speed=6)
    return data, completion

def message(from_, to, subj=None, body=None) -> object:
    """ Script for compiling email """
    msg = MIMEMultipart()
    msg['From'] = from_
    msg['To'] = to
    msg['Subject'] = subj
    messages = body
    msg.attach(MIMEText(messages.format("albi", "ibha-x"), 'plain'))
    return msg.as_string()
    
    
def send_mail(from_=None, pass_=None, subj=None, body=None,to=None) -> None:
    """ Script for sending email using gmail imap server"""
    SERVER = "smtp.gmail.com"
    PORT = 587
    EMAIL = from_
    PASS = pass_
    
    with SMTP(SERVER, PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL, PASS)
        Print("\nLogged In Successfully")
        Print("\nCompiling Message...")
        Print("\nSending Email...")
        msg = message(EMAIL, to, subj=subj, body=body)
        smtp.sendmail(EMAIL, to, msg)
        Print("\nEmail Successfully Sent!")

def main(from_=None, pass_=None, to=None) -> None:
    """ Main function responsible for executing every other functions """
    body, subject = quiz()
    input()
    if from_ and pass_ and to:
        Print("\nShare Results? (yes, no): ")
        share = input().lower()
        v_ans = "yesno"
        while share not in v_ans:
            Print("Invalid input, Choose one of (yes, no): ")
            share = input().lower()
            
        if share in ['y', 'yes']:
            send_mail(from_=from_, pass_=pass_,
                       to=to, subj=subject, body=body)
                           
    clear() # clears the screen
    print("\t\tPython Quiz")
    print("\t\t-----------\n")
    Print("Thank you for attending the quiz, All the best")

if __name__ == "__main__":
    from_ = "your_email@your_domain.com" # Your email address
    pass_ = "your_app_password"# Your app password
    # use your own password, preferably use an environment variable
    to = "recipient_email@recipient_domain.com" # To address, email address of the email recipient
    
    # pass the variables (from_, to, pass_) to the main function for sending email
    main()

