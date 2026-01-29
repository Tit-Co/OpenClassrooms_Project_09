# Django app - OpenClassrooms Project 09
**Develop a web application using Django**

---

## DESCRIPTION

This project was completed as part of the "Python Developer" path at OpenClassrooms.

The goal was to develop a web application with Django capable of:
- Publishing reviews of books or articles.
- Requesting reviews, as a ticket, on a book or a defined article.
- Looking for interesting books to read based on reviews from others users.

The application must:
- Comply with WCAG guidelines for users with disabilities
- Conform to the provided mockups in terms of its design
- Conform to the provided database schema, which covers the required features
---

## EXPLANATIONS OF WHAT THE APP DOES

### <u>Sign in and log in, log out</u>

- The app allows the user to sign up or log in from the homepage, and to log out

### <u>Tickets, comments, feeds and followers</u>

- The app displays tickets and reviews in the feed and allows the user to follow others users

### <u>Add, update, delete tickets and reviews</u>

- The app allows the user to create, update and delete tickets and reviews in the feed conforming to th CRUD operations

### <u>Subscription page</u>

- The app allows the user to subscribe to others users feeds or unsubscribe from

---

## PROJECT STRUCTURE
<p align="center">
<img src="docs/structure_1.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
<img src="docs/structure_2.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
</p>

---

## INSTALLATION

### - Clone the repository :
`git clone https://github.com/Tit-Co/OpenClassrooms_Project_09.git`

### - Navigate into the project directory :
`cd OpenClassrooms_Project_09`

### - Create a virtual environment and dependencies :
### Option 1 - with [uv](https://docs.astral.sh/uv/)

`uv` is an environment and dependencies manager.

#### - Install environment and dependencies

`uv sync`

### Option 2 - with pip

#### - Install the virtual env :

`python -m venv env`

#### - Activate the virtual env :
`source env/bin/activate`  
Or  
`env\Scripts\activate` on Windows  

### - Install dependencies 
#### Option 1 - with [uv](https://docs.astral.sh/uv/)

`uv pip install -U -r requirements.txt`

#### Option 2 - with pip

`pip install -r requirements.txt` 

---

## USAGE

### Launching server
- Open a terminal
- Go to project folder : `cd litreview`
- If needed, make migrations and execute them : 
  - `python manage.py makemigrations`
  - `python manage.py migrate`
- Launch the Django server : `python manage.py runserver`

### Launching the website
- Open a web browser
- And type the URL : `http://127.0.0.1:8000/`
---

## EXAMPLES

- Home page (sign up or log in)
<p align="center">
    <img src="docs/screenshots/homepage_screenshot.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
</p>

- Sign up form
<p align="center">
    <img src="docs/screenshots/signin_form_screenshot.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
</p>

- Feed page
<p align="center">
    <img src="docs/screenshots/feed_screenshot_1.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
    <img src="docs/screenshots/feed_screenshot_2.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
</p>

- Posts page
<p align="center">
    <img src="docs/screenshots/posts_screenshot_1.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
    <img src="docs/screenshots/posts_screenshot_2.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
</p>

- Version for people with disabilities
<p align="center">
    <img src="docs/screenshots/disabilities_version_1.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
    <img src="docs/screenshots/disabilities_version_2.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
    <img src="docs/screenshots/disabilities_version_3.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
</p>

- Tickets creation page
<p align="center">
    <img src="docs/screenshots/ticket_creation_screenshot.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
</p>

- Reviews creation page
<p align="center">
    <img src="docs/screenshots/review_creation_screenshot_2.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
    <img src="docs/screenshots/review_creation_screenshot_1.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
</p>

- Update posts and reviews pages
<p align="center">
    <img src="docs/screenshots/update_ticket_screenshot.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
    <img src="docs/screenshots/delete_ticket_screenshot.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
</p>

## PEP 8 CONVENTIONS

- Flake 8 report
<p align="center">
    <img src="docs/screenshots/flake8_screenshot.png" width="auto" style="border: 1px solid grey; border-radius: 10px;">
</p>

---

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## AUTHOR
**Name**: Nicolas MARIE  
**Track**: Python Developer – OpenClassrooms  
**Project – Develop a web app using Django – December 2025**
