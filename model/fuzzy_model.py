import json
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from pathlib import Path


def load_variables(config_path: str):
    """
    Load fuzzy variables from a JSON configuration file.
    Returns two dictionaries:
    - inputs: Antecedents
    - outputs: Consequents
    """

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    inputs = {}
    outputs = {}

    for var_name, var_data in config.items():
        start, end = var_data["range"]
        universe = np.arange(start, end + 1, 1)

        if var_data["type"] == "input":
            variable = ctrl.Antecedent(universe, var_name)
        elif var_data["type"] == "output":
            variable = ctrl.Consequent(universe, var_name)
        else:
            raise ValueError(f"Unknown variable type: {var_data['type']}")

        # Create membership functions
        for set_name, points in var_data["sets"].items():
            variable[set_name] = fuzz.trimf(universe, points)

        # Store variable
        if var_data["type"] == "input":
            inputs[var_name] = variable
        else:
            outputs[var_name] = variable

    return inputs, outputs


if __name__ == "__main__":
    # Simple test to verify loading works
    base_path = Path(__file__).resolve().parent.parent
    config_path = base_path / "config" / "variables.json"

    inputs, outputs = load_variables(config_path)

    print("Input variables:")
    for k in inputs:
        print(" -", k)

    print("\nOutput variables:")
    for k in outputs:
        print(" -", k)
