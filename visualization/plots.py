import matplotlib.pyplot as plt
from model.fuzzy_model import load_variables
from pathlib import Path


def plot_membership_functions():
    base_path = Path(__file__).resolve().parent.parent
    variables_path = base_path / "config" / "variables.json"

    inputs, outputs = load_variables(variables_path)

    for var in list(inputs.values()) + list(outputs.values()):
        var.view()
        plt.show()


if __name__ == "__main__":
    plot_membership_functions()




def get_membership_figures():
    """
    Return (variable_name, matplotlib_figure) for each fuzzy variable
    Optimized for Streamlit display
    """
    import matplotlib.pyplot as plt
    import numpy as np
    from model.fuzzy_model import load_variables
    from pathlib import Path

    base_path = Path(__file__).resolve().parent.parent
    variables_path = base_path / "config" / "variables.json"

    inputs, outputs = load_variables(variables_path)

    figures = []

    for var_name, var in {**inputs, **outputs}.items():
        fig, ax = plt.subplots(figsize=(3.5, 2.5))  # 👈 small size
  

        for term_name, term in var.terms.items():
            ax.plot(var.universe, term.mf, label=term_name)

        ax.set_title(var_name, fontsize=10)
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)

        fig.tight_layout()
        figures.append((var_name, fig))

    return figures


