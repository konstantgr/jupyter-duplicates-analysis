import pandas as pd
import json
from pathlib import Path


def input_data_to_df(base_path: Path):
    data = []
    for path in base_path.rglob('*.py'):
        with open(path, 'r') as f:
            data.append({'name': path.name, 'content': f.read()})

    return pd.DataFrame(data)


def output_data_to_df(base_path: Path):
    data = []
    for path in base_path.rglob('*.json'):
        try:
            with open(path, 'r') as f:
                d = json.loads(json.load(f).get('3'))
                d['name'] = path.name
                data.append(d)

        except TypeError:
            print(f"ERROR WITH OPEN {path}")
            continue

    return pd.json_normalize(data, max_level=1)


if __name__ == "__main__":
    df_in = output_data_to_df(Path('data/in/notebooks_1k'))
    df_out = output_data_to_df(Path('data/out/notebooks_1k'))

