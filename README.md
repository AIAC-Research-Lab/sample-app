# Greeting App

A simple FastAPI web application that asks for a user's name and displays a personalized greeting message.

This project is intentionally lightweight and beginner-friendly, making it a good example of:

- building a small web form with FastAPI
- validating user input on the server
- rendering HTML templates with Jinja2
- writing application logs to a local log file

## Features

- Clean HTML form for entering a name
- Personalized greeting output
- Strict validation rules for name input
- Friendly error messages for invalid submissions
- Logging to `logs/app.log`
- Simple startup script for local development

## Tech Stack

- Python 3
- FastAPI
- Uvicorn
- Jinja2
- Python Multipart

## Project Structure

```text
sample-app/
├── app.py
├── requirements.txt
├── startup.sh
├── templates/
│   └── index.html
├── logs/
│   └── app.log
├── env/            # created locally when you set up a virtual environment
└── README.md
```

## Prerequisites

Before running the app, make sure you have:

- Python 3.9 or newer
- `pip` available with your Python installation

## Quick Start

From the project directory, run the following commands:

```bash
cd sample-app
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python app.py
```

Then open the app in your browser at:

```text
http://127.0.0.1:5000
```

## Using the Startup Script

The included `startup.sh` script checks whether the required packages are installed in the local virtual environment and then starts the app.

```bash
cd sample-app
chmod +x startup.sh
./startup.sh
```

> Note: the script is intentionally not executable by default in classroom-style examples to demonstrate how permission issues are handled.

## Input Validation Behavior

The app accepts names that contain:

- letters only
- spaces between names or words

It rejects:

- empty names
- numbers
- symbols
- special characters

Example valid inputs:

```text
John
Mary Jane
Alice Smith
```

Example invalid inputs:

```text
John123
Alice!
@sam
```

## Logging

The app writes logs to:

```text
logs/app.log
```

This helps track requests, validation failures, and generated greetings during local development.

## Running in Production-Style Mode

If you want to run the app with Uvicorn directly:

```bash
cd sample-app
source env/bin/activate
uvicorn app:app --host 127.0.0.1 --port 5000 --reload
```

## License

This project is provided as a simple educational sample application.

## Summary

This app is a beginner-friendly example of how to create a small web app in Python using FastAPI, validate user input, and render a simple HTML interface.
