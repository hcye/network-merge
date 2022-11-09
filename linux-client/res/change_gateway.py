# --*-- coding:utf-8 --*--
import datetime
import subprocess

import requests

base_path = '/usr/local/scripts/'


def get_gateway():
    cmd = 'route -n'
    output = subprocess.getoutput(cmd)
    output_lines = output.strip().split('\n')
    gateway_lines = []
    for i in output_lines:
        if 'UG' in i and '0.0.0.0' in i:
            gateway_lines.append(i)
    if len(gateway_lines) != 1:
        raise 'Please close all the vpn in you system,then reboot rerun this script!'
    gateway_datas_tmp = gateway_lines[0].split(' ')
    gateway_datas = []
    for m in gateway_datas_tmp:
        if m.strip():
            gateway_datas.append(m)
    GATEWAY = gateway_datas[1]
    return GATEWAY


def update_routes():
    cu_day = int(datetime.datetime.now().day)
    if int(cu_day % 3) == 0:
        res_add = requests.get('http://gitlab.synsense.ai/add-routes.html')
        res_del = requests.get('http://gitlab.synsense.ai/del-routes.html')
        lines_add = res_add.text
        lines_del = res_del.text
        if 'route add' in lines_add:
            with open(f'{base_path}add-route.sh', 'w', encoding='utf-8') as fp:
                lines_li = lines_add.split('\n')
                for i in lines_li:
                    i = i.replace('\n', '')
                    i = i.replace('<br/>', '').strip()
                    fp.write(f'{i.strip()}\n')
        if 'route del' in lines_del:
            with open(f'{base_path}del-route.sh', 'w', encoding='utf-8') as fp:
                lines_li = lines_del.split('\n')
                for i in lines_li:
                    i = i.replace('\n', '')
                    i = i.replace('<br/>', '').strip()
                    fp.write(f'{i.strip()}\n')
    replace_gateway()


def replace_gateway():
    with open(f'{base_path}add-route.sh', 'r', encoding='utf-8') as fp:
        lines_add = fp.readlines()
    new_geteway = get_gateway()
    new_route_lines = []
    new_route_lines.append('#!/bin/bash \n')
    for i in lines_add:
        if 'gw' in lines_add[i]:
            i = i.replace('\n', '').strip()
            old_gateway = i.split(' ')[5].replace('\n', '')
            if new_geteway == old_gateway:
                subprocess.getoutput(f'bash {base_path}add-route.sh')
                return
            else:
                new_line = i.replace(old_gateway, new_geteway + '\n')
                new_route_lines.append(new_line)
    if len(new_route_lines) > 1:
        with open(f'{base_path}add-route.sh', 'w', encoding='utf-8') as new_fp:
            new_fp.writelines(new_route_lines)
    subprocess.getoutput(f'bash {base_path}add-route.sh')


if __name__ == '__main__':
    update_routes()
