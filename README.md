# Django Kamal Extension

The Django Kamal Extension adds the 'djamal' alias command to the .env file in the root of the Django project. This extension simplifies the usage of the Docker image 'ghcr.io/basecamp/kamal:latest' within your Django project.

## Installation

Install the Django Kamal Extension using pip:

```bash
python -m pip install djamal


# Usage
Add 'django_kamal_extension' to your Django project's INSTALLED_APPS and 'django_kamal_extension.middleware.Command' to the MIDDLEWARE:

# settings.py

INSTALLED_APPS = [
    # ...
    'django_kamal_extension',
    # ...
]

MIDDLEWARE = [
    # ...
    'django_kamal_extension.middleware.Command',
    # ...
]

## To add the 'kamal' alias command to the .env file, run the following Django management command:
```bash
python manage.py djamal add_alias

## This will append the necessary command to the .env file, enabling you to run the 'djamal' command within your Django project.

# License
This project is licensed under the MIT License - see the LICENSE file for details.

