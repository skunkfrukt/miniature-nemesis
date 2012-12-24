import json
import stage_new as stage

import logging
log = logging.getLogger(__name__)

from gameobjects.names import CLASSES as CLASS_KEYS

def json_to_stage(json_filename):
    log.info('Parsing JSON file {}'.format(json_filename))
    return parse_stage(json.load(open(json_filename)))

def parse_stage(data):
    stage_name = data['stageName']
    log.info('Parsing stage {}'.format(stage_name))

    parsed_stage = stage.Stage(stage_name)
    for section_data in data['sections']:
        parsed_stage.append_section(parse_section(section_data, parsed_stage))

    return parsed_stage

def parse_section(data, parent_stage):
    parent_name = parent_stage.name
    if 'sectionName' in data:
        section_name = data['sectionName']
    else:
        section_index = len(parent_stage.sections)
        section_name = '{}#{}'.format(parent_name, section_index)
    log.info('Parsing section {}.{}'.format(parent_name, section_name))

    if 'isProcedural' in data and data['isProcedural']:
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
