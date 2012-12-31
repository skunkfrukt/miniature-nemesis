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
    stage_name = str(data.get('name', 'UNNAMED STAGE'))
    parsed_stage = stage.Stage(stage_name)

    seed = data.get('seed', None)
    parsed_stage.seed = seed

    parsed_stage.setup_layers(**data.get('layers'))

    bg_color = data.get('background_color', [127,127,127,255])
    parsed_stage.background_color = tuple(bg_color)

    for section_data in data.get('section_list', []):
        parsed_section = parse_section(section_data)
        parsed_stage.add_section(parsed_section)

    if stage_name in world.stages:
        log.warning(W_DUPLICATE_STAGE.format(stg=stage_name))
    world.stages[stage_name] = parsed_stage

def parse_section(data):
    if data.get('is_procedural', False):
        return parse_procedural_section(data)
    elif data.get('condition', None) is not None:
        pass  ##TODO## Conditional sections.
    else:
        return parse_vanilla_section(data)

def parse_vanilla_section(data):
    section_name = data.get('name', 'UNNAMED SECTION')
    parsed_section = stage.StageSection(section_name)
    prop_list = data.get('prop_list', [])
    parsed_section.prop_list = parse_prop_list(prop_list)
    actor_list = data.get('actor_list', [])
    parsed_actor_list = parse_actor_list(actor_list)
    parsed_section.actor_list = parsed_actor_list['sentinel']
    parsed_section.second_actor_list = parsed_actor_list['pursuer']
    return parsed_section

def parse_procedural_section(data):
    section_name = data.get('name', 'UNNAMED SECTION')
    parsed_section = stage.ProceduralStageSection(section_name)
    prop_pool = parse_prop_pool(data.get('prop_pool', []))
    parsed_section.prop_pool = prop_pool
    return parsed_section

def parse_prop_pool(data):
    pool_dict = {}
    for pool_item in data:
        prop_class = parse_class(str(pool_item.get('cls', '')))
        pool_size = pool_item.get('pool_size', 0)
        pool_dict[prop_class] = pool_size
    return pool_dict

def parse_prop_list(data):
    prop_list = []
    for list_item in data:
        prop_list.append(parse_placeholder(**list_item))
    return prop_list

def parse_actor_list(data):
    actor_list = {'sentinel': [], 'pursuer': []}
    for list_item in data:
        if list_item['x'] < 0:
            actor_list['pursuer'].append(parse_placeholder(**list_item))
        else:
            actor_list['sentinel'].append(parse_placeholder(**list_item))
    return actor_list

def parse_class(class_key):
    return CLASS_KEYS[class_key]

def parse_placeholder(cls, x, y, **kwargs):
    parsed_cls = parse_class(cls)
    placeholder = stage.Placeholder(parsed_cls, x, y, **kwargs)
    return placeholder


W_DUPLICATE_STAGE = 'Stage {stg} already exists; overwriting.'
