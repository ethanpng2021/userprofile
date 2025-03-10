### Original Equation:

Without PMV:\
$$T_{sup} = T_{rtn} + (1 - CWV) \cdot (T_{rtn} - T_{set}) + k \cdot VSD$$

With PMV:\
$$T_{sup} = T_{rtn} + (1 - CWV) \cdot (T_{rtn} - T_{set}) + k \cdot VSD + \alpha \cdot pmv$$

Combined with VAV dampers downstream:\
$$T_{sup} = T_{rtn} + (1 - CWV) \cdot (T_{rtn} - T_{set}) + k \cdot VSD + \alpha \cdot pmv + \beta \cdot \left(\sum_{i=1}^{10} w_i \cdot D_i\right)$$

In this equation:

- $$\alpha$$ is a coefficient that determines the impact of 'pmv' on the supply temperature, $$\text T_{sup}$$.
- This formulation assumes that 'pmv' has an additive effect on the resultant value of the equation. The nature of this influence should be guided by the context (e.g., if 'pmv' represents thermal comfort, it might influence the setpoints or act as a feedback mechanism).
- $$\beta$$ is a coefficient that represents how strongly VAV damper positions affect the supply air temperature.
- $$D_{i}$$ is the damper position for the $$i^{th}$$ VAV.
- $$w_{i}$$ is the weight factor for each VAV damper position. These weights may need to be determined based on how significantly each VAV influences the system, potentially requiring calibration based on system performance or empirical data.

### Modified Equation Using Time Periodic Adjustment:

We'll enhance $$\text T_{rtn} $$ with a time-periodic adjustment using a rolling average over a specified window size, $$\text W $$.

1. **Rolling Average of $$\text T_{rtn} $$ over Window Size $$\text W $$**:
   Define the rolling average of $$\text T_{rtn}$$ as $$\text T_{rtn}^{MA}(t, W)$$, which is calculated over a window size $$\text W$$:

   $$\text T_{rtn}^{MA}(t, W) = \frac{1}{W} \sum_{i=0}^{W-1} T_{rtn}(t - i) $$

2. **Incorporate the Rolling Average $$\text T_{rtn}^{MA} $$ into the Original Equation**:
   Replace $$\text T_{rtn} $$ with $$\text T_{rtn}^{MA}(t, W) $$:

   $$T_{sup}(t) = T_{rtn}^{MA}(t, W) + (1 - CWV) \cdot \left( T_{rtn}^{MA}(t, W) - T_{set} \right) + k \cdot VSD$$

   Here, 
   - $$\text T_{rtn}^{MA}(t, W) $$ is the moving average of the return air temperature over a window size $$\text W $$.
   - $$\text t $$ represents the current time step.

### Optimization Strategy:

To find the optimal window size $$\text W $$ that minimizes the variance of $$\text T_{sup} $$, iterate over different values of $$\text W $$:

$$\text W_{opt} = \arg\min_{W} \text{Var}\left( T_{sup}(t) \right) $$

### Final Equation with Optimal Window:

Once the optimal window size $$\text W_{opt} $$ is found, the final equation for the supply air temperature adjustment is:

$$ T_{sup}(t) = T_{rtn}^{MA}(t, W_{opt}) + (1 - CWV) \cdot \left( T_{rtn}^{MA}(t, W_{opt}) - T_{set} \right) + k \cdot VSD $$

In summary:

- **$$\text T_{rtn}^{MA}(t, W) $$**: Rolling average of $$\text T_{rtn} $$ over window size $$\text W $$.
- **Optimization**: Find $$\text W_{opt} $$ that minimizes the variance of $$\text T_{sup} $$.
- **Final Equation**: Use $$\text W_{opt} $$ to adjust $$\text T_{sup} $$ periodically.

### Final Combined Equation:

$$ T_{sup}(t) = \frac{1}{W_{opt}} \sum_{i=0}^{W_{opt}-1} T_{rtn}(t - i) + (1 - CWV) \cdot \left( \frac{1}{W_{opt}} \sum_{i=0}^{W_{opt}-1} T_{rtn}(t - i) - T_{set} \right) + k \cdot VSD $$

By using this equation, the supply air temperature $$\text T_{sup} $$ will be periodically adjusted using a time-averaged return air temperature, optimizing stability and performance over the chosen time intervals.

### Executing LP (Linear Solver)
```python
from pulp import LpProblem, LpVariable, LpMinimize

# Create LP problem
lp = LpProblem("Cooling_Optimization", LpMinimize)

# Define variables
CWV = LpVariable("CWV", 0, 100)  # Chilled Water Valve (0% - 100%)
VSD = LpVariable("VSD", 0, 1)     # Variable Speed Drive (0 - 1)
T_sup = LpVariable("T_sup", 20, 26)  # Supply Temperature (20°C - 26°C)

# Given parameters (assumed)
T_rtn = 24  # Return Air Temperature (°C)
T_set = 22  # Setpoint Temperature (°C)
outsideTemp = 35  # Outdoor Temperature (°C)
alpha = 0.1  # Outdoor temp impact factor
k = 0.5  # VSD impact factor on T_sup
a, b = 0.2, 0.3  # Energy cost coefficients

# Supply temperature equation
lp += T_sup == T_rtn + (1 - CWV / 100) * (T_rtn - T_set) + k * VSD - alpha * (outsideTemp - 30)

# Temperature reduction constraint
lp += T_sup <= T_set - 2

# Energy minimization objective
lp += a * VSD + b * CWV

# Solve the problem
lp.solve()

# Output results
print("Optimized CWV:", CWV.varValue, "%")
print("Optimized VSD:", VSD.varValue)
print("Optimized Supply Temp:", T_sup.varValue, "°C")
```

### Executing LP + MPC (Linear Solver + Model Predictive Control)
```python
from pulp import LpProblem, LpVariable, LpMinimize, LpStatus
import pandas as pd
import numpy as np

class MPCHVACController:
    def __init__(self, data, prediction_horizon=3):
        self.data = data
        self.N = prediction_horizon
        self.T_set = 22
        self.current_step = 0
        
        # System parameters (from your original example)
        self.alpha = 0.1  # Outdoor temp impact factor
        self.k = 0.5      # VSD impact factor on T_sup
        self.a, self.b = 0.2, 0.3  # Energy cost coefficients
        
    def create_mpc_problem(self):
        # Initialize MPC problem
        mpc = LpProblem("MPC_Cooling_Optimization", LpMinimize)
        
        # Time indices
        time_steps = range(self.N)
        
        # Create decision variables for each time step
        CWV = {t: LpVariable(f"CWV_{t}", 0, 100) for t in time_steps}
        VSD = {t: LpVariable(f"VSD_{t}", 0, 1) for t in time_steps}
        T_sup = {t: LpVariable(f"T_sup_{t}", 20, 26) for t in time_steps}
        
        # State variables (using actual historical data)
        T_rtn = {t: self.get_future_value('temperature', t) for t in time_steps}
        outsideTemp = {t: self.get_future_value('outsidetemp', t) for t in time_steps}
        
        # System dynamics constraints
        for t in time_steps:
            mpc += T_sup[t] == T_rtn[t] + (1 - CWV[t]/100) * (T_rtn[t] - self.T_set) + \
                   self.k * VSD[t] - self.alpha * (outsideTemp[t] - 30)
            
            # Temperature reduction constraint
            mpc += T_sup[t] <= self.T_set - 2
            
            # Add coupling constraints between time steps
            if t > 0:
                mpc += CWV[t] <= CWV[t-1] + 10  # Rate constraint example
                mpc += CWV[t] >= CWV[t-1] - 10

        # Objective function (cumulative energy cost)
        mpc += self.a * sum(VSD[t] for t in time_steps) + \
               self.b * sum(CWV[t] for t in time_steps)/100
        
        return mpc, CWV, VSD, T_sup
    
    def get_future_value(self, col, offset):
        idx = self.current_step + offset
        if idx < len(self.data):
            return self.data[col].iloc[idx]
        return self.data[col].iloc[-1]  # Use last value if beyond data
    
    def update_state(self):
        self.current_step += 1
        if self.current_step >= len(self.data):
            self.current_step = 0

# Load your dataset
data = pd.read_csv('your_data.csv', parse_dates=['dateandtime'])

# Initialize MPC controller
mpc_controller = MPCHVACController(data, prediction_horizon=3)

# Simulation loop
results = []
for step in range(len(data)):
    # Create and solve MPC problem
    mpc, CWV, VSD, T_sup = mpc_controller.create_mpc_problem()
    mpc.solve()
    
    # Get optimal first control action
    if LpStatus[mpc.status] == 'Optimal':
        current_action = {
            'CWV': CWV[0].varValue,
            'VSD': VSD[0].varValue,
            'T_sup': T_sup[0].varValue
        }
    else:
        current_action = {'CWV': 50, 'VSD': 0.5, 'T_sup': 22}  # Fallback
        
    # Store results with actual measurements
    results.append({
        'time': data['dateandtime'].iloc[mpc_controller.current_step],
        **current_action,
        'actual_temp': data['temperature'].iloc[mpc_controller.current_step],
        'outside_temp': data['outsidetemp'].iloc[mpc_controller.current_step]
    })
    
    # Move to next time step
    mpc_controller.update_state()

# Print results analysis
print("\nMPC Performance Summary:")
print(f"Average CWV: {np.mean([r['CWV'] for r in results]):.1f}%")
print(f"Average VSD: {np.mean([r['VSD'] for r in results]):.2f}")
print(f"Temperature Deviations: {np.mean([abs(r['actual_temp'] - 22) for r in results]):.2f}°C")

# Plot results
pd.DataFrame(results).set_index('time').plot(subplots=True, figsize=(12, 8))
plt.tight_layout()
plt.show()
```
