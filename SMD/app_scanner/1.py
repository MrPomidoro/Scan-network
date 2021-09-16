'''
line = '00:09:BB:3D:D6:58   10.1.10.2   86250   dhcp-snooping   10  FastEthernet0/1'
match = re.search(r'(?P<mac>\S+) +(?P<ip>\S+) +\d+ +\S+ +(?P<vlan>\d+) +(?P<port>\S+)', line).groupdict()
print(match)
'''

'''log = 'Jun 3 14:39:05.941: %SW_MATM-4-MACFLAP_NOTIF: Host f03a.b216.7ad7 in vlan 10 is flapping between port Gi0/5 and port Gi0/15'
match = re.search(r'((\w{4}\.){2}\w{4}).+vlan (\d+).+port (\S+).+port (\S+)', log)
print(match.groups())

show_output = ssh.before.decode('utf-8')'''


# password = getpass.getpass()
# print(password)

# USERNAME = os.environ.get('SSH_USER')
# PASSWORD = os.environ.get('SSH_PASSWORD')
'''try:
    ssh = pexpect.spawn('ssh cisco@192.168.250.102')
    ssh.expect('[Pp]assword')
    ssh.expect(['password', 'Password'])
    ssh.sendline('cisco')
    ssh.expect('[>#]')
    ssh.sendline('enable')
    ssh.expect('[Pp]assword')
    ssh.sendline('cisco')
    ssh.expect('[>#]')
    ssh.sendline('sh ip int br')
    ssh.expect('#')
except Exception:
    pass
else:
    ssh.close()
print(ssh.before)'''


# import telnetlib
# import time
# from pprint import pprint
# def to_bytes(line):
#     return f"{line}\n".encode("utf-8")
# def send_show_command(ip, username, password, enable, commands):
#     with telnetlib.Telnet(ip) as telnet:
#         telnet.read_until(b"Username")
#         telnet.write(to_bytes(username))
#         telnet.read_until(b"Password")
#         telnet.write(to_bytes(password))
#         index, m, output = telnet.expect([b">", b"#"])
#         if index == 0:
#             telnet.write(b"enable\n")
#             telnet.read_until(b"Password")
#             telnet.write(to_bytes(enable))
#             telnet.read_until(b"#", timeout=5)
#         telnet.write(b"terminal length 0\n")
#         telnet.read_until(b"#", timeout=5)
#         time.sleep(3)
#         telnet.read_very_eager()
#         result = {}
#         for command in commands:
#             telnet.write(to_bytes(command))
#             output = telnet.read_until(b"#", timeout=5).decode("utf-8")
#             result[command] = output.replace("\r\n", "\n")
#     return result

# if __name__ == "__main__":
#     devices = ["192.168.0.1", "192.168.0.2", "192.168.0.3"]
#     commands = ["sh ip int br", "sh arp"]
#     for ip in devices:
#         result = send_show_command(ip, "cisco", "cisco", "cisco", commands)
#         pprint(result, width=120)


import subprocess, ipaddress
import re
# for ip in ipaddress.ip_network('192.168.250.0/25'):
#     fields = subprocess.Popen(['grep', str(ip), '/proc/net/arp'], stdout=subprocess.PIPE).stdout.read()
#     try:
#         r = re.search(r'\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2}', fields.decode('UTF 8')).group()
#         print(str(ip) + '  ' + r)
#     except:
#         pass
s='START'
print('\n'+s.center(60, '='))
sudoPassword = 'd12L03xd'
cmd1 = subprocess.Popen(['echo', sudoPassword], stdout=subprocess.PIPE)
# cmd2 = subprocess.Popen(['sudo', '-S', 'nmap', '-p', '22,23,80,7070', '--version-light', '-O', '192.168.250.22'], stdin=cmd1.stdout, stdout=subprocess.PIPE, encoding='utf-8')
# print(cmd2.stdout.read())
cmd2 = subprocess.Popen(['ping', '-c', '2', '-W', '1', '192.168.250.100'], stdin=cmd1.stdout, stdout=subprocess.PIPE, encoding='utf-8')
c = cmd2.stdout.read()
format = c.split('\n')
for form in format:
    if 'time=' in form:
        print('delay='+form[form.find('time=')+5:form.find('ms')+2])
    if 'ttl=' in form:
        print(form[form.find('ttl='):form.find('time')])
s='END'
print(''+s.center(60, '='))
# 082135051135907779250080