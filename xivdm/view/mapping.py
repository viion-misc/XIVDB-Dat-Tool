import logging
import re

from xivdm.language import get_language_name

def simple_mapping(exd_name, mapping_function):
    def generated_function(exd_manager):
        data = exd_manager.get_category(exd_name).get_data()
        data_ln = data[list(data.keys())[0]]
        return {
            id: mapping_function(data, id, v) for id, v in data_ln.items()
        }
    return generated_function

def string(data, id, member_id, enable_conditions = False):
    return {
        'enable_conditions': enable_conditions,
        'type': 'string',
        'ln': {
            get_language_name(language): data[language][id][member_id] for language in data.keys()
        }
    }

def ref(view_name, value):
    print('ref', view_name, value)
    return {
        'type': 'view_ref',
        'view': view_name,
        'id': value
    }

def full_ref(view_name, value):
    print('full_ref', view_name, value)
    return {
        'type': 'full_view_ref',
        'view': view_name,
        'id': value
    }

def name_ref(view_name, value):
    print('name_ref')
    return {
        'type': 'view_name_ref',
        'view': view_name,
        'name': value
    }

def unmapped(index_list, v):
    return {
        index: repr(v[index]) for index in index_list
    }

def food_stat(stat_type, percent_value, max_value):
    print('food_stat', stat_type, percent_value, max_value)
    return {
        'stat': ref('base_params', stat_type),
        'percent_value': percent_value,
        'max_value': max_value
    }

def stat(stat_type, stat_value):
    print('stat', stat_type, stat_value)
    return {
        'stat': ref('base_params', stat_type),
        'value': stat_value
    }

def hq_stat(stat_type, stat_value, hq_stat_value):
    print('stat', stat_type, stat_value)
    return_value = stat(stat_type, stat_value)
    return_value.update({
        'hq_value': stat_value + hq_stat_value
    })
    return return_value

def mat(item_id, quantity):
    print('mat')
    return {
        'item': ref('items', item_id),
        'quantity': quantity
    }

def crystals(crystal, amount):
    return {
        'crystal':     full_ref('craft_crystal_type', crystal),
        'amount':      amount
    }

def leve_stuff_range(return_dict, value):
    view_name = None

    if value == 0:
        pass
    elif value >= 917504:
        view_name = 'craft_leves'
    elif value >= 196608:
        view_name = 'company_leves'
    elif value >= 131072:
        view_name = 'gathering_leves'
    elif value >= 65536:
        view_name = 'battle_leves'
    elif value > 0:
        raise Exception('Unmapped id range: %d' % value)
    if view_name:
        return_dict[view_name] = ref(view_name, value)

def npc_stuff_range(return_dict, value):
    view_name = None

    if value == 0:
        pass
    elif value == 1835009:
        pass
    elif value > 1769484:
        logging.info('Unmapped id range: %d' % value)
    elif value >= 1769472:
        view_name = 'special_shops'
    elif value >= 1703936:
        view_name = 'stories'
    elif value >= 1572870:
        logging.info('Unmapped id range: %d' % value)
    elif value >= 1572864:
        view_name = 'guild_order_officers'
    elif value >= 1507328:
        view_name = 'guild_order_guides'
    elif value >= 1441792:
        view_name = 'gcshops'
    elif value >= 1179648:
        view_name = 'chocobo_taxi_stands'
    elif value >= 917504:
        view_name = 'craft_leves'
    elif value >= 720896:
        view_name = 'custom_talks'
    elif value >= 589824:
        view_name = 'default_talks'
    elif value >= 393216:
        view_name = 'guildleve_assignments'
    elif value >= 262144:
        view_name = 'shops'
    elif value >= 131072:
        view_name = 'gathering_leves'
    elif value >= 65536:
        #view_name = 'quests'
        pass #ignoring quests as it's too big
    elif value > 0:
        pass
    if view_name:
        return_dict.setdefault(view_name, []).append(full_ref(view_name, value))

def level_stuff_range(return_dict, value):
    view_name = None

    if value == 5000000:
        logging.info('Unmapped id range: %d' % value)
    elif value >= 2000000:
        view_name = 'eobjs'
    elif value >= 1000000:
        view_name = 'enpc_residents'
    elif value >= 30000:
        view_name = 'gathering_points'
    elif 30000 >= value > 0:
        logging.info('Unmapped id range BGMSituation: %d' % value)
    elif value > 0:
        raise Exception('Unmapped id range: %d' % value)

    if view_name:
        return_dict[view_name] = full_ref(view_name, value)

def gathering_items_range(return_dict, value):
    view_name = None

    if value < 2000000:
         view_name = 'items'
    elif value >= 2000000:
         view_name = 'event_items'
    elif value >= 3000000:
        raise Exception('Unmapped id range: %d' % value)

    if view_name:
        return_dict[view_name] = ref(view_name, value)

#### MAPPINGS ####
def achievements(data, id, v):
    print('achievements')
    return {
        'name':         string(data, id, 0),
        'description':  string(data, id, 1),
        'item':         ref('items', v[2]),
        'icon':         v[13],
        'category':     ref('achievement_categories', v[15]),


        'title':        ref('titles', v[12]),


        'points':       v[16],

        'unmapped_values':      unmapped(
            list(range(4, 12))
            + list(range(13, 16))
            + [17], v)
    }

def achievement_categories(data, id, v):
    print('achievement_categories')
    return {
        'name':     string(data, id, 0),
        'kind':     ref('achievement_kinds', v[1])
    }

def achievement_kinds(data, id, v):
    print('achievement_kinds')
    return {
        'name': string(data, id, 0)
    }

def action_categories(data, id, v):
    print('action_categories')
    return {
        'name': string(data, id, 0)
    }

def actions(data, id, v):
    print('actions')
    return {
        'name':                 string(data, id, 0),
        'description':          string(data, id, 1, enable_conditions = True),
        'icon':                 v[3],

        'resource_value':       v[5],

        'cast':                 v[9],
        'recast':               v[10],

        'category':             ref('action_categories', v[13]),

        'level':                v[16],
        'radius':               v[19],

        'resource_type':        v[21],

        'class_job_category':   ref('class_job_categories', v[25]),
        'class_job':            ref('class_jobs', v[29]),

        #'pvp':               	v[47],
        'range':                v[30],
        'attack_type':          ref('attack_types', v[32]),

        'unmapped_values':      unmapped(
            [3, 5, 6, 7, 10, 11, 13, 14]
            + list(range(18, 24))
            + [25]
            + list(range(29, 34)), v)
    }

def addons(data, id, v):
    print('addons')
    return {
        'name': string(data, id, 0)
    }

def attack_types(data, id, v):
    print('attack_types')
    return {
        'name': string(data, id, 0)
    }

def battle_leves(data, id, v):
    print('battle_leves')
    return {
        'mob': v[8],
        'mob_count': v[9],

        'unmapped_values':  unmapped(
            list(range(0, 8))
            + list(range(10, 183)), v)
    }

def balloons(data, id, v):
    print('balloons')
    return {
        'text': string(data, id, 0),

        'unmapped_values':  unmapped(
            [1], v)
    }

def base_params(data, id, v):
    print('base_params')
    return {
        'name'          : string(data, id, 0),
        'description'   : string(data, id, 1),
        'unmapped_values':      unmapped(
            list(range(1, 32)), v)
    }

#def behest_rewards(data, id, v):
#    return {
#        'items': [ref('items', v[i]) for i in range(1, 4)],
#
#        'level': v[5],
#
#        'unmapped_values':      unmapped(
#            [0]
#            + [4]
#            + [6], v)
#    }

def bnpc_names(exd_manager):
    print('bnpc_names')
    data = exd_manager.get_category('BNpcName').get_data()
    data_ln = data[list(data.keys())[0]]

    bnb_data = exd_manager.get_category('BNpcBase').get_data()
    bnpc_bases = bnb_data[list(bnb_data.keys())[0]]

    return_dict = {}
    for id, v in data_ln.items():
        return_dict[id] = {
            'name':                 string(data, id, 0),
            'plural_name':          string(data, id, 1),
            'unmapped_values':      unmapped(
            list(range(2, 7)), v)
        }
        if id in bnpc_bases:
            return_dict[id].update({
                'infos':                full_ref('bnpc_bases', id)
            })
    return return_dict

def bnpc_bases(data, id, v):
    print('bnpc_bases')
    return {
        'model':                full_ref('model_chara', v[3]),
        'unmapped_values':      unmapped(
            list(range(0, 3))
                + list(range(4,13)), v)
    }

def chain_bonuses(data, id, v):
    print('chain_bonuses')
    return {
        'exp_percent':  v[0],
        'timer':        v[1]
    }

def chocobo_taxi_stands(data, id, v):
    print('chocobo_taxi_stands')
    return {
        'name':                 string(data, id, 0),

        'unmapped_values':      unmapped(
            list(range(1, 9)), v)
    }

def class_job_categories(data, id, v):
    print('class_job_categories')
    return {
        'name':                     string(data, id, 0),
        'class_job_restrictions':   [v[index] for index in range(1, 35)]
    }

def class_jobs(data, id, v):
    print('class_jobs')
    return {
        'name':                 string(data, id, 0),
        'acronym':              string(data, id, 1),

        'caps_name':            string(data, id, 4),
        'class_job_category':   ref('class_job_categories', v[30]),

        'base_class':           ref('class_jobs', v[31]),
        'is_job':               0,


        'unmapped_values':  unmapped(list(range(0, 32)), v)
    }

def companions(data, id, v):
    print('companions')
    return {
        'name':                 string(data, id, 0),
        'plural_name':          string(data, id, 1),
		'description':			string(data, id, 2),

        'icon':                 v[14],

        '_':      unmapped(list(range(0, 21)), v)
    }

def complete_journals(data, id, v):
    print('complete_journals')
    return {
        'name':             string(data, id, 0),

        'header_image':     v[3],

        'unmapped_values':      unmapped(
            [1, 2]
            + list(range(4, 6)), v)
    }

def completions(data, id, v):
    print('completions')
    return {
        'name':                 string(data, id, 0),

        'unmapped_values':      unmapped(
            list(range(1, 4)), v)
    }

def company_leves(data, id, v):
    print('company_leves')
    return {
        'unmapped_values':  unmapped(
            list(range(0, 178)), v)
    }

def craft_crystal_type(data, id, v):
    print('items')
    return {
        'item':                 ref('items', v[0])
    }

def craft_leves(data, id, v):
    print('craft_leves')
    return {
        'unmapped_values':      unmapped(
            list(range(0, 15)), v)
    }

def craft_action(data, id, v):
    print('craft_action')
    return {
        'name':                 string(data, id, 0),
        'description':          string(data, id, 1),

        'icon':                 v[13],
        'class_job':            ref('class_jobs', v[17]),
        'class_job_category':   ref('class_job_categories', v[14]),
        'level':                v[15],
        'cp':                   v[16],

        'unmapped_values':      unmapped(
            list(range(2, 12)), v)
    }

def craft_types(data, id, v):
    print('craft_types')
    return {
        'name':                 string(data, id, 0),

        'unmapped_values':      unmapped(
            [1, 2], v)
    }

def custom_talks(data, id, v):
    print('custom_talks')
    return {
        'unmapped_values':      unmapped(
            list(range(0, 62)), v)
    }

def default_talks(data, id, v):
    print('default_talks')
    return {
        'unmapped_values':      unmapped(
            list(range(0, 21)), v)
    }

def emotes(data, id, v):
    print('emotes')
    return {
        'name':         string(data, id, 0),
        'icon':         v[10],

        'unmapped_values':      unmapped(
            list(range(1, 10))
            + list(range(11, 13)), v)
    }

def enpc_residents(data, id, v):
    print('enpc_residents')
    return {
        'name':                 string(data, id, 0),
        'name_bis':             string(data, id, 1),
        'title':                string(data, id, 2),

        'infos':                full_ref('enpc_bases', id),

        'unmapped_values':      unmapped(
            list(range(3, 10)), v)
    }

def enpc_bases(data, id, v):
    print('enpc_bases')
    return_dict = {
        'model':            v[32],
        'unmapped_values':      unmapped(
            [30, 31]
            + list(range(33, 63))
            + list(range(65, 91)), v)
    }
    for i in range(30):
        npc_stuff_range(return_dict, v[i])
    return return_dict

def eobjs(data, id, v):
    print('eobjs')
    return {
        'name':                 string(data, id, 0),
        'description':          string(data, id, 1),

        'unmapped_values':          unmapped(
            list(range(2, 12)), v)
    }

def errors(data, id, v):
    print('errors')
    return {
        'name':                 string(data, id, 0)
    }

def event_items(data, id, v):
    print('event_items')
    return {
        'name':                 string(data, id, 0),
        'name_plural':          string(data, id, 1),
        'description':          string(data, id, 2),
        'description_bis':      string(data, id, 3),

        'quest':                ref('quests', v[10]),


        'unmapped_values':          unmapped(
            list(range(4, 10))
            + list(range(11, 15)), v)
    }

def fates(data, id, v):
    print('fates')
    return {
        '_all': unmapped(list(range(0, 24)), v),

        'name':                 string(data, id, 0),
        'description':          string(data, id, 1),
        'special_text':         [string(data, id, i) for i in range(2, 5)],

        'position':             full_ref('levels', v[9]),

        'icon':                 v[11],

        'level':                v[20],


        'unmapped_values':          unmapped(
            list(range(5, 9))
            + [10]
            + list(range(12, 18))
            + list(range(19, 24)), v)
    }

def gathering_type(data, id, v):
    print('gathering_type')
    return {
        'name':          string(data, id, 0),
        'unmapped_values':          unmapped(
            [1], v)
    }

def gathering_points(exd_manager):
    print('gathering_points _ prep maps')
    data = exd_manager.get_category('GatheringPoint').get_data()
    data_ln = data[list(data.keys())[0]]
    return_dict = {}

    maps_data = exd_manager.get_category('Map').get_data()
    maps_data_in = maps_data[list(maps_data.keys())[0]]

    maps_search_dict = {
        m_data[7]: m_id for m_id, m_data in maps_data_in.items()
    }

    print(maps_search_dict);

    print('gathering_points')
    for id, v in data_ln.items():
        return_dict[id] = {
            'base':                 full_ref('gathering_points_base', v[0]),

            #'req':                  ref('gathering_condition', v[1]),
            #'bonus':                ref('gathering_bonus_type', v[2]),

            #'map':                  ref('maps', maps_search_dict[v[3]]),

            'req_max':              v[4],
            'bonus_amount':         v[5],

            'unmapped_values':          unmapped(
                list(range(0, 7)), v)
        }
    return return_dict

def gathering_points_base(data, id, v):
    print('gathering_points_base')
    return {
        'node_name':    full_ref('gathering_type', v[0]),
        'items':        [full_ref('gathering_items', v[i]) for i in range(1, 9)],
        'level':        v[9],

        'unmapped_values':          unmapped(
            list(range(10, 11)), v)
    }

def gathering_items(data, id, v):
    print('gathering_items')
    return_dict = {
        'gathering_level': v[1]
    }
    gathering_items_range(return_dict, v[0])
    return return_dict

def gathering_points_name(data, id, v):
    print('gathering_points_name')
    return {
        'name':          string(data, id, 0),
        'unmapped_values':          unmapped(
            list(range(1, 8)), v)
    }

def gathering_leves(data, id, v):
    print('gathering_leves')
    return {
        'unmapped_values':          unmapped(
            list(range(0, 19)), v)
    }

def gathering_condition(data, id, v):
    print('gathering_condition')
    return {
        'name':          string(data, id, 0)
    }

def gathering_bonus_type(data, id, v):
    print('gathering_bonus_type')
    return {
        'name':          string(data, id, 0)
    }

def gcrank(data, id, v):
    print('gcrank')
    return {
        'name':                 string(data, id, 0),
        'plural':               string(data, id, 1),

        'unmapped_values':          unmapped(
            list(range(2, 10)), v)
    }

def gcshops(data, id, v):
    print('gcshops')
    return {
        'unmapped_values':          unmapped(
            list(range(0, 2)), v)
    }

def gcshop_item_categories(data, id, v):
    print('gcshop_item_categories')
    return {
        'name':                 string(data, id, 0)
    }

def general_actions(data, id, v):
    print('general_actions')
    return {
        'name':                 string(data, id, 0),
        'description':          string(data, id, 1),

        'unmapped_values':      unmapped(
            [2], v)
    }

def grand_companies(data, id, v):
    print('grand_companies')
    return {
        'name':                 string(data, id, 0),

        'unmapped_values':      unmapped(
            list(range(1, 10)), v)
    }

def grand_company_ranks(data, id, v):
    print('grand_company_ranks')
    return {
        'rank':                 v[8],
        'max_seals':            v[9],

        'unmapped_values':      unmapped(
            list(range(0, 8))
            + [10], v)
    }

def grand_company_seal_shop_items(data, id, v):
    print('grand_company_seal_shop_items')
    return {
        'seal_cost':            v[1],
        'item':                 ref('items', v[2]),

        'category':             ref('gcshop_item_categories', v[4]),

        'unmapped_values':      unmapped(
            [0]
            + [3], v)
    }

def guardian_deities(data, id, v):
    print('guardian_deities')
    return {
        'name':                 string(data, id, 0),
        'description':          string(data, id, 1),
        'icon':                 v[2],
    }

def guild_order_guides(data, id, v):
    print('guild_order_guides')
    return {
        'unmapped_values':      unmapped(
            list(range(0, 6)), v)
    }

def guild_order_officers(data, id, v):
    print('guild_order_officers')
    return {
        'unmapped_values':      unmapped(
            list(range(0, 6)), v)
    }

def guildleve_assignments(data, id, v):
    print('guildleve_assignments')
    return {
        'unmapped_values':      unmapped(
            list(range(0, 5)), v)
    }

def instance_contents(exd_manager):
    print('instance_contents')
    data = exd_manager.get_category('InstanceContent').get_data()
    data_ln = data[list(data.keys())[0]]
    return_dict = {}
    for id, v in data_ln.items():
        return_dict[id] = {
            #'_': unmapped(list(range(0, 47), v),

            'name':                 string(data, id, 0),
            'lore':                 full_ref('content_description', id),

            'banner':               v[36],

            'todo_start':           v[40],
            'todo_end':             v[41],

            'time':                 v[43],

            'type':                 full_ref('instance_content_type', v[49]),
            'minlvl':               v[53],
            'synclvl':              v[54],

            'playercount':          v[55],



            #'unmapped_values':      unmapped(
            #    list(range(2, 20))
            #    + list(range(21, 24))
            #    + [26, 28, 29, 30, 32, 33], v)
        }
        #if v[48] > 10000:
            #return_dict[id].update({
                #'issuenpc': ref('enpc_residents', v[49])
            #})
    return return_dict

def instance_content_textdata(data, id, v):
    print('instance_content_textdata')
    return {
        'text':               string(data, id, 0)
    }

def content_type(data, id, v):
    print('content_type')
    return {
        'name': string(data, id, 0),
        'icon': v[1],
    }

def content_description(data, id, v):
    print('content_description')
    return {
        'lore': string(data, id, 0)
    }

def instance_content_type(data, id, v):
    print('instance_content_type')
    return {
        #'icon':                 v[0],

        'sort_key':             v[0],
        'content_type':         full_ref('content_type', v[2]),

        #'unmapped_values':      unmapped(
        #   list(range(2, 5)), v)
    }

def item_actions(data, id, v):
    print('item_actions')
    action_type = v[1]
    if action_type in [48, 49]:
        return {
            'item_food':    full_ref('item_foods', v[2]),
            'duration':     v[3],
        }
    else:
        return {
            'percentage':    v[1],
            'value_max':     v[2],
         }

def item_categories(data, id, v):
    print('item_categories')
    return {
        'name': string(data, id, 0)
    }

def item_foods(data, id, v):
    print('item_foods', id)
    return {
        'stats': [                  food_stat(v[0], v[3], v[6]),
                                    food_stat(v[1], v[4], v[7]),
                                    food_stat(v[2], v[5], v[8])],

        'unmapped_values':          unmapped(
            list(range(9, 18)), v)
    }

def item_search_categories(data, id, v):
    print('item_search_categories')
    return {
        'name': string(data, id, 0),
        'icon': v[1],

        'unmapped_values':  unmapped(
            list(range(2, 5)), v)
    }

def item_search_class_filters(data, id, v):
    print('item_search_class_filters')
    return {
        'name': string(data, id, 0),

        'unmapped_values':  unmapped(
             [1], v)
    }

def item_special_bonuses(data, id, v):
    print('item_special_bonuses')
    return {
        'name': string(data, id, 0),
    }

def item_series(data, id, v):
    print('item_series')
    return {
        'name': string(data, id, 0),
    }

def item_ui_categories(data, id, v):
    print('item_ui_categories')
    return {
        'name': string(data, id, 0),
        'icon': v[1]
    }

def items(data, id, v):
    #if id != 1663:
    #    return {}

    print('items')
    return {
            #'_': unmapped(list(range(0, 82)), v),

            'noon':                     string(data, id, 0),
            'plural_noon':              string(data, id, 1),
            'description':              string(data, id, 2),
            'name':                     string(data, id, 3),

            'model':                    v[10],

            'number_per_stack':         v[12],

            'buy_price':                v[15],

            'stats':                    [hq_stat(v[i], v[i-16], v[i+25]) for i in range(49, 53)] +
                                        [stat(v[i], v[i-16]) for i in range(53, 55)],

            'set_stats': {
                                        'special_bonus':    ref('item_special_bonuses', v[55]),
                                        'stats':            [stat(v[i], v[i+16]) for i in range(56, 62)]
            },

            'repair_class_job':         ref('class_jobs',                   v[62]),
            'repair_material':          ref('items',                        v[18]),
            'icon':                     v[20],

            'base_stats': [             hq_stat(12, v[22], v[72]),  # physical_damage
                                        hq_stat(13, v[23], v[73]),  # magic_damage
                                        stat(14, v[24]),  # delay
                                        stat(17, v[25]),  # block_rate
                                        stat(18, v[26]),  # block
                                        hq_stat(21, v[27], v[72]),  # defense
                                        hq_stat(24, v[28], v[73])], # magic_defense

            'item_action':              full_ref('item_actions',                   v[30]),

            'item_level':               v[39],
            'class_job_level':          v[40],

            'item_ui_category':         ref('item_ui_categories',           v[43]),

            'rarity':                   v[45],

            'materia_slots':            v[47],

            #'item_search_class_filter': ref('item_search_class_filters',    v[62]),
            #'class_job_categories':     ref('class_job_categories',         v[22]),


            'class_job_category':       ref('class_job_categories',         v[67]),
            'grand_company':            ref('grand_companies',              v[68]),

            #'set_name':                 ref('item_series',                  v[69]),


            'is_untradable':            v[78],
            'is_unique':                v[80],

            #'race_restrictions':        [v[i] for i in range(82, 85)],
            #'gender_restrictions':      [v[i] for i in range(90, 92)]
    }

def journal_genre(data, id , v):
    print('journal_genre')
    return {
        'name':         string(data, id, 0),
        'icon':         v[1],
        'cat':          ref('journal_cat', v[2])
    }

def journal_cat(data, id , v):
    print('journal_cat')
    return {
        'name':         string(data, id, 0)
    }

def leve_reward_item_groups(data, id, v):
    print('leve_reward_item_groups')
    return {
        'items':  [mat(v[i], v[i+9]) for i in range(0, 8)]
    }

def leve_reward_items(data, id, v):
    print('leve_reward_item_groups')
    return {
        'leve_reward_item_groups':  [ref('leve_reward_item_groups', v[i]) for i in range(0, 7)]
    }

def leves(data, id, v):
    print('leves')
    return_dict = {
        'name':                 string(data, id, 0),
        'description':          string(data, id, 1),

        'reward_item':          full_ref('leve_reward_items', v[5]),

        'start_npc':            full_ref('levels', v[7]),
        'start_position':       full_ref('levels', v[8]),
        'client':               ref('leve_clients', v[9]),

        'placename':            ref('place_names', v[13]),
        'genre':                v[15],

        'guildleve_eorzean':    v[18],
        'guildleve_banner':     v[20],

        'level':                v[21],
        'timelimit':            v[23],
        'leve_fx':              v[25],

        'unmapped_values':      unmapped(
            [2, 3]
            + [5, 6]
            + list(range(10, 13))
            + list(range(14, 17))
            + [19]
            + [21]
            + list(range(23, 27)), v)
    }
    leve_stuff_range(return_dict, v[19])
    return return_dict

def leves_vfx(data, id , v):
    print('leves_vfx')
    return {
        'file':         string(data, id, 0),
        'image':        v[1]
    }

def levels(data, id, v):
    print('levels')
    return_dict = {
        'x':                    v[0],
        'y':                    v[2],

        'map':                  full_ref('maps',v[6]),

        'place_name':           ref('place_names', v[8]),

        'unmapped_values':      unmapped(
            [1]
            + list(range(3, 5))
            + [7]
            + [9], v)
    }
    level_stuff_range(return_dict, v[5])
    return return_dict

def param_grow(data, id, v):
    print('param_grow')
    return {
        'exp':               v[0],

        'unmapped_values':      unmapped(
            list(range(1, 12)), v)
    }

def pet_action(data, id, v):
    print('pet_action')
    return {
        'name':               string(data, id, 0),
        'description':        string(data, id, 1, enable_conditions = True),
        'pet':                v[4],
        'icon':               v[2],

        'unmapped_values':      unmapped(
            list(range(3, 6)), v)
    }

def leve_clients(data, id, v):
    print('leve_clients')
    return {
        'name':                 string(data, id, 0)
    }

def maps(data, id, v):
    print('maps')
    return {
        'id':                   v[0].decode('utf-8'),
        'scale':                v[13],
        'floor':                v[12],

        'zone':                 full_ref('place_names', v[3]),
        'region':               full_ref('place_names', v[4]),

        'pseudo_link':          v[6], #used to link gathering points to maps and maybe others

        'unmapped_values':      unmapped(list(range(0, 14)), v)
    }

def markers(data, id, v):
    print('markers')
    return {
        'name':                 string(data, id, 0),
        'icon':                 v[1]
    }

def mounts(data, id, v):
    print('mounts')
    return {
        'name':                 string(data, id, 0),
        'desc1':                string(data, id, 2),
        'desc2':                string(data, id, 3),
        'desc3':                string(data, id, 4),
        'icon':                 v[36],
        '_':                    unmapped(list(range(0, 42)), v)
    }

def model_chara(data, id, v):
    print('model_chara')
    return {
        'm_value':              v[0],
        'b_value':              v[3],
        'unmapped_values':      unmapped(
            list(range(1, 3))
            + list(range(4, 6)), v)
    }

def materias(data, id, v):
    print('materias')
    return {
        'mat':                  [{
                                    'item': ref('items', v[i]),
                                    'value': v[i+11]
                                } for i in range(5)],
        'attribute':            ref('base_params', v[10]),

        'unmapped_values':      unmapped(
            list(range(5, 10))
            + list(range(16, 21)), v)
    }

def monster_notes(data, id, v):
    print('monster_notes')
    return {
        'name':                 string(data, id, 0),
        'exp':                  v[1],
        'npcs':                 [full_ref('monster_notes_target', v[i]) for i in range(2, 6)],

        'npc_quantities':       [v[i] for i in range(6, 10)],

        'unmapped_values':      unmapped(
            [5]
            + [9], v)
    }

def monster_notes_target(data,id,v):
    print('monster_notes_target')
    return {
        'mob':                 ref('bnpc_names', v[1]),
        'icon':                 v[0],

        'unmapped_values':      unmapped(
            list(range(2, 9)), v)
    }

def npc_yells(data, id, v):
    print('npc_yells')
    return {
        'name':                 string(data, id, 0),

        'unmapped_values':      unmapped(
            list(range(1, 5)), v)
    }


def online_statuses(data, id, v):
    print('online_statuses')
    return {
        'name':                 string(data, id, 0),
        'icon':                 v[1]
    }

def place_names(data, id, v):
    print('place_names')
    return {
        'name':                 string(data, id, 0),

        'unmapped_values':      unmapped(
            list(range(1, 10)), v)
    }

QUEST_STEP_RE = re.compile(r'^SEQ_(?P<step_number>\d+)_(?P<step_action>.*)$')
QUEST_ACTOR_RE = re.compile(r'^ACTOR(\d+)$')

def quest_steps(labels, ids):
    print('quest_steps')
    result_steps = []
    actor_dict = {}
    for index, label in enumerate(labels):
        label_utf8 = label.decode('utf-8')

        actor_match_result = QUEST_ACTOR_RE.match(label_utf8)
        if actor_match_result:
            if ids[index] >= 10000:
                actor_dict[label_utf8] = ids[index]
        else:
            step_match_result = QUEST_STEP_RE.match(label_utf8)
            if step_match_result:
                step_action = step_match_result.group('step_action')
                actor_match_result = QUEST_ACTOR_RE.match(step_action)
                if actor_match_result:
                    if step_action in actor_dict:
                        result_steps.append({
                            'step': int(step_match_result.group('step_number')),
                            'value': ref('enpc_residents', actor_dict[step_action])
                        })
    return result_steps

def quests(exd_manager):
    print('quests')
    data = exd_manager.get_category('Quest').get_data()
    data_ln = data[list(data.keys())[0]]
    return_dict = {}

    param_grow_data = exd_manager.get_category('ParamGrow').get_data()
    param_grow_data_ln = param_grow_data[list(param_grow_data.keys())[0]]

    complete_journal_data = exd_manager.get_category('CompleteJournal').get_data()
    complete_journal_data_in = complete_journal_data[list(complete_journal_data.keys())[0]]

    complete_journal_search_dict = {
        cj_data[0]: cj_id for cj_id, cj_data in complete_journal_data_in.items()
    }


    for id, v in data_ln.items():
        print('quests (loop)', id)
        return_dict[id] = {
            'name':                 string(data, id, 0),

            'vars':                 [[v[i].decode('utf-8'), v[i+1]] for i in range(1, 51, 2)],

            #'structs':              [v[i:i+15] for i in range(116, 1048, 15)],

            'gil_reward':           v[917],

            'main_rewards':         [mat(v[i], v[i+24]) for i in range(918, 921)],
            'optional_rewards':     [mat(v[i], v[i+31]) for i in range(924, 929)],

            'base_exp':             v[932],

            'prerequisit_quests':   [ref('quests', v[i]) for i in range(982, 985)],

            'start':                v[990],
            'end':                  v[991],
            'banner':               v[992],

            #'level':                (v[985] if v[985] != 0xFFFF else 0) + v[993],
            'level':                v[995],

            'class_job':            ref('class_jobs', v[1022]),
            'genre':                v[1024],



 #          'name':                 string(data, id, 0),
 #
 #          'level':                (v[1165] if v[1165] != 0xFFFF else 0) + v[1170],
 #
 #          'class':                v[1176],
 #
 #          'chain_quests':         [ref('quests', v[i]) for i in range(1157, 1160)],
 #
 #          'steps':                quest_steps([v[i] for i in range(1, 100, 2)], [v[i] for i in range(2, 101, 2)]),
 #
 #          'base_exp':             v[1124],
 #          'gil_reward':           v[1109],
 #
 #          'main_rewards':         [mat(v[i], v[i+3]) for i in range(1127, 1130)]
 #                                  + [mat(v[i], v[i+23]) for i in range(1110, 1113)],
 #
 #          'optional_rewards':     [mat(v[i], v[i+32]) for i in range(1113, 1118)],
        }

        # If exp_reward breaks, ensure the level and the base_exp are correct,
        # also some entries might have values which mean other things because
        # SE is stupid, so the below print will show values way to high, such
        # as a level being massively over 50.
        print("key", id);
        print("level", return_dict[id]['level']);
        print("base_exp", return_dict[id]['base_exp']);

        # If the level is above 50, we will just reset it..
        if return_dict[id]['level'] > 50:
            return_dict[id].update({ 'level': 50 })


        return_dict[id].update({
            'exp_reward': (return_dict[id]['base_exp'] *
                (param_grow_data_ln[return_dict[id]['level']][13] * (45 + 5 * return_dict[id]['level']))) // 100
        })
 #
 #      #Lookup complete journal by name and extract genre id (v[4])
 #      if complete_journal_data_in[complete_journal_search_dict[v[0]]][2] <= 49: #TEMP FIX UNTIL SE FIXES THEIR SHIT
 #          return_dict[id].update({
 #              'quest_genre': ref('journal_genre', complete_journal_data_in[complete_journal_search_dict[v[0]]][2])
 #          })
 #
 #      #Check second class column if first one is empty SERIOUSLY SE FIX YOUR SHIT
 #      if v[1176] == 0:
 #          return_dict[id].update({
 #              'class': v[1179]
 #          })
 #
        if v[981] != b'':
            quest_base_exd_name = v[981].decode('utf-8')
            quest_exd_name = 'quest/%s/%s' % (quest_base_exd_name[10:13], quest_base_exd_name)
            quest_exd_data = exd_manager.get_category(quest_exd_name).get_data()
            quest_exd_data_ln = quest_exd_data[list(quest_exd_data.keys())[0]]
            return_dict[id].update({
                'texts': {
                    quest_exd_data_ln[quest_exd_id][0].decode('utf-8'): {
                        'enable_conditions': False,
                        'type': 'string',
                        'ln': {
                            get_language_name(language): quest_exd_data[language][quest_exd_id][1] for language in quest_exd_data.keys()
                        }
                    } for quest_exd_id in sorted(quest_exd_data_ln.keys())
                }
            })

    return return_dict

def roles(data, id , v):
    print('roles')
    return {
        'name':                 string(data, id, 0),
        'abbr':                 string(data, id, 1),

        'unmapped_values':      unmapped(
            [2], v)
    }

def shops(data, id , v):
    print('shops')
    return {
        'name':                 string(data, id, 0),
        #'icon':                 v[1],
        'items':               [full_ref('shop_items', v[i]) for i in range(5, 45)],

        'unmapped_values':      unmapped(
            [42], v)
    }

def shop_items(data, id , v):
    print('shop_items')
    return {
        'item':                 ref('items', v[3]),

        'unmapped_values':      unmapped(
            list(range(0, 3))
            + list(range(4, 6)), v)
    }

def special_shops(data, id , v):
    print('special_shops')
    return {
        #'name':                 string(data, id, 0)
#
#                                        # Mat == item_id, qauntity
#        'items':                [{
#                                    #'_' : unmapped(list(range(1, 19)), v),
#                                    'out': mat(v[i+6], v[i+1]),##
#
#                                    'in': [mat(v[i+10], v[i+2]),
#                                           mat(v[i+11], v[i+3])]}#
#
#                                           for i in range(1, 1920, 25)]
    }

def statuses(data, id, v):
    print('statuses')
    return {
        'name':             string(data, id, 0),
        'description':      string(data, id, 1),
        'icon':             v[2],
        'company_action':   v[11],

        'unmapped_values':      unmapped(
            list(range(3, 12)), v)
    }

def recipes(data, id, v):
    print('recipes')
    return {
        'craft_type':   ref('craft_types', v[0]),
        'result':       mat(v[1], v[25]),

        'mats':         [mat(v[i], v[i+24]) for i in range(2, 10)],
        'crystals':     [crystals(v[i], v[i+24]) for i in range(10, 12)],
        'level':        v[24],
        'required':     v[20],
        'affinity':     v[36],

        'unmapped_values':      unmapped(
            list(range(20, 31)), v)
    }

def stories(data, id, v):
    print('stories')
    return {
        #'story_name':   v[1310].decode('utf-8')
    }

def text_commands(data, id , v):
    print('text_commands')
    return {
        'description':          string(data, id, 0),

        'name':                 string(data, id, 3),
        'small_name':           string(data, id, 4),

        'unmapped_values':      unmapped(
            list(range(1, 3))
            + list(range(5, 11)), v)
    }

def titles(data, id , v):
    print('titles')
    return {
        'name':                 string(data, id, 0),
        'plural_name':          string(data, id, 1),
        'unmapped_values':      unmapped(
            [2], v)
    }

def towns(data, id , v):
    print('towns')
    return {
        'name':            string(data, id, 0),
        'screen':          v[1]
    }

def traits(data, id, v):
    print('traits')
    return {
        'name':         string(data, id, 0),
        'description':  string(data, id, 1),
        'icon':         v[2],
        'class_job':    ref('class_jobs', v[5]),
        'level':        v[6],
        'pvp':          v[9],

        'unmapped_values':      unmapped(
            [3, 4] + [7, 8], v)
    }

def weathers(data, id , v):
    print('weathers')
    return {
        'name':          string(data, id, 0),
        'desc':          string(data, id, 1),
        'icon':          v[2]
    }

def worlds(data, id , v):
    print('worlds')
    return {
        'message':         string(data, id, 0),
        'name':            string(data, id, 1)
    }

def warps(data, id , v):
    print('warps')
    return {
        'name':            string(data, id, 1),
        'map':             full_ref('levels', v[2])
    }

