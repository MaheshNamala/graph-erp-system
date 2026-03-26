import os
import json
import pandas as pd

BASE_PATH = os.path.join(os.path.dirname(__file__), "../../data/sap-o2c-data")


def load_all_data():
    data = {}

    print("Reading from:", BASE_PATH)

    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith(".jsonl"):
                path = os.path.join(root, file)

                records = []
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        records.append(json.loads(line))

                df = pd.DataFrame(records)

                name = file.replace(".jsonl", "")
                data[name] = df

                print(f"Loaded {name}: {df.shape}")

    return data


if __name__ == "__main__":
    data = load_all_data()

    print("\nSummary:")
    for k, v in data.items():
        print(f"{k}: {v.shape}")
    for k, v in data.items():
        print(f"\n{k} columns:")
        print(v.columns.tolist())