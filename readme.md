Krakend Tuig – Website
======

**Website for Shantykoor Krakend Tuig**

This repository contains the source code for the official website of *Shantykoor Krakend Tuig*.  
The website combines a public-facing site with a members-only section and on-site content management, built with Django.

<img src="static/img/logo.webp" alt="Krakend Tuig logo" width="75%" height="75%">

:open_file_folder: Table of Contents
======

**<details><summary>UX & Functional Overview</summary>**
* [**_Target audience_**](#target-audience)
* [**_Public features_**](#public-features)
* [**_Members-only features_**](#members-only-features)
* [**_Content management_**](#content-management)
</details>

**<details><summary>Technologies</summary>**
* [**_Languages_**](#languages)
* [**_Frameworks & libraries_**](#frameworks--libraries)
* [**_Tools_**](#tools)
</details>

**<details><summary>Local Development</summary>**
* [**_Run locally_**](#run-locally)
</details>

**<details><summary>Deployment</summary>**
* [**_Deployment guide_**](#deployment-guide)
</details>

**<details><summary>Credits</summary>**
* [**_Content_**](#content)
* [**_Code_**](#code)
* [**_Media_**](#media)
</details>

<br>
<div align="right"><a href="#top">🔝</a></div>

:busts_in_silhouette: UX & Functional Overview
======

### Target audience
This website serves two main audiences:

- **Visitors & fans** of the choir  
- **Choir members & board members** who need access to internal information and planning

The focus is on clarity, ease of use and maintainability rather than marketing or commercial goals.

### Public features
Visitors can:
- View general information about the choir
- Read news and announcements
- View upcoming public performances
- Browse photos and videos
- Contact the choir via a contact form

### Members-only features
Logged-in members can:
- Access the members list
- View internal performance planning
- See song lyrics
- Manage their own profile

Access is role-based, with additional permissions for board members and administrators.

### Content management
Most content can be managed **via the website itself**, without needing direct access to the Django admin.
This includes:
- Homepage content
- Informational pages
- Media (photos and videos)
- Performance agenda

<div align="right"><a href="#top">🔝</a></div>

:gear: Technologies
======

### Languages
- Python
- HTML
- CSS
- JavaScript

### Frameworks & libraries
- Django
- PostgreSQL
- Django Jazzmin
- django-recaptcha
- Pillow
- Whitenoise

### Tools
- VS Code
- Git & GitHub
- Docker
- Coolify
- Object Storage (S3-compatible)

<div align="right"><a href="#top">🔝</a></div>

:computer: Local Development
======

### Run locally
Basic steps to run the project locally:

1. Clone the repository from GitHub
2. Create and activate a virtual environment
3. Install dependencies: <br>
pip install -r requirements.txt
4. Create an `env.py` or `.env` file with the required environment variables
5. Run migrations:<br>
python manage.py migrate
6. Load fixtures if applicable: <br>
python manage.py loaddata databasedump.json
7. Start the development server: <br>
python manage.py runserver

<div align="right"><a href="#top">🔝</a></div>

:rocket: Deployment
======

### Deployment guide
Deployment is handled separately and documented in detail.

Please see:<br>
readme/deployment/README.md

This guide covers:
- Server setup
- Environment variables
- Database configuration
- Static & media handling
- Deployment using Coolify

<div align="right"><a href="#top">🔝</a></div>

:copyright: Credits
======

### Content
All textual content is written by members of Shantykoor Krakend Tuig, with assistance from ChatGPT where applicable.  
All content has been reviewed and adapted where needed.

### Code
- Django documentation
- Stack Overflow
- ChatGPT for code-related problem solving

### Media
- Photos and videos are provided by the choir or taken during performances
- Logos and visual assets are created specifically for this project

<div align="right"><a href="#top">🔝</a></div>
