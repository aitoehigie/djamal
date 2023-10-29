from __future__ import annotations
import os
import re
import subprocess
import shlex
import pkg_resources
from argparse import REMAINDER

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Djamal commands"

    def add_arguments(self, parser):
        parser.add_argument("command", nargs="+", type=str, help="Specify the command to execute")
        parser.add_argument("--verbose", action="store_true", help="Detailed logging")
        parser.add_argument("--quiet", action="store_true", help="Minimal logging")
        parser.add_argument("--app-version", type=str, dest="app_version", help="Run commands against a specific app version")
        parser.add_argument("--primary", action="store_true", help="Run commands only on primary host instead of all")
        parser.add_argument("--hosts", type=str, help="Run commands on these hosts instead of all (separate by comma)")
        parser.add_argument("--roles", type=str, help="Run commands on these roles instead of all (separate by comma)")
        parser.add_argument("--config-file", type=str, help="Path to config file", default="config/deploy.yml")
        parser.add_argument("--destination", type=str, help="Specify destination to be used for config file (staging -> deploy.staging.yml)")
        parser.add_argument("--skip-hooks", action="store_true", help="Don't run hooks")

    def handle(self, *args, **options):
        command_list = options.pop("command")
        command = command_list.pop(0)
        verbose = options.pop("verbose")
        quiet = options.pop("quiet")
        app_version = options.pop("app_version")
        primary = options.pop("primary")
        hosts = options.pop("hosts")
        roles = options.pop("roles")
        config_file = options.pop("config_file")
        destination = options.pop("destination")
        skip_hooks = options.pop("skip_hooks")

        if command == "add_alias":
            self.add_alias()
        elif command == "help":
            self.print_help_text()
        elif command == "version":
            self.print_version()
        else:
            self.execute_djamal_command_if_alias_exists(command, command_list, verbose, quiet, app_version, primary, hosts, roles, config_file, destination, skip_hooks)

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

    def execute_djamal_command_if_alias_exists(self, djamal_command, optional_args, verbose, quiet, app_version, primary, hosts, roles, config_file, destination, skip_hooks):
        full_command = self.construct_full_command(djamal_command, optional_args, verbose, quiet, app_version, primary, hosts, roles, config_file, destination, skip_hooks)
        if full_command:
            subprocess.run(full_command, shell=True)

    def construct_full_command(self, djamal_command, optional_args, verbose, quiet, app_version, primary, hosts, roles, config_file, destination, skip_hooks):
        env_file_path = self.get_env_file_path()
        with open(env_file_path, "r") as env_file:
            content = env_file.read()
            alias_pattern = re.compile(r"alias\s+djamal\s*=\s*\"([^\"]+)\"")
            match = alias_pattern.search(content)
            if match:
                djamal_command_str = match.group(1)
                current_directory = os.getcwd()
                djamal_command_str = djamal_command_str.replace("${PWD}", current_directory)
                full_command = f"{djamal_command_str} {djamal_command}"
                if optional_args:
                    full_command += " " + " ".join(optional_args)
                if verbose:
                    full_command += " --verbose"
                if quiet:
                    full_command += " --quiet"
                if app_version:
                    full_command += f" --version={app_version}"
                if primary:
                    full_command += " --primary"
                if hosts:
                    full_command += f" --hosts={hosts}"
                if roles:
                    full_command += f" --roles={roles}"
                if config_file:
                    full_command += f" --config-file={config_file}"
                if destination:
                    full_command += f" --destination={destination}"
                if skip_hooks:
                    full_command += " --skip-hooks"
                return full_command
            else:
                self.add_alias()
                return None

    def get_env_file_path(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        possible_env_files = [".env", ".venv"]
        for file in possible_env_files:
            file_path = os.path.join(current_directory, file)
            if os.path.exists(file_path):
                return file_path
        env_file_path = os.path.join(current_directory, ".env")
        if not os.path.exists(env_file_path):
            with open(env_file_path, "w") as env_file:
                pass
        return env_file_path

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
"""
        self.stdout.write(help_text)

    def print_version(self):
        try:
            version = pkg_resources.get_distribution("djamal").version
            self.stdout.write(f"The version number is: {version}")
        except pkg_resources.DistributionNotFound:
            self.stdout.write("Package not found.")

