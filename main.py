#!/usr/bin/env python3

# IRCat 
# @author: kelj0 
# @date: 2019

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

from IRCat import IRCat

HOST = "tolkien.freenode.net"
PORT = 6667

NICK = "IRCat"
IDENT = "IRCat"
REALNAME = "Meow"
CHANNELS = ["#triglex"]

BOT = IRCat(HOST,PORT,NICK,IDENT,REALNAME,CHANNELS)
readbuffer = ""
while 1:
    readbuffer = readbuffer+ BOT.ReadBuffer(1024)
    temp = str.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        line = str.rstrip(line)
        line = str.split(line)

        if(line[0] == "PING"):
            BOT.Pong(line[1])
        if(line[1] == "PRIVMSG"):
            sender = ""
            for char in line[0][1:]:
                if(char == "!"):
                    break
                else:
                    sender += char 
            if(line[3]==":!usage"):
                BOT.PrintUsage(CHANNELS[0])
            elif(line[3]==":!b64e"):
                s = " ".join(line[3:])
                s.lstrip(":")
                BOT.SendMessage(CHANNELS[0],"Here you go %s///" % sender + BOT.Base64Encode(s)) # todo parse for multichannels
            elif(line[3]==":!b64d"):
                s = (line[3]).lstrip(":")
                BOT.SendMessage(CHANNELS[0],"Here you go %s" % sender + BOT.Base64Decode(s))
            elif(line[3]==":!code"):
                s = line[3].lstrip(":")
                BOT.SendMessage(CHANNELS[0],"Here you go %s" % sender + BOT.StatusCodeInfo(s))

        for index, i in enumerate(line):
            print(line[index],end="")
        print()

