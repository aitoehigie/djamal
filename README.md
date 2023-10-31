# Djamal: A Django Extension for [Kamal](https://github.com/basecamp/kamal)

This Django extension allows you deploy web apps anywhere from bare metal to cloud VMs, with zero downtime using [Kamal](https://github.com/basecamp/kamal) from within your Django project.


## Installation

Install djamal using pip:

```bash
python -m pip install djamal
```


## Usage
Add 'djamal' to your Django project's INSTALLED_APPS and 'djamal.middleware.Command' to the MIDDLEWARE:

settings.py

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
 ```yaml
 Commands:
  djamal accessory           # Manage accessories (db/redis/search)
  djamal app                 # Manage application
  djamal audit               # Show audit log from servers
  djamal build               # Build application image
  djamal config              # Show combined config (including secrets!)
  djamal deploy              # Deploy app to servers
  djamal details             # Show details about all containers
  djamal env                 # Manage environment files
  djamal envify              # Create .env by evaluating .env.erb (or .env.staging.erb -> .env.staging when using -d staging)
  djamal healthcheck         # Healthcheck application
  djamal help [COMMAND]      # Describe available commands or one specific command
  djamal init                # Create config stub in config/deploy.yml and env stub in .env
  djamal lock                # Manage the deploy lock
  djamal prune               # Prune old application images and containers
  djamal redeploy            # Deploy app to servers without bootstrapping servers, starting Traefik, pruning, and registry login
  djamal registry            # Login and -out of the image registry
  djamal remove              # Remove Traefik, app, accessories, and registry session from servers
  djamal rollback [VERSION]  # Rollback app to VERSION
  djamal server              # Bootstrap servers with curl and Docker
  djamal setup               # Setup all accessories, push the env, and deploy app to servers
  djamal traefik             # Manage Traefik load balancer
  djamal version             # Show Djamal version

Options:
  -v, [--verbose], [--no-verbose]        # Detailed logging
  -q, [--quiet], [--no-quiet]            # Minimal logging
      [--version=VERSION]                # Run commands against a specific app version
  -p, [--primary], [--no-primary]        # Run commands only on primary host instead of all
  -h, [--hosts=HOSTS]                    # Run commands on these hosts instead of all (separate by comma)
  -r, [--roles=ROLES]                    # Run commands on these roles instead of all (separate by comma)
  -c, [--config-file=CONFIG_FILE]        # Path to config file
                                         # Default: config/deploy.yml
  -d, [--destination=DESTINATION]        # Specify destination to be used for config file (staging -> deploy.staging.yml)
  -H, [--skip-hooks], [--no-skip-hooks]  # Don't run hooks
```
 
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

