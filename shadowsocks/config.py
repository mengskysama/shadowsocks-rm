import logging,os



#Config
MYSQL_HOST = '133.130.97.82'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASS = '11QQqqWW'
MYSQL_DB = 'sspanel'

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
SS_METHOD = 'rc4-md5'

#
LOG_ENABLE = True
#LOG_LEVEL = logging.WARNING
LOG_LEVEL = logging.DEBUG
LOG_FILE = '/var/log/shadowsocks.log'
