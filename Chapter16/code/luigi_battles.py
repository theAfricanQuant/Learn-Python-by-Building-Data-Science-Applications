# luigi_fronts.py
import json
import time
from pathlib import Path

import luigi
from luigi_fronts import ScrapeFronts
from misc import _parse_in_depth
from wikiwwii.collect.battles import parse_battle_page

folder = Path(__file__).parents[1] / "data"


class ParseFront(luigi.Task):
    front = luigi.Parameter()

    def requires(self):
        return ScrapeFronts()

    def output(self):
        path = str(folder / "fronts" / f"{self.front}.json")
        return luigi.LocalTarget(path)

    def run(self):
        with open(self.input().path, "r") as f:
            fronts = json.load(f)

        front = fronts[self.front]
        result = {
            cp_name: _parse_in_depth(campaign, cp_name)
            for cp_name, campaign in front.items()
        }
        self.output().makedirs()
        with open(self.output().path, "w") as f:
            json.dump(result, f)


class ParseAll(luigi.Task):
    fronts = [
        "African Front",
        "Mediterranean Front",
        "Western Front",
        "Atlantic Ocean",
        "Eastern Front",
        "Indian Ocean",
        "Pacific Theatre",
        "China Front",
        "Southeast Asia Front",
    ]

    def requires(self):
        return [ParseFront(front=f) for f in self.fronts]
