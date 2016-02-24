#!/usr/bin/python

import os
import subprocess


def main():
    cmdpath = "volatility"
    target = "zeus.vmem"
    commands = ["pslist"]

    profiles = parseInfo(findInfo(cmdpath, "imageinfo", target))

    for cmd in commands:
        print(run(cmdpath, profiles[0], cmd, target))

    print("Done!")

def run(cmdpath, profile, command, target):
    output = ""
    p = subprocess.Popen(cmdpath + " -f " + target + " profile=" + profile + " " + command, stdout=subprocess.PIPE, shell=True)
    p.wait()

    for line in p.stdout:
        s = str(line).strip('\n')
        output += s[2:-3] + "\n" #Makes everything pretty
    return output

def findInfo(cmdpath, command, target):
    output = ""
    p = subprocess.Popen(cmdpath + " -f " + target + " " + command, stdout=subprocess.PIPE, shell=True)
    p.wait()
    for line in p.stdout:
        output += str(line)
    return output

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

main()

