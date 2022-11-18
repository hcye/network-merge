# --*-- coding:utf-8 --*--
import math
import subprocess

new_lines = []


class merge_networks:
    merged_networks = []
    continus_networks = []

    def get_sep(self, lines):
        if len(lines) > 0:
            if '-' in lines[0]:
                return '-'
            elif ' ' in lines[0]:
                return ' '
        else:
            return ''

    def pre_proc(self, lines):
        sep = self.get_sep(lines)
        new_lines = []
        for i in lines:
            if i:
                i_s = i.replace('\n', '').strip().split(sep)
                if len(i_s) < 2:
                    continue
                starts = i_s[0].split('.')
                ends = i_s[1].split('.')
                starts[3] = '0'
                ends[3] = '255'
                if starts[1] != ends[1]:
                    starts[2] = '0'
                    ends[2] = '255'
                start = '.'.join(starts)
                end = '.'.join(ends)
                new_lines.append(f'{start}{sep}{end}')
        return new_lines

    # 192.168.8.0/24     ->192.168.8.0  255.255.255.0
    def yanma(self, lines):
        for i in lines:
            if i and '/' in i:
                i_s = i.split('/')
                mask_yan = int(i_s[1].replace('\n', ''))
                num_255 = int(mask_yan / 8)
                tail = int(mask_yan % 8)
                str_head = ''
                if tail == 0:
                    str_tail = '0'
                else:
                    str_tail = 256 - int(math.pow(2, 8 - tail))
                for i in range(0, num_255):
                    str_head = str_head + "255."

                mask_num = str_head + str(str_tail)
                for j in range(0, 4 - len(mask_num.split('.'))):
                    mask_num = mask_num + '.0'

                #            route_line = f'route {i_s[0]} {mask_num} net_gateway \n'
                route_line = f'{i_s[0]} {mask_num}\n'
                new_lines.append(route_line)
        return new_lines

    # 192.168.8.0 192.168.8.255   ->192.168.8.0  255.255.255.0
    def yanma_1(self, lines):
        separator = self.get_sep(lines)
        lines = self.pre_proc(lines)
        for i in lines:
            i_s = []
            for k in i.strip().split(separator):
                if k.strip():
                    i_s.append(k.replace('\n', ''))
            if not i_s:
                continue
            start = i_s[0]
            end = i_s[1]
            starts = start.split('.')
            ends = end.split('.')
            # 1.28.172.0 1.30.39.255
            if starts[0] == ends[0]:
                starts[1]
            starts[3] = '0'
            ends[3] = '255'
            mask = ''
            for j in range(0, 4):
                if ends[j] == starts[j]:
                    mask = mask + '255.'
                    continue
                if ends[j] == '255' and starts[j] == '0':
                    mask = mask + '0.'
                    continue
                else:
                    for m in range(1, 9):
                        if math.pow(2, m) == (int(ends[j]) + 1) - int(starts[j]):
                            break
                    mask = mask + str(int(256 - math.pow(2, m))) + '.'
            mask_list = []
            for r in mask.split('.'):
                if r.strip():
                    mask_list.append(r)
            target_mask = '.'.join(mask_list)
            route_line = f'{start}{separator}{target_mask}'
            new_lines.append(route_line)
        return new_lines

    # 192.168.8.0 192.168.8.255   ->192.168.8.0 255.255.255.0'
    def yanma_2(self, lines):
        separator = self.get_sep(lines)
        for m in lines:
            start = m.split(separator)[0].strip()
            end = m.split(separator)[1].strip()
            starts = start.split('.')
            ends = end.split('.')
            mask = ''
            for j in range(0, 4):
                if ends[j] == starts[j]:
                    mask = mask + '255.'
                    continue
                if ends[j] == '255' and starts[j] == '0':
                    mask = mask + '0.'
                    continue
                else:
                    for m in range(1, 9):
                        if math.pow(2, m) == (int(ends[j]) + 1) - int(starts[j]):
                            break
                    mask = mask + str(int(256 - math.pow(2, m))) + '.'
            mask_list = []
            for r in mask.split('.'):
                if r.strip():
                    mask_list.append(r)
            target_mask = '.'.join(mask_list)
            route_line = f'{start} {target_mask}'
            if '255.0.0.0' in target_mask:
                print(m)
            new_lines.append(route_line)
        return new_lines

    def remove_routes(self,origin_lines):
        repeat_lines = self.find_repeat_lines(origin_lines)
        new_lines = self.remove_repeat_lines(repeat_lines, origin_lines)
        includes = self.get_include_lines(new_lines)
        single_lines = self.remove_include_lines(includes, new_lines)
        return single_lines
    # 192.168.0.0 255.255.255.0 -> 192.168.0.0/24
    def yanma_3(self, lines):
        with open('/root/PycharmProjects/format_txt/res/yanma_duizhao.txt', 'r', encoding='utf-8') as fp_tmp:
            tmp_lines = fp_tmp.readlines()
        target_lines = []
        for i in lines:
            i = i.replace('\n', '').strip()
            if i:
                if '-' in i:
                    separator = '-'
                else:
                    separator = ' '
                if len(i.split(separator)) < 2:
                    print(i)
                yuanshi = i.split(separator)[1]
                yuanshi_1 = i.split(separator)[0]
                yuanshi_tmps = yuanshi_1.split('.')
                if yuanshi_tmps[3] != '0':
                    yuanshi_1 = yuanshi_tmps[0] + '.' + yuanshi_tmps[1] + '.' + yuanshi_tmps[2] + '.0'
                flag = True
                for n1 in tmp_lines:
                    if yuanshi in n1:
                        flag = False
                        break
                if flag:
                    # print(yuanshi)
                    yuanshi = '255.255.255.0'
                for n in tmp_lines:
                    n = n.replace('\n', '').strip()
                    if n:
                        tp1 = n.split(' ')[0]
                        tp2 = n.split(' ')[1]

                        if yuanshi == tp2:
                            target_lines.append(f'{yuanshi_1}/{tp1} \n')
                            break
        return target_lines

    def merge(self, lines):
        target_lines = []
        mask_edge_dict = {}
        fp = open('mask_edge', 'r', encoding='utf-8')
        all_lines = fp.readlines()
        fp.close()
        for n in all_lines:
            n_s = n.split('-')
            mask_edge_dict[n_s[0]] = n_s[1].split(',')
        separetor = self.get_sep(lines)
        for i in lines:
            if i.replace('\n', '').strip():
                start = i.split(separetor)[0]
                end = i.split(separetor)[1].replace('\n', '')
                starts = start.split('.')
                ends = end.split('.')
                if self.get_head(start, 2) == \
                        self.get_head(end, 2):
                    head_num = 2
                    if starts[head_num] == ends[head_num] or (starts[head_num] == '0' and ends[head_num] == '255'):
                        target_lines.append(i)
                        continue
                else:
                    head_num = 1
                res = self.cal_start_end(i.split(separetor), mask_edge_dict, head_num, separetor)
                target_lines.append(res)
        return target_lines

    def get_start_end(self,lines):
        target = []
        for i in lines:
            if i:
                sep = self.get_sep(i)
                start = i[0].split(sep)[0]
                end = i[len(i) - 1].split(sep)[1]
                target.append(f'{start}{sep}{end}')
        return target

    def cal_start_end(self, item, mask_edge_dict, head_num, sep):
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

    def add_route_cli(self, lines, html):
        ad_pf = open('add-route.sh', 'w', encoding='utf-8')
        ad_pf.write('#!/bin/bash \n')
        for i in lines:
            if i.replace('\n', '').strip():
                i = i.replace('\n', '')
                if html:
                    line = f'route add -net {i} gw 192.168.8.1<br/>\n'
                else:
                    line = f'route add -net {i} gw 192.168.8.1\n'
                ad_pf.write(line)
        ad_pf.close()

    def del_routes_cli_by_addfile(self, html):
        ad_pf = open('add-route.sh', 'r', encoding='utf-8')
        del_pf = open('del-route.sh', 'w', encoding='utf-8')
        if html:
            del_pf.write('#!/bin/bash <br/>\n')
        else:
            del_pf.write('#!/bin/bash \n')
        lines = ad_pf.readlines()
        for i in lines:
            if i.replace('\n', '') and '#' not in i:
                network = i.split(' ')[3]
                if html:
                    cmd = f'route del -net {network}<br/>\n'
                else:
                    cmd = f'route del -net {network}\n'
                del_pf.write(cmd)
        ad_pf.close()
        del_pf.close()

    def add_routes_win_by_addfile(self, html):

        ad_pf = open('add-route.sh', 'r', encoding='utf-8')
        add_win_pf = open('add-route.bat', 'w', encoding='utf-8')

        lines = ad_pf.readlines()
        for i in lines:
            if i.replace('\n', '') and '#' not in i:
                network = i.split(' ')[3]
                if html:
                    cmd = f'route add {network} 192.168.8.1<br/> \n'
                else:
                    cmd = f'route add {network} 192.168.8.1 \n'
                add_win_pf.write(cmd)
        ad_pf.close()
        add_win_pf.close()


    def add_route_win(self, lines):
        ad_pf = open('add-route.txt', 'w', encoding='utf-8')
        for i in lines:
            if i.replace('\n', '').strip():
                i = i.replace('\n', '')
                line = f'route {i} net_gateway\n'
                ad_pf.write(line)
        ad_pf.close()

    def find_repeat_lines(self, lines):
        repeate_lines = []
        for i in lines:
            n = 0
            for j in lines:
                if i == j:
                    n = n + 1
                    if n > 1:
                        if i not in repeate_lines:
                            repeate_lines.append(i)
        return repeate_lines

    def remove_include_lines(self, repeate_lines, origin_lines):
        new_lines = []
        for i in origin_lines:
            flag = True
            for j in repeate_lines:
                if not j.replace('\n', '').strip():
                    continue
                if i.replace('\n', '').strip() == j.replace('\n', '').strip():
                    flag = False
                    break
            if flag:
                if '\n' not in i:
                    new_lines.append(f'{i}\n')
                else:
                    new_lines.append(f'{i}')
        return new_lines

    def make_clear_route_cli(self, lines):
        del_fp = open('del_routes.sh', 'w', encoding='utf-8')
        del_lines = ['#!/bin/bash \n']
        for i in lines:
            i = f'route del -net {i}'
            del_lines.append(i)
        del_fp.writelines(del_lines)
        del_fp.close()

    # 192.168.0.0 255.255.0.0->192.168.0.0 192.168.255.255
    def yanma_4(self, lines):
        sep = self.get_sep(lines)
        all_net_lines = []
        for i in lines:
            i_s = i.replace('\n', '').split(sep)
            if len(i_s) < 2:
                continue
            net = i_s[0]
            mask = i_s[1]
            masks = mask.split('.')

            nets = net.split('.')
            net_tg = []
            for m in range(0, 4):
                if masks[m] == '255':
                    net_tg.append(nets[m])
                    continue
                if masks[m] == '0':
                    net_tg.append('255')
                    continue
                net_tg.append(str(int(nets[m]) + 255 - int(masks[m])))
            end = '.'.join(net_tg)
            target_line = f'{net} {end}'
            all_net_lines.append(target_line + '\n')
        return all_net_lines

    def get_include_lines(self, lines):

        fp = open('include_lines', 'w', encoding='utf-8')

        sep = self.get_sep(lines)
        target = []
        for i in lines:
            i_s = i.replace('\n', '').split(sep)
            if len(i_s) < 2:
                print(i_s)
                continue
            start = i_s[0]
            end = i_s[1]
            for m in lines:
                if i == m:
                    continue
                flag = True
                m_s = m.replace('\n', '').split(sep)
                start_m = m_s[0]
                end_m = m_s[1]
                start_m_l = start_m.split('.')
                start_l = start.split('.')
                end_l = end.split('.')
                end_m_l = end_m.split('.')
                if start_l[0] == start_m_l[0]:
                    for c in range(1, 4):
                        if int(start_l[c]) > int(start_m_l[c]) or int(end_l[c]) < int(end_m_l[c]):
                            # print(start_l[c] + '>' + start_m_l[c] + '---' + end_l[c] + '<' + end_m_l[c])
                            flag = False
                            break
                else:
                    continue
                if flag:
                    if i not in target:
                        fp.write(f'{i},{m}')
                        target.append(m)
        fp.close()
        return target

    def sort_ips(self, ips):
        target = []
        target_int = []
        for i in ips:
            i_start = i.replace('\n', '').strip().split(' ')[0]
            i_num = int(i_start.replace('.', ''))
            target_int.append(i_num)
        target_int.sort()
        for i in target_int:
            for j in ips:
                if int(j.replace('\n', '').strip().split(' ')[0].replace('.', '')) == i:
                    target.append(j)
                    break
        print(target)

    def get_head(self, ip1, n):
        ip1 = ip1.replace('\n', '')
        try:
            ip1_s = ip1.split('.')
            ip1_sum = ''
            for i in range(0, n):
                ip1_sum = ip1_sum + ip1_s[i] + "."
        except BaseException as e:
            print(ip1 + '---' + str(n))
            raise ip1 + '---' + str(n)
        return ip1_sum

    def sort_1(self, lines):
        separator = self.get_sep(lines)
        line_lists = []
        all_lists_signgle = []
        sorted_lists = []
        for i in lines:
            i_head = i.replace('\n', '').split(separator)[0]
            head_1 = self.get_head(i_head, 1)
            tmp = []
            flag = False
            for j in lines:
                head_j = j.replace('\n', '').split(separator)[0]
                if head_1 == self.get_head(head_j, 1):
                    if i not in tmp:
                        for l in line_lists:
                            if i in l:
                                flag = True
                                break
                    if not flag:
                        tmp.append(j)
            line_lists.append(tmp)

        all_list = []
        for k in line_lists:
            if k:
                all_list.append(self.sort_2(k, separator))

        for m in all_list:
            for n in m:
                if n:
                    all_lists_signgle.append(n)

        single_list = []
        for r in all_lists_signgle:
            if len(r) > 1:
                sorted_lists.append(r)
            else:
                single_list.append(r[0])
        sorted_lists.append(single_list)

        all_lianxu = []

        for qe in sorted_lists:
            sorted_list = self.sort_in_list(qe)
            lianxu = self.network_marge(sorted_list)
            if not lianxu:
                continue
            num_init = len(qe)

            # ----cal len of all items
            num_cal = 0
            for i10 in lianxu:
                if i10:
                    if type(i10[0]) == type([]):
                        for i11 in i10:
                            # print(i11)
                            num_cal = num_cal + len(i11)
                    else:
                        num_cal = num_cal + len(i10)

            # -------------------------
            if num_cal != num_init:
                print(qe + '\n\n\n\n\n')

            all_lianxu.append(lianxu)

        # print(num1)
        # print(all_lianxu)
        all_list = self.split_list(all_list)
        second_cal = []
        for i11 in all_list:
            if i11:
                second = self.network_marge(self.sort_in_list(i11))
                num_init = len(i11)

                # ----cal len of all items
                num_cal = 0
                for i10 in second:
                    if i10:
                        if type(i10[0]) == type([]):
                            for i11 in i10:
                                # print(i11)
                                num_cal = num_cal + len(i11)
                        else:
                            num_cal = num_cal + len(i10)

                # -------------------------
                if num_cal != num_init:
                    print(second + '\n\n\n\n\n')

                second_cal.append(second)

        all_list_1 = self.split_list(second_cal)
        all_list_2 = []
        # for aaa in all_list:
        #     print(aaa)
        for i111 in all_list_1:
            res = self.split_lianxu_list(i111, separator)
            all_list_2.append(res)

        all_list = self.split_list(all_list_2)
        # --------------------
        return all_list

    # ---------------------------------

    def sort_2(self, li, separator):
        lists = []
        for i in li:
            i_head = i.replace('\n', '').split(separator)[0]
            head_1 = self.get_head(i_head, 2)
            tmp = []
            flag = False
            for j in li:
                head_j = j.replace('\n', '').split(separator)[0]
                if head_1 == self.get_head(head_j, 2):
                    if j not in tmp:
                        for l1 in lists:
                            if j in l1:
                                flag = True
                                break
                    if not flag:
                        tmp.append(j)
            lists.append(tmp)

        tmp_lw = []
        for l1w in lists:
            if l1w:
                if len(l1w) == 1:
                    tmp_lw.append(l1w[0])
        tmp_lw2 = []
        for l2w in lists:
            if l2w and len(l2w) > 1:
                tmp_lw2.append(l2w)
        tmp_lw2.append(tmp_lw)

        return tmp_lw2

    def sort_in_list(self, list):
        separator = self.get_sep(list)
        num_networks_tmp = []
        num_networks = []
        num_list = []

        if len(list) > 1:
            if self.get_head(list[0].split(separator)[0], 2) == self.get_head(list[1].split(separator)[0], 2):
                for i in list:
                    num_list.append(int(i.split(separator)[0].split('.')[2]))
            else:
                for i in list:
                    num_list.append(int(i.split(separator)[0].split('.')[1]))
        else:
            return list
        for l in range(0, len(list)):
            num_net = str(num_list[l]) + separator + list[l]
            num_networks_tmp.append(num_net)
        num_list.sort()
        for n in num_list:
            for m in num_networks_tmp:
                if int(m.split(separator)[0]) == n:
                    target = m.split(separator)[1] + separator + m.split(separator)[2]
                    num_networks.append(target)
                    break
        return num_networks

    def get_ips_by_index_ranges(self, rge, lst):
        target_not_lianxu = []
        target = []
        for i in rge:
            for m in i:
                target_lianxu = []
                if '---' in m:
                    start = m.split('---')[0]
                    end = m.split('---')[1]
                    for l in range(0, len(lst)):
                        if int(start) <= l <= int(end):
                            target_lianxu.append(lst[l])
                else:
                    target_not_lianxu = []
                    target_not_lianxu.append(lst[int(m)])
                if target_lianxu and target_lianxu not in target:
                    target.append(target_lianxu)
                if target_not_lianxu and target_not_lianxu not in target:
                    target.append(target_not_lianxu)

        return target

    def get_big_range(self, lines):
        new_lines = []
        for i in lines:
            separate = self.get_sep(i)
            if i:
                start = i[0].split(separate)[0]
                end = i[len(i) - 1].split(separate)[1]
                network = f'{start}-{end}'
                print(f'{i}\n{network}')
                new_lines.append(network)
        return new_lines

    # ['172.106.12.0-172.107.255.255']->['172.106.0.0-172.107.255.255']
    def amend_error_network(self, lines):
        targets = []
        seperator = self.get_sep(lines)
        for i in lines:
            i_s = i.split(seperator)
            start = i_s[0]
            end = i_s[1]
            starts = start.split('.')
            ends = end.split('.')
            if starts[1] != ends[1] and starts[2] != ends[2]:
                starts[2] = '0'
                ends[2] = '255'
                start = '.'.join(starts)
                end = '.'.join(ends)
                targets.append(f'{start}{seperator}{end}')
            else:
                targets.append(i)
        return targets

    def do_merge(self, list):
        separate = self.get_sep(list)
        jiange_plus = [2, 6, 14, 30, 62, 126, 254]
        jianges = [1, 3, 7, 15, 31, 63, 127, 255]
        if not list:
            return
        start = list[0].split(separate)[0]
        end = list[len(list) - 1].split(separate)[1]
        target = []

        if self.get_head(list[0].split(separate)[0], 2) == \
                self.get_head(list[len(list) - 1].split(separate)[1].replace('\n', ''), 2):
            head_num = 2
        else:
            head_num = 1

        if head_num == 2:
            tail = end.split('.')[3]
        elif head_num == 1:
            tail = end.split('.')[2] + '.' + end.split('.')[3]
        head = self.get_head(list[0].split(separate)[0], head_num)
        jiange = int(end.split('.')[head_num]) - int(start.split('.')[head_num])
        if jiange in jianges:
            network = f'{start}{separate}{end}'
            self.merged_networks.append(network)
            return

        if jiange in jiange_plus:
            end_mid = str(int(end.split('.')[head_num]) + 1)
            end = f'{head}{end_mid}.{tail}'
            jiange1 = int(end.split('.')[head_num]) - int(start.split('.')[head_num])
            print(str(jiange), str(jiange1))
            network = f'{start}-{end}'
            self.merged_networks.append(network)
            return
        if jiange == 0:
            self.merged_networks.append(list[0])
            return
        else:
            for i in range(0, len(jianges) - 2):
                if jianges[i] < jiange < jianges[i + 1]:
                    mid_num = int(start.split('.')[head_num]) + jianges[i]
                    mid_num_str = str(mid_num)
                    mid = f'{head}{mid_num_str}.{tail}'
                    network = f'{start}-{mid}'
                    if head_num == 2:
                        mid_1 = f'{head}{mid_num + 1}.{0}'
                    elif head_num == 1:
                        mid_1 = f'{head}{mid_num + 1}.{0}.{0}'
                    network_end = f'{mid_1}{separate}{end}'
                    self.merged_networks.append(network)
                    target.append(network_end)
                    if mid_1.split('.')[head_num] == end.split('.')[head_num]:
                        self.merged_networks.append(network_end)
                        return
                    else:
                        self.do_merge(target)

    def network_marge(self, list):
        lianxu_step = 1
        separator = self.get_sep(list)
        target = []
        single_index_tmp = []
        lianxu = []
        if len(list) == 1:
            target.append(list)
            return target
        if len(list) > 1:
            if self.get_head(list[0].split(separator)[0], 1) != self.get_head(list[1].split(separator)[0], 1):
                target.append(list)
                return target
            if self.get_head(list[0].split(separator)[0], 2) == self.get_head(list[1].split(separator)[0], 2):
                compare_index = 2
            else:
                compare_index = 1
            for i in range(0, len(list)):
                if i == 0:
                    end_i = list[i].replace('\n', '').split(separator)[1].split('.')[compare_index]
                    next_start_i = list[i + 1].replace('\n', '').split(separator)[0].split('.')[compare_index]
                    if int(next_start_i) - int(end_i) > lianxu_step:
                        single_index_tmp.append(i)
                if 0 < i < len(list) - 1:
                    after_end_i = list[i].replace('\n', '').split(separator)[1].split('.')[compare_index]
                    after_next_start_i = list[i + 1].replace('\n', '').split(separator)[0].split('.')[compare_index]
                    if int(after_next_start_i) - int(after_end_i) > lianxu_step:
                        if i not in single_index_tmp:
                            single_index_tmp.append(i)

            str_list = []
            for k in range(0, len(list)):
                str_list.append(str(k))

            splited_list = self.split_list_index(single_index_tmp, str_list)
            if type(splited_list) != type([]):
                print(f'asdasdas{single_index_tmp},{str_list}')
            for i5 in splited_list:
                tmp = []
                i5_s = i5[0].split('---')
                start = i5_s[0]
                end = i5_s[1]
                if start == end:
                    tmp.append(list[int(start)])
                    lianxu.append(tmp)
                else:
                    for i6 in range(int(start), int(end) + 1):
                        tmp.append(list[int(i6)])
                    lianxu.append(tmp)
                # if not target:
                #     lianxu.append(list)

            target.append(lianxu)
            # print(target)
        return target

    def split_list_index(self, duandian, all_index):
        if not duandian:
            target = []
            tmp = []
            tmp.append(f'{all_index[0]}---{all_index[len(all_index) - 1]}')
            target.append(tmp)
            return target
        target_list = []
        all_num_str = ',' + ','.join(all_index) + ','
        for n in range(0, len(duandian)):
            tmp = []
            all_s = all_num_str.split(',' + str(duandian[n]) + ',')
            start = all_num_str.split(',')[1]
            tmp.append(f'{start}---{str(duandian[n])}')
            target_list.append(tmp)
            tmp_1 = []
            for m in all_s[1].split(','):
                if m:
                    tmp_1.append(m)
            all_num_str = ',' + ','.join(tmp_1) + ','
        all_num_strs = all_num_str.split(',')
        tmp = []

        if str(duandian[len(duandian) - 1]) != all_index[len(all_index) - 1]:
            tmp.append(f'{all_num_strs[1]}---{all_num_strs[len(all_num_strs) - 2]}')
            target_list.append(tmp)
        return target_list

    def split_list(self, list):
        all_list = []
        for i in list:
            if i:
                if type(i[0]) == type(''):
                    all_list.append(i)
                    # print(i)
                if type(i[0]) == type([]):
                    for i2 in i:
                        if i2:
                            if type(i2[0]) == type([]):
                                for i3 in i2:
                                    all_list.append(i3)
                            else:
                                all_list.append(i2)
        num = 0
        for i3 in all_list:
            if i3:
                if type(i3[0]) == type([]):
                    print(f'{i3}--------------\n\n\n')
            num = num + len(i3)
        print(num, 'asdasdas')
        return all_list

    def split_lianxu_list(self, list, separator):
        target = []
        duandian = []
        if len(list) == 1:
            target.append(list)
            return target
        if len(list) > 1:
            if self.get_head(list[0].split(separator)[0], 1) != self.get_head(list[1].split(separator)[0], 1):
                target.append(list)
                return target
            if self.get_head(list[0].split(separator)[0], 2) == self.get_head(list[1].split(separator)[0], 2):
                compare_index = 2
            else:
                compare_index = 1
            for i in range(0, len(list)):
                if 0 < i < len(list) - 2:
                    end_i = list[i].replace('\n', '').split(separator)[1].split('.')[compare_index]
                    next_start_i = list[i + 1].replace('\n', '').split(separator)[0].split('.')[compare_index]
                    if int(next_start_i) - int(end_i) > 5:
                        duandian.append(i)

            splited = []
            for i1 in range(0, len(duandian)):
                tmp_range = []
                if len(duandian) == 1:
                    for i6 in range(0, duandian[0] + 1):
                        tmp_range.append(list[i6])
                    splited.append(tmp_range)
                    tmp_range = []
                    for i7 in range(duandian[0] + 1, len(list)):
                        tmp_range.append(list[i7])
                    splited.append(tmp_range)
                if len(duandian) == 2:
                    tmp_range = []
                    for i8 in range(0, duandian[0] + 1):
                        tmp_range.append(list[i8])
                    splited.append(tmp_range)
                    tmp_range = []
                    for i90 in range(duandian[1] + 1, len(list)):
                        tmp_range.append(list[i90])
                    splited.append(tmp_range)
                    tmp_range = []
                    for i112 in range(duandian[0] + 1, duandian[1] + 1):
                        tmp_range.append(list[i112])
                    splited.append(tmp_range)
                    break
                elif len(duandian) > 2:

                    if i1 == 0:
                        tmp_range = []
                        for i2 in range(0, duandian[i1] + 1):
                            tmp_range.append(list[i2])
                        splited.append(tmp_range)

                        tmp_range = []
                        for i2 in range(duandian[i1] + 1, duandian[i1 + 1] + 1):
                            tmp_range.append(list[i2])
                        splited.append(tmp_range)

                    if i1 == len(duandian) - 1:
                        tmp_range = []
                        for i3 in range(duandian[i1] + 1, len(list)):
                            tmp_range.append(list[i3])
                        splited.append(tmp_range)

                    if 0 < i1 < len(duandian) - 1:
                        tmp_range = []
                        for i4 in range(duandian[i1] + 1, duandian[i1 + 1] + 1):
                            tmp_range.append(list[i4])
                        splited.append(tmp_range)
            if not splited:
                splited.append(list)

            return splited

    def cal_network_ip_num(self, lines):
        # with open('res/route.origin.txt', 'r', encoding='utf-8') as fp:
        #     lines = fp.readlines()
        num = 0
        for i in lines:
            i = i.replace('\n', '').strip()
            if i:
                ma = int(i.split('/')[1])
                number = math.pow(2, 32 - ma)
                num = num + number
        print(int(num))

    def add_routes(self, lines):
        for i in lines:
            i = i.replace('\n', '')
            out = subprocess.getoutput(f'{i}')
            if 'Usage:' in out:
                print(i)

    def remove_repeat_lines(self, repeate_lines, origin_lines):
        print(len(repeate_lines), len(origin_lines))
        new_lines = []
        for i in origin_lines:
            flag = True
            for j in repeate_lines:
                if not j.replace('\n', '').strip():
                    continue
                if i.replace('\n', '').strip() == j.replace('\n', '').strip():
                    flag = False
                    break
            if flag:
                if '\n' not in i:
                    new_lines.append(f'{i}\n')
                else:
                    new_lines.append(f'{i}')
        for n in repeate_lines:
            if '\n' not in n:
                new_lines.append(f'{n}\n')
            else:
                new_lines.append(f'{n}')
        return new_lines


def cast():
    with open('res.txt', 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    mrge = merge_networks()
    mrge.yanma_4(mrge.yanma(lines))





if __name__ == '__main__':
    with open('res.txt', 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    mrge = merge_networks()
    mrge.yanma_4(mrge.yanma(lines))


