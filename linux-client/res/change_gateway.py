# --*-- coding:utf-8 --*--
import subprocess

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


def replacd_gateway():

    with open(f'{base_path}add-route.sh', 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    new_geteway = get_gateway()
    new_route_lines = []
    new_route_lines.append('#!/bin/bash \n')
    for i in lines:
        if 'gw' in i:
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
    replacd_gateway()
