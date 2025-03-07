import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
import random

# ======================================
# Neural Network for Q-Learning (DQN)
# ======================================
class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 24)
        self.fc2 = nn.Linear(24, 24)
        self.fc3 = nn.Linear(24, action_size)
        
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
# HVAC Environment Simulation
# ======================================
class HVACEnv:
    def __init__(self):
        self.current_temp = 22.0  # Initial temperature (°C)
        self.occupancy = 0
        self.outdoor_temp = 25.0
        self.time_of_day = 12.0  # Hours (0-24)
        
    def step(self, action):
        # Action: 0=Decrease setpoint, 1=Maintain, 2=Increase setpoint
        setpoint_change = action - 1  # [-1, 0, +1]
        
        # Simulate temperature change
        self.current_temp += setpoint_change * 0.5
        self.current_temp += (self.outdoor_temp - self.current_temp) * 0.05
        
        # Update dynamic parameters
        self.time_of_day = (self.time_of_day + 0.1) % 24
        self.occupancy = 1 if 8 < self.time_of_day < 18 else 0  # Simulate occupancy
        
        # Calculate reward
        energy_use = abs(setpoint_change) * 0.2
        comfort_penalty = abs(self.current_temp - 22.0)  # Target 22°C
        reward = -(energy_use + 0.5 * comfort_penalty)
        
        # Create next state
        next_state = np.array([
            self.current_temp,
            self.occupancy,
            self.outdoor_temp,
            self.time_of_day
        ])
        
        return next_state, reward, False  # Never done in this continuous simulation

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
        self.batch_size = 32
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        
    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 2)  # Random action (0-2)
        else:
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state)
                q_values = self.policy_net(state_tensor)
                return q_values.argmax().item()
                
    def update_model(self):
        if len(self.memory) < self.batch_size:
            return
        
        # Sample batch from replay buffer
        batch = self.memory.sample(self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        
        # Convert to tensors
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)
        
        # Q-value calculation
        current_q = self.policy_net(states).gather(1, actions.unsqueeze(1))
        next_q = self.target_net(next_states).max(1)[0].detach()
        target_q = rewards + (1 - dones) * self.gamma * next_q
        
        # Backpropagation
        loss = nn.MSELoss()(current_q.squeeze(), target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Epsilon decay
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
        # Periodic target network update
        if random.random() < 0.1:
            self.target_net.load_state_dict(self.policy_net.state_dict())
            
        return loss.item()

# ======================================
# Training Loop
# ======================================
if __name__ == "__main__":
    # Initialize components
    env = HVACEnv()
    state_size = 4  # [temp, occupancy, outdoor_temp, time]
    action_size = 3  # 3 possible actions
    agent = DQNAgent(state_size, action_size)
    
    # Training parameters
    episodes = 500
    
    for episode in range(episodes):
        state = np.array([
            env.current_temp,
            env.occupancy,
            env.outdoor_temp,
            env.time_of_day
        ])
        
        total_reward = 0
        loss = 0
        
        # Simulate one day (240 steps)
        for _ in range(240):
            action = agent.select_action(state)
            next_state, reward, done = env.step(action)
            
            # Store experience
            agent.memory.push(state, action, reward, next_state, done)
            
            # Update model
            loss += agent.update_model()
            
            state = next_state
            total_reward += reward
            
        # Print training progress
        print(f"Episode {episode+1}/{episodes} | Total Reward: {total_reward:.2f} | Loss: {loss/240:.4f} | Epsilon: {agent.epsilon:.2f}")
    
    # Save trained model
    torch.save(agent.policy_net.state_dict(), "hvac_dqn.pth")

# ======================================
# Real-Time Control (Example Usage)
# ======================================
def real_time_control():
    # Load trained model
    state_size = 4
    action_size = 3
    policy_net = DQN(state_size, action_size)
    policy_net.load_state_dict(torch.load("hvac_dqn.pth"))
    policy_net.eval()
    
    # Initialize environment
    env = HVACEnv()
    
    while True:
        state = np.array([
            env.current_temp,
            env.occupancy,
            env.outdoor_temp,
            env.time_of_day
        ])
        
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state)
            action = policy_net(state_tensor).argmax().item()
        
        next_state, reward, _ = env.step(action)
        print(f"Action: {action} | Temp: {env.current_temp:.2f}°C | Reward: {reward:.2f}")

# Uncomment to run real-time control
# real_time_control()
