# -*- coding: utf-8 -*-

import argparse
import logging
from pprint import pformat
import sys
from os import path, makedirs
from configparser import SafeConfigParser
import json

from xivdm.logging_utils import set_logging
from xivdm.crc32_utils import crc_32, rev_crc_32
from xivdm.language import get_language_name
from xivdm.dat.Manager import Manager as DatManager, get_hashes
from xivdm.exd.Manager import Manager as ExdManager
from xivdm.exd.Category import Category as ExdCategory
from xivdm.exd.links_analyzer import analyze_links
from xivdm.view.Manager import Manager as ViewManager
from xivdm.json.Manager import Manager as JsonManager
from xivdm.gen.Manager import Manager as GenManager
from xivdm.patch.Manager import Manager as PatchManager
from xivdm.model.Texture import Texture

def extract_all(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))

    output_path = path.join(conf.get('output', 'path'), 'all')

    for category_name in dat_manager.get_categories():
        category = dat_manager.get_category(category_name)

        output_cat_path = path.join(output_path, category_name)

        for dir_hash in category.get_hash_table().keys():
            output_dir_path = path.join(output_cat_path, '%0.8X' % dir_hash)

            if not path.exists(output_dir_path):
                makedirs(output_dir_path)

            for file_hash in category.get_dir_hash_table(dir_hash).keys():
                output_file_path = path.join(output_dir_path, '%0.8X' % file_hash)

                file_data = category.get_file(dir_hash, file_hash)

                with open(output_file_path, 'wb') as file_handle:
                    file_handle.write(file_data.getvalue())

def extract_category(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))

    category = dat_manager.get_category(args.name)
    output_path = path.join(conf.get('output', 'path'), 'cat', args.name)

    for dir_hash in category.get_hash_table().keys():
        output_dir_path = path.join(output_path, '%0.8X' % dir_hash)

        if not path.exists(output_dir_path):
            makedirs(output_dir_path)

        for file_hash in category.get_dir_hash_table(dir_hash).keys():
            output_file_path = path.join(output_dir_path, '%0.8X' % file_hash)

            file_data = category.get_file(dir_hash, file_hash)

            with open(output_file_path, 'wb') as file_handle:
                file_handle.write(file_data.getvalue())

def extract_folder(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))

    output_path = path.join(conf.get('output', 'path'), 'folder', args.name)
    category = dat_manager.get_category_from_filename(args.name)

    (dir_hash, _) = get_hashes(args.name)

    dir_hash_table = category.get_dir_hash_table(dir_hash)

    if not path.exists(output_path):
        makedirs(output_path)

    for file_hash in dir_hash_table.keys():
        output_file_path = path.join(output_path, '%0.8X' % file_hash)

        file_data = category.get_file(dir_hash, file_hash)

        with open(output_file_path + '.dds', 'wb') as file_handle:
            file_handle.write(Texture(file_data).get_as_dds().getvalue())

        # with open(output_file_path, 'wb') as file_handle:
        #     file_handle.write(file_data.getvalue())

def extract_file(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))

    output_file_path = path.join(conf.get('output', 'path'), 'file', args.name)
    file_data = dat_manager.get_file(args.name)

    if not path.exists(path.dirname(output_file_path)):
        makedirs(path.dirname(output_file_path))

    if output_file_path.endswith('.tex'):
        with open(output_file_path[:-3] + 'dds', 'wb') as file_handle:
            file_handle.write(Texture(file_data).get_as_dds().getvalue())
    else:
        with open(output_file_path, 'wb') as file_handle:
            file_handle.write(file_data.getvalue())

def extract_exd(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    exd_manager = ExdManager(dat_manager)

    output_path = path.join(conf.get('output', 'path'), 'exd')

    for category_name in exd_manager.get_categories():
        data = exd_manager.get_category(category_name).get_csv()
        for language, csv in data.items():
            output_file_path = path.join(
                output_path,
                'exd/%s_%s.exd' % (category_name, get_language_name(language)))

            if not path.exists(path.dirname(output_file_path)):
                makedirs(path.dirname(output_file_path))

            with open(output_file_path, 'w') as file_handle:
                for line in csv:
                    file_handle.write(line)
                    file_handle.write('\n')

def extract_exh(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    exd_manager = ExdManager(dat_manager)

    output_path = path.join(conf.get('output', 'path'), 'exh')

    for category_name in exd_manager.get_categories():
        struct_def = exd_manager.get_category(category_name).get_struct_def()
        output_file_path = path.join(
            output_path,
            'exd/%s.exh' % category_name)

        if not path.exists(path.dirname(output_file_path)):
            makedirs(path.dirname(output_file_path))

        with open(output_file_path, 'w') as file_handle:
            for line in struct_def:
                file_handle.write(line)
                file_handle.write('\n')

def extract_view(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    exd_manager = ExdManager(dat_manager)
    view_manager = ViewManager(exd_manager)

    output_path = path.join(conf.get('output', 'path'), 'json')

    view_names = None
    if args.name:
        view_names = args.name.split(',')

    if not view_names:
        view_names = view_manager.get_mappings()

    for view_name in view_names:
        logging.info("Processing: %s", view_name)

        output_file_path = path.join(output_path, '%s.json' % (view_name))

        if not path.exists(path.dirname(output_file_path)):
            makedirs(path.dirname(output_file_path))

        json_output = view_manager.get_json(view_name);

        logging.info(json_output)

        print("length:", len(json_output), "- output:", output_file_path)

        with open(output_file_path, 'w') as file_handle:
            file_handle.write(
                json.dumps(
                    json_output,
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': ')))

def extract_json(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    exd_manager = ExdManager(dat_manager)
    json_manager = JsonManager(exd_manager)

    output_path = path.join(conf.get('output', 'path'), 'json_lists')

    json_names = None
    if args.name:
        json_names = args.name.split(',')

    if not json_names:
        json_names = json_manager.get_mappings()

    for json_name in json_names:
        logging.info("Processing: %s", json_name)

        output_file_path = path.join(output_path, '%s.json' % (json_name))

        if not path.exists(path.dirname(output_file_path)):
            makedirs(path.dirname(output_file_path))

        json_output = json_manager.get_json(json_name);

        logging.info(json_output)

        print("length:", len(json_output), "- output:", output_file_path)

        with open(output_file_path, 'w') as file_handle:
            file_handle.write(
                json.dumps(
                    json_output,
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': ')))

def walk_gen(dat_manager, node, output_path):
    if type(node) == dict:
        for key, value in node.items():
            walk_gen(dat_manager, value, output_path)
    elif type(node) == list:
        for value in node:
            walk_gen(dat_manager, value, output_path)
    elif type(node) == str:
        output_file_path = path.join(output_path, node)
        if not path.exists(path.dirname(output_file_path)):
            makedirs(path.dirname(output_file_path))
        data = dat_manager.get_file(node)
        if output_file_path.endswith('.tex'):
            with open(output_file_path[:-3] + 'dds', 'wb') as file_handle:
                item = Texture(data).get_as_dds()

                if hasattr(item, 'getvalue'):
                    file_handle.write(Texture(data).get_as_dds().getvalue())
        else:
            with open(output_file_path, 'wb') as file_handle:
                file_handle.write(data.getvalue())

def extract_gen(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    gen_manager = GenManager(dat_manager)
    output_path = path.join(conf.get('output', 'path'), 'gen', args.name)
    walk_gen(dat_manager, gen_manager.get_category(args.name), output_path)

def analyze_exd_links(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    exd_manager = ExdManager(dat_manager)

    source_categories = None
    destination_categories = None

    if args.source:
        source_categories = args.source.split(',')
    if args.destination:
        destination_categories = args.destination.split(',')

    results = analyze_links(exd_manager, int(args.hits_limit), source_categories, destination_categories)
    logging.info(pformat(results))
    print(pformat(results))

def extract_music(args, conf):
    dat_manager = DatManager(conf.get('game', 'path'))
    exd_manager = ExdManager(dat_manager)
    output_path = path.join(conf.get('output', 'path'), 'music')

    tried = 0
    completed = 0

    for data in exd_manager.get_category('BGM').get_ln_data(0).values():
        print('----------')
        tried = tried + 1
        file_path = data[0].decode('utf-8')

        if file_path == '':
            continue

        output_file_path = path.join(output_path, file_path)

        if not path.exists(path.dirname(output_file_path)):
            makedirs(path.dirname(output_file_path))

        try:
            print('Song:', file_path)
            file_data = dat_manager.get_file(file_path)
        except:
            continue

        if hasattr(file_data, 'getvalue'):
            completed = completed + 1
            with open(output_file_path, 'wb') as file_handle:
                file_handle.write(file_data.getvalue())
        else:
            continue

    print('tried', tried, 'completed', completed)

def patch_version(args, conf):
    patch_manager = PatchManager(conf.get('game', 'path'))

    for patchable_name in patch_manager.get_patchables():
        print('%s: %s' % (patchable_name, patch_manager.get_patchable(patchable_name).get_version()))

def patch_check(args, conf):
    patch_manager = PatchManager(path.join(conf.get('game', 'path'), '../ffxiv_data_test'))
    print('%s: %s' % ('boot', patch_manager.get_patchable('boot').check()))

def patch_update(args, conf):
    patch_manager = PatchManager(path.join(conf.get('game', 'path'), '../ffxiv_data_test'))
    patch_manager.get_patchable('boot').update()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='xivdm command line interface')
    subparsers = parser.add_subparsers(title='sub modules')

    ######################
    # Extract sub module #
    ######################
    extract_parser = subparsers.add_parser('extract', help='extract files')
    extract_subparsers = extract_parser.add_subparsers(title='type')

    # Extract all
    extract_all_parser = extract_subparsers.add_parser('all', help='extract all files')
    extract_all_parser.set_defaults(callback=extract_all)

    # Extract category
    extract_category_parser = extract_subparsers.add_parser('category', help='extract all files for category')
    extract_category_parser.add_argument('-n', '--name', required=True)
    extract_category_parser.set_defaults(callback=extract_category)

    # Extract folder
    extract_folder_parser = extract_subparsers.add_parser('folder', help='extract all files for folder')
    extract_folder_parser.add_argument('-n', '--name', required=True)
    extract_folder_parser.set_defaults(callback=extract_folder)

    # Extract file
    extract_file_parser = extract_subparsers.add_parser('file', help='extract a single file')
    extract_file_parser.add_argument('-n', '--name')
    extract_file_parser.set_defaults(callback=extract_file)

    # Extract exd
    extract_exd_parser = extract_subparsers.add_parser('exd', help='extract exd files as csv')
    extract_exd_parser.set_defaults(callback=extract_exd)

    # Extract exh
    extract_exh_parser = extract_subparsers.add_parser('exh', help='extract exh files as text')
    extract_exh_parser.set_defaults(callback=extract_exh)

    # Extract view
    extract_view_parser = extract_subparsers.add_parser('view', help='extract view files as json')
    extract_view_parser.add_argument('-n', '--name')
    extract_view_parser.set_defaults(callback=extract_view)

    # Extract json
    extract_json_parser = extract_subparsers.add_parser('json', help='extract json lists')
    extract_json_parser.add_argument('-n', '--name')
    extract_json_parser.set_defaults(callback=extract_json)

    # Extract music
    extract_music_parser = extract_subparsers.add_parser('music', help='extract music files')
    extract_music_parser.set_defaults(callback=extract_music)

    # Extract gen
    extract_gen_parser = extract_subparsers.add_parser('gen', help='extract gen files')
    extract_gen_parser.add_argument('-n', '--name', required=True)
    extract_gen_parser.set_defaults(callback=extract_gen)

    ######################
    # Analyze sub module #
    ######################
    analyze_parser = subparsers.add_parser('analyze', help='analyze stuff')
    analyze_subparsers = analyze_parser.add_subparsers(title='type')

    # Analyze exd_links category
    analyze_exd_links_parser = analyze_subparsers.add_parser('exd_links', help='analyze exd_links')
    analyze_exd_links_parser.add_argument('-s', '--source')
    analyze_exd_links_parser.add_argument('-d', '--destination')
    analyze_exd_links_parser.add_argument('-l', '--hits_limit')
    analyze_exd_links_parser.set_defaults(callback=analyze_exd_links)

    ######################
    # Patch sub module   #
    ######################
    patch_parser = subparsers.add_parser('patch', help='handle patch')
    patch_subparsers = patch_parser.add_subparsers(title='type')

    # Patch version
    patch_version_parser = patch_subparsers.add_parser('version', help='displays versions of patchables')
    patch_version_parser.set_defaults(callback=patch_version)

    # Patch check
    patch_check_parser = patch_subparsers.add_parser('check', help='displays checks of patchables')
    patch_check_parser.set_defaults(callback=patch_check)

    # Patch check
    patch_update_parser = patch_subparsers.add_parser('update', help='updates of patchables')
    patch_update_parser.set_defaults(callback=patch_update)

    args = parser.parse_args()

    config = SafeConfigParser()
    config.readfp(open('config.cfg'))

    set_logging(config.get('logs', 'path'), 'xivdmcli')

    logging.info('Executing command: ' + str(sys.argv))

    if not hasattr(args, 'callback'):
        logging.error('Command-line parsing error.')
        parser.print_help()
    else:
        args.callback(args, config)
