#! /usr/bin/python3
# @Author: allen
# @Date: Nov 29 11:07 2019
import configparser
import json
import locale
import os
import re
import sys
from collections import OrderedDict

import click
from dialog import Dialog

__author__ = 'Allen Shaw'
__version__ = '0.1.1'
CONFIG = os.path.expanduser('~/.config/gitclk/config/config.json')
TEMPERATE_CONFIG = os.path.expanduser('~/.config/gitclk/config/temperate.json')


def load_settings(file):
    with open(file, 'r') as f:
        git_platforms = json.loads(f.read())
    return git_platforms


def save_settings(file, config):
    with open(file, 'w') as f:
        f.write(json.dumps(config, ensure_ascii=False, indent=4))


def check_repository():
    dirs = os.getcwd().split(r'/')
    for i in range(len(dirs), 0, -1):
        repo = f"{'/'.join(dirs[:i])}/.git"
        if os.path.isdir(repo):
            return os.path.join(repo, 'config')
    return False


def set_config():
    git_platforms = load_settings(CONFIG)
    all_platforms = git_platforms.get('platforms')

    try:
        locale.setlocale(locale.LC_ALL, '')
    except Exception:
        pass
    d = Dialog(dialog="dialog")

    platforms_to_enable = [(p, '', all_platforms.get(p).get('enabled')) for p in all_platforms.keys()]
    code, enabled_plats = d.checklist("Git platforms to use ...",
                                      choices=platforms_to_enable,
                                      title="Enable Git Platforms",
                                      height=20, width=75, list_height=15)
    if code != d.OK:
        return

    proxies_to_disabled = [(p, '', all_platforms.get(p).get('prefer_ssh')) for p in enabled_plats]
    code, ssh_plats = d.checklist("Platforms to use SSH ...",
                                  choices=proxies_to_disabled,
                                  title="Select Platforms Use SSH",
                                  height=20, width=75, list_height=15)
    if code != d.OK:
        return

    enabled_to_ignore = [(p, '', all_platforms.get(p).get('reset_ignored')) for p in enabled_plats]
    code, ignored_plats = d.checklist("Platforms to ignore when reset ...",
                                      choices=enabled_to_ignore,
                                      title="Select Ignore Platforms",
                                      height=20, width=75, list_height=15)
    if code != d.OK:
        return

    proxies_to_disabled = [(p, '', all_platforms.get(p).get('no_proxy')) for p in enabled_plats]
    code, noproxy_plats = d.checklist("Platforms do not require proxy ...",
                                      choices=proxies_to_disabled,
                                      title="Select no-proxy Platforms",
                                      height=20, width=75, list_height=15)
    if code != d.OK:
        return

    enabled_to_default = [(p, '', p == git_platforms.get('default_plat')) for p in enabled_plats]
    code, default_palt = d.radiolist("Default platforms ...",
                                     choices=enabled_to_default,
                                     title="Set Default Platform",
                                     height=20, width=75, list_height=15)
    if code != d.OK:
        return

    git_platforms['default_plat'] = default_palt
    for p in all_platforms:
        git_platforms['platforms'][p]['prefer_ssh'] = True if p in ssh_plats else False
        git_platforms['platforms'][p]['enabled'] = True if p in enabled_plats else False
        git_platforms['platforms'][p]['reset_ignored'] = True if p in ignored_plats else False
        git_platforms['platforms'][p]['no_proxy'] = True if p in noproxy_plats else False

    save_settings(CONFIG, git_platforms)

    with open(GIT_CONFIG) as f:
        config = f.read()
    find_url = re.search(r'url\s*=\s*.*?\n', config)
    url = find_url.group() if find_url else ''
    find_repo = re.search(r'(?<=(/))[\w-]*?(?=(.git\n|\n))', url)
    ori_repo = find_repo.group() if find_repo else ''

    code, repo = d.inputbox('Enter a repository ...\n\nThen click <OK> to apply changes, <Cancel> to exit.',
                            init=ori_repo,
                            height=20, width=75)
    if (code == d.OK) and repo:
        set_remotes_config(False, repo)


def set_remotes_config(set_all, repository):
    git_platforms = load_settings(CONFIG)

    platforms = git_platforms.get('platforms')
    default_plat = git_platforms.get('default_plat')
    sections_ignored = [f'remote "{p}"' for p in platforms if platforms.get(p).get('reset_ignored') is True]

    remotes = {
        f'remote "{p}"': {
            'url': platforms.get(p).get('ssh' if platforms.get(p).get('prefer_ssh') else 'http') \
                .format(user=platforms.get(p).get('user'), repo=repository),
            'fetch': '+refs/heads/*:refs/remotes/{remote_name}/*'.format(remote_name=p)
        }
        for p in [p for p in platforms if platforms[p].get('enabled') is True]
    }

    # set no proxy
    for p in [p for p in platforms if platforms[p].get('enabled') is True]:
        if platforms[p].get('no_proxy') is True:
            remotes[f'remote "{p}"']['proxy'] = '""'

    remotes['remote "origin"'] = {
        'url': platforms.get(default_plat).get('ssh' if platforms.get(p).get('prefer_ssh') else 'http') \
            .format(user=platforms.get(default_plat).get('user'), repo=repository),
        'fetch': '+refs/heads/*:refs/remotes/origin/*'
    }

    ord_remotes = OrderedDict(sorted(remotes.items()))
    git_config_temperate = OrderedDict(sorted(load_settings(TEMPERATE_CONFIG).items()))
    git_config_temperate.update(ord_remotes)

    config = configparser.ConfigParser()
    config.read(GIT_CONFIG)

    if set_all is not True:
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


@click.command('set', help='Set remotes setting to git config.')
@click.option('-a', '--all', 'set_all', is_flag=True, default=False, show_default=True,
              help='Set all remotes include ignored.')
@click.option('-n', '--repository-name', 'repo', required=True, help='The repository name.')
def set_remotes(set_all, repo):
    set_remotes_config(set_all, repo)


cli.add_command(config)
cli.add_command(set_remotes)

if __name__ == '__main__':
    GIT_CONFIG = check_repository()
    if GIT_CONFIG is False:
        click.echo('fatal: not in a git directory')
        sys.exit(1)

    cli()
