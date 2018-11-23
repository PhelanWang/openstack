# coding: utf-8
from time import sleep
__author__ = 'Henry'
# Determine whether loaded by agent_loader
def is_load_external():
    return globals().has_key('AGENT_LOADER')

# Execute this while run this agent file directly
if not is_load_external():
    # Import ctest package
    from lib.agent.ctest import SwitchAgent

    # Create SwitchAgent instance
    agent = SwitchAgent(__name__)

# Register function "my_openvas" on service "openvas"

# OK
# 格式修改完成
@agent.entry("vnc", version="1.0.1")
def vnc(subtask_id, args):
    # Post report to switch server:
    # agent.post_report(subtask_id, severity, result, brief, detail, json_data)
    import os,time,ConfigParser
    from spice_vnc.format_data import get_format_data
    conf=ConfigParser.ConfigParser()
    conf.read('spice_vnc.conf')
    port=conf.get('VNC', 'port', '6080')
    cmd='tshark -i any -n -f "src port '+port+'" -d "tcp.port=='+port+',vnc" -a duration:60 -w vnc.cap'
    print 'please wait 2 mins,spice is testing...'
    print cmd
    os.system(cmd)
    #time.sleep(120)
    os.system('hexdump -C vnc.cap > vnc.txt')
    #print 'please wait 5 mins,spice is testing...'
    #time.sleep(120)
    print 'begin to anaylyse...'
    #os.system('chmod 777 data.cap')
    #result=os.popen('hexdump -C data.cap')
    file=open('vnc.txt')
    result=file.read()
    file.close()
    #print result
    os.system('rm -rf vnc.cap')
    # json_data is default as None
    result = get_format_data(result, 15)
    for item in result:
        print item
    agent.post_report(subtask_id,
                      severity=0,
                      result=1,
                      brief='VNC',
                      detail='获取VNC协议的数据内容，若有明文，则可能部分数据未加密!\n'.replace('\n', '</br>'),
                      json_data=result)

# Execute this while run this agent file directly
if not is_load_external():
    # vnc(0, 0)
    # Run agent
    agent.run()
    # os.system('bash spice/run.sh')
    
    
