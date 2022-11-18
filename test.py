import math

import requests

from format_txt import *

mg = merge_networks()

def main(origin_lines):

    fp = open('ips.txt', 'r', encoding='utf-8')
    origin_lines = fp.readlines()
    origin_lines = mg.pre_proc(origin_lines)
    fp.close()

    single_lines = mg.remove_routes(origin_lines)
    sorted_lines = mg.sort_1(single_lines)

    lines = mg.get_start_end(sorted_lines)
    amanded_lines = mg.amend_error_network(lines)
    mg.merged_networks = mg.merge(amanded_lines)

    single_lines = mg.remove_routes(mg.merged_networks)
    lines = mg.yanma_3(mg.yanma_2(single_lines))
    mg.add_route_cli(lines, '')
    mg.del_routes_cli_by_addfile('')


def test_merge():
    rep = mg.find_repeat_lines(origin_lines)
    res = mg.remove_repeat_lines(rep, origin_lines)
    lines = mg.yanma_3(mg.yanma_2(res))
    mg.add_route_cli(lines, '')
    mg.del_routes_cli_by_addfile('')


def cal_mask_edge():
    with open('mask_edge', 'w', encoding='utf-8') as fp:
        base = 0
        for i in range(8, 25):
            tmp = []
            mask_yu = 8 - int(i % 8)
            if mask_yu == 8:
                tmp.append('0')
            else:
                base = math.pow(2, mask_yu)
                sum = 0
                while sum < 256:
                    tmp.append(str(int(sum)))
                    sum = sum + base
            gateway_edges = ','.join(tmp) + ',256'
            fp.write(f'{i}-{gateway_edges}\n')


def merge(lines):
    target_lines = []
    mask_edge_dict = {}
    fp = open('mask_edge', 'r', encoding='utf-8')
    all_lines = fp.readlines()
    fp.close()
    for n in all_lines:
        n_s = n.split('-')
        mask_edge_dict[n_s[0]] = n_s[1].split(',')
    separetor = mg.get_sep(lines)
    for i in lines:
        if i.replace('\n', '').strip():
            start = i.split(separetor)[0]
            end = i.split(separetor)[1].replace('\n', '')
            starts = start.split('.')
            ends = end.split('.')
            if mg.get_head(start, 2) == \
                    mg.get_head(end, 2):
                head_num = 2
                if starts[head_num] == ends[head_num] or (starts[head_num] == '0' and ends[head_num] == '255'):
                    target_lines.append(i)
                    continue

            else:
                head_num = 1
            res = cal_start_end(i.split(separetor), mask_edge_dict, head_num, separetor)
            print(res, i)
            target_lines.append(res)
    return target_lines


def cal_start_end(item, mask_edge_dict, head_num, sep):
    item_start = item[0].split('.')
    item_end = item[1].split('.')
    start_num_origin = item_start[head_num]
    end_num_origin = item_end[head_num]
    if head_num == 1:
        mask_start = 15
        while mask_start >= 8:
            range_list = mask_edge_dict.get(str(mask_start))
            for i in range(0, len(range_list) - 1):
                if int(range_list[i]) <= int(start_num_origin) and int(range_list[i + 1]) >= int(end_num_origin):
                    item_start[head_num] = range_list[i].replace('\n', '')
                    item_end[head_num] = str(int(range_list[i + 1].replace('\n', '')) - 1)
                    new_item_start = '.'.join(item_start)
                    new_item_end = '.'.join(item_end)
                    return f'{new_item_start}{sep}{new_item_end}'
            mask_start = mask_start - 1
    if head_num == 2:
        mask_start = 23
        while mask_start >= 16:
            range_list = mask_edge_dict.get(str(mask_start))
            for i in range(0, len(range_list) - 1):
                if int(range_list[i]) <= int(start_num_origin) and int(range_list[i + 1]) > int(end_num_origin):
                    item_start[head_num] = range_list[i].replace('\n', '')
                    item_end[head_num] = str(int(range_list[i + 1].replace('\n', '')) - 1)
                    new_item_start = '.'.join(item_start)
                    new_item_end = '.'.join(item_end)
                    return f'{new_item_start}{sep}{new_item_end}'
            mask_start = mask_start - 1
        print('find error' + '-'.join(item))

    # print(start_num_origin, end_num_origin)


# remove_repeate_lines(origin_lines)
# lines=mg.yanma_3(mg.yanma_2(remove_include_lines()))
# mg.add_route_cli(lines,'')
# mg.del_routes_cli_by_addfile('')
if __name__ == '__main__':
    # sorted_lines = mg.sort_1(origin_lines)
    # big_ranges = mg.get_big_range(sorted_lines)
    # with open('big_ranges', 'w', encoding='utf-8') as fp:
    #     for i in big_ranges:
    #         fp.write(f'{i}\n')
    # main(origin_lines)
    mg.add_routes_win_by_addfile('')
