:computer: Deployment – Krakend Tuig
======

This document describes how to deploy the Krakend Tuig website using a Linux server and Coolify.
The setup is based on Docker containers and environment variables.

:open_file_folder: Table of Contents
======

**<details><summary>Deployment</summary>**
* [**_Overview_**](#overview)
* [**_Requirements_**](#requirements)
* [**_Environment variables_**](#environment-variables)
* [**_Database_**](#database)
* [**_Static & media files_**](#static--media-files)
* [**_Fixtures_**](#fixtures)
* [**_Deploy with Coolify_**](#deploy-with-coolify)
</details>

<br>

:rocket: Overview
======

The Krakend Tuig website is deployed as a Dockerized Django application.
Coolify is used to manage deployments, environment variables and updates.

Main components:
- Django application
- PostgreSQL database (external or managed)
- Object storage for media files (S3-compatible)
- GitHub repository as source

<div align="right"><a href="#top">🔝</a></div>

:gear: Requirements
======

- Linux server (e.g. Hetzner VPS)
- Coolify installed on the server
- GitHub repository
- Python 3.12+
- PostgreSQL database
- S3-compatible object storage (for media)

<div align="right"><a href="#top">🔝</a></div>

:key: Environment variables
======

All sensitive configuration is handled via environment variables.
These **must not** be committed to GitHub.

Required variables:<br>
DEBUG=False<br>
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.nl,www.yourdomain.nl

DATABASE_URL=postgres://user:password@host:5432/dbname

EMAIL_HOST=<br>
EMAIL_PORT=<br>
EMAIL_HOST_USER=<br>
EMAIL_HOST_PASSWORD=<br>
EMAIL_USE_TLS=True

RECAPTCHA_PUBLIC_KEY=
RECAPTCHA_PRIVATE_KEY=


Optional (media storage):<br>
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=

<div align="right"><a href="#top">🔝</a></div>

:card_file_box: Database
======

The project uses PostgreSQL.
The database can be:
- managed externally
- or hosted on the same server

After connecting the database, run: <br>
python manage.py migrate

To create an admin user:<br>
python manage.py createsuperuser

<div align="right"><a href="#top">🔝</a></div>

:framed_picture: Static & media files
======

Static files:
- Collected during deployment using `collectstatic`
- Served via Whitenoise or the webserver

Media files:
- Stored in S3-compatible object storage
- Uploaded files are **not** stored in the container
- This prevents data loss during redeployments

If needed: <br>
python manage.py collectstatic

<div align="right"><a href="#top">🔝</a></div>

:package: Fixtures
======

Existing data can be reused via fixtures.

To export data locally: <br>
python manage.py dumpdata > databasedump.json

To import data on the server: <br>
python manage.py loaddata databasedump.json

It is recommended to load fixtures **after** migrations have completed.

<div align="right"><a href="#top">🔝</a></div>

:whale: Deploy with Coolify
======

1. Create a new application in Coolify
2. Connect the GitHub repository
3. Configure the build as a Docker-based app
4. Add all required environment variables
5. Deploy the application

After the first deploy:
- Check logs for errors
- Run migrations if needed
- Verify media uploads
- Test admin and member login

Coolify will automatically redeploy the application on new commits.

<div align="right"><a href="#top">🔝</a></div>

:warning: Notes
======

- Never commit secrets or environment files
- Always test migrations locally first
- Keep backups of the database and media storage
- Deployment steps may evolve as the project grows

<div align="right"><a href="#top">🔝</a></div>

