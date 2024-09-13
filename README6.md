### Original Equation:

\[ T_{sup} = T_{rtn} + (1 - CWV) \cdot (T_{rtn} - T_{set}) + k \cdot VSD \]

### Modified Equation Using Time Periodic Adjustment:

We'll enhance \( T_{rtn} \) with a time-periodic adjustment using a rolling average over a specified window size, \( W \).

1. **Rolling Average of \( T_{rtn} \) over Window Size \( W \)**:
   Define the rolling average of \( T_{rtn} \) as \( T_{rtn}^{MA}(t, W) \), which is calculated over a window size \( W \):

   \[ T_{rtn}^{MA}(t, W) = \frac{1}{W} \sum_{i=0}^{W-1} T_{rtn}(t - i) \]

2. **Incorporate the Rolling Average \( T_{rtn}^{MA} \) into the Original Equation**:
   Replace \( T_{rtn} \) with \( T_{rtn}^{MA}(t, W) \):

   \[ T_{sup}(t) = T_{rtn}^{MA}(t, W) + (1 - CWV) \cdot \left( T_{rtn}^{MA}(t, W) - T_{set} \right) + k \cdot VSD \]

   Here, 
   - \( T_{rtn}^{MA}(t, W) \) is the moving average of the return air temperature over a window size \( W \).
   - \( t \) represents the current time step.

### Optimization Strategy:

To find the optimal window size \( W \) that minimizes the variance of \( T_{sup} \), iterate over different values of \( W \):

\[ W_{opt} = \arg\min_{W} \operatorname{Var}\left( T_{sup}(t) \right) \]

### Final Equation with Optimal Window:

Once the optimal window size \( W_{opt} \) is found, the final equation for the supply air temperature adjustment is:

\[ T_{sup}(t) = T_{rtn}^{MA}(t, W_{opt}) + (1 - CWV) \cdot \left( T_{rtn}^{MA}(t, W_{opt}) - T_{set} \right) + k \cdot VSD \]

In summary:

- **\( T_{rtn}^{MA}(t, W) \)**: Rolling average of \( T_{rtn} \) over window size \( W \).
- **Optimization**: Find \( W_{opt} \) that minimizes the variance of \( T_{sup} \).
- **Final Equation**: Use \( W_{opt} \) to adjust \( T_{sup} \) periodically.

### Final Combined Equation:

\[ T_{sup}(t) = \frac{1}{W_{opt}} \sum_{i=0}^{W_{opt}-1} T_{rtn}(t - i) + (1 - CWV) \cdot \left( \frac{1}{W_{opt}} \sum_{i=0}^{W_{opt}-1} T_{rtn}(t - i) - T_{set} \right) + k \cdot VSD \]

By using this equation, the supply air temperature \( T_{sup} \) will be periodically adjusted using a time-averaged return air temperature, optimizing stability and performance over the chosen time intervals.
