# --*-- coding:utf-8 --*--
import os.path
import subprocess


class install_add_route:
    OS = ''
    GATEWAY = ''

    def get_os_platform(self):
        if os.path.exists('/etc/centos-release'):
            return 'centos'
        inspect_release = subprocess.getoutput("cat /etc/os-release")
        if 'ubuntu' in inspect_release:
            self.OS = 'ubuntu'
        elif 'centos' in inspect_release:
            self.OS = 'centos'

        if not self.OS:
            raise 'Do not support this linux platform!'

    def install_net_tools(self):
        cmd = ''
        if self.OS == 'centos':
            cmd = 'yum install -y net-tools'
        elif self.OS == 'ubuntu':
            cmd = 'apt install -y net-tools'
        subprocess.getoutput(cmd)

    def get_gateway(self):

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
        self.GATEWAY = gateway_datas[1]

    def install_service(self):
        self.get_os_platform()
        self.install_net_tools()
        self.get_gateway()
        script_path = '/usr/local/scripts'
        service_file = 'res/add-routes.service'
        python_file = 'res/change_gateway.py'
        subprocess.getoutput(f'chmod +x add-route.sh ; mkdir -p {script_path}'
                             f' ; cp add-route.sh del-route.sh  {script_path}'
                             f' ;cp {python_file}  {script_path}')
        subprocess.getoutput(f' cp {service_file} /lib/systemd/system/ ; systemctl daemon-reload '
                             f'; systemctl enable add-routes;systemctl start add-routes')


# route add -net 222.195.158.0/24 gw gateway

if __name__ == '__main__':
    ins = install_add_route()
    ins.install_service()
