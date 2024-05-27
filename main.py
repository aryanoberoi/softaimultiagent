from flask import Flask,jsonify, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from openai import OpenAI
import time
import tempfile
import os
import ast
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from flask_socketio import SocketIO
from autogen import UserProxyAgent, GroupChat, GroupChatManager, config_list_from_json, autogen
app = Flask(__name__)


app.secret_key = ' key'
socket_io = SocketIO(app)
def new_print_received_message(self, message, sender):
    # Convert the message to a dictionary
    message_dict = self._message_to_dict(message)
    
    # Extract the content from the message dictionary
    content = message_dict.get('content')
    
    # Check if the content is a list (multiple messages) or a single message
    if isinstance(content, str):
        content = [content]

    # Emit each message separately
    for msg in content:
        print(f"{sender.name}: {msg}")
        socket_io.emit('message', {"sender": sender.name, "content": msg})

GroupChatManager._print_received_message = new_print_received_message


less_costly_config_list = config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json", 
    filter_dict={
        "model": [
            "gpt-4-turbo",
        ]
    }
)

less_costly_llm_config = {
    "config_list": less_costly_config_list,
    "timeout": 60,
    "use_docker": False,
}
from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor

# Create a temporary directory to store the code files.
temp_dir = tempfile.TemporaryDirectory()

# Create a local command line code executor.
executor = LocalCommandLineCodeExecutor(
    timeout=10,  # Timeout for each code execution in seconds.
    work_dir=temp_dir.name,  # Use the temporary directory to store the code files.
)

# Create an agent with code executor configuration.


user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
)
code_writer_agent = GPTAssistantAgent(
    name="engineer",
    instructions=""""You are a helpful AI assistant.
Solve tasks using your frontend coding and language skills.
You collaberate with the designer to write and give the code in a single html file where js and css is all in the same one file.
In the following cases, suggest html code for the user to execute. 
Reply 'TERMINATE' in the end when everything is done.
""",
    llm_config=less_costly_llm_config,
    code_execution_config=False, 
)

ceo = GPTAssistantAgent(
   name="CEO",
   llm_config=less_costly_llm_config,
   instructions="""You are the CEO of a company that specializes in making landing pages with html, css and javascript with good design for specific use cases.Discuss the requirements of the landing page and pass them to the CTO. Keep your message under 120 words.""",
   max_consecutive_auto_reply=5
)

sam = GPTAssistantAgent(
    name="CTO",
    llm_config=less_costly_llm_config,
    instructions="""You are the CTO of a software company. Engage in a aconversation with the ceo and gather requirements, discuss the features and requirements of making the landing page with html,  css and javascript. Then direct the conversation to the designer and the engineer to execute. Keep response under 100 words."""
)

bob = GPTAssistantAgent(
    name="Designer",
    llm_config=less_costly_llm_config,
    instructions="""You are a UI/UX designer for website landing pages. You will understand the requirements by talking to the CEO and the conversation between CEO and CTO and based on the takeaway you will create a proper and beautiful design for the landing page and pass it to the engineer to execute.""",
)

costly_config_list = config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json", 
    filter_dict={
        "model": [
            "gpt-4-turbo",
        ]
    
    }
)

costly_llm_config = {
    "config_list": costly_config_list,
    "timeout": 60,
}
# define group chat
groupchat = GroupChat(agents=[user_proxy, sam, code_writer_agent, bob,ceo], messages=[], max_round=1000)
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
    return render_template('login.html', msg='')

@app.route('/file')
def fil():
    import os
    print(os.listdir(temp_dir.name))

@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('index.html')

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
    return render_template("index.html")

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = str(msg)
    import os

    print(os.listdir(temp_dir.name))
    return get_Chat_response(input)


def get_Chat_response(text):
   user_proxy.initiate_chat(manager, message=text, summary_method="reflection_with_llm")
   messages = user_proxy.chat_messages[manager] 


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)