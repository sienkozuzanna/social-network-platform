# Social Network Platform

## Project Description

Social Network Platform is a web application that allows users to create profiles, connect with friends, and share content. This project is designed to demonstrate skills in building social networking applications.

## Technologies

The project is built using the following technologies:

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default), configurable with other Django-supported databases

## Features

- User registration with two-factor authentication
- Customizable user profiles (creation and editing)
- Sharing content (text and images)
- Engagement features (commenting and liking posts)
- Follow system (follow and unfollow other users)

## Installation

To set up the project locally, follow these steps:

```bash
# 1. Clone the repository
git clone https://github.com/sienkozuzanna/social-network-platform.git
cd social-network-platform

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Start the development server
python manage.py runserver

The application will be available at http://127.0.0.1:8000/.
