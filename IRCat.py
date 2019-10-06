import socket
import string
import base64
import requests
import time
from bs4 import BeautifulSoup

class IRCat:
    S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CHANNELS = []
    USAGE = (  "*Meows*, Hello there///"
                "!usage       - see this again///"
                "!b64e string - encodes string using base64///"
                "!b64d string - decodes string using base64///"
                "!code code   - gives more info about status code///"
            )

    def __init__(self,ip,port,nick,ident,realname,channels):
        """IP/hostname,port,name,ident,realname, channels(list of #strings)"""
        self.S.connect((ip,port))
        self.S.send(bytes("NICK %s\r\n" % nick, "UTF-8"))
        self.S.send(bytes("USER %s %s meow :%s\r\n" % (ident, ip, realname), "UTF-8"))
        for channel in channels:
            self.S.send(bytes("JOIN %s\r\n" % channel, "UTF-8"))
            self.PrintUsage(channel)
        self.CHANNELS = channels[:]

    def SendMessage(self,recipient,message):
        """Sends message to user/channel (use /// as newline)"""
        for m in message.split("///"):
            print(m)
            self.S.send(bytes("PRIVMSG %s %s \r\n" % (recipient, m), "UTF-8"))

    def Pong(self,extra):
        """Sends pong"""
        self.S.send(bytes("PONG %s\r\n" % extra,"UTF-8"))

    def ReadBuffer(self,size):
        return self.S.recv(size).decode("UTF-8")

    def PrintUsage(self,channel):
        self.SendMessage(channel,self.USAGE)
    #=== Commands ===#
    def Base64Decode(self,base64):
        """Decodes base64 to plaintext"""
        decoded = ""
        try:
            decoded = base64.b64decode(base64)
        except TypeError:
            decoded = "*Scratches you*, that is not a valid base64"
        return decoded
    
    def Base64Encode(self,text):
        """Decodes base64 to plaintext"""
        decoded = ""
        if len(text) < 2:
            decoded = "*Scratches you*, give me string por favor"
        else:
            decoded = base64.b64Encode(text)
        return decoded
    
    def StatusCodeInfo(self,code):
        """Returns more info about status code"""
        try:
            if(100 > int(code) > 600):
                return "*Knocks down your glass*, Give me normal status code"
            else:
                builder = ""
                res = requests.get("https://httpstatuses.com/%s" % code)
                bs = BeautifulSoup(res.text,"lxml")
                builder += bs.select("h1").getText() + "///"
                builder += bs.select("p")[1].getText() + "///"
                builder += "https://http.cat/%s\n" % code
                return builder
        except ValueError:
            return "*Spills milk*, You didn't even give me number"

if __name__ == '__main__':
    print("This is used only as import!")

