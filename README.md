# Django Kamal Extension

The Django Kamal Extension adds the 'djamal' alias command to the .env file in the root of the Django project. This extension simplifies the usage of the Docker image 'ghcr.io/basecamp/kamal:latest' within your Django project.

## Installation

Install djamal using pip:

```bash
python -m pip install djamal


# Usage
Add 'djamal' to your Django project's INSTALLED_APPS and 'djamal.middleware.Command' to the MIDDLEWARE:

# settings.py

INSTALLED_APPS = [
    # ...
    'djamal',
    # ...
]

MIDDLEWARE = [
    # ...
    'djamal.middleware.Command',
    # ...
]

## To view the list of djamal commands and options, run the following Django management command:
```bash
python manage.py djamal help


# License
This project is licensed under the MIT License - see the LICENSE file for details.

