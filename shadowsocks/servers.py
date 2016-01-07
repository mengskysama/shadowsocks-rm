#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 mengskysama
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

import sys
import os
import logging
import thread
import config
import signal
import time

logging.basicConfig(filename=config.logfile,level=logging.INFO)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from shadowsocks import shell, daemon, eventloop, tcprelay, udprelay, \
    asyncdns, manager

import manager
import config
from dbtransfer import DbTransfer

def handler_SIGQUIT():
    return

def main():
    configer = {
        'server': '%s' % config.SS_BIND_IP,
        'local_port': 1081,
        'port_password': {
        },
        'method': '%s' % config.SS_METHOD,
        'manager_address': '%s:%s' % (config.MANAGE_BIND_IP, config.MANAGE_PORT),
        'timeout': 185, # some protocol keepalive packet 3 min Eg bt
        'fast_open': False,
        'verbose': 2
    }
    t = thread.start_new_thread(manager.run, (configer,))
    time.sleep(1)
    t = thread.start_new_thread(DbTransfer.thread_db, ())

    while True:
        time.sleep(100)


if __name__ == '__main__':
    main()
