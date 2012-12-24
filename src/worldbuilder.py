import json

import logging
log = logging.getLogger(__name__)

import stagebuilder
import animbuilder


def json_to_world(filename):
    json_data = json.load(open(filename))
    return parse_world(json_data)


def parse_world(data):
    parsed_world = world.GameWorld()
    for stage_file in data['stages']:
        parsed_stage = stagebuilder.json_to_stage(stage_file)
        world.add_stage(parsed_stage)
    for anim_file in data['anims']:
        parsed_animset_set = animbuilder.json_to_animset_set(anim_file)
    return parsed_world
