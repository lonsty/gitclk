#! /usr/bin/python3
# @Author: allen
# @Date: Nov 29 11:07 2019
import configparser
import json
import locale
import os
import sys
from collections import OrderedDict

import click
from dialog import Dialog

__author__ = 'Allen Shaw'
__version__ = '0.1.0'
CONFIG = os.path.expanduser('~/.config/git-clk/config/config.json')
TEMPERATE_CONFIG = os.path.expanduser('~/.config/git-clk/config/temperate.json')
GIT_CONFIG = '.git/config'


def load_settings(file):
    with open(file, 'r') as f:
        git_platforms = json.loads(f.read())
    return git_platforms


def save_settings(file, config):
    with open(file, 'w') as f:
        f.write(json.dumps(config, ensure_ascii=False, indent=4))


def set_config():
    git_platforms = load_settings(CONFIG)
    all_platforms = git_platforms.get('platforms')

    locale.setlocale(locale.LC_ALL, '')
    d = Dialog(dialog="dialog")

    platforms_to_enable = [(p, '', all_platforms.get(p).get('enabled')) for p in all_platforms.keys()]
    code, enabled_plats = d.checklist("Which git platforms do you want to use?",
                                      choices=platforms_to_enable,
                                      title="Enable Git Platforms",
                                      height=20, width=75, list_height=15)
    if code != d.OK:
        return

    enabled_to_default = [(p, '', p == git_platforms.get('default_plat')) for p in enabled_plats]
    code, default_palt = d.radiolist("Please select a default platforms:",
                                     choices=enabled_to_default,
                                     title="Set Default Platform",
                                     height=20, width=75, list_height=15)
    if code != d.OK:
        return

    enabled_to_ignore = [(p, '', all_platforms.get(p).get('reset_ignored')) for p in enabled_plats]
    code, ignored_plats = d.checklist("Please select platforms to ignore when reset？",
                                      choices=enabled_to_ignore,
                                      title="Select Ignore Platforms",
                                      height=20, width=75, list_height=15)
    if code != d.OK:
        return

    git_platforms['default'] = default_palt
    for p in all_platforms:
        git_platforms['platforms'][p]['enabled'] = True if p in enabled_plats else False
        git_platforms['platforms'][p]['reset_ignored'] = True if p in ignored_plats else False

    save_settings(CONFIG, git_platforms)


def set_remotes_config(add_all, repository):
    if not os.path.isfile(GIT_CONFIG):
        print('Exit: current working directory is not the root directory of repository!')
        return

    git_platforms = load_settings(CONFIG)

    platforms = git_platforms.get('platforms')
    default_plat = git_platforms.get('default_plat')
    sections_ignored = [f'remote "{p}"' for p in platforms if platforms.get(p).get('reset_ignored') is True]

    remotes = {
        f'remote "{p}"': {
            'url': platforms.get(p).get(platforms.get(p).get('prefer_url')) \
                .format(user=platforms.get(p).get('user'), repo=repository),
            'fetch': '+refs/heads/*:refs/remotes/{remote_name}/*'.format(remote_name=p)
        }
        for p in [p for p in platforms if platforms[p].get('enabled') is True]
    }
    remotes['remote "origin"'] = {
        'url': platforms.get(default_plat).get(platforms.get(default_plat).get('prefer_url')) \
            .format(user=platforms.get(default_plat).get('user'), repo=repository),
        'fetch': '+refs/heads/*:refs/remotes/origin/*'
    }

    ord_remotes = OrderedDict(sorted(remotes.items()))
    git_config_temperate = OrderedDict(sorted(load_settings(TEMPERATE_CONFIG).items()))
    git_config_temperate.update(ord_remotes)

    config = configparser.ConfigParser()
    config.read(GIT_CONFIG)

    if add_all is not True:
        for section in sections_ignored:
            try:
                for k, v in config[section].items():
                    git_config_temperate[section][k] = v
            except KeyError:
                pass

    for section in config.sections():
        config.remove_section(section)

    for section, kvs in git_config_temperate.items():
        for k, v in kvs.items():
            try:
                config.set(section, '\t' + k.strip(), v)
            except configparser.NoSectionError:
                config.add_section(section)
                config.set(section, '\t' + k.strip(), v)

    with open(GIT_CONFIG, 'w') as cf:
        config.write(cf)


@click.group(help='Git remotes setting.')
def cli():
    ...


@click.command('config', help='Configure the git platforms.')
@click.option('-e', '--edit', 'edit', is_flag=True, default=False, help='Edit the config file.')
def config(edit):
    if edit is True:
        os.system(f'vi {CONFIG}')
        sys.exit(0)

    set_config()


@click.command('set', help='Add remotes setting to git config.')
@click.option('-a', '--all', 'add_all', is_flag=True, default=False, show_default=True,
              help='Add all remotes include ignored.')
@click.option('-n' , '--repository-name', 'repo', required=True, help='The repository name.')
def set_remotes(add_all, repo):
    set_remotes_config(add_all, repo)


cli.add_command(config)
cli.add_command(set_remotes)


if __name__ == '__main__':
    cli()
