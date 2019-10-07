#!/usr/bin/env python3

# IRCat 
# @author: kelj0 
# @date: 2019

from IRCat import IRCat

HOST = "tolkien.freenode.net"
PORT = 6667

NICK = "IRCat"
IDENT = "IRCat"
REALNAME = "Meow"
CHANNELS = ["#python"]
ADMINS = ["kelj0"]

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
            if(line[3] == ":!usage"):
                BOT.PrintUsage(CHANNELS[0])
            elif(line[3] == ":!b64e"):
                s = " ".join(line[4:])
                s.lstrip(":")
                BOT.SendMessage(CHANNELS[0],"Here you go %s///%s" % (sender,BOT.Base64Encode(s))) # todo parse for multichannels
            elif(line[3] == ":!b64d"):
                s = line[4].lstrip(":")
                print(s)
                BOT.SendMessage(CHANNELS[0],"Here you go %s///%s" % (sender, BOT.Base64Decode(s)))
            elif(line[3] == ":!code"):
                s = line[4].lstrip(":")
                BOT.SendMessage(CHANNELS[0],"Here you go %s///%s" % (sender, BOT.StatusCodeInfo(s)))
            elif(line[3] == ":!fact"):
                BOT.SendMessage(CHANNELS[0], BOT.RandomFact())
            elif(line[3] == ":!begone"):
                if(sender not in ADMINS):
                    BOT.SendMessage(CHANNELS[0], "Pathethic..")
                else:
                    BOT.Leave()

        for index, i in enumerate(line):
            print(line[index],end="")
        print()

