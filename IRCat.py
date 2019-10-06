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
                "!fact        - gives you a random cat fact///"
                "!begone      - leaves room(but listens you only if you are admin)"
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
            self.S.send(bytes("PRIVMSG %s :%s \r\n" % (recipient, m), "UTF-8"))

    def Pong(self,extra):
        """Sends pong"""
        self.S.send(bytes("PONG %s\r\n" % extra,"UTF-8"))

    def ReadBuffer(self,size):
        return self.S.recv(size).decode("UTF-8")

    def PrintUsage(self,channel):
        self.SendMessage(channel,self.USAGE)
    #=== Commands ===#
    def Base64Decode(self,cypher):
        """Decodes base64 to plaintext"""
        decoded = ""
        if len(cypher) < 2:
            decoded = "*Scratches you*, give me string por favor"
        else:
            try:
                decoded = base64.b64decode(bytes(cypher,"UTF-8")).decode("UTF-8")
            except Exception:
                decoded = "*Scratches you*, that is not a valid base64"
        return decoded
    
    def Base64Encode(self,text):
        """Decodes base64 to plaintext"""
        decoded = ""
        if len(text) < 2:
            decoded = "*Scratches you*, give me string por favor"
        else:
            try:
                decoded = base64.b64encode(bytes(text,"UTF-8")).decode("UTF-8")
            except UnicodeEncodeError:
                decoded = "*Bites you*, Is that even a language?"
        return decoded
    
    def StatusCodeInfo(self,code):
        """Returns more info about status code"""
        try:
            if(code < 100 and code > 599):
                return "*Knocks down your glass*, Give me normal status code"
            else:
                builder = ""
                res = requests.get("https://httpstatuses.com/%s" % code)
                bs = BeautifulSoup(res.text,"lxml")
                builder += bs.select("h1")[0].getText() + "///"
                builder += bs.select("p")[1].getText() + "///"
                builder += "https://http.cat/%s\n" % code
                return builder
        except ValueError:
            return "*Spills milk*, You didn't even give me number"
        
    def RandomFact(self):
        return requests.get("https://catfact.ninja/fact").json()['fact'] 

    def Leave(self):
        self.SendMessage(self.CHANNELS[0],"Ok i'm leaving.")
        self.SendMessage(self.CHANNELS[0], "!leave %s" % self.CHANNELS[0])

if __name__ == '__main__':
    print("This is used only as import!")


