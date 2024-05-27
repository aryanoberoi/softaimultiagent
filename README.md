


## Tech Stack

**Client:** HTML, CSS, TailwindCSS, Javascript

<<<<<<< HEAD
**Server:** Flask,MySQL, SocketIO

**GPT:** Open AI API, AutoGEN framework
=======
**Server:** Flask,SocketIO

**GenAI:** Open AI API, AutoGEN framework
>>>>>>> 9e79067fe5f7a8c8d0ad1efd19856035b1672f71

## Installation

Clone the repository

Install necessary dependencies from requirements.txt 

Run the application by running python main.py
    

## Documentation

Soft AI, virtual chat-powered company for software
<<<<<<< HEAD
 development, brings together agents including chief officers, professional programmers, test
 engineers, and UI/UX designers. When presented with a preliminary
=======
 development, brings together agents including chief officers, professional programmers and UI/UX designers. When presented with a preliminary
>>>>>>> 9e79067fe5f7a8c8d0ad1efd19856035b1672f71
 task by a human “client, the agents at SoftAI engage in
 effective communication and mutual verification
 through collaborative chatting. This process enables them to
 automatically craft comprehensive
<<<<<<< HEAD
 software solutions that encompass source codes, environment
 dependencies, and user manuals.

=======
 landing pages that are well designed, tested and satisfy user requirement.
>>>>>>> 9e79067fe5f7a8c8d0ad1efd19856035b1672f71
#### Setup

- Flask Setup: The application is built on Flask, a lightweight WSGI web application framework in Python, providing tools and features to build web apps quickly.

- MySQL Integration: Utilizes Flask-MySQLdb for database interactions, storing user accounts and managing sessions for authentication.

- Session Management: Uses secret keys to securely manage user sessions, enabling personalized experiences like user authentication and maintaining chat state.

#### Authentication System

- Login Functionality: Processes user login requests, validating credentials against the MySQL database, and managing session data for logged-in users.

- Registration Process: Handles new user registrations, including validation of user inputs and insertion of new accounts into the database.

- Logout Mechanism: Provides users the ability to securely logout, clearing session data to prevent unauthorized access.


#### AI Integration for Chat Simulation

- GPT Assistant Agents: Implements GPT-based AI agents (CTO, Engineer) with specific roles and directives to participate in chat discussions, simulating a real project planning and execution conversation.

- SocketIO for Real-time Communication: Leverages Flask-SocketIO to enable real-time messaging, allowing users and AI agents to interact seamlessly.

- Custom Message Handling: Overrides default message handling to extract and broadcast chat content dynamically, enhancing the chat experience.

<<<<<<< HEAD
#### AI Agents and Group Chats
=======
#### AI Agents and Group Chats (Autogen)
>>>>>>> 9e79067fe5f7a8c8d0ad1efd19856035b1672f71

- GroupChat and GroupChatManager: Orchestrates conversations among multiple participants, including real users and AI agents, enforcing turn-based messaging and chat progression.

- Dynamic Chat Flow: Adjusts the chat flow based on directives, ensuring each participant (CEO, CTO, Engineer) contributes meaningfully to the conversation.

#### Role of Prompt Engineering in Chat Simulation

- Prompt engineering involves crafting specific instructions to guide AI models in generating contextually appropriate responses.

- Implementation of Chat Simulation:
 Each AI agent (CEO, CTO, Engineer) receives tailored instructions that define    their role-specific behaviors and dialogue styles within the chat.

- Directives included in these prompts dictate how each agent should contribute to the conversation, ensuring smooth transitions and maintaining focus.



<<<<<<< HEAD
#### Overview of AutoGen LLM

##### Introduction to AutoGen:

AutoGen is a cutting-edge framework designed for developing LLM (Large Language Models) applications. It enables seamless integration of multiple conversational agents that can autonomously or collaboratively perform complex tasks.
=======
>>>>>>> 9e79067fe5f7a8c8d0ad1efd19856035b1672f71






<<<<<<< HEAD
## Demo

Insert gif or link to demo


## License

[MIT](https://choosealicense.com/licenses/mit/)


=======
>>>>>>> 9e79067fe5f7a8c8d0ad1efd19856035b1672f71
