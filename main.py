from flask import Flask,jsonify, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from openai import OpenAI
import time
import os
import ast
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from flask_socketio import SocketIO
from autogen import UserProxyAgent, GroupChat, GroupChatManager, config_list_from_json
app = Flask(__name__)


app.secret_key = ' key'
socket_io = SocketIO(app)
def new_print_received_message(self, message, sender):
    message=str(message)
    start_index = message.find("'content': '") + len("'content': '")
    end_index = message.find("'", start_index)
    content = message[start_index:end_index]
    socket_io.emit('message', {"sender": sender.name, "content": content})

GroupChatManager._print_received_message = new_print_received_message

less_costly_config_list = config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json", 
    filter_dict={
        "model": [
            "gpt-3.5-turbo-1106",
        ]
    }
)

less_costly_llm_config = {
    "config_list": less_costly_config_list,
    "timeout": 60,
}

user_proxy = UserProxyAgent(
   name="User_proxy",
   llm_config=less_costly_llm_config,
   system_message="""You are the CEO of a tech company. Your role is to provide a base for cto and engineer to engage in a discussion about the company requirement. You are responsible for introducing topics and moderating the conversation to ensure it remains on track and productive. 
Directive: Facilitate a smooth and engaging conversation between engineer and cto.""",
   human_input_mode="TERMINATE",
   max_consecutive_auto_reply=5
)

# define two GPTAssistants
sam = GPTAssistantAgent(
    name="CTO",
    llm_config=less_costly_llm_config,
    instructions="""You are the CTO of a software company. Engage in a aconversation with the ceo and gather requirements about the project requirements then tell the engineer to start working and discuss with him the technologies.
  At the end of each message, you hand the conversation back to the CEO, by name: User_proxy"""
)

bob = GPTAssistantAgent(
    name="Engineer",
    llm_config=less_costly_llm_config,
    instructions="""You are a software engineer. Your role is to talk to the CTO and figure out how tom carry out the project.
Directive: You write code and pass it to the cto to check.  At the end of each message, you hand the conversation back to the moderator, by name: User_proxy""",
)
summ = GPTAssistantAgent(
    name="summ",
    llm_config=less_costly_llm_config,
    instructions="""You are a software engineer. Your role is to talk to the CTO and figure out how tom carry out the project.
Directive: You write code and pass it to the cto to check.  At the end of each message, you hand the conversation back to the moderator, by name: User_proxy""",
)

costly_config_list = config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json", 
    filter_dict={
        "model": [
            "gpt-3.5-turbo-1106",
        ]
    }
)

costly_llm_config = {
    "config_list": costly_config_list,
    "timeout": 60,
}

# define group chat
groupchat = GroupChat(agents=[user_proxy, sam, bob], messages=[], max_round=100)
manager = GroupChatManager(groupchat=groupchat, llm_config=costly_llm_config)








# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'addie2006'
app.config['MYSQL_DB'] = 'acc'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect('/')
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg='')


@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('chat.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = str(msg)
    return get_Chat_response(input)


def get_Chat_response(text):
   user_proxy.initiate_chat(manager, message=text)
   messages = user_proxy.chat_messages[manager] 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)