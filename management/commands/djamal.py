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
        if command == 'add_alias':
            self.add_alias()
        elif command == 'init':
            self.init()
        elif command == "cleanup":
            self.cleanup()
        elif command == "push_env":
            self.push_env()
        elif command == "deploy":
            self.deploy()
        elif command == "setup":
            self.setup()
        elif command == "audit":
            self.audit()

    def add_alias(self):
        alias_command = "alias djamal=\"docker run -it --rm -v '${PWD}:/workdir' -e SSH_AUTH_SOCK='/run/host-services/ssh-auth.sock' -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/basecamp/kamal:latest\""
        env_file_path = self.get_env_file_path()
        with open(env_file_path, 'a') as env_file:
            env_file.write(alias_command)
        self.stdout.write(self.style.SUCCESS('Alias command added to the environmental file successfully.'))

    def init(self):
        env_file_path = self.get_env_file_path()
        with open(env_file_path, 'r') as env_file:
            content = env_file.read()
            alias_pattern = re.compile(r"alias\s+djamal\s*=\s*\"([^\"]+)\"")
            match = alias_pattern.search(content)
            if match:
                djamal_command = match.group(1)
                current_directory = os.getcwd()
                djamal_command = djamal_command.replace('${PWD}', current_directory)
                subprocess.run(f'{djamal_command} init', shell=True)
            else:
                self.stdout.write(self.style.ERROR('djamal alias command not found in the environment file.'))

    def push_env(self):
        env_file_path = self.get_env_file_path()
        with open(env_file_path, 'r') as env_file:
            content = env_file.read()
            alias_pattern = re.compile(r"alias\s+djamal\s*=\s*\"([^\"]+)\"")
            match = alias_pattern.search(content)
            if match:
                djamal_command = match.group(1)
                current_directory = os.getcwd()
                djamal_command = djamal_command.replace('${PWD}', current_directory)
                subprocess.run(f'{djamal_command} env push', shell=True)
                self.stdout.write(self.style.SUCCESS('Env files have been successfully pushed to the servers.'))
            else:
                self.stdout.write(self.style.ERROR('djamal alias command not found in the environment file.'))

    def deploy(self):
        env_file_path = self.get_env_file_path()
        with open(env_file_path, 'r') as env_file:
            content = env_file.read()
            alias_pattern = re.compile(r"alias\s+djamal\s*=\s*\"([^\"]+)\"")
            match = alias_pattern.search(content)
            if match:
                djamal_command = match.group(1)
                current_directory = os.getcwd()
                djamal_command = djamal_command.replace('${PWD}', current_directory)
                subprocess.run(f'{djamal_command} env push', shell=True)
                subprocess.run(f'{djamal_command} deploy', shell=True)
                self.stdout.write(self.style.SUCCESS('Application successfully deployed to remote servers.'))
            else:
                self.stdout.write(self.style.ERROR('djamal alias command not found in the environment file.'))

    def setup(self):
        env_file_path = self.get_env_file_path()
        with open(env_file_path, 'r') as env_file:
            content = env_file.read()
            alias_pattern = re.compile(r"alias\s+djamal\s*=\s*\"([^\"]+)\"")
            match = alias_pattern.search(content)
            if match:
                djamal_command = match.group(1)
                current_directory = os.getcwd()
                djamal_command = djamal_command.replace('${PWD}', current_directory)
                subprocess.run(f'{djamal_command} setup', shell=True)
                self.stdout.write(self.style.SUCCESS('Application successfully setup and deployed to remote servers.'))
            else:
                self.stdout.write(self.style.ERROR('djamal alias command not found in the environment file.'))


    def cleanup(self):
        env_file_path = self.get_env_file_path()
        with open(env_file_path, 'r') as env_file:
            content = env_file.read()
            alias_pattern = re.compile(r"alias\s+djamal\s*=\s*\"([^\"]+)\"")
            match = alias_pattern.search(content)
            if match:
                djamal_command = match.group(1)
                current_directory = os.getcwd()
                djamal_command = djamal_command.replace('${PWD}', current_directory)
                subprocess.run(f'{djamal_command} remove', shell=True)
                self.stdout.write(self.style.SUCCESS('Application, including Traefik, containers, images, and registry session have been removed.'))
            else:
                self.stdout.write(self.style.ERROR('djamal alias command not found in the environment file.'))

    def audit(self):
        env_file_path = self.get_env_file_path()
        with open(env_file_path, 'r') as env_file:
            content = env_file.read()
            alias_pattern = re.compile(r"alias\s+djamal\s*=\s*\"([^\"]+)\"")
            match = alias_pattern.search(content)
            if match:
                djamal_command = match.group(1)
                current_directory = os.getcwd()
                djamal_command = djamal_command.replace('${PWD}', current_directory)
                subprocess.run(f'{djamal_command} audit', shell=True)
            else:
                self.stdout.write(self.style.ERROR('djamal alias command not found in the environment file.'))



    def get_env_file_path(self):
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        possible_env_files = ['.env', '.venv']
        env_file_path = None
        for file in possible_env_files:
            if os.path.exists(os.path.join(current_directory, file)):
                env_file_path = os.path.join(current_directory, file)
                break
        if not env_file_path:
            env_file_path = os.path.join(current_directory, '.env')
        return env_file_path

