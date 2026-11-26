"""Replay released observations and compare with cached publisher summaries."""
import argparse
import csv
import json
import math
import os
import statistics
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/ravel-mu-matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import load_workbook


def cells(sheet, address):
    return [cell for row in sheet[address] for cell in row if cell.value is not None]


def replay(config, output):
    books = {
        number: load_workbook(f"raw_data/mu2026/MOESM{number}.xlsx", data_only=True)["Feuil1"]
        for number in sorted({panel["book"] for panel in config})
    }
    rows, summaries, contrasts = [], [], []
    figure, axes = plt.subplots(math.ceil(len(config) / 3), 3, squeeze=False,
                                figsize=(14, 3.6 * math.ceil(len(config) / 3)))
    for ax, panel in zip(axes.flat, config):
        name, book = panel["panel"], panel["book"]
        sheet = books[book]
        means = {}
        for index, (label, source, avg, sem) in enumerate(panel["groups"]):
            entries = cells(sheet, source)
            values = [cell.value for cell in entries]
            assert len(values) >= 2 and all(type(value) in (int, float) for value in values), (name, label)
            for cell in entries:
                rows.append([name, label, book, cell.coordinate, cell.value])
            mean = statistics.mean(values)
            se = statistics.stdev(values) / math.sqrt(len(values))
            saved_mean = sheet[avg].value if avg else None
            saved_se = sheet[sem].value if sem else None
            summaries.append([name, label, len(values), mean, se, avg, saved_mean,
                              None if saved_mean is None else mean - saved_mean,
                              sem, saved_se, None if saved_se is None else se - saved_se])
            means[label] = mean
            offsets = [index + 0.24 * (i / (len(values) - 1) - 0.5) for i in range(len(values))]
            ax.scatter(offsets, values, s=12, alpha=0.68, color="#315c82")
            ax.hlines(mean, index - 0.22, index + 0.22, color="#912e20")
        for contrast, weights in panel["contrasts"].items():
            contrasts.append([name, contrast, math.fsum(means[label] * w for label, w in weights.items())])
        ax.set_title(name)
        ax.set_ylabel(panel["scale"])
        ax.set_xticks(range(len(means)), means, rotation=40, ha="right", fontsize=8)
        ax.spines[["top", "right"]].set_visible(False)
    for ax in list(axes.flat)[len(config):]:
        ax.set_visible(False)
    figure.tight_layout()
    figure.savefig(output / "source_values.pdf")
    for filename, header, data in [
        ("observations.tsv", ["panel", "group", "MOESM", "cell", "value"], rows),
        ("summaries.tsv", ["panel", "group", "n_values", "mean", "value_sem", "mean_cell",
                           "cached_mean", "mean_delta", "sem_cell", "cached_sem", "sem_delta"], summaries),
        ("contrasts.tsv", ["panel", "contrast", "estimate"], contrasts),
    ]:
        with (output / filename).open("w", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
            writer.writerow(header)
            writer.writerows(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    replay(json.loads(args.map.read_text()), args.output)
