# --*-- coding:utf-8 --*--
import math
import subprocess

new_lines = []


class merge_networks:
    merged_networks = []
    continus_networks = []

    def pre_proc(self, lines, sep):
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
                str_tail = ''
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
    def yanma_1(self, lines, separator):
        lines = self.pre_proc(lines, separator)
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
    def yanma_2(self, lines, separator):
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

    # 192.168.0.0 255.255.255.0 -> 192.168.0.0/24
    def yanma_3(self, lines, separator):
        with open('res/yanma_duizhao.txt', 'r', encoding='utf-8') as fp_tmp:
            tmp_lines = fp_tmp.readlines()
        target_lines = []
        for i in lines:
            i = i.replace('\n', '').strip()
            if i:
                if len(i.split(separator))<2:
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
        new_lines = []
        for m in target_lines:
            net_head = m.split('/')[0]
            net_mask = m.split('/')[1].strip().replace('\n', '')
            if net_mask == '24':
                new_lines.append(m)
                continue
            mask_num = int(int(net_mask) / 8)
            mask_num_yu = int(int(net_mask) % 8)
            compare_num = net_head.split('.')[int(mask_num)]
            compare_num = compare_num.strip().replace('\n', '')
            net_heads = m.split(f'.{compare_num}.')[0]
            net_tail = m.split(f'.{compare_num}.')[1]
            if '0.0/8' in m:
                m = net_head + '/' + '16\n'
                new_lines.append(m)
                continue
            elif mask_num_yu == 0:
                new_lines.append(m)
                continue
            elif int(int(compare_num) % int(math.pow(2, 8 - mask_num_yu))) != 0:

                ip_num = int(int(compare_num) + int(math.pow(2, 8 - mask_num_yu))
                             - int(compare_num) % math.pow(2, 8 - mask_num_yu))
                if ip_num > 255:
                    ip_num = int(int(compare_num) - int(compare_num) % math.pow(2, 8 - mask_num_yu))
                new_network = net_heads + '.' + str(ip_num) + '.' + net_tail
                new_lines.append(new_network)
            elif int(int(compare_num) % int(math.pow(2, 8 - mask_num_yu))) == 0:
                new_lines.append(m)
        return new_lines

    def add_route_cli(self, lines):
        ad_pf = open('add-route.sh', 'w', encoding='utf-8')
        ad_pf.write('#!/bin/bash \n')
        for i in lines:
            if i.replace('\n', '').strip():
                i = i.replace('\n', '')
                line = f'route add -net {i} gw 192.168.8.1\n'
                ad_pf.write(line)
        ad_pf.close()

    def remove_error_lines(self, lines):
        new_lines = []
        for i in lines:
            if i.replace('\n', '').strip():
                i = i.replace('\n', '')
                line = f'route add -net {i} gw 192.168.8.1\n'
                output = subprocess.getoutput(line)
                if not output:
                    new_lines.append(i + "\n")
                else:
                    line = f'route del -net {i}'
                    subprocess.getoutput(line)
        return new_lines

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
                        repeate_lines.append(i)
        return repeate_lines

    def remove_repeat_lines(self, repeate_lines, origin_lines):
        print(f'{len(repeate_lines)},{len(origin_lines)}')
        new_lines = []
        for i in origin_lines:
            flag = True
            for j in repeate_lines:
                if not j.replace('\n', '').strip():
                    continue
                if i == j:
                    flag = False
                    break
            if flag:
                if '\n' not in i:
                    new_lines.append(f'{i}\n')
                else:
                    new_lines.append(f'{i}')
        print(f'{len(new_lines)}')
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
    def yanma_4(self, lines, sep):
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

    def get_include(self, lines, sep):
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
                if start.split('.')[0] == start_m.split('.')[0]:
                    for c in range(1, 4):
                        if int(start_l[c]) > int(start_m_l[c]) or int(end_l[c]) < int(end_m_l[c]):
                            # print(start_l[c] + '>' + start_m_l[c] + '---' + end_l[c] + '<' + end_m_l[c])
                            flag = False
                            break
                else:
                    continue
                if flag:
                    target.append(m)
        # for k in target:
        #     print(k)
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

    def sort_1(self, lines, separator):
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
            res = self.sort_in_list(r, separator)
            if len(res) > 1:
                sorted_lists.append(res)
            else:
                single_list.append(res[0])
        sorted_lists.append(single_list)

        all_lianxu = []

        for qe in sorted_lists:
            lianxu = self.network_marge(qe, separator)
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
                second = self.network_marge(i11, separator)
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
        self.continus_networks = all_list
        for i in all_list:
            self.do_merge(i, separator)
        print(len(self.merged_networks))

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

    def sort_in_list(self, list, separator):
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

    def do_merge(self, list, separate):
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
                        self.do_merge(target, separate)

    def network_marge(self, list, separator):
        target = []
        single_index_tmp = []
        lianxu_num = []
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
                    if int(next_start_i) - int(end_i) > 5:
                        single_index_tmp.append(i)
                if 0 < i < len(list) - 1:
                    after_end_i = list[i].replace('\n', '').split(separator)[1].split('.')[compare_index]
                    after_next_start_i = list[i + 1].replace('\n', '').split(separator)[0].split('.')[compare_index]

                    before_end_i = list[i - 1].replace('\n', '').split(separator)[1].split('.')[compare_index]
                    before_next_start_i = list[i].replace('\n', '').split(separator)[0].split('.')[compare_index]

                    if int(after_next_start_i) - int(after_end_i) > 5 and int(before_next_start_i) - int(
                            before_end_i) > 5:
                        single_index_tmp.append(i)
                if i == len(list) - 1:

                    end_i = list[i - 1].replace('\n', '').split(separator)[1].split('.')[compare_index]
                    next_start_i = list[i].replace('\n', '').split(separator)[0].split('.')[compare_index]
                    if int(next_start_i) - int(end_i) > 5:
                        single_index_tmp.append(i)
            if len(single_index_tmp) == 1:
                if single_index_tmp[0] == 0:
                    lianxu_num.append(f'1---{len(list) - 1}')
                if single_index_tmp[0] == len(list) - 1:
                    lianxu_num.append(f'0---{len(list) - 2}')
                if 0 < single_index_tmp[0] < len(list) - 1:
                    lianxu_num.append(f'0---{single_index_tmp[0] - 1}')
                    lianxu_num.append(f'{single_index_tmp[0] + 1}---{len(list) - 1}')
            if len(single_index_tmp) == 0:
                lianxu_num.append(f'0---{len(list) - 1}')
            if len(single_index_tmp) > 1:
                for i2 in range(0, len(single_index_tmp) - 1):
                    if single_index_tmp[i2] - single_index_tmp[i2 + 1] < -1:
                        lianxu_num.append(f'{single_index_tmp[i2] + 1}---{single_index_tmp[i2 + 1] - 1}')
            if single_index_tmp and len(single_index_tmp) > 1:
                if single_index_tmp[len(single_index_tmp) - 1] != len(list) - 1:
                    if f'{single_index_tmp[len(single_index_tmp) - 1] + 1}---{len(list) - 1}' not in lianxu_num:
                        lianxu_num.append(f'{single_index_tmp[len(single_index_tmp) - 1] + 1}---{len(list) - 1}')
                if single_index_tmp[0] != 0 and single_index_tmp[0] != len(list) - 1:
                    if f'0---{single_index_tmp[0]}' not in lianxu_num:
                        lianxu_num.append(f'0---{single_index_tmp[0] - 1}')
            if single_index_tmp:
                for i4 in single_index_tmp:
                    tmp = []
                    tmp.append(list[i4])
                    target.append(tmp)
            for i5 in lianxu_num:
                start = int(i5.split('---')[0])
                end = int(i5.split('---')[1])
                lianxu_tmp = []
                for i6 in range(0, len(list)):

                    if start <= i6 <= end:
                        if compare_index == 1:
                            if list[i6].split(separator)[0].split('.')[2] != '0':
                                add_flag = True
                                if target:
                                    for i7 in target:
                                        if i7:
                                            if i7[0] == list[i6]:
                                                add_flag = False
                                                break
                                if add_flag:
                                    tmp1 = []
                                    tmp1.append(list[i6])
                                    target.append(tmp1)
                            else:
                                lianxu_tmp.append(list[i6])
                        else:
                            lianxu_tmp.append(list[i6])

                lianxu.append(lianxu_tmp)
                # if not target:
                #     lianxu.append(list)

            target.append(lianxu)
            # print(target)
            return target

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


def cast():
    with open('res.txt', 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    mrge = merge_networks()
    mrge.yanma_4(mrge.yanma(lines))


# network_marge(sort_in_list(test_list3))
# split_lianxu_list(test_list3)


# cal_network_ip_num()
# yanma_3(yanma_2(test_list3))
# do_merge(test_list2)
# print(merged_networks)
# with open('merge_res.txt','r',encoding='utf-8') as fp:
#     lines1=fp.readlines()
#
# lines=yanma_3(yanma_2(lines1))
# cal_network_ip_num(lines)

# if __name__ == '__main__':
#     merge = merge_networks()
#     merge.sort_1()
#     routes = merge.yanma_3(merge.yanma_2(merge.merged_networks))
#     merge.add_route_win(routes)
#     merge.add_route_cli(routes)
#     merge.make_clear_route(routes)

#


if __name__ == '__main__':
    with open('res.txt', 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    mrge = merge_networks()
    mrge.yanma_4(mrge.yanma(lines))

    # ---------------2---------------------------------------

    # formated_cn_ip_blocks = merge.yanma_1('ips_test', '-')
    # repeate_lines = merge.find_repeat_lines(formated_cn_ip_blocks)
    # if repeate_lines:
    #     formated_cn_ip_blocks = merge.remove_repeat_lines(repeate_lines, formated_cn_ip_blocks)
    # print(repeate_lines)
    # with open('add-route.sh', 'r', encoding='utf-8') as fp:
    #     lines = fp.readlines()
    # merge.add_routes(lines)
