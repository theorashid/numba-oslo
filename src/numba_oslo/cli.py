from pathlib import Path
from typing import Optional

import numpy as np
import polars as pl
import altair as alt
import typer

from .model import RicePile

app = typer.Typer()


def create_plot(avalanches: np.ndarray) -> alt.Chart:
    """Create power law distribution plot from avalanche data."""
    unique, counts = np.unique(avalanches, return_counts=True)

    data = pl.DataFrame({"size": unique, "count": counts})
    typer.echo(data)

    chart = (
        alt.Chart(data)
        .mark_circle(size=0.8, opacity=0.8, color="#E63946")
        .encode(
            x=alt.X("size:Q", scale=alt.Scale(type="symlog"), title="Avalanche Size"),
            y=alt.Y("count:Q", scale=alt.Scale(type="log"), title="Frequency"),
        )
        .properties(width=500, height=400)
        .configure_axis(
            gridWidth=0.5,  # Thinner grid lines
            gridOpacity=0.3,  # Lighter grid lines
        )
    )
    return chart


@app.command()
def run_and_save(
    size: int = typer.Option(4, "-L", "--size", help="Size of the rice pile"),
    steps: int = typer.Option(1000, "-N", "--steps", help="Number of simulation steps"),
    output: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output",
        help="Output file name (default: avalanches_L{size}_N{steps}.npy)",
    ),
    plot: bool = typer.Option(
        False, "--plot", help="Create and save plot of avalanche sizes"
    ),
) -> None:
    rice = RicePile(size)
    avalanches = rice.run(steps)

    if output is None:
        output = Path(f"avalanches_L{size}_N{steps}.npy")

    np.save(output, avalanches)
    typer.echo(f"Saved results to {output}")

    if plot:
        if rice.reached_steady_state:
            steady_state_avalanches = avalanches[rice.steady_state_time :]
            plot_path = output.with_suffix(".png")
            chart = create_plot(steady_state_avalanches)
            chart.save(str(plot_path), dpi=600, scale_factor=2.0)
            typer.echo(f"Saved plot to {plot_path}")
        else:
            typer.echo("Steady state not reached - no plot generated")

    typer.echo(f"Reached steady state: {rice.reached_steady_state}")
    if rice.reached_steady_state:
        typer.echo(f"Steady state reached at step: {rice.steady_state_time}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
