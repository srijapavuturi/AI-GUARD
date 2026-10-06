# 🛡️ AI-GUARD

AI-GUARD is a Django-based web application that helps users identify potential job scams and suspicious job offers.

## 🚀 Features

* 🔍 Analyze job descriptions
* 📊 Calculate job scam risk score
* 🚦 Low, Medium, and High Risk classification
* 🚩 Detect suspicious warning signs
* 🛡️ Provide safety recommendations
* 📋 Save analysis results
* 🗂️ View analysis history
* 🗑️ Delete previous analyses
* 📱 Simple and user-friendly web interface

## 🛠️ Technologies Used

* Python
* Django
* HTML
* CSS
* JavaScript
* SQLite

## 📂 Project Structure

```text
AI-GUARD
│
├── backend
│   ├── analyzer
│   ├── config
│   ├── templates
│   └── manage.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ How to Run the Project

### Step 1: Clone the project

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Open the project folder

```bash
cd JobGuard-AI
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

### Step 4: Activate the virtual environment

For Windows:

```bash
venv\Scripts\activate
```

### Step 5: Install the required packages

```bash
pip install -r requirements.txt
```

### Step 6: Go to the backend folder

```bash
cd backend
```

### Step 7: Apply database migrations

```bash
python manage.py migrate
```

### Step 8: Start the Django server

```bash
python manage.py runserver
```

### Step 9: Open the website

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

🎉 AI-GUARD is now running!

## 🎯 How It Works

1. User enters a job description.
2. AI-GUARD checks the description for suspicious patterns.
3. A risk score is calculated.
4. The application displays the risk level and warning signs.
5. The result is saved in the database.
6. Users can view previous analyses from Analysis History.
7. Users can delete previous analysis records.

## 🔐 Security

Sensitive information such as API keys and environment files should not be uploaded to GitHub.

The `.gitignore` file is used to prevent sensitive and unnecessary files from being uploaded.

## 📌 Future Improvements

* 🤖 AI-powered scam detection
* 👤 User authentication
* 📊 Advanced analytics
* 🌐 Online deployment
* 🔎 Improved scam detection

## 👩‍💻 Project Purpose

AI-GUARD was developed as a portfolio project to demonstrate skills in Python, Django, web development, database handling, and basic job scam detection.
