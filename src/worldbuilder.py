import logging
log = logging.getLogger(__name__)

import json
import glob

import stagebuilder
import animbuilder

import world


def json_to_world(filename):
    json_data = json.load(open(filename))
    parse_world(json_data)

def parse_world(data):
    world.constants.update(data['constants'])
    for anim_set_glob in data['animSetFiles']:
        for anim_set_file in glob.glob(anim_set_glob):
            animbuilder.json_to_anim_sets(anim_set_file)
    for stage_glob in data['stageFiles']:
        for stage_file in glob.glob(stage_glob):
            stagebuilder.json_to_stage(stage_file)
