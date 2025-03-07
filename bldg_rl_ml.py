### Backpropagation + Reinforcement Learning

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from collections import deque
import random
from sklearn.preprocessing import MinMaxScaler

# ======================================
# Neural Network for Q-Learning (DQN)
# ======================================
class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_size)
        
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# ======================================
# Replay Buffer (Experience Replay)
# ======================================
class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
    
    def __len__(self):
        return len(self.buffer)

# ======================================
# Data Preprocessing and Environment
# ======================================
class HVACDataEnvironment:
    def __init__(self, file_path):
        self.data = read_excel(file_path, sheet_name="room36s")
        self.current_step = 0
        self.scaler = MinMaxScaler()
        
        # Extract relevant features
        self.features = self.data[['humidity', 'temperature', 'co2', 'pressure',
                                  'flowspeed', 'flowrate', 'outsidetemp']]
        
        # Normalize data
        self.normalized_features = self.scaler.fit_transform(self.features)
        
        # Convert angles to discrete actions (19-24 → 0-5)
        self.actions = (self.data['angle'] - 19).astype(int).values
        self.num_actions = 6  # 19-24 inclusive
        
    def reset(self):
        self.current_step = 0
        return self.normalized_features[0]
    
    def step(self, action):
        self.current_step += 1
        if self.current_step >= len(self.data) - 1:
            done = True
            next_state = self.normalized_features[self.current_step]
        else:
            done = False
            next_state = self.normalized_features[self.current_step]
        
        # Calculate reward components from next state
        energy_use = self.data.iloc[self.current_step]['flowrate']
        temp_deviation = abs(self.data.iloc[self.current_step]['temperature'] - 22)  # 22°C target
        reward = - (0.7 * energy_use + 0.3 * temp_deviation)
        
        return next_state, reward, done

# ======================================
# DQN Agent
# ======================================
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.policy_net = DQN(state_size, action_size)
        self.target_net = DQN(state_size, action_size)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=0.001)
        self.memory = ReplayBuffer(10000)
        self.batch_size = 64
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        
    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.target_net.fc3.out_features - 1)
        else:
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state)
                q_values = self.policy_net(state_tensor)
                return q_values.argmax().item()
                
    def update_model(self):
        if len(self.memory) < self.batch_size:
            return 0
        
        batch = self.memory.sample(self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)
        
        current_q = self.policy_net(states).gather(1, actions.unsqueeze(1))
        next_q = self.target_net(next_states).max(1)[0].detach()
        target_q = rewards + (1 - dones) * self.gamma * next_q
        
        loss = nn.MSELoss()(current_q.squeeze(), target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
        if random.random() < 0.1:
            self.target_net.load_state_dict(self.policy_net.state_dict())
            
        return loss.item()

# ======================================
# Training Loop with Real Data
# ======================================
if __name__ == "__main__":
    # Initialize environment with your data
    env = HVACDataEnvironment('room36.xlsx')  # Replace with your file path
    state_size = 7  # 7 features: humidity, temp, co2, pressure, flowspeed, flowrate, outsidetemp
    action_size = env.num_actions
    agent = DQNAgent(state_size, action_size)
    
    # Training parameters
    episodes = 100
    max_steps = len(env.data) - 1
    
    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        loss = 0
        
        for step in range(max_steps):
            action = agent.select_action(state)
            next_state, reward, done = env.step(action)
            
            agent.memory.push(state, action, reward, next_state, done)
            loss += agent.update_model()
            
            state = next_state
            total_reward += reward
            
            if done:
                break
        
        print(f"Episode {episode+1}/{episodes} | Total Reward: {total_reward:.2f} | Avg Loss: {loss/step:.4f} | Epsilon: {agent.epsilon:.2f}")
    
    # Save trained model
    torch.save(agent.policy_net.state_dict(), "hvac_dqn_real.pth")

# ======================================
# Real-Time Control with Trained Model
# ======================================
def real_time_control():
    state_size = 7
    action_size = 6  # 19-24 damper angles
    
    policy_net = DQN(state_size, action_size)
    policy_net.load_state_dict(torch.load("hvac_dqn_real.pth"))
    policy_net.eval()
    
    env = HVACDataEnvironment('your_data.csv')
    state = env.reset()
    
    while True:
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state)
            action = policy_net(state_tensor).argmax().item()
        
        next_state, reward, _ = env.step(action)
        print(f"Action: {action + 19} | Temperature: {env.data.iloc[env.current_step]['temperature']:.2f}°C | Reward: {reward:.2f}")
        state = next_state

# Uncomment to run real-time control
# real_time_control()
