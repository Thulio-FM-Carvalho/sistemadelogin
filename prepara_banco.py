import os

import mysql.connector
from mysql.connector import errorcode

conn = mysql.connector.connect(
    host=os.environ.get('HOST'),
    user=os.environ.get('USER'),
    password=os.environ.get('PASSWORD')
)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `sistemadelogin`;")

cursor.execute("CREATE DATABASE `sistemadelogin`;")

cursor.execute("USE `sistemadelogin`;")

# criando tabelas
TABLES = {}
TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `first_name` varchar(50) NOT NULL,
      `last_name` varchar(50) NOT NULL,
      `username` varchar(50) NOT NULL,
      `email` varchar(50) NOT NULL,
      `password` varchar(255) NOT NULL,
      `status` int(11) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (first_name, last_name, username, email, password, status ) VALUES (%s, %s, %s, %s, %s, %s)'
usuarios = [
      ("Thulio", "Freires Maia Carvalho", "Thulio", "thuliofreires05@gmail.com", "alohomora", "0")
]
cursor.executemany(usuario_sql, usuarios)
conn.commit()

cursor.close()
conn.close()