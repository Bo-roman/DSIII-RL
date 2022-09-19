import sys
sys.path.insert(1, '..//PythonLibs//SQLite3')
from collections import deque
import numpy as np
from sqlite_3 import SQLite_3
import SQLiteCommands
import logging



class TrainigDataLogger:

    def __init__(self,db_name,max_experience_data_per_episode):
        self.database_name = db_name
        self.experience_data = deque(maxlen=max_experience_data_per_episode)
        self.sqlite = SQLite_3(db_name)


    def enqueue_experience_data(self,epoch,episode,reward,action,epsilon):
        if epoch == None or episode == None or reward == None or action == None or epsilon == None:
            logging.error('\'enqueue_experience_data\' received a None parameter')
            return

        self.experience_data.append((epoch,episode,reward,action,epsilon))

    def log_experience_data(self,table):
        """Stores on disk epoch, episode, reward, acton, epsilon"""
        self.sqlite.connect()
        self.sqlite.create_table(table,SQLiteCommands.sql_create_experience_data_table)

        for exp in self.experience_data:
            insert_exp = {'epoch': exp[0],
                          'episode': exp[1],
                          'reward': exp[2],
                          'action': int(exp[3]),
                          'epsilon': exp[4]}
            self.sqlite.insert(table,insert_exp)
            
        self.sqlite.close()
        self.experience_data.clear()

    def log_training_data(self,table,epoch,training_batch,loss):
        """Stores on disk epoch, training_batch, loss"""
        self.sqlite.connect()
        self.sqlite.create_table(table,SQLiteCommands.sql_create_training_data_table)

        insert_train_data =  {'epoch': epoch,
                              'training_batch': training_batch,
                              'loss': loss}

        self.sqlite.insert(table,insert_train_data)
        self.sqlite.close()
