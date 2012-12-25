import logging
log = logging.getLogger(__name__)

import json
import pyglet

import graphics
import world


def json_to_anim_sets(filename):
    json_data = json.load(open(filename))
    return parse_anim_set_file(json_data)

def parse_anim_set_file(data):
    if data.get('multiple', False):
        parse_multiple_anim_sets(data)
    else:
        parse_single_anim_set(data)

def parse_multiple_anim_sets(data):
    for single_anim_set_data in data['animSets']:
        parse_single_anim_set(single_anim_set_data)

def parse_single_anim_set(data):
    anim_set_name = str(data['animSetName'])
    source = data['source']
    image = pyglet.resource.image(str(source['image']))
    rows = int(source['rows'])
    cols = int(source['cols'])
    parsed_anim_set = graphics.AnimSet(anim_set_name, image, rows, cols)
    for anim in data['anims']:
        anim_key = anim['key']
        frames = [int(f) for f in anim['frames']]
        period = float(anim['period'])
        loop = bool(anim['loop'])
        parsed_anim_set.add_anim(anim_key, frames, period, loop)
    if anim_set_name in world.anim_sets:
        log.warning(W_DUPLICATE_ANIMSET.format(aset=anim_set_name))
    world.anim_sets[anim_set_name] = parsed_anim_set


W_DUPLICATE_ANIMSET = 'AnimSet {aset} already exists; overwriting.'
