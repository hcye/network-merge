import subprocess

import requests

from format_txt import *


# ---1---
# 1.15.0.0-1.15.255.255
def clear_repeat_include_networks(lines, sep):
    merge = merge_networks()
    pre_deal_lines = merge.pre_proc(lines, sep)
    duplicat_lines = merge.get_include(pre_deal_lines, sep)
    target_lines = merge.remove_repeat_lines(duplicat_lines, pre_deal_lines)
    repeate_lines = merge.find_repeat_lines(target_lines)
    target_lines = merge.remove_repeat_lines(repeate_lines, target_lines)
    return target_lines


#  old merge old data
# ---2---
# 1.15.0.0-1.15.255.255
def merge(origin_lines):
    merge = merge_networks()
    merge.sort_1(origin_lines, '-')
    tg_lines = clear_repeat_include_networks(merge.merged_networks, '-')
    formated_lines = merge.yanma_1(tg_lines, '-')
    lines = merge.yanma_4(formated_lines, '-')
    return lines


def fo():
    with open('res/route.txt', 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    fp_1 = open('ips_1.txt', 'r+', encoding='utf-8')
    for i in lines:
        if i.strip().replace('\n', ''):
            if '\n' in i:
                fp_1.write(i.replace(' ', '-'))
            else:
                fp_1.write(i.replace(' ', '-') + '\n')


def format_ad():
    with open('add-route.sh', 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    new_lines = []
    for i in lines:
        i = i.replace('\n', '<br/>\n')
        new_lines.append(i)
    with open('add-route1.sh', 'w', encoding='utf-8') as fp:
        fp.writelines(new_lines)


# 192.168.8.0 255.255.255.0
def remove_255_lines(lines):
    new_lines = []
    for i in lines:
        if '255.255.255.0' not in i:
            new_lines.append(i)
    return new_lines


def final_work(lines):
    mg = merge_networks()
    lines = mg.yanma_1(lines, '-')
    lines = remove_255_lines(lines)
    lines = mg.yanma_3(lines, '-')
    correct_lines = mg.remove_error_lines(lines)
    mg.add_route_cli(correct_lines,1)
    mg.del_routes_cli_by_addfile(1)


# 192.168.8.0/24
if __name__ == '__main__':
    with open('ips_1.txt', 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    lines = clear_repeat_include_networks(lines, '-')
    lines = merge(lines)
    final_work(lines)

    # mg = merge_networks()
    # lines = clear_repeat_include_networks(lines, ' ')
    # print(f'{lines}\n\n')
    # lines = mg.yanma_1(lines, '-')
    # new_lines = []
    # for i in lines:
    #     if '255.255.255.0' not in i:
    #         new_lines.append(i)
    # lines = mg.yanma_3(new_lines, '-')
    # # mg.add_route_cli(lines)
