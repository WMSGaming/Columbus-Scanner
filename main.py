import random
import dhooks
import colorama
import threading
from os import system
from dhooks import Embed
from mcstatus import JavaServer
from configparser import ConfigParser
system("title "+"WMS Server Scanner")
config = ConfigParser()
try:
    config.read("Setting.ini")
    settings = config["info"]
except:
    config["info"] = {
        "webhook": "on",
        "webhook_url": "URL_HERE",
        "verbose": "on"
    }
    with open("Setting.ini","w") as c:
        config.write(c)
        config.read("Setting.ini")
        settings = config["info"]
shouldSendWebhook = settings["webhook"]
webhookUrl = settings["webhook_url"]
verbose = settings["verbose"]


def magenta(string):
    print(colorama.Fore.MAGENTA + string)


magenta("-" * 75)
magenta("-- Christopher Columbus Scanner by WMS https://wmsgaming.github.io/WMS/ --")
magenta("-" * 75)
magenta(f"-Loaded Settings... ")
magenta(f"-Send to webhook: {shouldSendWebhook}")
magenta(f"-Verbose: {verbose}")
magenta("-" * 75)
threads = int(input("How many threads would you like to use? "))
magenta("-" * 75)
magenta("Scanning in Progress... Please be patient.")
magenta("-" * 75)
checkIPS = []


def checkStatus(ip):
    if verbose == "on":
        print(f"Checking {ip}")

    try:
        status = JavaServer.lookup(ip)
        s = status.status()
        logIP(ip, s.version.name)
    except:
        pass


def randIP():
    ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    while ip not in checkIPS:
        checkIPS.append(ip)
        return ip


def writeFile(s):
    with open("Server.txt", "a") as f:
        f.write(f"{s}\n")


def logIP(ip, version):
    print(colorama.Fore.GREEN + "[+] " + colorama.Fore.MAGENTA + f"{ip} is a minecraft server, Version: {version}")
    writeFile(f"IP: {ip} Version: {version}")
    if shouldSendWebhook == "on":
        sendWebhook(ip, version)


def sendWebhook(ip, version):
    try:
        hook = dhooks.Webhook(webhookUrl)
        embed = Embed(
            description="Found a server!",
            color=0xFF0000,
            timestamp='now'
        )
        embed.set_author("Christopher Columbus Scanner")
        embed.add_field(name="IP: ", value=str(ip))
        embed.add_field(name="Version: ", value=str(version))
        hook.send(embed=embed)
    except Exception as error:
        print(error, " (Make sure that a webhook is in the Settings.ini config file!)")


def startSearch():
    while True:
        checkStatus(randIP())


def startThreads():
    for i in range(threads):
        t = threading.Thread(target=startSearch)
        t.start()


startThreads()
