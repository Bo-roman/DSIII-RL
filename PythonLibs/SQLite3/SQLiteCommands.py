sql_create_experience_table = {'id' : 'INTEGER NOT NULL UNIQUE',
                               'state':'BLOB NOT NULL',
                               'next_state':'BLOB NOT NULL',
                               'reward': 'NUMERIC NOT NULL',
                               'action': 'INTEGER NOT NULL',
                               'done' : 'INTEGER NOT NULL',
                               'PRIMARY KEY' : '(\"id\" AUTOINCREMENT)'}
                                        

sql_create_experience_data_table =        {'id' : 'INTEGER NOT NULL UNIQUE',
                                           'epoch': 'NUMERIC NOT NULL',
                                           'episode': 'NUMERIC NOT NULL',
                                           'reward': 'INTEGER NOT NULL',
                                           'action' : 'INTEGER NOT NULL',
                                           'epsilon' : 'REAL NOT NULL',
                                           'PRIMARY KEY' : '(\"id\" AUTOINCREMENT)'}

sql_create_training_data_table =          {'id' : 'INTEGER NOT NULL UNIQUE',
                                           'epoch': 'NUMERIC NOT NULL',
                                           'training_batch': 'NUMERIC NOT NULL',
                                           'loss': 'REAL NOT NULL',
                                           'PRIMARY KEY' : '(\"id\" AUTOINCREMENT)'}
