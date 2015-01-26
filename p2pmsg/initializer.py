__author__ = 'Excelle'

import mysql.connector
import config

conn = mysql.connector.connect(config.db_user, config.db_password, config.db_name, use_unicode=True)
cursor = conn.cursor()
cursor.execute('create table user (id INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, '
               'username VARCHAR(16) CHARACTER SET utf8 NOT NULL,'
               ' password VARCHAR(32) NOT NULL, wan_ip VARCHAR(16), '
               'lan_ip VARCHAR(16), nickname VARCHAR(20));')
conn.commit()
conn.close()

