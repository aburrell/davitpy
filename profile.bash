#!/bin/bash

# To make changes to server addresses, passwords, etc., please see the new
# run control file: davitpy/davitpy/davitpyrc.
# Be sure to re-run 'python setup.py install' in order to copy the new
# davitpyrc file into its proper operating location and activate the new
# settings.

# Sets path and fundamental environment variables for DaViT-py

# *********************************
# You probably do not need to modify the following part
# *********************************
# Set path to DAVITPY
export DAVITPY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PATH=${DAVITPY}/bin:${PATH}

