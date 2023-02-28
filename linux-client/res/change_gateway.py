# --*-- coding:utf-8 --*--

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
    count = read_counter()
    if not count:
        count = 1
    count = int(count)
    if count < 15:
        write_counter(str(count + 1))
    elif count == 15:
        write_counter(str(1))
        get_routes()
    replace_gateway()



def get_routes():
    res_add = requests.get('http://xxx.com/add-routes.html')
    res_del = requests.get('http://xxx.com/del-routes.html')
    if '200' in str(res_add) and '200' in str(res_del):
        lines_add = res_add.text.replace('  ', ' ')
        lines_del = res_del.text.replace('  ', ' ')
        if 'route add' in lines_add:
            with open(f'{base_path}add-route.sh', 'w', encoding='utf-8') as fp:
                lines_li = lines_add.split('\n')
                for i in lines_li:
                    i = i.replace('\n', '').strip()
                    fp.write(f'{i}\n')
        subprocess.getoutput(f'chmod +x {base_path}add-route.sh')
        if 'route del' in lines_del:
            with open(f'{base_path}del-route.sh', 'w', encoding='utf-8') as fp:
                lines_li = lines_del.split('\n')
                for i in lines_li:
                    i = i.replace('\n', '').strip()
                    fp.write(f'{i.strip()}\n')
        subprocess.getoutput(f'chmod +x {base_path}del-route.sh')


def read_counter():
    with open(f'{base_path}counter', 'r', encoding='utf-8') as fp:
        count = fp.read()
    return count


def write_counter(count):
    with open(f'{base_path}counter', 'w', encoding='utf-8') as fp:
        fp.write(count)


def replace_gateway():
    with open(f'{base_path}add-route.sh', 'r', encoding='utf-8') as fp:
        lines_add = fp.readlines()
    new_geteway = get_gateway()
    new_route_lines = []
    new_route_lines.append('#!/bin/bash \n')
    for i in lines_add:
        if 'gw' in i:
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
