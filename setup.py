#!/usr/bin/env python
#
# Copyright 2011 Vitaly Glibin
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import distutils.core
import sys
# Importing setuptools adds some features like "setup.py develop", but
# it's optional so swallow the error if it's not there.
try:
    import setuptools
except ImportError:
    pass

kwargs = {}

version = "0.3.6"

major, minor = sys.version_info[:2]
if major >= 3:
    import setuptools  # setuptools is required for use_2to3
    kwargs["use_2to3"] = True

distutils.core.setup(
    name="session",
    version=version,
    packages = ["session", "session.transport", "session.tornado"],
    package_data = {
        "session": [],
        },
    install_requires = [
        "tornado >= 2.0"
    ],
    author="Vitaly Glibin",
    author_email="glibin.v@gmail.com",
    url="http://www.glibin.ru/",
    download_url="http://github.com/downloads/glibin/session/session-%s.tar.gz" % version,
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="Simple session handling in python",
    **kwargs
)