# numba-oslo

Oslo model implemented in numba.

This is based on the Complexity and Networks course at Imperial College London (probably my favourite).
It was one of my first coding projects and wrote the model with a while loop.
I set my notebook running overnight and hoped for the best.
Going to see if `numba` works better.

## The Oslo Model

The Oslo model is a simple 1D model of a ricepile that exhibits self-organised criticality (scale invariance) when it reaches a steady state.

__Refer to Christensen, Christensen, Kim, and Nicholas R. Moloney. Complexity and criticality. Vol. 1. World Scientific Publishing Company, 2005. for the full details.__

It is a 1D model where each site has a height, $h_i$, equal to number of grains of rice on that site.
The local slope at that site is $z_i = h_i - h_{i+1}$.
Relaxation happens when the local slope is too large and a grain topples in an avalanche.
The model introduces randomness through thresholds for slopes, where the threshold slopes for toppling are $z_c \in \{ 1, 2 \}$ with equal probability (uniform) between the two values.

Once the sites are initialised with $z_i = 0$, the model is updated:

1. __Drive__. Add a grain of sand to the first site, $h_1 \to h_1 + 1$ (so $z_1 \to z_1 + 1$).
2. __Relaxation__. If the local slope of a site exceeds the threshold, $z_i > z_c$, then the site relaxes (topples).

$$
\begin{align*}
i = 1: \\
z_1 &\to z_1 - 2 \\
z_2 &\to z_2 + 1 \\
i = 2, ..., L-1: \\
z_i &\to z_i - 2 \\
z_{i \pm 1} &\to z_{i \pm 1} + 1 \\
i = L: \\
z_L &\to z_L - 1 \\
z_{L-1} &\to z_{L-1} + 1 \\
\end{align*}
$$

The final site, $L$, is open and grains that fall off the end are lost.

The time to reach steady state is equal to number of grains added before a grain leaves the system for the first time, or
$$
t_c(L) = \sum_{i=1}^{L} z_i \cdot i.
$$
After this critical point, the ricepile passes through a set of recurrent configurations.

The avalanche size, $s$, is the total number of relaxations upon driving.

Plot avalanche sizes after critical point against number of avalanches on log-log scale.
