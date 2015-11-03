import logging

from xivdm.language import get_language_id
from xivdm.view.mapping import *
from xivdm.view.strings import StringConverter

class Manager:
    def __init__(self, exd_manager):
        self._exd_manager = exd_manager
        self._mappings = {
            'achievements': simple_mapping('Achievement', achievements),
            'achievement_categories': simple_mapping('AchievementCategory', achievement_categories),
            'achievement_kinds': simple_mapping('AchievementKind', achievement_kinds),
            'action_categories': simple_mapping('ActionCategory', action_categories),
            'actions': simple_mapping('Action', actions),
            'addons': simple_mapping('Addon', addons),
            'attack_types': simple_mapping('AttackType', attack_types),
            'balloons': simple_mapping('Balloon', balloons),
            'battle_leves': simple_mapping('BattleLeve', battle_leves),
            #'behest_rewards': simple_mapping('BehestReward', behest_rewards),
            'bnpc_names': bnpc_names,
            'bnpc_bases': simple_mapping('BNpcBase', bnpc_bases),
            'chain_bonuses': simple_mapping('ChainBonus', chain_bonuses),
            'chocobo_taxi_stands': simple_mapping('ChocoboTaxiStand', chocobo_taxi_stands),
            'class_jobs': simple_mapping('ClassJob', class_jobs),
            'class_job_categories': simple_mapping('ClassJobCategory', class_job_categories),
            'companions': simple_mapping('Companion', companions),
            'complete_journals': simple_mapping('CompleteJournal', complete_journals),
            'completions': simple_mapping('Completion', completions),
            'company_leves': simple_mapping('CompanyLeve', company_leves),
            'content_type': simple_mapping('ContentType', content_type),
            'content_description': simple_mapping('ContentDescription', content_description),
            'craft_action': simple_mapping('CraftAction', craft_action),
            'craft_crystal_type': simple_mapping('CraftCrystalType', craft_crystal_type),
            'craft_leves': simple_mapping('CraftLeve', craft_leves),
            'craft_types': simple_mapping('CraftType', craft_types),
            'custom_talks': simple_mapping('CustomTalk', custom_talks),
            'default_talks': simple_mapping('DefaultTalk', default_talks),
            'emotes': simple_mapping('Emote', emotes),
            'enpc_bases': simple_mapping('ENpcBase', enpc_bases),
            'enpc_residents': simple_mapping('ENpcResident', enpc_residents),
            'eobjs': simple_mapping('EObj', eobjs),
            'errors': simple_mapping('Error', errors),
            'event_items': simple_mapping('EventItem', event_items),
            'fates': simple_mapping('Fate', fates),
            'gathering_leves': simple_mapping('GatheringLeve', gathering_leves),
            'gathering_points': gathering_points,
            'gathering_points_base': simple_mapping('GatheringPointBase', gathering_points_base),
            'gathering_points_name': simple_mapping('GatheringPointName', gathering_points_name),
            'gathering_items': simple_mapping('GatheringItem', gathering_items),
            'gathering_type': simple_mapping('GatheringType', gathering_type),
            'gathering_condition': simple_mapping('GatheringCondition', gathering_condition),
            'gathering_bonus_type': simple_mapping('GatheringPointBonusType', gathering_bonus_type),
            'gcrank_gridania_female_texts': simple_mapping('GCRankGridaniaFemaleText', gcrank),
            'gcrank_gridania_male_texts': simple_mapping('GCRankGridaniaMaleText', gcrank),
            'gcrank_limsa_female_texts': simple_mapping('GCRankLimsaFemaleText', gcrank),
            'gcrank_limsa_male_texts': simple_mapping('GCRankLimsaMaleText', gcrank),
            'gcrank_uldah_female_texts': simple_mapping('GCRankUldahFemaleText', gcrank),
            'gcrank_uldah_male_texts': simple_mapping('GCRankUldahMaleText', gcrank),
            'gcshops': simple_mapping('GCShop', gcshops),
            'gcshop_item_categories': simple_mapping('GCShopItemCategory', gcshop_item_categories),
            'general_actions': simple_mapping('GeneralAction', general_actions),
            'grand_companies': simple_mapping('GrandCompany', grand_companies),
            'grand_company_ranks': simple_mapping('GrandCompanyRank', grand_company_ranks),
            'grand_company_seal_shop_items': simple_mapping('GrandCompanySealShopItem', grand_company_seal_shop_items),
            'guardian_deities': simple_mapping('GuardianDeity', guardian_deities),
            'guild_order_guides': simple_mapping('GuildOrderGuide', guild_order_guides),
            'guild_order_officers': simple_mapping('GuildOrderOfficer', guild_order_officers),
            'guildleve_assignments': simple_mapping('GuildleveAssignment', guildleve_assignments),
            'instance_contents': instance_contents,
            'instance_content_type': simple_mapping('InstanceContentType', instance_content_type),
			'instance_content_textdata': simple_mapping('InstanceContentTextData', instance_content_textdata),
            'item_actions': simple_mapping('ItemAction', item_actions),
            #'item_categories': simple_mapping('ItemCategory', item_categories),
            'item_foods': simple_mapping('ItemFood', item_foods),
            'item_search_categories': simple_mapping('ItemSearchCategory', item_search_categories),
            #'item_search_class_filters': simple_mapping('ItemSearchClassFilter', item_search_class_filters),
            'item_series': simple_mapping('ItemSeries', item_series),
			'item_special_bonuses': simple_mapping('ItemSpecialBonus', item_special_bonuses),
            'item_ui_categories': simple_mapping('ItemUICategory', item_ui_categories),
            'items': simple_mapping('Item', items),
            'leves': simple_mapping('Leve', leves),
            'levels': simple_mapping('Level', levels),
            'leve_reward_items': simple_mapping('LeveRewardItem', leve_reward_items),
            'leve_reward_item_groups': simple_mapping('LeveRewardItemGroup', leve_reward_item_groups),
            'leve_clients': simple_mapping('LeveClient', leve_clients),
			'leves_vfx': simple_mapping('LeveVfx', leves_vfx),
            'param_grow': simple_mapping('ParamGrow', param_grow),
            'maps': simple_mapping('Map', maps),
			'materias': simple_mapping('Materia', materias),
            'markers': simple_mapping('Marker', markers),
            'model_chara': simple_mapping('ModelChara', model_chara),
            'mounts': simple_mapping('Mount', mounts),
            'monster_notes': simple_mapping('MonsterNote', monster_notes),
            'monster_notes_target': simple_mapping('MonsterNoteTarget', monster_notes_target),
            'npc_yells': simple_mapping('NpcYell', npc_yells),
            'online_statuses': simple_mapping('OnlineStatus', online_statuses),
            'base_params': simple_mapping('BaseParam', base_params),
            'pet_action': simple_mapping('PetAction', pet_action),
            'place_names': simple_mapping('PlaceName', place_names),
            'quests': quests,
            'recipes': simple_mapping('Recipe', recipes),
            'roles': simple_mapping('Role', roles),
            'special_shops': simple_mapping('SpecialShop', special_shops),
            'shops': simple_mapping('Shop', shops),
            'shop_items': simple_mapping('ShopItem', shop_items),
            'statuses': simple_mapping('Status', statuses),
            'stories': simple_mapping('Story', stories),
            'text_commands': simple_mapping('TextCommand', text_commands),
            'titles': simple_mapping('Title', titles),
            'towns': simple_mapping('Town', towns),
            'traits': simple_mapping('Trait', traits),
            'journal_genre': simple_mapping('JournalGenre', journal_genre),
            'journal_cat': simple_mapping('JournalCategory', journal_cat),
            'weathers': simple_mapping('Weather', weathers),
            'worlds': simple_mapping('World', worlds),
            'warps': simple_mapping('Warp', warps)
        }
        self._jsons = {}

    def get_mappings(self):
        return self._mappings.keys()

    def get_json(self, name):
        if not name in self._jsons:
            self._create_json(name)
        return self._jsons[name]

    def _create_json(self, name):
        print("Creating:", name)
        self._jsons[name] = self._mappings[name](self._exd_manager)
        self._walk_json(self._jsons[name], self._parse_string)
        self._walk_json(self._jsons[name], self._parse_view_refs)

    def _parse_string(self, key, value):
        if type(value) == dict:
            if 'type' in value:
                if value['type'] == 'string':
                    logging.info(value)
                    return_dict = dict()
                    languages = value['ln']
                    enable_conditions = value['enable_conditions']
                    for ln in languages.keys():
                        if type(languages[ln]) == list:
                            return_dict[ln] = [
                                StringConverter(self._exd_manager, get_language_id(ln), enable_conditions).convert(memoryview(sub_str)) for sub_str in languages[ln]
                            ]
                        else:
                            try:
                                return_dict[ln] = StringConverter(self._exd_manager, get_language_id(ln), enable_conditions).convert(memoryview(languages[ln]))
                            except TypeError:
                                print('TypeError', ln)
                    return return_dict
        return None

    def _parse_view_refs(self, key, value):
        if type(value) == dict:
            if 'type' in value:
                dict_type = value['type']
                if dict_type in ['view_ref', 'full_view_ref']:
                    is_full = dict_type == 'full_view_ref'
                    view_ref = value.get('view')
                    id = value.get('id')
                    if view_ref and id is not None:
                        raw_json = self.get_json(view_ref)
                        if not id in raw_json:
                            if id in [-1, 0]:
                                return None
                            else:
                                print("Key:", key, "Value:", value)
                                raise Exception('Id not found for view: %s - id: %d' % (view_ref, id))
                        id_json = self.get_json(view_ref)[id]
                        if not is_full:
                            if 'name' in id_json:
                                value['value'] = id_json['name']['en']
                                return value
                        else:
                            value['value'] = id_json
                            return value
        return None

    def _walk_json(self, node, process_function):
        keys, values = self._get_keys_values(node)
        if keys and values:
            for index, value in enumerate(values):
                new_value = process_function(keys[index], value)
                if new_value is not None:
                    node[keys[index]] = new_value
                else:
                    self._walk_json(value, process_function)


    def _get_keys_values(self, node):
        if type(node) == dict:
            return list(node.keys()), list(node.values())
        elif type(node) == list:
            return list(range(len(node))), node
        else:
            return None, None

