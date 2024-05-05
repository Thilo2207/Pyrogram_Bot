from pyrogram import Client,filters
import os
from dotenv import load_dotenv
import requests 
import random
import html
load_dotenv()

api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
bot_token = os.getenv("bot_token")

app = Client(
      "Thilo",
      api_id ,
      api_hash 
)
def get_question(amount: int) -> list:
    try:
        url = f"https://opentdb.com/api.php?amount={amount}"
        response = requests.get(url)
        response_js = response.json()
        if response.status_code == 200:
            return response_js["results"]
        else:
            return None
    except Exception as e:
        print("Error fetching question:", e)
        return None

def shuffle_choices(choices:list) -> list:
      random.shuffle(choices)
      return choices
def print_choices(choices:list) -> str:
      choices_str = ""
      for choice_index,choice in enumerate(choices,start=1):
            choices_str+= f"{choice_index}.{html.unescape(choice)}\n"
      return choices_str
def user_choice(choices_count:int,message) -> int:
      try:
            user_input = int(message.text)
            if 1 <= user_input <= choices_count:
                  return user_input -1
            else:
                  message.reply_text(f'Invalid choice.Please enter a number between 1 to {choices_count}.')
                  return None
      except ValueError:
            message.reply_text("Invalid input.Please enter a valid integer.")
@app.on_message(filters.command("start"))
def start(client,message):
      message.reply_text("Welcome to the ZoroBot! Type /quiz to start playing.")
@app.on_message(filters.command("quiz"))
def quizz(client, message):
    amount = 1 
    choices_count = 4 
    questions = get_question(amount)
    if questions is None:
        message.reply_text("Failed to fetch questions. Please try again later.")
        return
    global question
    question = questions[0]
    if question is None:
        message.reply_text("No question received. Please try again later.")
        return

    question_text = html.unescape(question['question'])
    choices = question['incorrect_answers']
    choices.append(question['correct_answer'])
    global shuffle_choice
    shuffle_choice = shuffle_choices(choices)
    choices_str = print_choices(shuffle_choice)
    message.reply_text(f'{question_text}\n{choices_str}')
@app.on_message(filters.text)
def check_answer(client, message):
    global question
    global shuffle_choice
    choices_count = len(shuffle_choice)

    try:
        user_choice_index = user_choice(choices_count, message)
        if user_choice_index is not None:
            if shuffle_choice[user_choice_index] == html.unescape(question['correct_answer']):
                message.reply_text("Correct Answer")
            else:
                message.reply_text(f'Wrong Answer. The Correct Answer is: {html.unescape(question["correct_answer"])}')
    except ValueError:
        pass

app.run()