import json

import graphics.AnimSet


def json_to_animset_set(filename):
    json_data = json.load(open(filename))
    return parse_animset_set(json_data)


def parse_animset_set(data):
    parsed_animset =
