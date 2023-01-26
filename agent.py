import random
import numpy as np
from queue import Queue
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense

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

    def create_model(self):
        model = Sequential()
        model.add(Conv2D(filters=4, kernel_size=3, activation='softmax', input_shape=(7, 7, 1)))
        model.add(Flatten())
        model.add(Dense(100, activation='softmax'))
        model.add(Dense(len(self.action_space)))
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
        if self.batch_size > len(memory): return
        batch = random.sample(memory, self.batch_size)

        training_inputs = []
        training_outputs = []
        for state, action_index, next_state, reward, game_over in batch:
            target = self.model.predict(np.array([state]), verbose=0)[0]
            if game_over:
                target[action_index] = reward / 530
            else:
                q_values = self.model.predict(np.array([next_state]), verbose=0)[0]
                target[action_index] = reward / 530 + self.gamma * np.max(q_values)
            training_inputs += [state]
            training_outputs += [target]

        self.model.fit(np.array(training_inputs), np.array(training_outputs), use_multiprocessing=True, verbose=0)
        if self.epsilon > self.epsilon_lower:
            self.epsilon *= self.epsilon_decay

    def load(self):
        self.model.load_weights('model')

    def save(self):
        self.model.save_weights('model')
