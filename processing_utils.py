import json
from typing import List, Dict
from pathlib import Path


def read_clones_data(filepath: Path) -> Dict:
    with open(filepath, 'r') as f:
        d = json.load(f)

        for i, d_i in d.items():
            try:
                d[i] = json.loads(d_i)
            except (json.decoder.JSONDecodeError, TypeError):
                continue

        return d


def filter_clones(
        data: Dict,
        min_length: int = 10,
        max_length: int = 10_000,
        breaks: bool = False,
        source_path: Path = None
):
    lst = list(filter(
        lambda f: min_length <= f["clone_length"] <= max_length,
        data["3"]["groups"]
    ))
    if breaks:
        for i, g in enumerate(lst):
            lst[i]['clones'] = filter_breaks(g['clones'], source_path)

    return lst


def get_stats(lst: List, norm: int = 1) -> Dict:
    return {
        'groups_cnt': len(lst) / norm,
        'clones_cnt': sum([len(g["clones"]) for g in lst]) / norm
    }


def is_break(start: int, finish: int, source: str) -> bool:
    sep = '\n# [___CELL_SEPARATOR___]\n'
    return sep in source[start:finish]


def filter_breaks(clones, source_path: Path) -> List[Dict]:
    with open(source_path, 'r') as f:
        source = f.read()
    return [clone for clone in clones
            if not is_break(*clone['position'], source)]


def get_source_path(name, in_folder=Path("data/in/notebooks_1k")):
    return in_folder / Path(str(name).split("/")[-1].replace("#", '/')[:-5])
