#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################################################
#
#    zencli.py - A Zenoss JSON API Commandline Client
#    Copyright 2012 Stephan Adig <stephan.adig@citrix.com>
#       Licensed under the Apache License, Version 2.0 (the "License");
#       you may not use this file except in compliance with the License.
#       You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#       Unless required by applicable law or agreed to in writing, software
#       distributed under the License is distributed on an "AS IS" BASIS,
#       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#       See the License for the specific language governing permissions and
#       limitations under the License.
#################################################################################

from distutils.core import setup
from distutils.command.install_scripts import install_scripts

setup(
        name='zenossapi',
        version='0.1',
        description='Zenoss JSON API Command line client',
        author='Stephan Adig',
        author_email='stephan.adig@citrix.com',
        url='http://github.com/sadig/zenoss-api',
        packages=['zenoss'],
        scripts=[
            'scripts/zencli'
            ]
)
