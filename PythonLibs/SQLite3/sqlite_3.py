import sqlite3
import SQLiteCommands
import logging

class SQLite_3:
    
    def __init__(self,database_name):
        self.connection = None
        self.database_name = database_name

    def connect(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :return: Connection object or None
        """
        try:
            self.connection = sqlite3.connect(self.database_name)
            return self.connection
        except sqlite3.Error as e:
            logging.warning(e)

        return None

    def close(self):
         try:
            self.connection.close()
         except sqlite3.Error as e:
            logging.warning(e)

    def create_table(self, table,columns):
        """ create a table from the create_table_sql statement
        :param table: table name
        :param columns: a dictionary consisting of key:value where key is the
                        name of the column and the value is the property, eg
                        {'state':'<data_type> <...property>'}
        :return:
        """

        sql_command = 'CREATE TABLE ' + table + ' ('
        
        for i, (k, v) in enumerate(columns.items()):
            sql_command += k + ' ' + v
            
            if i != len(columns) - 1:
                sql_command += ','

        sql_command += ')'
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_command)
            return True
        except sqlite3.Error as e:
            logging.warning(e)

        return False

    def insert(self,table,params):
        """ Inserts data into a table
        :param table: Table name
        :param params: dictionary of parameters for the table consisting of
                       key : value pair, where key is the table column and id the value
        :return: 
        """
        
        sql_command = 'INSERT INTO ' + table + '('
        sql_values = ''
        
        for i, (k, v) in enumerate(params.items()):            
            sql_command += k
            sql_values += '?'
            
            if i != len(params) - 1:
                sql_command += ','
                sql_values += ','

        sql_command += ') VALUES(' + sql_values + ')'

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_command,list(params.values()))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logging.warning(e)

        return False

        
    def select(self,table,columns=None,conditions=None):
        """ Selects data from a table
        :param table: Table name
        :param columns: list of columns that you wish to select, use * for every
        :param conditions: string of conditions
        :return:

        #warning : work in progress
        """
        sql_command = 'SELECT '
        columns_len = None
        
        if columns_len == None:
            sql_command += '*'
        else:
            columns_len = len(columns)
            for i,column in columns:
                sql_command += column
                if i != columns_len:
                    sql_command += ','

        sql_command += ' FROM ' + table
        
        if conditions != None:
            sql_command += ' WHERE ' + conditions
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_command)
            return cursor.fetchall()
        except sqlite3.Error as e:
            logging.warning(e)

        return None

    def getCount(self,table):
        sql_command = 'SELECT Count() FROM ' + table
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_command)
            return cursor.fetchone()[0]
        except sqlite3.Error as e:
            logging.warning(e)

        return None
        




















        

