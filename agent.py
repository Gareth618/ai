import random
import os
import numpy as np
from queue import Queue
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense
from keras.optimizers import Adam
from tensorflow.python.keras.saving.save import load_model


class Agent:
    def __init__(self, memory_size, batch_size, **hyper):
        self.alpha = hyper['alpha']
        self.gamma = hyper['gamma']
        self.epsilon = hyper['epsilon']
        self.epsilon_lower = hyper['epsilon_lower']
        self.epsilon_decay = hyper['epsilon_decay']
        self.memory = Queue(memory_size)
        self.batch_size = batch_size
        self.action_space = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # check if target_model.h5 file exists
        if os.path.exists('target_model.h5'):
            self.model = load_model('target_model.h5')
            self.target_model = load_model('target_model.h5')
            print('***** Model loaded successfully from file *****')
        else:
            self.model = self.create_model()
            self.target_model = self.create_model()

    def create_model(self):
        model = Sequential()
        model.add(Conv2D(filters=4, kernel_size=3, activation='relu', input_shape=(7, 7, 1)))
        model.add(Flatten())
        model.add(Dense(100, activation='relu'))
        model.add(Dense(4))
        model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=self.alpha))
        model.summary()
        return model

    def step(self, state, take_action):
        if random.random() < self.epsilon:
            action_index = random.randrange(4)
        else:
            q_values = self.model.predict(np.array([state]), verbose=0)[0]
            action_index = np.argmax(q_values)

        next_state, reward, game_over = take_action(self.action_space[action_index])

        # in case of invalid move
        while next_state is None:
            action_index = random.randrange(4)
            next_state, reward, game_over = take_action(self.action_space[action_index])

        if len(self.memory.queue) == self.memory.maxsize:
            self.memory.get()
        self.memory.put((state, action_index, next_state, reward, game_over))

    def replay(self):
        memory = list(self.memory.queue)
        if self.batch_size > len(memory):
            return
        batch = random.sample(memory, self.batch_size)

        training_inputs = []
        training_outputs = []

        for state, action_index, next_state, reward, game_over in batch:
            target = self.model.predict(np.array([state]), verbose=0)[0]
            if game_over:
                target[action_index] = reward
            else:
                # q_values = self.target_model.predict(np.array([next_state]), verbose=0)[0]
                q_values = self.model.predict(np.array([next_state]), verbose=0)[0]
                target[action_index] = reward + self.gamma * np.max(q_values)
            training_inputs += [state]
            training_outputs += [target]

        self.model.fit(np.array(training_inputs), np.array(training_outputs), use_multiprocessing=True, verbose=0)
        # self.target_model.fit(np.array(training_inputs), np.array(training_outputs), use_multiprocessing=True,
        # verbose=0)

        if self.epsilon > self.epsilon_lower:
            self.epsilon *= self.epsilon_decay

    def update_target(self):
        # self.model.set_weights(self.target_model.get_weights())
        self.target_model.set_weights(self.model.get_weights())

    def load(self):
        self.model.load_weights('model')

    def save(self):
        self.model.save_weights('model')

    def save_model(self, filename):
        self.model.save(filename)

    def load_model(self, filename):
        self.model = load_model(filename)
