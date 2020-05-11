import json
import os
import pathlib
import sys

from skcriteria import Data, MAX
from skcriteria.madm import closeness


def main():
    user_criteria = json.loads(sys.argv[1])

    weights = {k: criteria_preference_to_weight(v) for k, v in
               user_criteria["user_criteria"]["question_big_data"][0].items()}

    with open(os.path.join(pathlib.Path(__file__).parent.absolute(), 'rating_matrix.json')) as f:
        data = json.load(f)

    rating_mtx = []
    alternative_names = data["rating"].keys()
    criteria_names = data["criteria"].keys()
    criteria = [MAX for i in range(len(criteria_names))]

    for v_name, v_info in data["rating"].items():
        rating_mtx.append(list(v_info.values()))

    data = Data(rating_mtx, criteria, weights, alternative_names, criteria_names)
    dm = closeness.TOPSIS()
    dec = dm.decide(data)

    ranking = {"ranking": dict(zip(alternative_names, dec.rank_.tolist()))}
    print(json.dumps(ranking))


def criteria_preference_to_weight(value):
    weight_ratio = {'1': 0, '2': 0.25, '3': 0.5, '4': 0.75, '5': 1}
    return weight_ratio[value]


if __name__ == '__main__':
    main()
