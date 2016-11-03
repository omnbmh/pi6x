#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import commands



def monitor(ip,port):
    if not ip or not port:
        return False;

    command = ('(sleep 2;) | telnet %s ' % (ip))+ port +' | grep \"\\^]\" | wc -l';
    #print 'prepare run command: %s' % command
    # 直接调用返回系统的返回值 0 是成功 会阻塞
    # is_started = os.system(command);
    is_started = commands.getoutput(command);
    #is_started = commands.getstatusoutput(command);
    #is_started = is_started.replace("\r\n","#")
    #print 'run result: %s' % is_started;
    print 'Server IP: %s, Port: %s, Status: %s.' % (ip, port, 'opened' if is_started.endswith('1') else 'closed');
    return is_started.endswith('1');


if __name__ == '__main__':
    monitor('127.0.0.1','8080');
