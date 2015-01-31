#!/usr/bin/env python
from distutils.core import setup

setup(author='Matus Makovy',
      author_email='matus.makovy@gmail.com',
      name='irc-server',
      version='1.0',
      description='Symple IRC chat server',    
      py_modules=['server', 'zoznam', 'chat_handler', 'chat_server'],
      data_files=[('config', '\config.ini')]
      )
