import logging
log = logging.getLogger(__name__)

import world

import json
import stage

from gameobjects.names import CLASSES as CLASS_KEYS

def json_to_stage(json_filename):
    log.info('Parsing Stage file {}'.format(json_filename))
    data = json.load(open(json_filename))
    if data.get('multiple', False):
        parse_multiple_stages(data)
    else:
        parse_single_stage(data)

def parse_multiple_stages(data):
    for single_stage_data in data.get('stages', []):
        parse_single_stage(single_stage_data)

def parse_single_stage(data):
    stage_name = str(data['stageName'])
    parsed_stage = stage.Stage(stage_name)

    bg_color = data.get('backgroundColor', [127,127,127,255])
    parsed_stage.background_color = tuple([int(c) for c in bg_color])

    for section_data in data.get('sections', []):
        parsed_section = parse_section(section_data)
        parsed_stage.add_section(parsed_section)

    if stage_name in world.stages:
        log.warning(W_DUPLICATE_STAGE.format(stg=stage_name))
    world.stages[stage_name] = parsed_stage

def parse_section(data):
    section_name = data.get('sectionName', 'UNNAMED SECTION')

    if data.get('isProcedural', False):
        parsed_section = stage.ProceduralStageSection(section_name)
        if 'proceduralData' in data:
            procedural_data = data['proceduralData']
            parsed_section.seed = procedural_data.get('seed', None)
            if 'propPool' in procedural_data:
                prop_pool = procedural_data['propPool']
                parsed_section.prop_pool = parse_prop_pool(prop_pool)
    else:
        parsed_section = stage.StageSection(section_name)
    static_data = data.get('staticData', {})
    prop_list = static_data.get('propList', [])
    parsed_section.prop_list = parse_prop_list(prop_list)
    actor_list = static_data.get('actorList', [])
    parsed_section.actor_list = parse_actor_list(actor_list)
    return parsed_section

def parse_prop_pool(data):
    for pool_item in data:
        prop_class = parse_class(str(pool_item.get('propClass', '')))
        pool_size = int(pool_item.get('poolSize', 0))
    ##TODO## Actually add stuff.

def parse_prop_list(data):
    parsed_prop_list = []
    for list_item in data:
        prop_class = parse_class(str(list_item.pop('propClass')))
        x = int(list_item.pop('x'))
        y = int(list_item.pop('y'))
        kwargs = list_item
        parsed_prop_list.append(parse_placeholder(prop_class, x, y, **kwargs))
    return parsed_prop_list

def parse_actor_list(data):
    parsed_actor_list = []
    for list_item in data:
        prop_class = parse_class(str(list_item.pop('actorClass')))
        x = int(list_item.pop('x'))
        y = int(list_item.pop('y'))
        is_ambusher = (x < 0)
        kwargs = list_item
        parsed_actor_list.append(parse_placeholder(prop_class, x, y, **kwargs))
    return parsed_actor_list

def parse_class(class_key):
    return CLASS_KEYS[class_key]

def parse_placeholder(cls, x, y, **kwargs):
    placeholder = stage.Placeholder(cls, x, y, **kwargs)
    return placeholder

W_DUPLICATE_STAGE = 'Stage {stg} already exists; overwriting.'
