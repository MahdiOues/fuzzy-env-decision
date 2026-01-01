import json
from pathlib import Path
from skfuzzy import control as ctrl
from io_utils.logger import logger

from model.fuzzy_model import load_variables
from model.action_mapper import action_to_label

def load_rules(rules_path, inputs, outputs):
    """
    Convert JSON rules into scikit-fuzzy Rule objects
    """
    with open(rules_path, "r", encoding="utf-8") as f:
        rules_config = json.load(f)

    rules = []

    for rule in rules_config:
        # Build IF part
        antecedent = None
        for var_name, set_name in rule["if"].items():
            condition = inputs[var_name][set_name]
            antecedent = condition if antecedent is None else antecedent & condition

        # Build THEN part (can be multi-output)
        consequents = []
        for var_name, set_name in rule["then"].items():
            consequents.append(outputs[var_name][set_name])

        rules.append(ctrl.Rule(antecedent, consequents))

    return rules


class FuzzyInferenceEngine:
    def __init__(self):
        base_path = Path(__file__).resolve().parent.parent

        # Load variables
        variables_path = base_path / "config" / "variables.json"
        self.inputs, self.outputs = load_variables(variables_path)

        # Load rules
        rules_path = base_path / "config" / "rules.json"
        rules = load_rules(rules_path, self.inputs, self.outputs)

        # Create Mamdani control system
        self.system = ctrl.ControlSystem(rules)
        self.simulation = ctrl.ControlSystemSimulation(self.system)

    def compute(self, input_values: dict):
        """
        Compute fuzzy outputs with robustness, logging, and safe defaults.
        """

        # --------------------------------------------------
        # INPUT VALIDATION (ROBUSTNESS)
        # --------------------------------------------------
        for var, value in input_values.items():
            if var not in self.inputs:
                raise ValueError(f"Unknown input variable: {var}")

            if not isinstance(value, (int, float)):
                raise ValueError(f"Invalid type for {var}: {value}")

            if value < 0 or value > 100:
                raise ValueError(f"Out-of-range value for {var}: {value}")

        logger.info(f"Inputs received: {input_values}")

        # --------------------------------------------------
        # RESET + ASSIGN INPUTS
        # --------------------------------------------------
        self.simulation.reset()

        for var, value in input_values.items():
            self.simulation.input[var] = value

        # --------------------------------------------------
        # COMPUTE
        # --------------------------------------------------
        try:
            self.simulation.compute()
        except Exception as e:
            logger.warning(f"Fuzzy computation failed: {e}")

        outputs = {}

        # --------------------------------------------------
        # RISK OUTPUT
        # --------------------------------------------------
        if "risque" in self.simulation.output:
            outputs["risque"] = float(self.simulation.output["risque"])
        else:
            outputs["risque"] = 0.0

        # --------------------------------------------------
        # ACTION OUTPUT (numeric + label)
        # --------------------------------------------------
        if "action" in self.simulation.output:
            action_value = float(self.simulation.output["action"])
        else:
            action_value = 0.0

        outputs["action_value"] = action_value
        outputs["action_label"] = action_to_label(action_value)

        logger.info(f"Outputs produced: {outputs}")

        return outputs

    

if __name__ == "__main__":
    # Quick test
    engine = FuzzyInferenceEngine()

    test_input = {
        "pollution_air": 80,
        "pollution_eau": 70,
        "humidite_sol": 30,
        "erosion": 60,
        "vegetation": 20,
        "biodiversite": 25,
        "temperature": 35,
        "urbanisation": 70,
        "deforestation": 65,
        "stress_hydrique": 75
    }

    result = engine.compute(test_input)
    print("Outputs:")
    for k, v in result.items():
        print(f" - {k}: {v:.2f}")
