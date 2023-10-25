from __future__ import annotations
import os
import re
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Manage custom Django commands'

    def add_arguments(self, parser):
        parser.add_argument('command', type=str, help='Specify the command to execute')

    def handle(self, *args, **options):
        command = options['command']
        if command in {'add_alias', 'init', 'cleanup', 'push_env', 'deploy', 'setup', 'audit'}:
            getattr(self, command)()

    def add_alias(self):
        alias_command = "alias djamal=\"docker run -it --rm -v '${PWD}:/workdir' -e SSH_AUTH_SOCK='/run/host-services/ssh-auth.sock' -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/basecamp/kamal:latest\""
        env_file_path = self.get_env_file_path()
        with open(env_file_path, 'a') as env_file:
            env_file.write(alias_command)
        self.stdout.write(self.style.SUCCESS('Alias command added to the environmental file successfully.'))

    def execute_djamal_command(self, djamal_command, command_string):
        current_directory = os.getcwd()
        djamal_command = djamal_command.replace('${PWD}', current_directory)
        subprocess.run(f'{djamal_command} {command_string}', shell=True)

    def init(self):
        self.execute_djamal_command_if_alias_exists('init')

    def push_env(self):
        self.execute_djamal_command_if_alias_exists('env push')
        self.stdout.write(self.style.SUCCESS('Env files have been successfully pushed to the servers.'))

    def deploy(self):
        self.execute_djamal_command_if_alias_exists('env push')
        self.execute_djamal_command_if_alias_exists('deploy')
        self.stdout.write(self.style.SUCCESS('Application successfully deployed to remote servers.'))

    def setup(self):
        self.execute_djamal_command_if_alias_exists('setup')
        self.stdout.write(self.style.SUCCESS('Application successfully setup and deployed to remote servers.'))

    def cleanup(self):
        self.execute_djamal_command_if_alias_exists('remove')
        self.stdout.write(self.style.SUCCESS('Application, including Traefik, containers, images, and registry session have been removed.'))

    def audit(self):
        self.execute_djamal_command_if_alias_exists('audit')

    def get_env_file_path(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        possible_env_files = ['.env', '.venv']
        for file in possible_env_files:
            if os.path.exists(os.path.join(current_directory, file)):
                return os.path.join(current_directory, file)
        return os.path.join(current_directory, '.env')

