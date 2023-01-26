import random
import os
import numpy as np
from queue import Queue

import tensorflow
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense
from keras.optimizers import Adam
from keras import activations


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
        self.model = self.create_model()
        self.target_model = self.model.__copy__()
        # load model from file if exists
        if os.path.exists('model.index'):
            self.load()

    def create_model(self):
        model = Sequential()
        # model.add(Conv2D(filters=4, kernel_size=3, activation='relu', input_shape=(7, 7, 1)))
        model.add(Conv2D(filters=4, kernel_size=3, activation='sigmoid', input_shape=(7, 7, 1)))
        # activation_function = lambda x: activations.relu(x, alpha=.5, threshold=-100.0)
        # model.add(Conv2D(filters=4, kernel_size=3, activation=activation_function, input_shape=(7, 7, 1)))
        model.add(Flatten())
        # model.add(Dense(100, activation='relu'))
        model.add(Dense(100, activation='sigmoid'))
        # model.add(Dense(100, activation=activation_function))
        # add an activation function to the output layer
        model.add(Dense(4, activation='sigmoid'))
        # model.add(Dense(4))
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
                q_values = self.target_model.predict(np.array([next_state]), verbose=0)[0]
                # q_values = self.model.predict(np.array([next_state]), verbose=0)[0]
                target[action_index] = reward + self.gamma * np.max(q_values)
            training_inputs += [state]
            training_outputs += [target]
        # gradient descent update of weights in the neural network
        self.model.fit(np.array(training_inputs), np.array(training_outputs), use_multiprocessing=True, verbose=0)
        # self.target_model.fit(np.array(training_inputs), np.array(training_outputs), use_multiprocessing=True, verbose=0)

        if self.epsilon > self.epsilon_lower:
            self.epsilon *= self.epsilon_decay

    def train(self):
        memory = list(self.memory.queue)
        if self.batch_size > len(memory):
            return
        batch = random.sample(memory, self.batch_size)
        # get the states from the batch
        states = np.array([transition[0] for transition in batch])
        # get the actions from the batch
        actions = np.array([transition[1] for transition in batch])
        # get the rewards from the batch
        rewards = np.array([transition[3] for transition in batch])
        # get the next states from the batch
        next_states = np.array([transition[2] for transition in batch])
        # get the dones from the batch
        dones = np.array([transition[4] for transition in batch])

        # Compute the targets for the Q-network
        targets = rewards + (1 - dones) * self.gamma * np.amax(self.model.predict(next_states), axis=1)
        # Compute the Q-values for the current states
        q_values = self.model.predict(states)
        # Update the Q-values for the taken actions
        for i, action in enumerate(actions):
            q_values[i][action] = targets[i]
        # Train the Q-network on the updated Q-values
        self.model.fit(states, q_values, epochs=1, verbose=0, batch_size=32, shuffle=False)

        if self.epsilon > self.epsilon_lower:
            self.epsilon *= self.epsilon_decay

    def update_target(self):
        # self.model.set_weights(self.target_model.get_weights())
        self.target_model.set_weights(self.model.get_weights())

    def load(self):
        self.model.load_weights('model')
        self.target_model.load_weights('model')
        print('***** Model loaded successfully from file *****')

    def save(self):
        self.model.save_weights('model')
        print('***** Model saved successfully to file *****')
