import pandas as pd
from model.inference_engine import FuzzyInferenceEngine


def process_csv(input_csv, output_csv="results.csv"):
    engine = FuzzyInferenceEngine()

    df = pd.read_csv(input_csv)
    results = []

    for _, row in df.iterrows():
        inputs = row.to_dict()
        outputs = engine.compute(inputs)
        results.append({**inputs, **outputs})

    pd.DataFrame(results).to_csv(output_csv, index=False)
    print(f"Résultats sauvegardés dans {output_csv}")


if __name__ == "__main__":
    print("Use process_csv(input_csv) to run batch processing.")
def process_dataframe(df):
    engine = FuzzyInferenceEngine()
    rows = []

    for _, row in df.iterrows():
        inputs = row.to_dict()
        outputs = engine.compute(inputs)

        rows.append({
            **inputs,
            "risque": outputs["risque"],
            "action": outputs["action_label"]
        })

    return pd.DataFrame(rows)
