# Django-SystemList

An inventory systems and stats list.

----

## Directories

- inventory -> Top level Django project directory.

## Files

- requirements.txt -> Python3 pip package requirements.

----

## Setup Instructions

- Setup the Python3 virtual environment

```bash
python3 -m venv django_pyvenv
source django_pyvenv/bin/activate

pip install -r requirements.txt
```

- Generate a secret key for settings.conf (used for crypto calculations)

```bash
python -c 'import secrets ; print(secrets.token_urlsafe(50))'
```

- Configure the settings.conf file (Example below)

```bash
inventory/inventory/settings/settings.conf

[creds]
SECRET_KEY = GENERATEDSECRETHERE

[network]
server_fqdn = myservername.mydomain.org
server_alias = mysite.mydomain.org

[logging]
logfile_location = systemlist.log
logfile_maxsize_bytes = 500000000
logfile_maxrotate = 10
```

- Source the local dev settings

```bash
source inventory/env_vars_local.sourceme
```

- Create the database models

```bash
cd inventory
python3 manage.py migrate
```

- Start the development server

```bash
python3 manage.py runserver
```

- Access at: <http://127.0.0.1:8000/systemlist/>
