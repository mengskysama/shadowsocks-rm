About manyuser
----------------

Install
-------

install MySQL 5.x.x

`pip install cymysql`

create a database named `shadowsocks`

import `shadowsocks.sql` into `shadowsocks`

if you upgrade from old version make sure:

  `pass` is varchar(32) NOT NULL,
  `passwd` is varchar(32) NOT NULL,
  `last_get_gift_time` not `last_get_gitf_time`


edit config.py

Example:

    #Config
    MYSQL_HOST = 'mengsky.net'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASS = 'root'
    MYSQL_DB = 'shadowsocks'

    MANAGE_PASS = 'passwd'
    #if you want manage in other server you should set this value to global ip
    MANAGE_BIND_IP = '127.0.0.1'
    #make sure this port is idle
    MANAGE_PORT = 23333
    #BIND IP
    #if you want bind ipv4 and ipv6 '[::]'
    #if you want bind all of ipv4 if '0.0.0.0'
    #if you want bind all of if only '4.4.4.4'
    SS_BIND_IP = '0.0.0.0'


TestRun `cd shadowsocks` ` python servers.py` not server.py

if no exception server will startup. you will see such like
Example:

    add: {"server_port": XXXXX, "password":"XXXXX"}


Database user table column
------------------
`passwd` server pass

`port` server port

`t` last keepalive time

`u` upload transfer

`d` download transfer (upload & download in here now)

`transfer_enable` if u + d > transfer_enable this server will be stop (db_transfer.py del_server_out_of_bound_safe)

