import subprocess
import sys
import PySimpleGUI as sg
import subprocess, time, re, sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

"""

    Network Troubleshooting Tool - Testing CMD Interface

"""

open('pingfile.txt', 'w')

def animate():
    style.use('fivethirtyeight')
    plt.rcParams.update({'font.size': 8})
    fig = plt.figure(figsize=(10,5))
    ax1 = fig.add_subplot(1,1,1)
    graph_data = open('pingfile.txt', 'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line)>1:
            x, y = line.split(',')
            xs.append(x)
            ys.append(y)
    ax1.clear()
    ax1.plot(xs, ys)
    ax1.set(xlabel='Times Pinged', ylabel='MS',
       title='Ping results')
    plt.show(block=False)

def ipaddrpng():
    loop = False
    
    while not loop:
        global iping
        if iping == None:
            break
        if iping == str(iping):
            open('pingfile.txt', 'w')
            host = iping
            pingCounter = 0
            runCommand(cmd='ping '+ str(iping))
            for i in range(50):
                ping = subprocess.run(['ping', '-n', '1', host], capture_output=True)
                output = ping.stdout.decode()
                pingMS = ''.join(re.findall('time=(\d+)', output)) # This returns milliseconds (e.g. '14') in string
                pingCounter += 1 # You can use the pingCounter as "seconds" in your graph
                with open('pingfile.txt', 'a') as f:
                    print(pingCounter,pingMS, file=f, sep=',')
        if pingCounter == 50:
            loop = True
def ipaddrtrc():
    loop = False
    while not loop:
        if iptrcrt == None:
            break
        else:
            loop = True
            runCommand(cmd='tracert ' + str(iptrcrt))
            
def nslooku():
    loop = False
    while not loop:
        if nslook == None:
            break
        else:
            loop = True
            runCommand(cmd='nslookup ' + str(nslook))

## [sg.Button('1', button_color=('white', 'blue'), size=(5, 1), font=("Helvetica", 20))]
def mainGUI():
    menu_def = [['Help', 'About...'],]
    sg.change_look_and_feel('Dark')
    layout = [  [sg.Menu(menu_def)],
                [sg.Text('Enter the command you wish to run:', font='fixedsys')],
                [sg.Input(key='_INPUT_'), sg.Button('Run'), sg.Button('Clear')],
                [sg.Text('Premade commands below', font='fixedsys')],
                [sg.Button('IPConfig'),sg.Button(image_filename='questions.png', key='_ipconfg_'), sg.Button('System Info', pad=((35,3),3)),sg.Button(image_filename='questions.png', key='_sysinf_'), sg.Button('NbtStat',pad=((35,3),3)),sg.Button(image_filename='questions.png', key='_nbtstat_')],
                [sg.Button('Ping'),sg.Button(image_filename='questions.png', key='_ping_'),sg.Button('Graph', key='_graph_'),sg.Button(image_filename='questions.png', key='_grph_'), sg.Button('Nslookup',pad=((25,3),3)),sg.Button(image_filename='questions.png', key='_nslook_'), sg.Button('Traceroute',pad=((25,3),3)),sg.Button(image_filename='questions.png', key='_trrt_')],
                [sg.Output(size=(60,30), background_color=('black'))],
                [sg.Button('Exit')] ]
    window = sg.Window('CLI Networking Tool', keep_on_top=False, no_titlebar=False, location=(500,10), size=(500,700),icon='cmd-ico.ico').Layout(layout).Finalize()

    while True:             # The Main Button Event Loop
        global iping
        global iptrcrt
        global nslook
        event, values = window.Read()
        # print(event, values)
        if event in (None, 'Exit'):
            break
        elif event == 'Run':
            runCommand(cmd=values['_INPUT_'], window=window)
        elif event == 'Clear':
            for i in range(30):
                i = "cls"
                runCommand(cmd=str(i))
                open('pingfile.txt', 'w')
            continue
        elif event == 'IPConfig':
            runCommand(cmd='ipconfig' , window=window)
        elif event == 'About...':
            sg.PopupAnnoying("Hello! This is a simple networking tool. It is very barebones for now but is made as a proof of concept for a troubleshooting tool for networking issues. This GUI is made with the CMD as a subprocess, and will execute commands through that and collect information, and show it off in the output window. Made by Group 2: Ovidijus, Jacob, Lukas P, Vlad."
,keep_on_top=True)
        elif event == 'Ping':
            iping = sg.PopupGetText('Enter IP address', 'Enter IP address', keep_on_top=True)
            ipaddrpng()
        elif event == 'Traceroute':
            iptrcrt = sg.PopupGetText('Enter IP address', 'Enter IP address', keep_on_top=True)
            ipaddrtrc()
        elif event == "Nslookup":
            nslook = sg.PopupGetText('Enter Address', 'Enter Address', keep_on_top=True)
            nslooku()
        elif event == 'System Info':
            runCommand(cmd='systeminfo', window=window)
        elif event == 'NbtStat':
            runCommand(cmd='nbtstat', window=window)
        elif event == "_ipconfg_":
            sg.PopupAnnoying("IPConfig or IPConfig /all is a command to show you current TCP/IP Network configurations. This is helpful to show your current IP, if you’re portforwarding an IP. It can be helpful to show the default gateway as well, for specific use cases. Will also show what DNS server you are currently connected to. Usually IPConfig has additional features to use like IPConfig /renew and /release. Which will either release a currently offered IP, or request a new one from the current DHCP server you are connected to.", keep_on_top=True)
        elif event == "_sysinf_":
            sg.PopupAnnoying("Here we see the system info of the system you are running. Results will vary depending on your machine. It will show you your currently running setup of CPU, RAM, and OS. This information is only useful if you are a new user of a PC, and are unaware of the OS, or current system specifications the hardware is running.", keep_on_top=True)
        elif event == '_nbtstat_':
            sg.PopupAnnoying('Netstat will show you the name of the currently running protocol which is TCP or UDP. It will show you the Local Address - which is the IP your machine is currently running. It will show you which IP addresses the computer you are on is currently connected to, which is useful for troubleshooting when you are unsure what ports specific programs are using. It will then lastly show you the state of a TCP connection, which will cycle between: CLOSE_WAIT, CLOSED, ESTABLISHED, FIN_WAIT_1, FIN_WAIT_2, LAST_ACK, LISTEN, SYN_RECEIVED, SYN_SEND, and TIME_WAIT.', keep_on_top=True)
        elif event == '_ping_':
            sg.PopupAnnoying('Ping is a simple command that most people that used a computer should know. It simply pings an address with a packet of information and awaits a response. This will check if you have a connection between you and a node, and how much time it takes from start to finish. To use this command efficiently, simply type in the address you want to ping, and start pinging.', keep_on_top=True)
        elif event == '_nslook_':
            sg.PopupAnnoying('NsLookup simply means “Name Server Lookup” which is useful for DNS requests. So, you can either retrieve an IP or a name of that IP. So, let’s say you only have the IP, you can NsLookup that IP and retrieve the domain name of that IP. Same thing the other way around, if you only have the domain name, you can retrieve the IP of the domain name. This can be tricky, because domains might have many different IPs.', keep_on_top=True)
        elif event == '_trrt_':
            sg.PopupAnnoying('Traceroute is an upgraded version of ping. It will show you which nodes your connection is hooping through to end up at the receiver. It will show you the average time, and how many times it needs to jump.', keep_on_top=True)
        elif event == '_graph_':
            animate()
        elif event == '_grph_':
            sg.PopupAnnoying('This will show you a statistic and an average of the ping command, between you and the address you have chosen')

    window.Close()

def runCommand(cmd, timeout=None, window=None):
    global line
    global output
    """ run shell command
    @param cmd: command to execute
    @param timeout: timeout for command execution
    @param window: the PySimpleGUI window that the output is going to (needed to do refresh on)
    @return: (return code from command, command output)
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None        # yes, a 1-line if, so shoot me

    return (output)

mainGUI() #Starts main window loop