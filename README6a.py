import pandas as pd
import numpy as np

# Load data into a pandas DataFrame
data = pd.read_excel("room.xlsx", sheet_name="room_t")  # Replace with your actual file path

# Convert datetime to pandas datetime
data['dateandtime'] = pd.to_datetime(data['dateandtime'])

# Define parameters for Q-learning
alpha = 0.1      # Learning rate
gamma = 0.9      # Discount factor
epsilon = 0.1    # Exploration factor

# Initialize the Q-table
q_table = np.zeros((len(data), 3))  # Three actions: do nothing, lower by 1 degree, lower by 2 degrees

# Function to determine reward based on conditions
def calculate_reward(desiredT, hour, occupancy, action):
    if 11 <= hour <= 14 and action == 2:
        return 1  # Reward for lowering by 2 degrees between 11 am and 2 pm
    elif occupancy == 1 and action == 1:
        return 1  # Reward for lowering by 1 degree when occupancy is 1
    else:
        return -1  # Penalize otherwise

# Training the agent
for episode in range(1000):  # Number of training episodes
    for i in range(len(data)):
        # Extract current state
        current_state = data.iloc[i]
        hour = current_state['dateandtime'].hour
        occupancy = current_state['occupancy']
        desiredT = current_state['desiredT']

        # Choose an action based on epsilon-greedy strategy
        if np.random.rand() < epsilon:
            action = np.random.choice([0, 1, 2])  # Explore
        else:
            action = np.argmax(q_table[i])  # Exploit

        # Calculate reward
        reward = calculate_reward(desiredT, hour, occupancy, action)

        # Estimate max future reward
        future_estimate = np.max(q_table[i + 1]) if i + 1 < len(data) else 0

        # Update Q-table
        q_table[i, action] = q_table[i, action] + alpha * (reward + gamma * future_estimate - q_table[i, action])

# Choose best action for each time point in the dataset
best_actions = np.argmax(q_table, axis=1)

# Apply actions to modify desiredT
for i, action in enumerate(best_actions):
    if action == 1:
        data.at[i, 'desiredT'] -= 1
    elif action == 2:
        data.at[i, 'desiredT'] -= 2

print(data)
