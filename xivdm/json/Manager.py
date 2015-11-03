import logging

from xivdm.language import get_language_id
from xivdm.json.mapping import *
from xivdm.json.strings import StringConverter

class Manager:
    def __init__(self, exd_manager):
        self._exd_manager = exd_manager
        self._mappings = {
            'AchievementCategory': simple_mapping('AchievementCategory', AchievementCategory),
            'AchievementKind': simple_mapping('AchievementKind', AchievementKind),
            'Achievement': simple_mapping('Achievement', Achievement),
            'ActionCategory': simple_mapping('ActionCategory', ActionCategory),
            'Action': simple_mapping('Action', Action),
            'AddonHud': simple_mapping('AddonHud', AddonHud),
            'AddonTransient': simple_mapping('AddonTransient', AddonTransient),
            'AddonParam': simple_mapping('AddonParam', AddonParam),
            'Addon': simple_mapping('Addon', Addon),
            'Adventure': simple_mapping('Adventure', Adventure),
            'Aetheryte': simple_mapping('Aetheryte', Aetheryte),
            'AirshipExplorationLog': simple_mapping('AirshipExplorationLog', AirshipExplorationLog),
            'AirshipExplorationParamType': simple_mapping('AirshipExplorationParamType', AirshipExplorationParamType),
            'AirshipExplorationPoint': simple_mapping('AirshipExplorationPoint', AirshipExplorationPoint),
            'AttackType': simple_mapping('AttackType', AttackType),
            'Attributive': simple_mapping('Attributive', Attributive),
            'BNpcName': simple_mapping('BNpcName', BNpcName),
            'Balloon': simple_mapping('Balloon', Balloon),
            'BaseParam': simple_mapping('BaseParam', BaseParam),
            'BeastReputationRank': simple_mapping('BeastReputationRank', BeastReputationRank),
            'BeastTribe': simple_mapping('BeastTribe', BeastTribe),
            'BuddyAction': simple_mapping('BuddyAction', BuddyAction),
            'BuddyEquip': simple_mapping('BuddyEquip', BuddyEquip),
            'CharaMakeName': simple_mapping('CharaMakeName', CharaMakeName),
            'CharaMakeType': simple_mapping('CharaMakeType', CharaMakeType),
            'ChocoboRaceAbility': simple_mapping('ChocoboRaceAbility', ChocoboRaceAbility),
            'ChocoboRaceItem': simple_mapping('ChocoboRaceItem', ChocoboRaceItem),
            'ChocoboTaxiStand': simple_mapping('ChocoboTaxiStand', ChocoboTaxiStand),
            'ClassJobCategory': simple_mapping('ClassJobCategory', ClassJobCategory),
            'ClassJob': simple_mapping('ClassJob', ClassJob),
            'CompanionMove': simple_mapping('CompanionMove', CompanionMove),
            'Companion': simple_mapping('Companion', Companion),
            'CompanyAction': simple_mapping('CompanyAction', CompanyAction),
            'CompanyCraftDraftCategoryTxt': simple_mapping('CompanyCraftDraftCategoryTxt', CompanyCraftDraftCategoryTxt),
            'CompanyCraftDraftCategory': simple_mapping('CompanyCraftDraftCategory', CompanyCraftDraftCategory),
            'CompanyCraftDraft': simple_mapping('CompanyCraftDraft', CompanyCraftDraft),
            'CompanyCraftManufactoryState': simple_mapping('CompanyCraftManufactoryState', CompanyCraftManufactoryState),
            'CompanyCraftType': simple_mapping('CompanyCraftType', CompanyCraftType),
            'CompleteJournal': simple_mapping('CompleteJournal', CompleteJournal),
            'Completion': simple_mapping('Completion', Completion),
            'ConfigKey': simple_mapping('ConfigKey', ConfigKey),
            'ContentDescription': simple_mapping('ContentDescription', ContentDescription),
            'ContentRoulette': simple_mapping('ContentRoulette', ContentRoulette),
            'ContentTalk': simple_mapping('ContentTalk', ContentTalk),
            'ContentType': simple_mapping('ContentType', ContentType),
            'ContentsNote': simple_mapping('ContentsNote', ContentsNote),
            'CraftAction': simple_mapping('CraftAction', CraftAction),
            'CraftLeveTalk': simple_mapping('CraftLeveTalk', CraftLeveTalk),
            'CraftType': simple_mapping('CraftType', CraftType),
            'CreditCast': simple_mapping('CreditCast', CreditCast),
            'CustomTalk': simple_mapping('CustomTalk', CustomTalk),
            'DefaultTalk': simple_mapping('DefaultTalk', DefaultTalk),
            'ENpcResident': simple_mapping('ENpcResident', ENpcResident),
            'EObj': simple_mapping('EObj', EObj),
            'EmoteCategory': simple_mapping('EmoteCategory', EmoteCategory),
            'Emote': simple_mapping('Emote', Emote),
            'Error': simple_mapping('Error', Error),
            'EventAction': simple_mapping('EventAction', EventAction),
            'EventItem': simple_mapping('EventItem', EventItem),
            'ExVersion': simple_mapping('ExVersion', ExVersion),
            'FCActivityCategory': simple_mapping('FCActivityCategory', FCActivityCategory),
            'FCActivity': simple_mapping('FCActivity', FCActivity),
            'FCAuthorityCategory': simple_mapping('FCAuthorityCategory', FCAuthorityCategory),
            'FCAuthority': simple_mapping('FCAuthority', FCAuthority),
            'FCChestName': simple_mapping('FCChestName', FCChestName),
            'FCHierarchy': simple_mapping('FCHierarchy', FCHierarchy),
            'FCProfile': simple_mapping('FCProfile', FCProfile),
            'FCReputation': simple_mapping('FCReputation', FCReputation),
            'FCRights': simple_mapping('FCRights', FCRights),
            'FateEvent': simple_mapping('FateEvent', FateEvent),
            'Fate': simple_mapping('Fate', Fate),
            'FccShop': simple_mapping('FccShop', FccShop),
            'FieldMarkerText': simple_mapping('FieldMarkerText', FieldMarkerText),
            'FieldMarker': simple_mapping('FieldMarker', FieldMarker),
            'FishParameter': simple_mapping('FishParameter', FishParameter),
            'FishingSpotCategory': simple_mapping('FishingSpotCategory', FishingSpotCategory),
            'FishingSpot': simple_mapping('FishingSpot', FishingSpot),
            'GCRankGridaniaFemaleText': simple_mapping('GCRankGridaniaFemaleText', GCRankGridaniaFemaleText),
            'GCRankGridaniaMaleText': simple_mapping('GCRankGridaniaMaleText', GCRankGridaniaMaleText),
            'GCRankLimsaFemaleText': simple_mapping('GCRankLimsaFemaleText', GCRankLimsaFemaleText),
            'GCRankLimsaMaleText': simple_mapping('GCRankLimsaMaleText', GCRankLimsaMaleText),
            'GCRankUldahFemaleText': simple_mapping('GCRankUldahFemaleText', GCRankUldahFemaleText),
            'GCRankUldahMaleText': simple_mapping('GCRankUldahMaleText', GCRankUldahMaleText),
            'GCShopItemCategory': simple_mapping('GCShopItemCategory', GCShopItemCategory),
            'GFateClimbing': simple_mapping('GFateClimbing', GFateClimbing),
            'GFateStelth': simple_mapping('GFateStelth', GFateStelth),
            'GatheringCondition': simple_mapping('GatheringCondition', GatheringCondition),
            'GatheringPointBonusType': simple_mapping('GatheringPointBonusType', GatheringPointBonusType),
            'GatheringPointName': simple_mapping('GatheringPointName', GatheringPointName),
            'GatheringSubCategory': simple_mapping('GatheringSubCategory', GatheringSubCategory),
            'GatheringType': simple_mapping('GatheringType', GatheringType),
            'GeneralAction': simple_mapping('GeneralAction', GeneralAction),
            'GimmickBill': simple_mapping('GimmickBill', GimmickBill),
            'GimmickYesNo': simple_mapping('GimmickYesNo', GimmickYesNo),
            'GoldSaucerArcadeMachine': simple_mapping('GoldSaucerArcadeMachine', GoldSaucerArcadeMachine),
            'GoldSaucerTalk': simple_mapping('GoldSaucerTalk', GoldSaucerTalk),
            'GoldSaucerTextData': simple_mapping('GoldSaucerTextData', GoldSaucerTextData),
            'GrandCompany': simple_mapping('GrandCompany', GrandCompany),
            'GuardianDeity': simple_mapping('GuardianDeity', GuardianDeity),
            'GuildOrder': simple_mapping('GuildOrder', GuildOrder),
            'GuildleveAssignmentTalk': simple_mapping('GuildleveAssignmentTalk', GuildleveAssignmentTalk),
            'GuildleveEvaluation': simple_mapping('GuildleveEvaluation', GuildleveEvaluation),
            'HousingItemCategory': simple_mapping('HousingItemCategory', HousingItemCategory),
            'HousingPreset': simple_mapping('HousingPreset', HousingPreset),
            'HowToCategory': simple_mapping('HowToCategory', HowToCategory),
            'HowToPage': simple_mapping('HowToPage', HowToPage),
            'HowTo': simple_mapping('HowTo', HowTo),
            'InstanceContentTextData': simple_mapping('InstanceContentTextData', InstanceContentTextData),
            'InstanceContent': simple_mapping('InstanceContent', InstanceContent),
            'ItemSearchCategory': simple_mapping('ItemSearchCategory', ItemSearchCategory),
            'ItemSeries': simple_mapping('ItemSeries', ItemSeries),
            'ItemSpecialBonus': simple_mapping('ItemSpecialBonus', ItemSpecialBonus),
            'ItemUICategory': simple_mapping('ItemUICategory', ItemUICategory),
            'Item': simple_mapping('Item', Item),
            'JournalCategory': simple_mapping('JournalCategory', JournalCategory),
            'JournalGenre': simple_mapping('JournalGenre', JournalGenre),
            'LegacyQuest': simple_mapping('LegacyQuest', LegacyQuest),
            'LeveAssignmentType': simple_mapping('LeveAssignmentType', LeveAssignmentType),
            'LeveClient': simple_mapping('LeveClient', LeveClient),
            'LeveString': simple_mapping('LeveString', LeveString),
            'Leve': simple_mapping('Leve', Leve),
            'LiveConditionSign': simple_mapping('LiveConditionSign', LiveConditionSign),
            'LiveCondition': simple_mapping('LiveCondition', LiveCondition),
            'LoadingTipsSub': simple_mapping('LoadingTipsSub', LoadingTipsSub),
            'LoadingTips': simple_mapping('LoadingTips', LoadingTips),
            'Lobby': simple_mapping('Lobby', Lobby),
            'LogFilter': simple_mapping('LogFilter', LogFilter),
            'LogKindCategoryText': simple_mapping('LogKindCategoryText', LogKindCategoryText),
            'LogKind': simple_mapping('LogKind', LogKind),
            'LogMessage': simple_mapping('LogMessage', LogMessage),
            'MainCommandCategory': simple_mapping('MainCommandCategory', MainCommandCategory),
            'MainCommand': simple_mapping('MainCommand', MainCommand),
            'Marker': simple_mapping('Marker', Marker),
            'MonsterNote': simple_mapping('MonsterNote', MonsterNote),
            'Mount': simple_mapping('Mount', Mount),
            'MovieSubtitleVoyage': simple_mapping('MovieSubtitleVoyage', MovieSubtitleVoyage),
            'MovieSubtitle': simple_mapping('MovieSubtitle', MovieSubtitle),
            'NotebookDivision': simple_mapping('NotebookDivision', NotebookDivision),
            'NpcYell': simple_mapping('NpcYell', NpcYell),
            'OnlineStatus': simple_mapping('OnlineStatus', OnlineStatus),
            'PetAction': simple_mapping('PetAction', PetAction),
            'Pet': simple_mapping('Pet', Pet),
            'PlaceName': simple_mapping('PlaceName', PlaceName),
            'PublicContentTextData': simple_mapping('PublicContentTextData', PublicContentTextData),
            'PublicContent': simple_mapping('PublicContent', PublicContent),
            'PvPRank': simple_mapping('PvPRank', PvPRank),
            'QuestRewardOther': simple_mapping('QuestRewardOther', QuestRewardOther),
            'RCNameCategoryText': simple_mapping('RCNameCategoryText', RCNameCategoryText),
            'Race': simple_mapping('Race', Race),
            'RacingChocoboNameCategory': simple_mapping('RacingChocoboNameCategory', RacingChocoboNameCategory),
            'RacingChocoboNameText': simple_mapping('RacingChocoboNameText', RacingChocoboNameText),
            'RacingChocoboName': simple_mapping('RacingChocoboName', RacingChocoboName),
            'RacingChocoboParamText': simple_mapping('RacingChocoboParamText', RacingChocoboParamText),
            'RacingChocoboParam': simple_mapping('RacingChocoboParam', RacingChocoboParam),
            'RecipeElement': simple_mapping('RecipeElement', RecipeElement),
            'Relic6MagiciteText': simple_mapping('Relic6MagiciteText', Relic6MagiciteText),
            'Relic6Magicite': simple_mapping('Relic6Magicite', Relic6Magicite),
            'RelicNoteCategoryText': simple_mapping('RelicNoteCategoryText', RelicNoteCategoryText),
            'RelicNoteCategory': simple_mapping('RelicNoteCategory', RelicNoteCategory),
            'RetainerTaskRandomText': simple_mapping('RetainerTaskRandomText', RetainerTaskRandomText),
            'RetainerTaskRandom': simple_mapping('RetainerTaskRandom', RetainerTaskRandom),
            'Role': simple_mapping('Role', Role),
            'Shop': simple_mapping('Shop', Shop),
            'SpecialShopItemCategory': simple_mapping('SpecialShopItemCategory', SpecialShopItemCategory),
            'SpecialShop': simple_mapping('SpecialShop', SpecialShop),
            'Stain': simple_mapping('Stain', Stain),
            'Status': simple_mapping('Status', Status),
            'TextCommandParam': simple_mapping('TextCommandParam', TextCommandParam),
            'TextCommand': simple_mapping('TextCommand', TextCommand),
            'Title': simple_mapping('Title', Title),
            'Town': simple_mapping('Town', Town),
            'Trait': simple_mapping('Trait', Trait),
            'Treasure': simple_mapping('Treasure', Treasure),
            'Tribe': simple_mapping('Tribe', Tribe),
            'TripleTriadCardType': simple_mapping('TripleTriadCardType', TripleTriadCardType),
            'TripleTriadCard': simple_mapping('TripleTriadCard', TripleTriadCard),
            'TripleTriadCompetition': simple_mapping('TripleTriadCompetition', TripleTriadCompetition),
            'TripleTriadRule': simple_mapping('TripleTriadRule', TripleTriadRule),
            'WarpLogic': simple_mapping('WarpLogic', WarpLogic),
            'Warp': simple_mapping('Warp', Warp),
            'Weather': simple_mapping('Weather', Weather),
            'WeddingBGM': simple_mapping('WeddingBGM', WeddingBGM),
            'World': simple_mapping('World', World),

            # Special ones


            'Quest': Quest,

            #'ActionTimeline': simple_mapping('ActionTimeline', ActionTimeline),
            #'
            #'BGM': simple_mapping('BGM', BGM),
            #'Cutscene': simple_mapping('Cutscene', Cutscene),
            #'EventSystemDefine': simple_mapping('EventSystemDefine', EventSystemDefine),
            #'ExportedSG': simple_mapping('ExportedSG', ExportedSG),
            #'Festival': simple_mapping('Festival', Festival),
            #'HousingExterior': simple_mapping('HousingExterior', HousingExterior),
            #'HousingInterior': simple_mapping('HousingInterior', HousingInterior),
            #'Jingle': simple_mapping('Jingle', Jingle),
            #'Map': simple_mapping('Map', Map),
            #'SE': simple_mapping('SE', SE),
            #'TerritoryType': simple_mapping('TerritoryType', TerritoryType),
            #'VFX': simple_mapping('VFX', VFX),
            #'WeaponTimeline': simple_mapping('WeaponTimeline', WeaponTimeline),
            #'WorldDCGroupType': simple_mapping('WorldDCGroupType', WorldDCGroupType),
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
