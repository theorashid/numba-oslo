"""Implementation of the Oslo model in numba."""

from beartype.claw import beartype_this_package

beartype_this_package() 

__version__ = "0.1.0"

def main() -> None:
    print("Hello from numba-oslo!")
