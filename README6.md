### Original Equation:

Without PMV:\
$$T_{sup} = T_{rtn} + (1 - CWV) \cdot (T_{rtn} - T_{set}) + k \cdot VSD$$

With PMV:\
$$T_{sup} = T_{rtn} + (1 - CWV) \cdot (T_{rtn} - T_{set}) + k \cdot VSD + \alpha \cdot pmv$$

In this equation:

- $$\alpha$$ is a coefficient that determines the impact of 'pmv' on the supply temperature, $$\text T_{sup}$$.
- This formulation assumes that 'pmv' has an additive effect on the resultant value of the equation. The nature of this influence should be guided by the context (e.g., if 'pmv' represents thermal comfort, it might influence the setpoints or act as a feedback mechanism).

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
