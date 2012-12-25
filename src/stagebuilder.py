import logging
log = logging.getLogger(__name__)

import world

import json
import stage

from gameobjects.names import CLASSES as CLASS_KEYS

def json_to_stage(json_filename):
    log.info('Parsing JSON file {}'.format(json_filename))
    parse_stage_file(json.load(open(json_filename)))

def parse_stage_file(data):
    if data.get('multiple', False):
        parse_multiple_stages(data)
    else:
        parse_single_stage(data)

def parse_multiple_stages(data):
    for single_stage_data in data['stages']:
        parse_single_stage(single_stage_data)

def parse_single_stage(data):
    stage_name = str(data['stageName'])
    parsed_stage = stage.Stage(stage_name)

    parsed_stage.backgroundColor = [int(c) for c in data['backgroundColor']]

    for section_data in data['sections']:
        parsed_section = parse_section(section_data)
        parsed_stage.add_section(parsed_section)

    if stage_name in world.stages:
        log.warning("!!! stage key already exists")
    world.stages[stage_name] = parsed_stage
    print world.stages

def parse_section(data):
    if 'sectionName' in data:
        section_name = data['sectionName']
    else:
        section_name = stage.generate_section_name()

    if data.get('isProcedural', False):
        parsed_section = stage.ProceduralStageSection(section_name)
        if 'proceduralData' in data:
            procedural_data = data['proceduralData']
            if 'seed' in procedural_data:
                parsed_section.seed = procedural_data['seed']
            if 'propPool' in procedural_data:
                prop_pool = procedural_data['propPool']
                parsed_section.prop_pool = parse_prop_pool(prop_pool)
    else:
        parsed_section = stage.StageSection(section_name)
    if 'staticData' in data:
        static_data = data['staticData']

    return parsed_section

def parse_prop_pool(data):
    pool = {}
    for key in data:
        try:
            pool[CLASS_KEYS[key]] = data[key]
        except KeyError:
            log.error('Invalid builder name: {}'.format(key))
    return pool

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    stg = json_to_stage('/Users/Namida/Desktop/village.json')
    print('{} sections:'.format(len(stg.sections)))
    for sect in stg.sections:
        print sect.name
