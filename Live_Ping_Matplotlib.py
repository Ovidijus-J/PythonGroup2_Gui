import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import subprocess, time, re, math, threading, queue
import PySimpleGUI as sg
from sys import platform

open('pingfile.txt', 'w')
host = 'google.com'
pingCounter = 0
def pingcalc():
    global pingCounter
    ping = subprocess.run(['ping', '-n', '1', host], capture_output=True)
    output = ping.stdout.decode()
        
    pingMS = ''.join(re.findall('time=(\d+)', output)) # This returns milliseconds (e.g. '14') in string
    pingCounter += 1# You can use the pingCounter as "seconds" in your graph
    with open('pingfile.txt', 'a') as f:
        print(pingCounter, pingMS, file=f, sep=',')
    time.sleep(1)

pingCounter = 0

style.use('fivethirtyeight')

fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    global ani
    global pingCounter
    plt.rcParams.update({'font.size': 8})
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
       title='Ping results: '+host)
    threading.Thread(target=pingcalc, daemon=True).start()
    if pingCounter == 55:
        open('pingfile.txt', 'w')
        pingCounter = 0
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
