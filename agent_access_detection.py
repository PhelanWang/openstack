# coding: utf-8

import os


def is_load_external():
    return globals().has_key('AGENT_LOADER')


if not is_load_external():
    from lib.agent.ctest import SwitchAgent
    agent = SwitchAgent(__name__)


# 主机文件访问控制检测
@agent.entry("host_access_detection", version="1.0.1")
def host_access_controll_detection(subtask_id, args):
    # 使用系统命令，列出根目录的文件访问控制权限
    result = ''.join(os.popen("ls -lh / | awk '{print $1,$3,$4,$9}'").readlines()[1:])
    detail = '本次测试获取物理机根目录下文件或目录访问控制权限。\n' \
             '列出的被测试节点的根目录访问权限，第一列的第一个字符代表文件(-)、目录(d)、链接(l)。\n' \
             '其余字符每3个一组(rwx)，第一组是文件所有者的权限，第二组是与文件所有者同一组的用户权限，第三组是与文件所有者不同组用户权限。\n' \
             '每组中字符代表无权限(-）、可读(r)、可写(w)、可执行(x)\n' \
             '第二列表示为文件用户，第三列表文件用户所在的组，第四列表示文件名或目录名。'


    print result
    print detail

    agent.post_report(subtask_id,
                      severity=1,
                      result=0,
                      brief='',
                      detail=detail,
                      json_data=result.replace('\n', '</br>'))


# 虚拟机访问控制检测
@agent.entry("vm_access_detection", version="1.0.1")
def vm_access_controller_detection(subtask_id, args):
    from access_detection.vm_access_controll_detection import list_access_controll, get_vm_infor
    import time
    time.sleep(5)
    print 'path is:'+args['path']
    result = list_access_controll(args)
    detail = '本次测试获取虚拟机根目录下文件或目录访问控制权限。\n' \
             '列出的被测试虚拟机的根目录访问权限，第一列的第一个字符代表文件(-)、目录(d)、链接(l)。\n' \
             '其余字符每3个一组(rwx)，第一组是文件所有者的权限，第二组是与文件所有者同一组的用户权限，第三组是与文件所有者不同组用户权限。\n' \
             '每组中字符代表无权限(-）、可读(r)、可写(w)、可执行(x)\n' \
             '第二列表示为文件用户，第三列表文件用户所在的组，第四列表示文件名或目录名。'
    print result
    print detail

    agent.post_report(subtask_id,
                      severity=1,
                      result=0,
                      brief='',
                      detail=detail.replace('\n', '</br>'),
                      json_data=result.replace('\n', '</br>'))


# Execute this while run this agent file directly
if not is_load_external():
    args = {}
    # args['path'] = '/root/PycharmProjects/cp/96d9b1b5-2f45-4baf-8462-5a166c87a3bb'
    # vm_access_controller_detection(0, args)
    # host_access_controll_detection(0, args)
    agent.run()