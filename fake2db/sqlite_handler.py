import sqlite3
import random
import string

from db_patterns import db_patterns
from logging import getLogger

logger = getLogger(__name__)

class DbConnException(Exception):
    """Database Connection or Creation Exception"""

class fake2dbSqliteHandler():

    def str_generator(self):
        '''generates uppercase 6 chars
        '''
        return ''.join(random.choice(string.ascii_uppercase) for i in range(6))

    def _rnd_number(self):
        return random.randint(0, 100000000)

    def database_caller_creator(self, tag):
        '''creates a sqlite3 db
        '''
        database = ''
        
        try:
            database = tag + self.str_generator() + '.db'
            conn=sqlite3.connect(database)
            conn.close()
            logger.warning('Database created and opened succesfully: %s' %database)
        except:
            logger.error('Failed to connect or create database / sqlite3')
            raise DbConnException
            
        return database

    def data_filler_simple_registration(self, number_of_rows):
        '''creates and fills the table
        '''
        # incoming data structure 
        # {'emails' : a_list_of_emails,
        # 'passwords': a_list_of_passwords
        # }
        db_patterns_instance = db_patterns()
        data = db_patterns_instance.simple_registration(number_of_rows)

        database = self.database_caller_creator('simpleRegistration_')
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE simple_registration(id INTEGER PRIMARY KEY, 
        email TEXT unique, password TEXT)
        ''')
        conn.commit()
        
        for password in data['passwords']:
            for email in data['emails']:
                try:
                    cursor.execute('insert into simple_registration values(?,?,?)',
                                   (self._rnd_number(),email,password))
                    conn.commit()
                    logger.warning('Commit successful after write job!')
                except Exception as e:
                    logger.error(e)

        conn.close()
        

    def data_filler_detailed_registration(self, number_of_rows):
        '''creates and fills the table
        '''
        # incoming data structure
        #fake_data = {'names': list_of_names,
        #             'lastnames': list_of_lastnames,
        #             'addresses': list_of_lastnames,
        #             'phones': list_of_phones,
        #             'emails': list_of_emails,
        #             'passwords': list_of_passwords}

        db_patterns_instance = db_patterns()
        data = db_patterns_instance.detailed_registration(number_of_rows)

        database = self.database_caller_creator('detailedRegistration_')
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE detailed_registration(id INTEGER PRIMARY KEY, 
        email TEXT unique, password TEXT, lastname TEXT,
        name TEXT, adress TEXT, phone TEXT,)
        ''')
        conn.commit()
        
        # UGLY AS HELL , TODO: USE ITERTOOLS!!!!!!
        # TEMPORARY
        for password in data['passwords']:
            for email in data['emails']:
                for name in data['names']:
                    for lastname in data['lastnames']:
                        for phone in data['phones']:
                            for address in data['addresses']:
                                try:
                                    cursor.execute('insert into detailed_registration values(?,?,?,?,?,?,?)',(self._rnd_number(), email, password, lastname, name, address, phone))
                                    conn.commit()
                                    logger.warning('Commit successful after write job!')
                                except Exception as e:
                                    logger.error(e)

        conn.close()
