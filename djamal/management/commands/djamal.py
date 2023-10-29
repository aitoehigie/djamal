from __future__ import annotations
import os
import re
import subprocess
import pkg_resources

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Djamal commands"

    def add_arguments(self, parser):
        parser.add_argument("command", type=str, help="Specify the command to execute")

    def handle(self, *args, **options):
        command = options["command"]
        if command == "add_alias":
            self.add_alias()
        elif command == "help":
            self.print_help_text()
        elif command == "version":
            self.print_version()
        elif command in [
            "init",
            "cleanup",
            "push_env",
            "deploy",
            "setup",
            "audit",
            "accessory",
            "app",
            "build",
            "config",
            "details",
            "env",
            "envify",
            "healthcheck",
            "lock",
            "prune",
            "redeploy",
            "registry",
            "remove",
            "rollback",
            "server",
            "setup",
            "traefik",
        ]:
            self.execute_djamal_command_if_alias_exists(command)

    def add_alias(self):
        alias_command = (
            'alias djamal="docker run -it --rm '
            "-v '${PWD}:/workdir' "
            f"-v $(echo $SSH_AUTH_SOCK):/ssh-agent "
            "-e SSH_AUTH_SOCK=/ssh-agent "
            "-v /var/run/docker.sock:/var/run/docker.sock "
            'ghcr.io/basecamp/kamal:latest"\n'
        )
        env_file_path = self.get_env_file_path()
        with open(env_file_path, "a") as env_file:
            env_file.write(alias_command)
        self.stdout.write(
            self.style.SUCCESS(
                "Alias command added to the environmental file successfully."
            )
        )

    def execute_djamal_command_if_alias_exists(self, command_string):
        env_file_path = self.get_env_file_path()
        with open(env_file_path, "r") as env_file:
            content = env_file.read()
            alias_pattern = re.compile(r"alias\s+djamal\s*=\s*\"([^\"]+)\"")
            match = alias_pattern.search(content)
            if match:
                djamal_command = match.group(1)
                current_directory = os.getcwd()
                djamal_command = djamal_command.replace("${PWD}", current_directory)
                subprocess.run(f"{djamal_command} {command_string}", shell=True)
            else:
                self.stdout.write(
                    "djamal alias command not found in the environment file."
                )


    def get_env_file_path(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        possible_env_files = [".env", ".venv"]
        for file in possible_env_files:
            if os.path.exists(os.path.join(current_directory, file)):
                return os.path.join(current_directory, file)
        return os.path.join(current_directory, ".env")

    def print_help_text(self):
        help_text = """
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
                                         # Default: false
"""
        self.stdout.write(help_text)

    def print_version(self):
        try:
            version = pkg_resources.get_distribution("djamal").version
            self.stdout.write(f"The version number is: {version}")
        except pkg_resources.DistributionNotFound:
            self.stdout.write("Package not found.")
