#!/bin/bash

PYTHONUNBUFFERED=1 python3 -m unittest discover -s src -v --buffer
