import json
import os
import pathlib
import sys

from skcriteria import Data, MAX
from skcriteria.madm import closeness


class RankingResponse:
    def __init__(self, alternative_name, rank):
        self.alternative_name = alternative_name
        self.rank = rank


CRITERIA_DEFAULT = {
    "volume": "0",
    "variety": "0",
    "velocity": "0",
    "temporal": "0",
    "one_ts": "0",
    "multiple_ts": "0",
    "categoric": "0",
    "numeric": "0",
    "mixed_categoric_numeric": "0",
    "geospatial": "0",
    "hierarchical": "0",
    "network": "0",
    "distribution": "0",
    "flow": "0",
    "performance": "0",
    "composition": "0",
    "space_efficiency": "0",
    "range": "0",
    "outliers": "0",
    "process_modeling": "0",
    "relationships": "0",
    "comparison": "0",
    "negative_values": "0",
    "number_of_variables": "0",
    "relative_proportions": "0"
}


def main():
    user_criteria_raw = json.loads(sys.argv[1])
    user_criteria = {k: criteria_preference_to_weight(v) for k, v in list(extract_criteria(user_criteria_raw))}
    criteria = update_criteria(user_criteria)
    weights = list(criteria.values())

    with open(os.path.join(pathlib.Path(__file__).parent.absolute(), 'rating_matrix.json')) as f:
        data = json.load(f)

    rating_mtx = []
    alternative_names = data["rating"].keys()
    criteria_names = data["criteria"].keys()
    criteria_impact = [MAX for i in range(len(criteria_names))]

    for v_name, v_info in data["rating"].items():
        rating_mtx.append(list(v_info.values()))

    data = Data(rating_mtx, criteria_impact, weights, alternative_names, criteria_names)
    dm = closeness.TOPSIS()
    dec = dm.decide(data)

    ranking = export_ranking(alternative_names, dec.rank_.tolist())
    print(json.dumps(ranking))


def criteria_preference_to_weight(value):
    weight_ratio = {'True': 1, 'False': 0, '1': 0, '2': 0.25, '3': 0.5, '4': 0.75, '5': 1}
    return weight_ratio[value]


def extract_criteria(source):
    for question_key, question_content in source.items():
        for criteria_key, criteria_value in question_content[0].items():
            yield criteria_key, str(criteria_value)


def export_ranking(alternative_names, ranking):
    obj_list = [RankingResponse(alternative, rank).__dict__ for alternative, rank in zip(alternative_names, ranking)]
    response = {"ranking": obj_list}
    return response


def update_criteria(source):
    criteria = CRITERIA_DEFAULT
    for i in source:
        if i in CRITERIA_DEFAULT:
            CRITERIA_DEFAULT[i] = source[i]
    return criteria


if __name__ == '__main__':
    main()
