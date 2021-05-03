#!/usr/local/bin/python3
# Copyright (c) 2021 Robert Bosch GmbH Copyright holder of the paper "Multi-Class Uncertainty Calibration via Mutual Information Maximization-based Binning" accepted at ICLR 2021.
# All rights reserved.
#
# The paper "Multi-Class Uncertainty Calibration via Mutual Information Maximization-based Binning" accepted at ICLR 2021.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Author: Kanil Patel
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


#requirements are already fullfilled if you use the conda environment with the requirements.yml file, see readme.md
#if we keep the requirements here, isntallation of the package will fail somehow
requirements = []

setup(
    name='imax_calib',
    version='0.1.0',
    description="I-Max paper code",
    author="Kanil Patel",
    author_email='kanil.patel@de.bosch.com',
    url='git@github.com:boschresearch/imax-calibration.git',
    packages=find_packages(),
    install_requires=requirements,
    keywords='imax_calib',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)
