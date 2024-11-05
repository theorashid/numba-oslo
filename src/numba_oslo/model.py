from dataclasses import dataclass
from typing import Tuple

import numpy as np
from numba import njit


@njit  # equivalent to @jit(nopython=True)
def _init_slopes(L: int) -> Tuple[np.array, np.array]:
    """Initialize slopes and thresholds"""
    slopes = np.zeros(L, dtype=np.int32)
    thresholds = np.ones(L, dtype=np.int32)

    # cannot use np.random.choice here because of numba
    for i in range(L):
        thresholds[i] = 1 if np.random.random() < 0.5 else 2
    return slopes, thresholds


@njit
def _relax_sites(slopes: np.array, thresholds: np.array, L: int) -> Tuple[int, bool]:
    """Relax unstable sites, return (avalanche_size, grain_left_system)"""
    avalanche_size = 0
    grain_left = False

    while True:
        stable = True
        # for debugging
        # heights = np.cumsum(slopes[::-1])[::-1]
        # print(heights, slopes, thresholds)
        for i in range(L):
            if slopes[i] > thresholds[i]:
                stable = False
                avalanche_size += 1

                if i == 0:  # first site
                    slopes[i] -= 2
                    slopes[i + 1] += 1
                elif i == L - 1:  # last site
                    slopes[i] -= 1
                    slopes[i - 1] += 1
                    grain_left = True
                else:  # middle sites
                    slopes[i] -= 2
                    slopes[i - 1] += 1
                    slopes[i + 1] += 1

                # update threshold each time this site topples
                thresholds[i] = 1 if np.random.random() < 0.5 else 2

        if stable:
            break

    return avalanche_size, grain_left


@njit
def _run_simulation(
    L: int, steps: int, slopes: np.ndarray, thresholds: np.ndarray
) -> Tuple[np.ndarray, int, bool]:
    """Jitted simulation core"""
    avalanches = np.zeros(steps, dtype=np.int32)
    steady_state_time = 0
    reached_steady = False

    for step in range(steps):
        # drive
        slopes[0] += 1

        # relax and record
        avalanche_size, grain_left = _relax_sites(slopes, thresholds, L)
        avalanches[step] = avalanche_size

        # check steady state
        if not reached_steady and grain_left:
            reached_steady = True
            steady_state_time = step + 1

    return avalanches, steady_state_time, reached_steady


@dataclass
class RicePile:
    L: int
    steady_state_time: int = 0
    reached_steady_state: bool = False

    def __init__(self, L: int):
        """Initialize ricepile with size L"""
        self.L = L
        self.slopes, self.thresholds = _init_slopes(L)

    def run(self, steps: int) -> np.ndarray:
        """Run simulation wrapper"""
        avalanches, self.steady_state_time, self.reached_steady_state = _run_simulation(
            self.L,
            steps,
            self.slopes,
            self.thresholds,
        )
        return avalanches
