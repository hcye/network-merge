# network-merge
合并网络以减小路由表

## 被合并的网络文件要求
1. 查看ips_test.txt或ips.txt。ips是大陆全量ip库，已半年未更新。ips_test.txt是缩减的ip库文件用于测试
2. 行格式 192.168.1.0-192.168.8.255

## 开始合并
1.  启动脚本在test.py内， 详见main函数，默认在合并后输出linux使用的add-route.sh 和 del-route.sh。生成windows的add-route调用add_route_win(lines)

## linux开机加入我们的路由
1.  查看linux-client目录，该脚本创建了个add-route服务。
2.  可以根据当前机器的默认路由修改add-route的网关
