### Model Predictive Control (MPC)

import pandas as pd
import numpy as np
import cvxpy as cp
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load and preprocess data
data = pd.read_csv('hvac_data.csv', parse_dates=['dateandtime'])
data['hour'] = data['dateandtime'].dt.hour  # Extract hour from timestamp

# System Identification (Linear Regression Model)
# Predict next temperature and flowrate based on current state
X = data[['temperature', 'angle', 'outsidetemp', 'flowrate', 'humidity', 'co2', 'pressure', 'flowspeed', 'hour']]
y_temp = data['temperature'].shift(-1).fillna(method='ffill')
y_flow = data['flowrate'].shift(-1).fillna(method='ffill')

model_temp = LinearRegression().fit(X[:-1], y_temp[:-1])
model_flow = LinearRegression().fit(X[:-1], y_flow[:-1])

# MPC Parameters
N = 5  # Prediction horizon
TARGET_TEMP = 22
MAX_ANGLE = 24
MIN_ANGLE = 19
WEIGHT_ENERGY = 0.5
WEIGHT_COMFORT = 1.0

class MPCHVACController:
    def __init__(self, model_temp, model_flow):
        self.model_temp = model_temp
        self.model_flow = model_flow
        self.coef_temp = model_temp.coef_
        self.intercept_temp = model_temp.intercept_
        self.coef_flow = model_flow.coef_
        self.intercept_flow = model_flow.intercept_
        
    def create_optimization_problem(self, current_state, future_disturbances):
        n = N
        angle = cp.Variable(n)
        temp = cp.Variable(n+1)
        flowrate = cp.Variable(n+1)
        
        # Initial conditions
        constraints = [
            temp[0] == current_state['temperature'],
            flowrate[0] == current_state['flowrate']
        ]
        
        cost = 0
        for i in range(n):
            # System dynamics from linear model
            temp_next = self.coef_temp[0]*temp[i] + self.coef_temp[1]*angle[i] + \
                        sum(self.coef_temp[j]*future_disturbances[j,i] for j in range(2,9)) + \
                        self.intercept_temp
            
            flow_next = self.coef_flow[0]*temp[i] + self.coef_flow[1]*angle[i] + \
                        sum(self.coef_flow[j]*future_disturbances[j,i] for j in range(2,9)) + \
                        self.intercept_flow
            
            constraints += [
                temp[i+1] == temp_next,
                flowrate[i+1] == flow_next,
                angle[i] >= MIN_ANGLE,
                angle[i] <= MAX_ANGLE
            ]
            
            # Cost function components
            comfort_cost = WEIGHT_COMFORT * cp.square(temp[i+1] - TARGET_TEMP)
            energy_cost = WEIGHT_ENERGY * cp.square(flowrate[i+1])
            cost += comfort_cost + energy_cost
            
        return cp.Problem(cp.Minimize(cost), constraints), angle

# Simulation Parameters
TEST_START = 100  # Starting index for simulation
SIM_STEPS = 50

# Initialize controller
controller = MPCHVACController(model_temp, model_flow)

# Storage for results
history = {
    'temp': [],
    'angle': [],
    'flowrate': [],
    'time': []
}

current_state = {
    'temperature': data['temperature'].iloc[TEST_START],
    'flowrate': data['flowrate'].iloc[TEST_START]
}

for step in range(SIM_STEPS):
    current_idx = TEST_START + step
    
    # Get future disturbances (next N hours of external factors)
    future_data = data.iloc[current_idx:current_idx+N]
    if len(future_data) < N:
        future_data = future_data.append([future_data.iloc[-1]]*(N - len(future_data)))
    
    # Format disturbance matrix [outsidetemp, humidity, co2, pressure, flowspeed, hour]
    future_disturbances = np.vstack([
        future_data['outsidetemp'].values,
        future_data['humidity'].values,
        future_data['co2'].values,
        future_data['pressure'].values,
        future_data['flowspeed'].values,
        future_data['hour'].values,
        np.ones(N)  # For intercept term
    ])
    
    # Solve MPC optimization
    problem, angle_var = controller.create_optimization_problem(current_state, future_disturbances)
    problem.solve(solver=cp.ECOS, verbose=False)
    
    if problem.status not in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE]:
        print(f"Step {step}: Solver failed")
        optimal_angle = current_state['angle']
    else:
        optimal_angle = angle_var.value[0]
    
    # Apply first control action
    current_state['angle'] = np.clip(optimal_angle, MIN_ANGLE, MAX_ANGLE)
    
    # Simulate system forward using real data
    next_state = data.iloc[current_idx + 1]
    
    # Store results
    history['temp'].append(current_state['temperature'])
    history['angle'].append(current_state['angle'])
    history['flowrate'].append(current_state['flowrate'])
    history['time'].append(current_idx)
    
    # Update state (in real system, this would come from sensors)
    current_state['temperature'] = next_state['temperature']
    current_state['flowrate'] = next_state['flowrate']

# Plot results
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(history['time'], history['temp'], label='Temperature')
plt.axhline(TARGET_TEMP, color='r', linestyle='--', label='Target')
plt.ylabel('Temperature (°C)')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(history['time'], history['angle'], label='Damper Angle')
plt.ylabel('Angle')
plt.ylim([18, 25])

plt.subplot(3, 1, 3)
plt.plot(history['time'], history['flowrate'], label='Flowrate')
plt.ylabel('Flowrate')
plt.xlabel('Time Step')

plt.tight_layout()
plt.show()
