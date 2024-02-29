# Installing Dependences
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import openai
import os
import re
from dotenv import load_dotenv
from openai import OpenAI
from flask_basicauth import BasicAuth
import random
#loading environment
import gc
import time

load_dotenv()
#creating basic auth
app = Flask(__name__)
# app.config['BASIC_AUTH_USERNAME'] = os.getenv("PASSWORD")
# app.config['BASIC_AUTH_PASSWORD'] = os.getenv("USERNAME")
app.config['BASIC_AUTH_USERNAME'] = 'Esteem'
app.config['BASIC_AUTH_PASSWORD'] = '29~DE6gjNJ&J'
basic_auth = BasicAuth(app)

openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = "asst_PQhmvRHRqlllXtysPdf1vQV3"

@app.route('/', methods=['GET','POST'])
@basic_auth.required
def ask_question():
    try:
        client = OpenAI()
        user_question = request.json.get('user_question')
        user_location = request.json.get('location')
        user_doj = request.json.get('yearOfJoining')
        user_doj = int(user_doj)
        user_question = user_question.lower()
        # Create a new thread for each question
        thread = client.beta.threads.create()
        print(thread.id)

        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_question
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run.status == "completed":
                break

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        latest_message = messages.data[0]
        text = latest_message.content[0].text.value
        text = re.sub(r'[\[\]\(\)\{\}]', '', text)
        text = text.replace('\n', ' ')
        client = None
        gc.collect()


        # Check if the response starts with "https"
        if text.strip().startswith("https"):
            # List of random texts to choose from
            random_texts = ["Sure!, Here's the Url you can refer to:", "To answer your query, you can refer to below mentioned URL that will provide more information on this", "Check this URL below for more info"]

            # Choose a random text from the list
            random_text = random.choice(random_texts)

            # Concatenate the random text with the GPT-3 response
            text = f"{random_text} {text.strip()}"

        if "https://infobeans_admin_committee" in text:
            if user_location == "Pune":
                text = text.replace("https://infobeans_admin_committee","https://docs.google.com/forms/d/e/1FAIpQLSemXT1GOuBftcj9w2-0W3NZRXGL0eCSWZ9dDsj9uy7Dv5PDcw/viewform")
            elif user_location in ["Indore","Chennai","Vadodara", "Bangalore"]:
                text = text.replace("https://infobeans_admin_committee","https://docs.google.com/forms/d/e/1FAIpQLSfsR415c0QuF5F9bEXi6RSrP1pSzkGX2Z8To3SkqGuqkbXUxg/viewform?pli=1")

        if "https://payroll.creatingwow.in/" in text:
            if user_location == "Chennai":
                text = text.replace("https://payroll.creatingwow.in/","https://payroll.creatingwow.in/chennai")
            elif user_location == "Pune":
                text = text.replace("https://payroll.creatingwow.in/","https://payroll.creatingwow.in/sezpune")
            elif user_location == "Vadodara":
                text = text.replace("https://payroll.creatingwow.in/","https://payroll.creatingwow.in/unit_3")
            elif user_location == "Bangalore":
                text = text.replace("https://payroll.creatingwow.in/","https://payroll.creatingwow.in/unit_3")
            elif user_location == "Indore":
                if user_doj >= 2011:
                    text = text.replace("https://payroll.creatingwow.in/", "https://payroll.creatingwow.in/unit_3")
                elif user_doj < 2011:
                    text = text.replace("https://payroll.creatingwow.in/", "https://payroll.creatingwow.in/SEZINDORE")


        return jsonify({'response': text, 'thread_id': thread.id})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
