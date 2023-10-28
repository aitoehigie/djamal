from __future__ import annotations
import os
import re
import subprocess
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Djamal commands"

    def add_arguments(self, parser):
        parser.add_argument("command", type=str, help="Specify the command to execute")

    def handle(self, *args, **options):
        command = options["command"]
        if command == "add_alias":
            self.add_alias()
        elif command in ["init", "cleanup", "push_env", "deploy", "setup", "audit"]:
            self.execute_djamal_command_if_alias_exists(command)

    def add_alias(self):
        #alias_command = "alias djamal=\"docker run -it --rm -v '${PWD}:/workdir' -v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK='/run/host-services/ssh-auth.sock' -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/basecamp/kamal:latest\""
        alias_command = (
            "alias djamal=\"docker run -it --rm "
            "-v '${PWD}:/workdir' "
            f"-v $(echo $SSH_AUTH_SOCK):/ssh-agent "
            "-e SSH_AUTH_SOCK=/ssh-agent "
            "-v /var/run/docker.sock:/var/run/docker.sock "
            "ghcr.io/basecamp/kamal:latest\"\n"
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
