#!/usr/local/bin/env python3
# -*- coding:utf-8 -*-
# __author__:"Howard"

import platform
import pathlib
import os

if platform.system() == 'linux' or platform.system() == 'Darwin':
    BASE_DIR = pathlib.Path(__file__).parent.parent
DB_DIR = os.path.join(BASE_DIR, 'db', 'record.db')