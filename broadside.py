#!/usr/bin/python

import os
import sys
import subprocess
import fileinput

"""Runs multiple volatility commands and outputs the results itno an html report"""
def main(args):
    cmdpath = "volatility" #Default volatility command. Works on *.nix with volatility in path
    target = args[-1] #Memory file path defaults to last argument
    commands = ["pslist", "psscan", "pstree","cmdscan", "consoles", "connections", "sockets", "sockscan","netscan", "hivelist", "hashdump"]

    #Runs help if no arguments are specified
    if len(args) <= 1:
        args.append("-h")

    #Parses the command line arguments
    for arg in args:
        if arg in ("-h", "--help"):
            print("broadside.py [OPTIONS] FILE")
            print("broadside.py -v path/to/volatility -f FILE \n")
            print("-v, --volalility PATH \n\tSets the path to the volatility executable")
            print("-f, --file FILE \n\tPath to memeory image")
            print("-a, --add COMMAND \n\tAdds a command to be run")
            print("-r, --remove COMMAND \n\tRemoves a command")
            sys.exit()

        elif arg in ("-v", "--volatility"):
            cmdpath = args[args.index(arg)+1]
        elif arg in ("-f", "--file"):
            target = args[args.index(arg)+1]
        elif arg in ("-a", "--add"):
            commands.append(args[args.index(arg)+1])
        elif arg in ("-r", "--remove"):
            commands = remove(commands, args[args.index(arg)+1])

    #Report body that will be written into the html report
    text = ""

    #Finds the volatility profile
    profiles = parseInfo(findInfo(cmdpath, "imageinfo", target))

    #Runs each command, gets the output, and wraps it in html tags
    for cmd in commands:
        text += "<h3>" + cmd + "</h3> \n"
        text += "<pre>" + run(cmdpath, profiles[0], cmd, target) + "</pre> \n"

    #Writes the output into an *.html file
    writeHTML(text , target)

    print("The report " + target + "_report.html is ready.")

"""Runs a volatility command and returns the output"""
def run(cmdpath, profile, command, target):
    output = ""
    p = subprocess.Popen(cmdpath + " -f " + target + " profile=" + profile + " " + command, stdout=subprocess.PIPE, shell=True)
    p.wait()

    for line in p.stdout:
        s = str(line).strip('\n')
        output += s[2:-3] + "\n" #Makes everything pretty
    return output

"""Runs imageinfo and returns the output"""
def findInfo(cmdpath, command, target):
    output = ""
    p = subprocess.Popen(cmdpath + " -f " + target + " " + command, stdout=subprocess.PIPE, shell=True)
    p.wait()
    for line in p.stdout:
        output += str(line)
    return output

"""Takes the output of imageinfo and parses out the supported profiles"""
def parseInfo(info):
    output = []
    profiles = "VistaSP0x64 VistaSP0x86 VistaSP1x64 VistaSP1x86 VistaSP2x64 VistaSP2x86 Win10x64 Win10x86 Win2003SP0x86 Win2003SP1x64 Win2003SP1x86 Win2003SP2x64 Win2003SP2x86 Win2008R2SP0x64 Win2008R2SP1x64 Win2008SP1x64 Win2008SP1x86 Win2008SP2x64 Win2008SP2x86 Win2012R2x64 Win2012x64 Win7SP0x64 Win7SP0x86 Win7SP1x64 Win7SP1x86 Win81U1x64 Win81U1x86 Win8SP0x64 Win8SP0x86 Win8SP1x64 Win8SP1x86 WinXPSP1x64 WinXPSP1x86 WinXPSP2x64 WinXPSP2x86 WinXPSP3x86".split()

    for profile in profiles:
        if profile in info:
            output.append(profile)
    if len(output) == 0:
        print("Profile not found. Exiting")
        exit()
    return output


"""Writes the output of all commands into an html file named after the memory file"""
def writeHTML(text, target):
    f = open("report.html",'r')
    filedata = f.read()
    f.close()

    newdata = filedata.replace("MAGIC",text)
    newdata = newdata.replace("FILE",target)

    f = open(target + "_report.html",'w')
    f.write(newdata)
    f.close()

"""Removes a command from the list of commands to run"""
def remove(commands, arg):
    cmds = []
    for cmd in commands:
        if not(arg == cmd):
            cmds.append(cmd)
    return cmds

main(sys.argv)
