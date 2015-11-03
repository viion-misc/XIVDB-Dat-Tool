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

def unmapped(index_list, v):
    return {
        index: repr(v[index]) for index in index_list
    }

#### MAPPINGS ####

def AchievementCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def AchievementKind(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Achievement(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
    }

def ActionCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Action(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1, enable_conditions = True),
    }

def AddonParam(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def AddonHud(data, id, v):
    return {
        'name': string(data, id, 0),
        'command': string(data, id, 1),
        'command_short': string(data, id, 2),
    }

def AddonTransient(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Addon(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Adventure(data, id, v):
    return {
        'name': string(data, id, 0),
        'text1': string(data, id, 1),
        'text2': string(data, id, 2),
    }

def Aetheryte(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def AirshipExplorationLog(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def AirshipExplorationParamType(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def AirshipExplorationPoint(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
    }

def AttackType(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Attributive(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def BNpcName(data, id, v):
    return {
        'name': string(data, id, 0),
        'name_plural': string(data, id, 1),
    }

def Balloon(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def BaseParam(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
    }

def BeastReputationRank(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def BeastTribe(data, id, v):
    return {
        'name': string(data, id, 0),
        'reputation': string(data, id, 2),
    }

def BuddyAction(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
    }

def BuddyEquip(data, id, v):
    return {
        'item': string(data, id, 0),
        'item_plural': string(data, id, 1),
        'name': string(data, id, 2),
    }

def CharaMakeName(data, id, v):
    return {
        'name0': string(data, id, 0),
        'name1': string(data, id, 1),
        'name2': string(data, id, 2),
        'name3': string(data, id, 3),
        'name4': string(data, id, 4),
        'name5': string(data, id, 5),
        'name6': string(data, id, 6),
        'name7': string(data, id, 7),
        'name8': string(data, id, 8),
        'name9': string(data, id, 9),
        'name10': string(data, id, 10),
        'name11': string(data, id, 11),
        'name12': string(data, id, 12),
        'name13': string(data, id, 13),
        'name14': string(data, id, 14),
        'name15': string(data, id, 15),
        'name16': string(data, id, 16),
        'name17': string(data, id, 17),
        'name18': string(data, id, 18),
        'name19': string(data, id, 19),
        'name20': string(data, id, 20),
        'name21': string(data, id, 21),
        'name22': string(data, id, 22),
        'name23': string(data, id, 23),
        'name24': string(data, id, 24),
        'name25': string(data, id, 25),
        'name26': string(data, id, 26),
        'name27': string(data, id, 27),
        'name28': string(data, id, 28),
        'name29': string(data, id, 29),
        'name30': string(data, id, 30),
        'name31': string(data, id, 31),
        'name32': string(data, id, 32),
        'name33': string(data, id, 33),
        'name34': string(data, id, 34),
        'name35': string(data, id, 35),
        'name36': string(data, id, 36),
    }

def CharaMakeType(data, id, v):
    return {}

def ChocoboRaceAbility(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1, enable_conditions = True),
    }

def ChocoboRaceItem(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1, enable_conditions = True),
    }

def ChocoboTaxiStand(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def ClassJobCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def ClassJob(data, id, v):
    return {
        'name': string(data, id, 0),
        'caps': string(data, id, 4),
        'abbr': string(data, id, 1),
        'is_job': 1 if v[3] != 0 else 0,
    }

def CompanionMove(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Companion(data, id, v):
    return {
        'name': string(data, id, 0),
        'name_plural': string(data, id, 1),
        'action': string(data, id, 2),
        'help1': string(data, id, 3),
        'help2': string(data, id, 4),
    }

def CompanyAction(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1, enable_conditions = True),
    }

def CompanyCraftDraftCategoryTxt(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def CompanyCraftDraftCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def CompanyCraftDraft(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def CompanyCraftManufactoryState(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def CompanyCraftType(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def CompleteJournal(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Completion(data, id, v):
    return {
        'name': string(data, id, 0),
        'group': string(data, id, 2),
        'code': string(data, id, 1),
    }

def ConfigKey(data, id, v):
    return {
        'name': string(data, id, 0),
        'bind': string(data, id, 1),
    }

def ContentDescription(data, id, v):
    return {
        'help': string(data, id, 0),
    }

def ContentRoulette(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
        'type': string(data, id, 2),
    }

def ContentTalk(data, id, v):
    return {
        'text': string(data, id, 0),
    }

def ContentType(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def ContentsNote(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
    }

def CraftAction(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1, enable_conditions = True),
    }

def CraftLeveTalk(data, id, v):
    return {
        'question': string(data, id, 36),
        'yes': string(data, id, 37),
        'no': string(data, id, 38),
    }

def CraftType(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def CreditCast(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def CustomTalk(data, id, v):
    return {
        'text': string(data, id, 30),
    }

def DefaultTalk(data, id, v):
    return {
        'text1': string(data, id, 18),
        'text2': string(data, id, 19),
        'text3': string(data, id, 20),
        'text4': string(data, id, 21),
    }

def ENpcResident(data, id, v):
    return {
        'name': string(data, id, 0),
        'name_plural': string(data, id, 1),
        'name_title': string(data, id, 2),
    }

def EObj(data, id, v):
    return {
        'name': string(data, id, 0),
        'name_plural': string(data, id, 1),
    }

def EmoteCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Emote(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Error(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def EventAction(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def EventItem(data, id, v):
    return {
        'name': string(data, id, 0),
        'name_plural': string(data, id, 1),
        'help': string(data, id, 2),
        'name_title': string(data, id, 3),
    }

def ExVersion(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def FCActivityCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def FCActivity(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def FCAuthorityCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def FCAuthority(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def FCChestName(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def FCHierarchy(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def FCProfile(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def FCReputation(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def FCRights(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
    }

def FateEvent(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Fate(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
    }

def FccShop(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def FieldMarkerText(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def FieldMarker(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def FishParameter(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def FishingSpotCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def FishingSpot(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def GCRankGridaniaFemaleText(data, id, v):
    return {
        'name': string(data, id, 0),
        'rank': string(data, id, 2),
    }

def GCRankGridaniaMaleText(data, id, v):
    return {
        'name': string(data, id, 0),
        'rank': string(data, id, 2),
    }

def GCRankLimsaFemaleText(data, id, v):
    return {
        'name': string(data, id, 0),
        'rank': string(data, id, 2),
    }

def GCRankLimsaMaleText(data, id, v):
    return {
        'name': string(data, id, 0),
        'rank': string(data, id, 2),
    }

def GCRankUldahFemaleText(data, id, v):
    return {
        'name': string(data, id, 0),
        'rank': string(data, id, 2),
    }

def GCRankUldahMaleText(data, id, v):
    return {
        'name': string(data, id, 0),
        'rank': string(data, id, 2),
    }

def GCShopItemCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def GFateClimbing(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def GFateStelth(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def GatheringCondition(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def GatheringPointBonusType(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def GatheringPointName(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def GatheringSubCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def GatheringType(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def GeneralAction(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1, enable_conditions = True),
    }

def GimmickBill(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def GimmickYesNo(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def GoldSaucerArcadeMachine(data, id, v):
    return {
        'name': string(data, id, 25),
        'help': string(data, id, 26),
    }

def GoldSaucerTalk(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def GoldSaucerTextData(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def GrandCompany(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def GuardianDeity(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
    }

def GuildOrder(data, id, v):
    return {
        'text1': string(data, id, 0),
        'text2': string(data, id, 1),
        'text3': string(data, id, 2),
        'text4': string(data, id, 3),
    }

def GuildleveAssignmentTalk(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def GuildleveEvaluation(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def HousingItemCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def HousingPreset(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def HowToCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def HowToPage(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def HowTo(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def InstanceContentTextData(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def InstanceContent(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def ItemSearchCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def ItemSeries(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def ItemSpecialBonus(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def ItemUICategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Item(data, id, v):
    return {
        'noun': string(data, id, 0),
        'plural_noun': string(data, id, 1),
        'help': string(data, id, 2),
        'name': string(data, id, 3),
    }

def JournalCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def JournalGenre(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def LegacyQuest(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def LeveAssignmentType(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def LeveClient(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def LeveString(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Leve(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
    }

def LiveConditionSign(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def LiveCondition(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def LoadingTipsSub(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def LoadingTips(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Lobby(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def LogFilter(data, id, v):
    return {
        'name': string(data, id, 0),
        'example': string(data, id, 1),
    }

def LogKindCategoryText(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def LogKind(data, id, v):
    return {
        'name': string(data, id, 0),
        'type': string(data, id, 1),
    }

def LogMessage(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def MainCommandCategory(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
    }

def MainCommand(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
    }

def Marker(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def MonsterNote(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Mount(data, id, v):
    return {
        'name': string(data, id, 0),
        'name_plural': string(data, id, 1),
        'action': string(data, id, 2),
        'help1': string(data, id, 3),
        'help2': string(data, id, 4),
    }

def MovieSubtitleVoyage(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def MovieSubtitle(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def NotebookDivision(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def NpcYell(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def OnlineStatus(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def PetAction(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
    }

def Pet(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def PlaceName(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def PublicContentTextData(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def PublicContent(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def PvPRank(data, id, v):
    return {
        'storm': string(data, id, 0),
        'serpent': string(data, id, 1),
        'flame': string(data, id, 2),
    }

def QuestRewardOther(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Quest(exd_manager):
    data = exd_manager.get_category('Quest').get_data()
    data_ln = data[list(data.keys())[0]]
    data_return = {}

    for id, v in data_ln.items():
        data_return[id] = {
            'name': string(data, id, 0),
        }

        # if quest data
        if v[981] != b'':
            quest_base_exd_name = v[981].decode('utf-8')
            quest_exd_name = 'quest/%s/%s' % (quest_base_exd_name[10:13], quest_base_exd_name)
            quest_exd_data = exd_manager.get_category(quest_exd_name).get_data()
            quest_exd_data_ln = quest_exd_data[list(quest_exd_data.keys())[0]]
            data_return[id].update({
                'text_data': {
                    quest_exd_data_ln[quest_exd_id][0].decode('utf-8'): {
                        'enable_conditions': False,
                        'type': 'string',
                        'ln': {
                            get_language_name(language): quest_exd_data[language][quest_exd_id][1] for language in quest_exd_data.keys()
                        }
                    } for quest_exd_id in sorted(quest_exd_data_ln.keys())
                }
            })

    return data_return

def RCNameCategoryText(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Race(data, id, v):
    return {
        'name': string(data, id, 0),
        'name_female': string(data, id, 0),
    }

def RacingChocoboNameCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def RacingChocoboNameText(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def RacingChocoboName(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def RacingChocoboParamText(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def RacingChocoboParam(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def RecipeElement(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Relic6MagiciteText(data, id, v):
    return {
        'name': string(data, id, 0),
        'type': string(data, id, 1),
    }

def Relic6Magicite(data, id, v):
    return {
        'name': string(data, id, 0),
        'type': string(data, id, 1),
    }

def RelicNoteCategoryText(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def RelicNoteCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def RetainerTaskRandomText(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def RetainerTaskRandom(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Role(data, id, v):
    return {
        'name': string(data, id, 0),
        'letter': string(data, id, 1),
    }

def Shop(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def SpecialShopItemCategory(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def SpecialShop(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Stain(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Status(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
    }

def TextCommandParam(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def TextCommand(data, id, v):
    return {
        'help': string(data, id, 0),
        'command1': string(data, id, 0),
        'command2': string(data, id, 0),
        'command3': string(data, id, 0),
        'command4': string(data, id, 0),
    }

def Title(data, id, v):
    return {
        'name': string(data, id, 0),
        'name_female': string(data, id, 1),
        'front': string(data, id, 2),
    }

def Town(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Trait(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
    }

def Treasure(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Tribe(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def TripleTriadCardType(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def TripleTriadCard(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 2),
    }

def TripleTriadCompetition(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def TripleTriadRule(data, id, v):
    return {
        'name': string(data, id, 0),
        'help': string(data, id, 1),
    }

def WarpLogic(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Warp(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def Weather(data, id, v):
    return {
        'name': string(data, id, 0),
        'type': string(data, id, 1),
    }

def WeddingBGM(data, id, v):
    return {
        'name': string(data, id, 0),
    }

def World(data, id, v):
    return {
        'help': string(data, id, 0),
        'name': string(data, id, 1),
    }

# special

def ActionTimeline(data, id, v):
    return {
        'name': v[0],
    }

def BGM(data, id, v):
    return {
        'name': v[0],
    }

def Cutscene(data, id, v):
    return {
        'name': v[0],
    }

def EventSystemDefine(data, id, v):
    return {
        'name': v[0],
    }

def ExportedSG(data, id, v):
    return {
        'name': v[0],
    }

def Festival(data, id, v):
    return {
        'name': v[0],
    }

def HousingExterior(data, id, v):
    return {
        'name': v[0],
    }

def HousingInterior(data, id, v):
    return {
        'name': v[0],
    }

def Jingle(data, id, v):
    return {
        'name': v[0],
    }

def Map(data, id, v):
    return {
        'name': v[0],
    }

def SE(data, id, v):
    return {
        'name': v[0],
    }

def TerritoryType(data, id, v):
    return {
        'name': v[0],
    }


def VFX(data, id, v):
    return {
        'name': v[0],
    }

def WeaponTimeline(data, id, v):
    return {
        'name': v[0],
    }

def WorldDCGroupType(data, id, v):
    return {
        'name': v[0],
    }
