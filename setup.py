# Copyright 2015 Florian Lehner. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

from setuptools import setup, find_packages

setup(
    name='pyOSCapi',
    version='0.1',
    py_modules=['pyOSCapi'],
    packages=find_packages(),
    include_package_data=True,
    description = 'Python API to interact with network devices using the Open Spherical Camera API',
    author = 'Florian Lehner',
    author_email = 'dev@der-flo.net',
    url = 'https://github.com/florianl/pyOSCapi/',
    download_url = 'https://github.com/florianl/pyOSCapi/archive/master.tar.gz',
    keywords = ['Open Spherical Camera', 'API '],
    install_requires=['requests', 'simplejson'],
    classifiers=[   'Development Status :: 4 - Beta',
                    'Intended Audience :: Developers'
                ],
    license = 'Apache License 2.0',
)
