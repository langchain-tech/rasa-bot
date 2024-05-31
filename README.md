# RASA CHATBOT

This repository contains the code for the Zappy Healthcare Shipment Tracking Chatbot project. The goal of this project is to create an interactive chatbot that allows users to track the status of their shipment orders and handle queries related to Zappy Healthcare. The chatbot uses Rasa for natural language understanding and dialogue management, integrates with shipment tracking APIs, and utilizes a web interface for user interaction.



## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)


## Introduction
The Zappy Healthcare Shipment Tracking Chatbot project simplifies the process of tracking shipment orders and querying information related to Zappy Healthcare services. It leverages state-of-the-art natural language processing models and provides a user-friendly interface to interact with users.

## Features

- **Order Tracking**: Track the status of shipment orders in real-time.
- **Interactive Q&A**: Ask questions and receive answers related to Zappy Healthcare.
- **User-Friendly Interface**: Built with a web framework for ease of use.
- **Integration with Shipment APIs**: Retrieves real-time shipment data.
- **Natural Language Understanding** : Utilizes Rasa for robust dialogue management

## Technologies Used

- **Rasa**: Framework for building conversational AI.
- **Python**: Programming language for backend development.

## Setup Instructions

Follow these steps to set up the project on your local machine:


**1. Clone the Repository**
Begin by cloning the repository to your local machine:
```
https://github.com/langchain-tech/zappyhealth-rasa-bot.git
cd zappyhealth-rasa-bot
```

**2. Create a Virtual Environment**
It is recommended to create a virtual environment to manage dependencies:
```
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```

**3. Install Dependencies**
Install the necessary packages listed in the requirements.txt file:
```
pip install -r requirements.txt
```



**4. Start the Application**

Train your model
```
rasa train
```

Run your rasa bot 
```
rasa run --enable-api
```

## Usage

- **Interact with the Chatbot**: Use the web interface to start a conversation with the chatbot.
- **Track Orders**: Enter your shipment order details to get real-time tracking information.
- **Ask Questions**: Enter your questions related to Zappy Healthcare and receive relevant answers.