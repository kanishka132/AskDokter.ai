from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session 
import requests
import re
import json
import os
from markdown import markdown
from markupsafe import Markup

app = Flask(__name__)

#Add secret key to access session
app.secret_key = os.urandom(24)

#Configure to use server-side session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False  # avoids setting permanent session cookies

Session(app)  # initialize the session handler

#Calling API
#API key
api_key = "Insert your perplexity api key here"
#API endpoint
url = "https://api.perplexity.ai/chat/completions"


#Home route
@app.route('/')
def home():
    return render_template('index.html')


#Mythbuster route
@app.route('/mythbuster', methods=['GET','POST'])
def mythbuster():
    reply = None
    if request.method == 'POST':
        #Extract user input from submitted form
        user_input = request.form.get('userInput','')

        #call API
        prompt = f"""
        You are a trusted health expert whose job is to debunk or confirm health myths 
        in a simple, accurate, and respectful way.
        Only return the raw JSON object, not wrapped in any text and no markdown
        Provide a output with exactly 4 keys:
        "reply": A one line clear statement telling if it is a myth or a fact.
        "verdict": One of "True", "False", or "Partially True".
        "explanation": A brief explanation of the reasoning, including scientific context.(without citation markers)
        "citations": A list of 10 trusted sources along wiht statements from these sources which backup the reply and a full URL format link.
        Now only answer this question:
        "{user_input}"
        """.strip()

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "sonar",
            "messages": [{"role":"user", "content":(prompt)  }]
        }

        response = requests.post(url, headers=headers,json=payload)
        data = response.json()

        ## Debug: Print raw API response from backend
        # print(data)

        content = data["choices"][0]["message"]["content"]

        #clean content by removing markdown format
        result = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip(), flags=re.IGNORECASE)

        #parse JSON formatted string into dictionary
        parsed = json.loads(result)

        # Store in session to persist after redirect
        session["reply"] = parsed["reply"]
        session["verdict"] = parsed["verdict"]
        session["explanation"] = parsed["explanation"]
        session["citations"] = parsed.get("citations", [])
        session["question"] = user_input

        # Redirect to avoid re-running on refresh
        return redirect(url_for('mythbuster'))

    # GET request — retrieve values from session if they exist
    reply = session.pop("reply", None)
    verdict = session.pop("verdict", None)
    explanation = session.pop("explanation", None)
    citations = session.pop("citations", [])
    question = session.pop("question", None)

    return render_template('mythbuster.html',
                           reply=reply,
                           verdict=verdict,
                           explanation=explanation,
                           citations=citations,
                           question=question)


#function for sonar chatbot
def ask_sonar(message, history):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    messages = history + [{"role": "user", "content": message}]
    payload = {
        "model": "sonar-pro",
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=payload)
    try:
        data = response.json()
        print("DEBUG response:", data)
        reply = data['choices'][0]['message']['content']
        
    except Exception as e:
        reply = f"[Error: {e}. Response: {response.text}]"
        

    messages.append({"role": "assistant", "content": reply})
    return  messages

def format_bot_message(msg):
    html = markdown(msg, extensions=['extra'])
    return Markup(html)
app.jinja_env.globals.update(format_bot_message = format_bot_message)


#Symptom checker route
@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('symptom'))

@app.route('/symptom', methods=['GET', 'POST'])
def symptom():
    
    if 'symptom_chat_history' not in session:
        prompt = """
        You are a helpful and respectful AI medical assistant.

        Rules:
        1. Respond only to health-related or medical questions.
        2. Give a nice, readable format
        3. Greet the user if they say hello or else more forward with their concern. Do not greet twice.
        4. Do not ask multiple questions at once. Only ask one follow-up question based on the user's previous answer.
        5. If you present a numbered list (e.g., 1. Tickly cough, 2. Hacking cough...), and the user replies with a number (e.g., "3"), assume they are selecting that option. Do not repeat the list.
        
        Do Not:
        1. No citations in any form. No reference numbers or links.
        2. Do not repeat any question unless the user's response is unrelated or unclear.

        Steps:
        1. Begin by asking the user to describe their symptom (if they haven't already).
        2. According to the conversation only ask relevant follow-up questions one at a time. Decide which of the below are relevant or if you need to add any other helpful question for accurate diagnosis
        - Type or variant of the symptom (use a list with brief definitions)
        - Duration of the symptom
        - Relevant personal or family medical history

        3.When you are ready to provide a diagnosis, structure it under the heading Diagnosis.
        Use the following format:
        Diagnosis
        1. Diagnosis Name
        - Reasoning: Short explanation
        - Treatment: Brief guidance
        - Medical Attention: Yes/No and when to seek it
        - Severity: Low / Moderate / High
        Never include citation numbers

        If you still need more information from the user, do not include the diagnosis section yet. Instead, continue asking clarifying questions until confident.
        If only partial information is available but a tentative diagnosis is possible, label it as:
        Preliminary Diagnosis
        Only present one of these sections (Diagnosis / Preliminary Diagnosis) after all appropriate follow-ups.

        Important:
        - Wait for the user's response before moving to the next step.
        - Be friendly, clear, and medically informative, but concise.

        """.strip()

        session['symptom_chat_history'] = [
            {"role": "system", "content": prompt}
        ]
        

    if request.method == 'POST':
        user_input = request.form['user_input']
        updated_history = ask_sonar(user_input, session['symptom_chat_history'])
        session['symptom_chat_history'] = updated_history
        session.modified = True

    return render_template("symptom.html", chat=session['symptom_chat_history'])



# Mental Health Assistant route
@app.route('/mental_reset')
def mental_reset():
    session.clear()
    return redirect(url_for('mentalhealth'))

@app.route('/mentalhealth', methods=['GET', 'POST'])
def mentalhealth():
    
    if 'mental_chat_history' not in session:
        prompt = """
        You are a supportive, empathetic, and respectful AI mental wellness assistant.

        Rules:
        1. Always create a safe and non-judgmental space for users to express their thoughts and feelings.
        2. Greet users warmly if they say hello. Otherwise, gently ask how they're feeling or what's on their mind.
        3. Avoid diagnosing or labeling the user. Provide emotional support, coping strategies, and self-help techniques.

        Do Not:
        1. Do not give citations/citation numbers in response.
        2. Do not repeat questions unless the response was completely unrelated or unclear.

        Steps:
        1. Based on user responses, ask reflective or clarifying follow-up questions to encourage deeper expression.
        2. Provide relevant coping strategies, mindfulness tips, or supportive affirmations when appropriate.
        3. If the user indicates distress or crisis, gently suggest they talk to a mental health professional or reach out to emergency support.

        Important:
        - Be conversational and emotionally intelligent.
        - Keep tone warm, reassuring, and compassionate.
        - Focus on listening, reflecting, and supporting rather than solving or diagnosing.
        """.strip()

        session['mental_chat_history'] = [
            {"role": "system", "content": prompt}
        ]

    if request.method == 'POST':
        user_input = request.form['user_input']
        updated_history = ask_sonar(user_input, session['mental_chat_history'])
        session['mental_chat_history'] = updated_history
        session.modified = True

    return render_template("mentalhealth.html", chat=session['mental_chat_history'])


if __name__ == "__main__":
    app.run(debug=True)
