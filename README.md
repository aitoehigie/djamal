# Djamal: A Django Extension for [Kamal](https://github.com/basecamp/kamal)

This Django extension allows you deploy web apps anywhere from bare metal to cloud VMs, with zero downtime using [Kamal](https://github.com/basecamp/kamal) from within your Django project.


## Installation

Install djamal using pip:

```bash
python -m pip install djamal
```


# Usage
Add 'djamal' to your Django project's INSTALLED_APPS and 'djamal.middleware.Command' to the MIDDLEWARE:

# settings.py
```yaml
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
```

## Commands and options
 To view the list of djamal commands and options, run the following Django management command:
 
```bash
python manage.py djamal help
```

## Setting up a project
Change into your Django app directory, and run the command 
```bash
djamal init
```

Now edit the new file config/deploy.yml. It could look as simple as this:
```yaml
service: webservice
image: django-image
servers:
  - 192.168.0.1
  - 192.168.0.2
registry:
  username: registry-user-name
  password:
    - DJAMAL_REGISTRY_PASSWORD
env:
  secret:
    - DJANGO_MASTER_KEY
```

Then edit your .env file to add your registry password as DJAMAL_REGISTRY_PASSWORD (and your DJANGO_MASTER_KEY for production with a Django app).

Now you’re ready to deploy to the servers by running this command:
```bash
djamal setup
```

This command will:

- Connect to the servers over SSH (using root by default, authenticated by your ssh key).
- Install Docker and curl on any server that might be missing it (using apt-get): root access is needed via ssh for this.
- Log into the registry both locally and remotely.
- Build the image using the standard Dockerfile in the root of the application.
- Push the image to the registry.
- Pull the image from the registry onto the servers.
- Push the ENV variables from .env onto the servers.
- Ensure Traefik is running and accepting traffic on port 80.
- Ensure your app responds with 200 OK to GET /up (you must have curl installed inside your app image!).
- Start a new container with the version of the app that matches the current git version hash.
- Stop the old container running the previous version of the app.
- Prune unused images and stopped containers to ensure servers don’t fill up.
- Now all the servers are now serving the app on port 80. If you’re just running a single server, you’re ready to go. If you’re running multiple servers, you need to put a load balancer in front of them. For subsequent deploys, or if your servers already have Docker and curl installed, you can just run djamal deploy.


# License
This project is licensed under the MIT License - see the LICENSE file for details.

