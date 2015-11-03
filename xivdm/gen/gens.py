import logging

from xivdm.crc32_utils import rev_crc_32
from xivdm.dat.Manager import get_hash

def get_rev_digits_values_matches(prefix_value, suffix_value, hash_dict):
    results = {}
    prefix_crc = get_hash(prefix_value)
    for dir_hash, file_hash_list in hash_dict.items():
        for file_hash in file_hash_list:
            value = get_rev_digits_values(prefix_crc, suffix_value, file_hash)
            if value:
                results.setdefault(dir_hash, {})[file_hash] = value
    return results

def get_rev_digits_values(prefix_crc, suffix_value, final_crc):
    rev_patched_crc = rev_crc_32(bytes(suffix_value, encoding='ascii'), final_crc)
    rev_crc = prefix_crc ^ rev_patched_crc

    values = [(rev_crc & (0xFF << (i * 8))) >> (i * 8) for i in range(4)]

    for value in values:
        if not(0x30 <= value < 0x40):
            return None
    return ''.join(chr(c) for c in values)

def icons(dat_manager):
    icons_result_tree = {}

    # Data hash table for chara dat
    icon_cat_hash_table = dat_manager.get_category('ui').get_hash_table()

    icon_folder_prefix_crc = get_hash('ui/icon/')
    for dir_hash, dir_hash_table in icon_cat_hash_table.items():
        folder_value = get_rev_digits_values(icon_folder_prefix_crc, '00', dir_hash)
        if folder_value:
            folder_value = folder_value[0:3]
            dir_path = 'ui/icon/%s000' % folder_value
            file_prefix_crc = get_hash(folder_value[0:2])
            for file_hash in dir_hash_table.keys():
                file_value = get_rev_digits_values(file_prefix_crc, '.tex', file_hash)
                if file_value:
                    file_value = file_value[1:4]
                    icons_result_tree.setdefault(folder_value, {})[file_value] = '%s/%s%s.tex' % (dir_path, folder_value, file_value)
        else:
            for suffix in ['en', 'fr', 'de', 'ja', 'hq']:
                folder_value = get_rev_digits_values(icon_folder_prefix_crc, '00/%s' % suffix, dir_hash)
                if folder_value:
                    folder_value = folder_value[0:3]
                    dir_path = 'ui/icon/%s000/%s' % (folder_value, suffix)
                    file_prefix_crc = get_hash(folder_value[0:2])
                    for file_hash in dir_hash_table.keys():
                        file_value = get_rev_digits_values(file_prefix_crc, '.tex', file_hash)
                        if file_value:
                            file_value = file_value[1:4]
                            icons_result_tree.setdefault(folder_value, {}).setdefault(suffix, {})[file_value] = '%s/%s%s.tex' % (dir_path, folder_value, file_value)
    return icons_result_tree

def maps_icons(dat_manager):
    maps_icons_result_tree = {}
    for a in list(map(chr, range(ord('a'), ord('z') + 1))) + list(range(10)):
        for i in list(map(chr, range(ord('a'), ord('z') + 1))) + list(range(10)):
            for b in list(map(chr, range(ord('a'), ord('z') + 1))) + list(range(10)):
                for j in list(map(chr, range(ord('a'), ord('z') + 1))) + list(range(10)):
                    for k in range(100):
                        basename = '%s%s%s%s' % (a, i, b, j)
                        num = '%0.2d' % k
                        folder_path = 'ui/map/%s/%s/' % (basename, num)
                        if dat_manager.check_dir_existence(folder_path):
                            for suffix in ['_s', '_m', 'm_s', 'm_m', 'd']:
                                file_path = '%s%s%s%s.tex' % (folder_path, basename, num, suffix)
                                if dat_manager.check_file_existence(file_path):
                                    maps_icons_result_tree.setdefault(basename, {}).setdefault(num, []).append(file_path)
    for basename in ['world', 'region', 'default']:
        for k in range(100):
            num = '%0.2d' % k
            folder_path = 'ui/map/%s/%s/' % (basename, num)
            if dat_manager.check_dir_existence(folder_path):
                for suffix in ['_s', '_m', 'd']:
                    file_path = '%s%s%s%s.tex' % (folder_path, basename, num, suffix)
                    if dat_manager.check_file_existence(file_path):
                        maps_icons_result_tree.setdefault(basename, {}).setdefault(num, []).append(file_path)

    return maps_icons_result_tree

def models(dat_manager):
    models_result_tree = {}

    # Data hash table for chara dat
    chara_cat_hash_table = dat_manager.get_category('chara').get_hash_table()
    print('get models')

    attach_offset_search_folder_hash = get_hash('chara/xls/attachoffset')
    if attach_offset_search_folder_hash in chara_cat_hash_table:

        # Humans
        # Search for chara/xls/attachOffset/c%04d.atch

        prefix_crc = get_hash('c')
        for file_hash in chara_cat_hash_table[attach_offset_search_folder_hash].keys():
            print('Humans: ', file_hash)
            c_value = get_rev_digits_values(prefix_crc, '.atch', file_hash)
            if c_value:
                for part, suffix in [('face', 'fac'), ('hair', 'hir'), ('tail', 'til'), ('body', 'top')]:
                    for p in range(10000):
                        p_value = '%0.4d' % p
                        p_name = '%s%s' % (part[0], p_value)
                        file_path = 'chara/human/c%s/obj/%s/%s/model/c%s%s_%s.mdl' % (c_value, part, p_name, c_value, p_name, suffix)
                        if dat_manager.check_file_existence(file_path):
                            models_result_tree.setdefault('human', {}).setdefault(c_value, {}).setdefault(part, {})[p_value] = file_path

        # Demihumans
        # Search for chara/xls/attachOffset/d%04d.atch

        prefix_crc = get_hash('d')
        for file_hash in chara_cat_hash_table[attach_offset_search_folder_hash].keys():
            print('Demihumans: ', file_hash)
            d_value = get_rev_digits_values(prefix_crc, '.atch', file_hash)
            if d_value:
                for suffix in ['sho', 'dwn', 'glv', 'top', 'met']:
                    for e in range(10000):
                        e_value = '%0.4d' % e
                        e_name = 'e%s' % e_value
                        file_path = 'chara/demihuman/d%s/obj/equipment/%s/model/d%s%s_%s.mdl' % (d_value, e_name, d_value, e_name, suffix)
                        if dat_manager.check_file_existence(file_path):
                            models_result_tree.setdefault('demihuman', {}).setdefault(d_value, {})[e_value] = file_path

    # Search for .imc
    single_file_dirs = {}
    for dir_hash, dir_hash_table in chara_cat_hash_table.items():
        if len(dir_hash_table) == 1:
            for file_hash in dir_hash_table.keys():
                single_file_dirs[dir_hash] = [file_hash]

    file_matches = {}
    file_matches['b'] = get_rev_digits_values_matches('b', '.imc', single_file_dirs)
    file_matches['e'] = get_rev_digits_values_matches('e', '.imc', single_file_dirs)
    file_matches['a'] = get_rev_digits_values_matches('a', '.imc', single_file_dirs)

    # Monster/Weapon
    for cat_type in ['weapon', 'monster']:
        print('Monster/Weapon: ', cat_type)
        prefix_crc = get_hash('chara/%s/%s' % (cat_type, cat_type[0]))
        for dir_hash, dir_hash_table in file_matches['b'].items():
            for file_hash, b_name in dir_hash_table.items():
                cat_name = get_rev_digits_values(prefix_crc, '/obj/body/b%s' % b_name, dir_hash)
                if cat_name:
                    file_path = 'chara/%s/%s%s/obj/body/b%s/model/%s%sb%s.mdl' % (cat_type, cat_type[0], cat_name, b_name, cat_type[0], cat_name, b_name)
                    if dat_manager.check_file_existence(file_path):
                        models_result_tree.setdefault(cat_type, {}).setdefault(cat_name, {})[b_name] = file_path

    # Equipment/Accessory
    for cat_type in ['equipment', 'accessory']:
        print('Equipment/Accessory: ', cat_type)
        prefix_crc = get_hash('chara/%s/%s' % (cat_type, cat_type[0]))
        for dir_hash, dir_hash_table in file_matches[cat_type[0]].items():
            print('- hash: ', dir_hash)
            for file_hash, b_name in dir_hash_table.items():
                value = get_rev_digits_values(prefix_crc, '', dir_hash)
                print('- value: ', value)
                if value:
                    for suffix in ['ril', 'rir', 'wrs', 'nek', 'ear', 'sho', 'dwn', 'glv', 'top', 'met']:
                        print('- suffix: ', suffix)
                        for c in range(10000):
                            c_value = '%0.4d' % c
                            c_name = 'c%s' % c_value
                            file_path = 'chara/%s/%s%s/model/%s%s%s_%s.mdl' % (cat_type, cat_type[0], value, c_name, cat_type[0], value, suffix)
                            print('- file_path: ', file_path)
                            if dat_manager.check_file_existence(file_path):
                                models_result_tree.setdefault(cat_type, {}).setdefault(value, {})[c_value] = file_path

    return models_result_tree
