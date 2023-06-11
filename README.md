# Traveling salesman problem using simulated annealing

<p align="center">
<img src="https://github.com/Roninkoi/ParPS/assets/12766039/5e1784a3-4f29-433f-b079-84cf2fb1f439" width=40% height=40%>
<img src="https://github.com/Roninkoi/ParPS/assets/12766039/3549f160-f1bb-42b6-ac88-172df1add424" width=40% height=40%>
</p>

This Python program solves the traveling salesman problem using simulated annealing with the Metropolis Monte Carlo algorithm. The problem has many local minima, so to make sure we find a global minimum, we want so sample the space widely while staying within reasonable computational time. The concept of a ``temperature'' is useful, since it allows us to control the probability of a transition is between minima. The simulated annealing is done by controlling the temperature profile. We want to go from a high temperature to a low temperature to first do rough sampling for the global minimum and then narrow down to a single point. When temperature is high, the MMC algorithm accepts states almost randomly. When temperature is low, the MMC algorithm only accepts states below the current one.

Paths of the salesman are states of the system, and the the length of the path is equivalent to energy of the system. The ``energy minimum'' of the system is the shortest path. Since we have an ergodic system, we can start from a random path. We can reach a path from any other path by swapping two path elements. We can represent the path between points (e.g. in a 2D plane) using their indices $0 \rightarrow 1 \rightarrow 2 \rightarrow \cdots \rightarrow N$. To generate a random path, we can swap indices randomly. Starting from a random path, the algorithm proceeds by generating a trial state $\bm{v}'$ by swapping. We calculate the distance of the path before and after swapping, and used the difference $\Delta L$ to decide whether to accept the trial state. We calculate a probability based on $\Delta L$ and a temperature $T$ as

$$
P = \exp \left ( -\Delta L / T \right ).
$$

We accept the trial state $\bm{v} \leftarrow \bm{v}'$ only if $\Delta L < 0$ or if a random number $U \sim \mathcal{U}(0, 1)$ satisfies $U < P$. This allows the path length to increase when the temperature is high to get out of a local minimum.

The program takes a file containing the $xy$ positions and names of the cities, the starting temperature and the number of MC steps as arguments. The salesman starts from home and returns to home, which forms a closed path. This means the first and last points of the path must be the same and must not change (we can assume home is the first city, since the path can be shifted). In order to ensure this, we need to skip the first and last points when swapping. When reading in the list of cities, we add the starting point to the end of the path. The MMC algorithm is run for this path at various temperatures in multiple annealing passes to determine the shortest path.

The simulated annealing starts from a temperature $T_0$ and reduces to some lower temperature. A range of temperatures $T \in [T_0, 0]$ is used for the MMC algorithm in multiple stages. At each stage, the MMC algorithm runs for $N_\text{steps}$ steps. We use a general power function $T^{1/\alpha}$, where we have a linear range $T \in [T_0^{\alpha}, (T_0/T_e)^{\alpha}]$ consisting of $N_\text{steps}$ points. The parameter $\alpha$ determines the shape of the temperature curve. The temperature reduction at the end of the range is defined by $T_e$, e.g. $T_e = 2$ halves the temperature from $T_0$. Between stages, we reduce the starting temperature $T_0$ by a reduction factor $T_f$, i.e. $T_0 \leftarrow T_0 / T_f$. We stop annealing when temperature becomes low $T_0 < T_\varepsilon$. To control $T_0$ based on the path length $L$, we keep track of the minimum $L_\text{min}$. When $L > L_\text{min}$, we return the previous $T_0 \leftarrow T_0 T_f$. This discourages the state from getting too far from the minimum. We use parameters $\alpha = 0.5$, $T_f = 2$, $T_e = 20$ and $T_\varepsilon = 0.001$.

## Running

All simulations can be run using:
```
./run.sh
```

Usage:
```
./annealed_salesman.py [input.dat] [T0] [nsteps] [show]
```

`input.dat` = input file of location coordinates with names

`T0` = starting temperature for simulated annealing

`nsteps` = number of MC steps

`show` = if 0, don't show plots

The awk script `random.sh` can be used to generate randomized $xy$ data for testing.

