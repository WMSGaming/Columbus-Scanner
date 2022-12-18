import random, dhooks, json, threading
from os import system
from dhooks import Embed
from mcstatus import JavaServer
from colorama import Fore

system("title "+"WMS Server Scanner")


with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)
    shouldSendWebhook = config["enable_webhook"]
    webhookUrl = config["webhook_url"]
    verbose = config["verbose"]


def magenta(string):
    print(Fore.MAGENTA + string + Fore.RESET)


magenta("-" * 75)
magenta("-- Christopher Columbus Scanner by WMS https://wmsgaming.github.io/WMS/ --")
magenta("-" * 75)
magenta(f"-Loaded Settings... ")
magenta(f"-Send to webhook: {shouldSendWebhook}")
magenta(f"-Verbose: {verbose}")
magenta("-" * 75)
threads = int(input("How many threads would you like to use? "))
magenta("-" * 75)
magenta(f"Scanning in Progress... Please be patient.")
magenta("-" * 75)
checkIPS = []


def checkStatus(ip):
    if verbose:
        print(f"{Fore.WHITE}[{Fore.BLUE}...{Fore.WHITE}]{Fore.MAGENTA} Checking {ip}")

    try:
        status = JavaServer.lookup(ip)
        s = status.status()
        logIP(ip, s.version.name)
    except:
        print(f"{Fore.WHITE}[{Fore.RED}-{Fore.WHITE}]{Fore.MAGENTA} {ip} is invalid. {Fore.RESET}")
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
    print(f"{Fore.WHITE}[{Fore.GREEN}+{Fore.WHITE}]{Fore.MAGENTA} {ip} is a minecraft server, Version: {version} {Fore.RESET}")
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
        print(error, " (Make sure that a webhook is in config.json!)")


def startSearch():
    while True:
        checkStatus(randIP())


def startThreads():
    for i in range(threads):
        t = threading.Thread(target=startSearch)
        t.start()


startThreads()
