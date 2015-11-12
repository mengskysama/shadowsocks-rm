#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import cymysql
import time
import sys
import socket
import config
import json

class DbTransfer(object):

    instance = None

    def __init__(self):
        self.last_get_transfer = {}

    @staticmethod
    def get_instance():
        if DbTransfer.instance is None:
            DbTransfer.instance = DbTransfer()
        return DbTransfer.instance

    @staticmethod
    def send_command(cmd, retry = 3):
        while True:
            try:
                cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                cli.settimeout(2)
                cli.sendto(cmd, ('%s' % (config.MANAGE_BIND_IP), config.MANAGE_PORT))
                data, addr = cli.recvfrom(1500)
                cli.close()
                return data
            except:
                retry -= 1
                if retry == 0:
                    raise

    @staticmethod
    def get_servers_transfer():
        dt_transfer = {}
        cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cli.settimeout(2)
        cli.sendto('transfer: {}', ('%s' % (config.MANAGE_BIND_IP), config.MANAGE_PORT))
        bflag = False
        while True:
            data, addr = cli.recvfrom(1500)
            if data == 'e':
                break
            data = json.loads(data)
            print data
            dt_transfer.update(data)
        cli.close()
        return dt_transfer


    def push_db_all_user(self):
        dt_transfer = self.get_servers_transfer()
        query_head = 'UPDATE user'
        query_sub_when = ''
        query_sub_when2 = ''
        query_sub_in = None
        last_time = time.time()
        for id in dt_transfer.keys():
            query_sub_when += ' WHEN %s THEN u+%s' % (id, 0) # all in d
            query_sub_when2 += ' WHEN %s THEN d+%s' % (id, dt_transfer[id])
            if query_sub_in is not None:
                query_sub_in += ',%s' % id
            else:
                query_sub_in = '%s' % id
        if query_sub_when == '':
            return
        query_sql = query_head + ' SET u = CASE port' + query_sub_when + \
                    ' END, d = CASE port' + query_sub_when2 + \
                    ' END, t = ' + str(int(last_time)) + \
                    ' WHERE port IN (%s)' % query_sub_in
        # print query_sql
        conn = cymysql.connect(host=config.MYSQL_HOST, port=config.MYSQL_PORT, user=config.MYSQL_USER,
                               passwd=config.MYSQL_PASS, db=config.MYSQL_DB, charset='utf8')
        cur = conn.cursor()
        cur.execute(query_sql)
        cur.close()
        conn.commit()
        conn.close()

    @staticmethod
    def pull_db_all_user():
        conn = cymysql.connect(host=config.MYSQL_HOST, port=config.MYSQL_PORT, user=config.MYSQL_USER,
                               passwd=config.MYSQL_PASS, db=config.MYSQL_DB, charset='utf8')
        cur = conn.cursor()
        cur.execute("SELECT port, u, d, transfer_enable, passwd, switch, enable FROM user")
        rows = []
        for r in cur.fetchall():
            rows.append(list(r))
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def del_server_out_of_bound_safe(rows):
        for row in rows:
            server = json.loads(DbTransfer.get_instance().send_command('stat: {"server_port":%s}' % row[0]))
            if server['stat'] != 'ko':
                if row[5] == 0 or row[6] == 0:
                    #stop disable or switch off user
                    logging.info('db stop server at port [%s] reason: disable' % (row[0]))
                    DbTransfer.send_command('remove: {"server_port":%s}' % row[0])
                elif row[1] + row[2] >= row[3]:
                    #stop out bandwidth user
                    logging.info('db stop server at port [%s] reason: out bandwidth' % (row[0]))
                    SDbTransfer.send_command('remove: {"server_port":%s}' % row[0])
                if server['password'] != row[4]:
                    #password changed
                    logging.info('db stop server at port [%s] reason: password changed' % (row[0]))
                    DbTransfer.send_command('remove: {"server_port":%s}' % row[0])
            else:
                if row[5] == 1 and row[6] == 1 and row[1] + row[2] < row[3]:
                    logging.info('db start server at port [%s] pass [%s]' % (row[0], row[4]))
                    DbTransfer.send_command('add: {"server_port": %s, "password":"%s"}'% (row[0], row[4]))
                    print('add: {"server_port": %s, "password":"%s"}'% (row[0], row[4]))

    @staticmethod
    def thread_db():
        import socket
        import time
        timeout = 60
        socket.setdefaulttimeout(timeout)
        while True:
            logging.warn('db loop')
            try:
                DbTransfer.get_instance().push_db_all_user()
                rows = DbTransfer.get_instance().pull_db_all_user()
                DbTransfer.del_server_out_of_bound_safe(rows)
            except Exception as e:
                import traceback
                traceback.print_exc()
                logging.warn('db thread except:%s' % e)
            finally:
                time.sleep(15)


#SQLData.pull_db_all_user()
#print DbTransfer.send_command("")
