import sys
sys.path.insert(1, '..//PythonLibs//SQLite3')
from collections import deque
from sqlite_3 import SQLite_3
import random
import numpy as np
import SQLiteCommands


class ReplayBuffer:
    """
    Replay Buffer

    Stores and retrieves gameplay experiences
    """

    def __init__(self,db_name,state_shape,batch_size=32,max_steps_per_episode=200):
        self.state_shape = state_shape
        self.batch_size = batch_size
        self.gameplay_experiences = deque(maxlen=max_steps_per_episode)
        self.max_steps_per_episode= max_steps_per_episode
        self.sqlite = SQLite_3(db_name)
        self.array_of_sampled_indexes = np.array([])
        self.finised_sampling_episode = False
        self.current_number_of_experiences = 0

        

    def store_gameplay_experience(self,state, next_state, reward, action,done):
        """
        Records a single step (state transition) of gameplay experience.

        :param state: the current game state
        :param next_state: the game state after taking action
        :param reward: the reward taking action at the current state brings
        :param action: the action taken at the current state
        :param done: a boolean indicating if the game is finished after
        taking the action
        :return: None
        """
        if reward == None or action == None or done == None:
            return
           
        self.gameplay_experiences.append((state, next_state, reward, action,done))

        
    def sample_gameplay_batch(self,table,number_of_batches):
        """
        Samples a batch of gameplay experiences for training.

        :return: a list of gameplay experiences
        """

        current_number_of_experiences = self.getDBExperiencesCount(table)
     
        if current_number_of_experiences / self.batch_size < number_of_batches:
            raise Exception('Number of experiences {0} stored cannot create batches of {1}'.format(current_number_of_experiences,self.batch_size))

        if not self.finised_sampling_episode:
            self.array_of_sampled_indexes = self._create_array_of_sampled_indexes(current_number_of_experiences)
            self.finised_sampling_episode = False

        sample_indexes_array = self.array_of_sampled_indexes[:self.batch_size] # samples of batch_size indexes
        self.array_of_sampled_indexes = np.delete(self.array_of_sampled_indexes,list(range(self.batch_size))) # updates the array
     
        if len(self.array_of_sampled_indexes) == 0:
            self.finised_sampling_episode = True
            
        sampled_gameplay_batch = self._load_localstore_experience(table,sample_indexes_array)
        state_batch = []
        next_state_batch = []
        action_batch = []
        reward_batch = []
        done_batch = []
     
        for gameplay_experience in sampled_gameplay_batch:
            state_batch.append(gameplay_experience[0])
            next_state_batch.append(gameplay_experience[1])
            reward_batch.append(gameplay_experience[2])
            action_batch.append(gameplay_experience[3])
            done_batch.append(gameplay_experience[4])
        
        return np.array(state_batch), np.array(next_state_batch), np.array(
            reward_batch), np.array(action_batch), np.array(done_batch)


    def store_in_database(self,table):
        self.sqlite.connect()
        self.sqlite.create_table(table,SQLiteCommands.sql_create_experience_table)
        for exp in self.gameplay_experiences:
            self._save_localstore_experience(table,exp[0],exp[1],int(exp[2]),int(exp[3]),int(exp[4]))

        self.sqlite.close()
        self.gameplay_experiences.clear()

    def retrieve_all_samples(self,table):
        array = list(range(32))
        random.shuffle(array)
        experiences = self._load_localstore_experience(table,np.array(array))
        print(experiences)
        number_of_experiences = len(experiences)
        data_type = np.dtype(np.float64)
        state_batch = []
        next_state_batch = []
        action_batch = []
        reward_batch = []
        done_batch = []
     
        for gameplay_experience in experiences:
            state_batch.append(gameplay_experience[0])
            next_state_batch.append(gameplay_experience[1])
            reward_batch.append(gameplay_experience[2])
            action_batch.append(gameplay_experience[3])
            done_batch.append(gameplay_experience[4])
        
        return np.array(state_batch), np.array(next_state_batch), np.array(reward_batch), np.array(action_batch), np.array(done_batch)


    def _save_localstore_experience(self,table,state,next_state,reward,action,done):
        """"
        Saves the experience in sqlite3 db in table,
        Db must be open apriory
        
        :param state:
        :param next_state:
        :param action:
        :param reward:
        :param done:
        
        :return: None
        """
        experience = {'state' : state.tobytes(),
                      'next_state' : next_state.tobytes(),
                      'action' : action,
                      'reward' : reward,
                      'done' : done}
        
        self.sqlite.insert(table,experience)

    def _load_localstore_experience(self,table,index_array):
        """Loads the experience replay buffer from table
        :param table:
        :param index_array:

        return None
        """

        sql_conditions = ''
        index_array_len = None
        data_type = None
        counter = 0
        index_array_len = len(index_array)
        
        for index in index_array:
            sql_conditions += 'id=' + str(index.item())
            if counter != index_array_len - 1:
                sql_conditions += ' OR '
            counter += 1
            
        self.sqlite.connect()
        experiences = self.sqlite.select(table,conditions=sql_conditions)
        self.sqlite.close()
        data_type = np.dtype(np.uint8)
        result = deque(maxlen=len(experiences))
        
        for exp in experiences:
            result.append((self._reshape_image(exp[1]),self._reshape_image(exp[2]), exp[3], exp[4],exp[5]))

        return result
    
    def _reshape_image(self,byte_array):
        """Reshapes a byte array into an RGB image
        :param byte_array: 1D byte array from sqlite db 
        """

        data_type = np.dtype(np.float64)
        new_image = np.frombuffer(byte_array,data_type)
        return np.reshape(new_image,self.state_shape)

    def _create_array_of_sampled_indexes(self,current_number_of_experiences):
        return np.array(random.sample(range(current_number_of_experiences),current_number_of_experiences))

    def getExperiencesCount(self):
        """Returns the number of experiences stored in queue
        :return: <int>
        """
        return len(self.gameplay_experiences)

    def cleanMemoryBuffer(self):
        self.gameplay_experiences.clear()

    def hasSamplingFinished(self):
        """Returns a bool that tells if the array_of_sampled_indexes has been depleted and the episode has finished
        :return: <bool>
        """
        return self.finised_sampling_episode

    def getDBExperiencesCount(self,table):
        self.sqlite.connect()
        number_of_experiences = self.sqlite.getCount(table)
        self.sqlite.close()
        
        return number_of_experiences if number_of_experiences != None else 0
