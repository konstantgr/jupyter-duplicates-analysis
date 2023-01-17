import os
import matplotlib.pyplot as plt
import pandas as pd

from pathlib import Path
from utils.processing_utils import read_clones_data, filter_clones, get_stats, get_source_path
from tqdm import tqdm


class Experiment:
    def __init__(self, notebooks_folder, scripts_folder=None, max_num=50, in_path=None):
        self.notebooks_folder = notebooks_folder
        self.scripts_folder = scripts_folder
        self.max_num = max_num

        self.files = self._get_files()
        self.in_path = in_path
        self.source_files = self._get_source_files() if in_path else {'notebooks': [], 'scripts': []}

        self.length_range = None
        self.aggregated_stats = {'notebooks': None, 'scripts': None}

    @staticmethod
    def _get_json_files(folder, max_num):
        return [folder / Path(pos_json) for pos_json in os.listdir(folder) if
                pos_json.endswith('.json')][:max_num]

    def _get_source_files(self):
        return {k: [get_source_path(file, in_folder=folder) for file in self.files[k]]
                for k, folder in self.in_path.items()}

    def _get_files(self):
        notebook_files = self._get_json_files(self.notebooks_folder, self.max_num)
        scripts_files = None if not self.scripts_folder else self._get_json_files(self.scripts_folder, self.max_num)

        files = {'notebooks': notebook_files, 'scripts': scripts_files}
        return files

    @staticmethod
    def aggregate(files, length_range, source_paths, normalize=False, drop_breaks=False):
        stats = []

        for i, file in tqdm(enumerate(files)):
            data_tmp = read_clones_data(file)
            try:
                norm = data_tmp.get('initial_tree_length') if normalize else 1
                path = source_paths[i] if source_paths else None
                drop_breaks = drop_breaks if path else None

                stats_tmp = [
                    get_stats(
                        filter_clones(data=data_tmp, min_length=min_l, breaks=drop_breaks, source_path=path),
                        norm=norm
                    )
                    for min_l in length_range
                ]
                stats_tmp = pd.DataFrame(stats_tmp)
                stats_tmp['min_length'] = list(length_range)

                stats.append(pd.DataFrame(stats_tmp))
            except KeyError:
                continue

        stats = pd.concat(stats)
        return stats

    def run(self, length_range=range(3, 60), normalize=False, drop_breaks=False):
        self.length_range = length_range
        for files_type, files in self.files.items():
            if files is not None:
                self.aggregated_stats[files_type] = self.aggregate(
                    files, length_range, self.source_files.get(files_type),
                    normalize=normalize, drop_breaks=drop_breaks
                )

    @staticmethod
    def plot_stats(ax, stats_type, stats, params):
        x, y = stats.min_length, stats.clones_cnt
        ax.scatter(x, y, color='k', s=2, alpha=0.1)

        stats_tmp = stats.groupby("min_length").mean().reset_index()
        x, y = stats_tmp.min_length, stats_tmp.clones_cnt
        ax.plot(x, y, 'o-', color='r')

        ax.set_title(f"Clones count {stats_type}")
        ax.set_xlabel("Min clone length")
        ax.set_ylabel("Clones count")

        if params and params.get('log'):
            ax.set_yscale('log')
            ax.set_ylabel("Clones count (log)")

        return ax

    def plot_results(self, params=None, **kwargs):
        fig, axs = plt.subplots(2, figsize=(6, 10))

        for i, (files_type, stats_df) in enumerate(self.aggregated_stats.items()):
            axs[i] = self.plot_stats(axs[i], files_type, stats_df, params)

        plt.show()


if __name__ == "__main__":
    notebooks_path = Path('data/out/notebooks_1k')
    scripts_path = Path('data/out/scripts_1k')

    e = Experiment(
        notebooks_folder=notebooks_path,
        scripts_folder=scripts_path,
        max_num=10
    )

    min_clone_length, max_clone_length = 3, 90
    e.run(normalize=False, drop_breaks=False, length_range=range(3, max_clone_length + 1))
