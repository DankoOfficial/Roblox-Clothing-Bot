from time import sleep, time
from os import path, makedirs, getcwd, remove, rename, listdir, system, startfile
from requests import Session
from ctypes import windll
from configparser import ConfigParser
from colorama import Fore, Back
from pystyle import *
from glob import glob
from unidecode import unidecode
from datetime import datetime
from webview import create_window, start

class settings:
    robux = 0
    username = 'DankoOfficial'
    assetid = ""
    robuxspent = 0
    session = Session()
    uploaded = {'shirts': 0, 'pants': 0}
    def _logo_():
        S = r"""
                                                ┏━┓ ┳┓    ┓   ┏┓┏┏• •  ┓ - @DankoOfficial
                                                ┃┗┛ ┃┃┏┓┏┓┃┏┏┓┃┃╋╋┓┏┓┏┓┃ - On
                                                ┗━┛ ┻┛┗┻┛┗┛┗┗┛┗┛┛┛┗┗┗┗┻┗ - Github"""
        print(Center.XCenter(Colorate.Vertical(Col.blue_to_red, S, 5))+Fore.RESET)
    sep = f'{Fore.CYAN}>>{Fore.RESET}'

pants = False
debugmode = False

def initialize_config():
    global cookie, group, description, priceconfig, ratelimz, maxrobux, debugmode
    try:
        config = ConfigParser()
        config.read_file(open(r"Config.ini"))
        cookie = str(config.get("auth","cookie"))
        group = str(config.get("clothing","group"))
        description = str(config.get("clothing","description"))
        priceconfig = int(config.get("clothing","price"))
        ratelimz = int(config.get("optional","ratelimitwaitseconds"))
        maxrobux = int(config.get("optional","maxrobuxtospend"))
        debugmode = config.getboolean('optional', 'debugmode') 
    except:
        default_config = '''[auth]
cookie = _|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in........

[optional]
debugmode = false
ratelimitwaitseconds = 60
maxrobuxtospend = 20

[clothing]
price = 5
group = 1010101010101
description = notfun, fun, description'''
        open('Config.ini', 'a').write(default_config)
        input("[ERROR] Failed to open/read config file, generated a new one for you, please fill it out then press continue...")

def make_sure_path_exists():
    what = 0
    for path_to_create in ['Storage','Storage/Clothes','Storage/Clothes/Pants','Storage/Clothes/Shirts']:
        if not path.exists(path_to_create):
            makedirs(path_to_create)
            print(f'{Back.GREEN}{Fore.BLACK}[Created]{Back.BLACK}{Fore.WHITE} {path_to_create}')
            what = 1
    if what:
        input(f'{Back.YELLOW}{Fore.BLACK}[Info]{Back.BLACK}{Fore.WHITE} Please put your templates in the the storage folder, then hit enter')

def updateTitle(title,sl=None):
    windll.kernel32.SetConsoleTitleW(title)
    if sl: sleep(sl)

def log(text): 
    print(f"[{datetime.utcfromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')}] → {text}")

def setup_session():
    global cookie
    settings.session.cookies[".ROBLOSECURITY"] = cookie
    req = settings.session.post(url="https://auth.roblox.com/")
    if "X-CSRF-Token" in req.headers: 
        settings.session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]

def authenticate_user():
    try:
        settings.username = settings.session.get("https://users.roblox.com/v1/users/authenticated").json()['name']
    except:
        print(f"{Back.RED}{Fore.BLACK}[Error]{Back.BLACK}{Fore.WHITE} Your cookie is invalid")
        print(f"{Back.YELLOW}{Fore.BLACK}[Info]{Back.BLACK}{Fore.WHITE} Please restart the program, with a valid cookie")
        input()
        exit()

def display_robux():
    try:
        brokie = settings.session.get("https://economy.roblox.com/v1/user/currency").json()["robux"]
        print(f"{Back.CYAN}{Fore.BLACK}[Robux]{Back.BLACK}{Fore.WHITE} Remaining: R$ {brokie}")
        print()
    except:
        input(f'{Back.RED}{Fore.BLACK}[Error]{Back.BLACK}{Fore.WHITE} Failed to get robux, make sure the account didnt get banned, press enter to resume')

def r_path():
    return getcwd()

def remove_unnecessary_files():
    try:
        remove(f"{r_path()}\\Storage\\Clothes\\Shirts\\deleteme.png")
        remove(f"{r_path()}\\Storage\\Clothes\\Pants\\deleteme.png")
    except:
        pass

def clean_files_in_folder():
    for d in ['Shirts', 'Pants']:
        directory_path = path.join(getcwd(), 'Storage', 'Clothes', d)
        file_paths = glob(path.join(directory_path, '*'))

        for file_path in file_paths:
            filename = path.basename(file_path)
            cleaned_filename = unidecode(filename)
            if cleaned_filename != filename:
                cleaned_filepath = path.join(directory_path, cleaned_filename)
                rename(file_path, cleaned_filepath)
                print(f'Renamed {filename} to {cleaned_filename}')

def shirts():
    global group,description,priceconfig, name, pants,assetid, maxrobux
    updateTitle(f'Clothing Uploader | Welcome back {settings.username}! | Robux Remaining: {settings.robux-settings.robuxspent} | Status: [Uploading] | Uploaded: [Shirts: {settings.uploaded["shirts"]} - Pants: {settings.uploaded["pants"]}]')
    if settings.robuxspent >= maxrobux:
        updateTitle(f'Clothing Uploader - Status: [Limit reached]')
        print(f"{Back.RED}{Fore.BLACK}[Stopped]{Back.BLACK}{Fore.WHITE} Max robux spent reached, program stopped")
        input()
        return

    try:
        path = getcwd()
        if not pants:
            pathz = f"{path}\\Storage\\Clothes\\Shirts"
        else:
            pathz = f"{path}\\Storage\\Clothes\\Pants"
        name = listdir(pathz)[0].split(".")[0]
    except:
        if not pants:
            
            print(f"{Back.MAGENTA}{Fore.BLACK}[Shirts]{Back.BLACK}{Fore.WHITE} All shirts have been uploaded, moving to pants\n")
            pants = True
            shirts()
            return
            
        else:
            print(f"{Back.MAGENTA}{Fore.BLACK}[Pants]{Back.BLACK}{Fore.WHITE} All pants have been uploaded, you may close the program")
            input()
            exit()
        
    path = getcwd()
    if len(name)>50:
        name = name[:50]
        print(f'{Back.YELLOW}{Fore.BLACK}[Info]{Back.BLACK}{Fore.WHITE} Name too long, shortening to {name}')
    
    s = settings.session.post('https://apis.roblox.com/assets/user-auth/v1/assets',files={'fileContent': open(fr"{pathz}\\{listdir(pathz)[0]}", 'rb'),'request': ('', '{"displayName":"<n>","description":"<des>","assetType":"<tt>","creationContext":{"creator":{"groupId":<grp>},"expectedPrice":10}}'.replace('<n>',name).replace('<des>',description).replace('<tt>','Pants' if pants else 'Shirt').replace('<grp>',group))})
    open('log.txt','a').write(f'{s.status_code} - {s.text}\n')
    if debugmode: log(f'Uploaded {name} - {s.status_code} - {s.text}')
    if s.status_code != 200:
        if 'InsufficientFunds' in s.text:
            print(f"{Back.RED}{Fore.BLACK}[ERROR]{Back.BLACK}{Fore.WHITE} Failed to upload {'pants' if pants else 'shirt'}: {name} [Insufficient funds]")
            print(f"{Back.RED}{Fore.BLACK}[ERROR]{Back.BLACK}{Fore.WHITE} Stopped program, you can continue once you have funds")
            input()
            exit()
        elif 'Asset name and description is fully moderated' in s.text or 'Asset name is fully moderated' in s.text:
            print(f"{Back.RED}{Fore.BLACK}[ERROR]{Back.BLACK}{Fore.WHITE} Failed to upload {'pants' if pants else 'shirt'}: {name} [Moderated name] [{name}] - Renaming")
            s = settings.session.post('https://apis.roblox.com/assets/user-auth/v1/assets',files={'fileContent': open(fr"{pathz}\\{listdir(pathz)[0]}", 'rb'),'request': ('', '{"displayName":"<n>","description":"<des>","assetType":"<tt>","creationContext":{"creator":{"groupId":<grp>},"expectedPrice":10}}'.replace('<n>',f'{"pants" if pants else "shirt"}').replace('<des>','hi').replace('<tt>','Pants' if pants else 'Shirt').replace('<grp>',group))})                
            if s.status_code!= 200:
                print(f"{Back.RED}{Fore.BLACK}[ERROR]{Back.BLACK}{Fore.WHITE} Failed to upload {'pants' if pants else 'shirt'}: {name} [Moderated name/description] [{name}] - Renaming")
                remove(fr"{pathz}\\{listdir(pathz)[0]}")
                shirts()

            operationId = s.json()['operationId']
            while True:
                reee = settings.session.get(f'https://apis.roblox.com/assets/user-auth/v1/operations/{operationId}')
                if 'assetId' in reee.text:
                    try:
                        assetid = reee.text.split('"assetId":"')[1].split('"')[0]
                        print(f"{Back.GREEN}{Fore.BLACK}[AssetID]{Back.BLACK}{Fore.WHITE} {assetid}")
                    except:
                        assetid = None
                        print(f'{Back.RED}{Fore.BLACK}[ERROR] Failed to get asset id]{Back.BLACK}{Fore.WHITE} {assetid}')
                    break
                else:
                    print(f"{Back.YELLOW}{Fore.BLACK}[Getting ID]{Back.BLACK}{Fore.WHITE}: {name}")
                sleep(4)

            if debugmode:
                print(f"Status: {s.status_code}\nResponse: {s.text}")

            if not assetid:
                try:
                    remove(fr"{pathz}\\{listdir(pathz)[0]}")
                except:
                    pass
            s = settings.session.post(f'https://itemconfiguration.roblox.com/v1/assets/{assetid}/release',json={"priceConfiguration":{"priceInRobux":priceconfig},"saleStatus":"OnSale","releaseConfiguration":{"saleAvailabilityLocations":[0,1]}})
            price = settings.session.patch(f'https://develop.roblox.com/v1/assets/{assetid}',json={"name":name,"description":description,"enableComments":True})
            
            if not pants:
                if s.status_code == 200:
                    print(f"{Back.GREEN}{Fore.BLACK}[Upload]{Back.BLACK}{Fore.WHITE} Successfully uploaded a shirt: {name}")
                    try: remove(fr"{pathz}\\{listdir(pathz)[0]}")
                    except: pass
                    settings.uploaded["shirts"]+=1
                    settings.robuxspent+=10
                else:
                    print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Failed to upload a shirt: {name}")
                    try: remove(fr"{pathz}\\{listdir(pathz)[0]}")
                    except: pass
            else:
                if s.status_code == 200:
                    print(f"{Back.GREEN}{Fore.BLACK}[Upload]{Back.BLACK}{Fore.WHITE} Successfully uploaded pants: {name}")
                    settings.uploaded["pants"]+=1
                    try: remove(fr"{pathz}\\{listdir(pathz)[0]}")
                    except: pass
                    settings.robuxspent+=10
                else:
                    print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Failed to upload pants: {name}")
                    try: remove(fr"{pathz}\\{listdir(pathz)[0]}")
                    except: pass

            if price.status_code == 200:
                print(f"{Back.GREEN}{Fore.BLACK}[Upload]{Back.BLACK}{Fore.WHITE} Successfully set price to R$ {priceconfig}")
            else:
                print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Failed to set a price: {name}")

            brokie = settings.session.get("https://economy.roblox.com/v1/user/currency").json()["robux"]
            print(f"{Back.CYAN}{Fore.BLACK}[Robux]{Back.BLACK}{Fore.WHITE} Remaining: R$ {brokie}")
            print()
            shirts()
        elif 'User is Banned' in s.text:
            print(f"{Back.RED}{Fore.BLACK}[ERROR]{Back.BLACK}{Fore.WHITE} Failed to upload {'pants' if pants else 'shirt'}: {name} [Banned account]")
            input()
    else:
        operationId = s.json()['operationId']
        while True:
            reee = settings.session.get(f'https://apis.roblox.com/assets/user-auth/v1/operations/{operationId}')
            if 'assetId' in reee.text:
                try:
                    assetid = reee.text.split('"assetId":"')[1].split('"')[0]
                    print(f"{Back.GREEN}{Fore.BLACK}[AssetID]{Back.BLACK}{Fore.WHITE} {assetid}")
                except:
                    assetid = None
                    print(f'{Back.RED}{Fore.BLACK}[ERROR] Failed to get asset id]{Back.BLACK}{Fore.WHITE} {assetid}')
                    break
                else:
                    print(f"{Back.YELLOW}{Fore.BLACK}[Getting ID]{Back.BLACK}{Fore.WHITE}: {name}")
                    sleep(4)

                    if debugmode:
                        print(f"Status: {s.status_code}\nResponse: {s.text}")

                    if not assetid:
                        try:
                            remove(fr"{pathz}\\{listdir(pathz)[0]}")
                        except:
                            pass
                    s = settings.session.post(f'https://itemconfiguration.roblox.com/v1/assets/{assetid}/release',json={"priceConfiguration":{"priceInRobux":priceconfig},"saleStatus":"OnSale","releaseConfiguration":{"saleAvailabilityLocations":[0,1]}})
                    price = settings.session.patch(f'https://develop.roblox.com/v1/assets/{assetid}',json={"name":name,"description":description,"enableComments":True})
                    
                    if not pants:
                        if s.status_code == 200:
                            print(f"{Back.GREEN}{Fore.BLACK}[Upload]{Back.BLACK}{Fore.WHITE} Successfully uploaded a shirt: {name}")
                            try: remove(fr"{pathz}\\{listdir(pathz)[0]}")
                            except: pass
                            settings.uploaded["shirts"]+=1
                            settings.robuxspent+=10
                        else:
                            print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Failed to upload a shirt: {name}")
                            try: remove(fr"{pathz}\\{listdir(pathz)[0]}")
                            except: pass
                    else:
                        if s.status_code == 200:
                            print(f"{Back.GREEN}{Fore.BLACK}[Upload]{Back.BLACK}{Fore.WHITE} Successfully uploaded pants: {name}")
                            settings.uploaded["pants"]+=1
                            try: remove(fr"{pathz}\\{listdir(pathz)[0]}")
                            except: pass
                            settings.robuxspent+=10
                        else:
                            print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Failed to upload pants: {name}")
                            try: remove(fr"{pathz}\\{listdir(pathz)[0]}")
                            except: pass

                    if price.status_code == 200:
                        print(f"{Back.GREEN}{Fore.BLACK}[Upload]{Back.BLACK}{Fore.WHITE} Successfully set price to R$ {priceconfig}")
                    else:
                        print(f"{Back.RED}{Fore.BLACK}[Fail]{Back.BLACK}{Fore.WHITE} Failed to set a price: {name}")

                    brokie = settings.session.get("https://economy.roblox.com/v1/user/currency").json()["robux"]
                    print(f"{Back.CYAN}{Fore.BLACK}[Robux]{Back.BLACK}{Fore.WHITE} Remaining: R$ {brokie}")
                    print()
                    shirts()
def main():
    global pants
    display_robux()
    updateTitle(f'Clothing Uploader | Welcome back {settings.username}! | Robux Remaining: {settings.robux-settings.robuxspent} | Status: [Uploading] | Uploaded: [Shirts: {settings.uploaded["shirts"]} - Pants: {settings.uploaded["pants"]}]')
    if not pants:
        shirts_result = shirts()
        if shirts_result == "hey":
            pants = True
            shirts()

if __name__ == "__main__":
    settings._logo_()
    updateTitle('Clothing Uploader - Status: Initializing config...',0.2)
    initialize_config()
    try:
        if debugmode: log(f'Initialized config')
    except:
        pass
    make_sure_path_exists()
    try:
        if debugmode: log(f'Making sure folder path exists...')
    except:
        pass
    updateTitle('Clothing Uploader - Status: Setting up session...',0.2)
    setup_session()
    updateTitle('Clothing Uploader - Status: Logging in...',0.2)
    authenticate_user()
    updateTitle(f'Clothing Uploader - Main Menu')
    while True:
        system('cls')
        settings._logo_()
        option = input(f"""
                                                {Col.white}A  {settings.sep} {Col.white}License Expires at {Fore.CYAN}Never{Fore.RESET}
                                                {Col.white}A  {settings.sep} {Col.white}Welcome back {Fore.CYAN}{settings.username}{Fore.RESET}\n
                                                {Col.white}1  {settings.sep} {Col.white}Mass clothing uploader{Fore.RESET}\n
                                                {Col.white}2  {settings.sep} {Col.white}Mass clothing downloader{Fore.RESET} (Coming soon)\n
                                                {Col.white}3  {settings.sep} {Col.white}Preview Avatar in-game clothing{Fore.RESET}\n
                                                {Col.white}O  {settings.sep} {Col.white}>> """)
        if option not in ['1', '2','3']:
            print(f"                                                {Back.RED}{Fore.BLACK}[ERROR]{Back.BLACK}{Fore.WHITE} Invalid option..")
            sleep(3)
            system('cls')
            continue
        else:
            if option == '1':
                settings.robux = settings.session.get("https://economy.roblox.com/v1/user/currency").json()["robux"]
                while True:
                    system('cls')
                    settings._logo_()
                    print()
                    print(f'                                                {Col.white}Lets make sure of the settings  {settings.sep} {Col.white}\n')
                    print(f'                                                {Col.white}1  {settings.sep} {Col.white}Group ID: {Fore.CYAN}{group}{Fore.RESET}')
                    print(f'                                                {Col.white}2  {settings.sep} {Col.white}Description: {Fore.CYAN}{description[:20]}....{Fore.RESET}')
                    print(f'                                                {Col.white}3  {settings.sep} {Col.white}Price: {Fore.CYAN}{priceconfig}{Fore.RESET}')
                    print(f'                                                {Col.white}4  {settings.sep} {Col.white}Max Robux to spend: {Fore.CYAN}{maxrobux}{Fore.RESET}')
                    print(f'                                                {Col.white}5  {settings.sep} {Col.white}Rate limit wait seconds: {Fore.CYAN}{ratelimz}{Fore.RESET}')
                    print(f'                                                {Col.white}6  {settings.sep} {Col.white}Debug Mode: {Fore.CYAN}{debugmode}{Fore.RESET}')
                    print(f'                                                {Col.white}7  {settings.sep} {Col.white}Cookie: {Fore.CYAN}{cookie[-10:]}....{Fore.RESET}')
                    len_shirts = len(glob(path.join(f"{getcwd()}\\Storage\\Clothes\\Shirts", "*")))
                    print(f'                                                {Col.white}8  {settings.sep} {Col.white}Amount of shirts to upload: {Fore.CYAN}{len_shirts}{Fore.RESET}')
                    len_pants = len(glob(path.join(f"{getcwd()}\\Storage\\Clothes\\Pants", "*")))
                    print(f'                                                {Col.white}9  {settings.sep} {Col.white}Amount of pants to upload: {Fore.CYAN}{len_pants}{Fore.RESET}')
                    print(f'                                                {Col.white}10 {settings.sep} {Col.white}Amount to spend to upload everything: {Fore.CYAN}{(len_shirts+len_pants)*10}{Fore.RESET}\n')
                    yuh = input(f'                                                {Col.white}O  {settings.sep} {Col.white}Seems right? (x to reload config) press enter to continue...{Fore.RESET} ')
                    if 'x' in yuh.lower():
                        initialize_config()
                    elif yuh in ['8','9','10']:
                        if yuh == '8':
                            startfile(path.join(getcwd(), "Storage", "Clothes", "Shirts"))
                        elif yuh == '9':
                            startfile(path.join(getcwd(), "Storage", "Clothes", "Pants"))
                        else:
                            startfile(path.join(getcwd(), "Storage", "Clothes"))
                    elif yuh in ['1','2','3','4','5','6','7']:
                        startfile(path.join(getcwd(), "Config.ini"))
                    else:
                        clean_files_in_folder()
                        system('cls')
                        settings._logo_()
                        main()
                        break
            elif option == '2':
                print(f"                                                {Back.RED}{Fore.BLACK}[ERROR]{Back.BLACK}{Fore.WHITE} This option is not available yet: But you can join https://discord.gg/MG4uudjD7U")
                sleep(3)
                system('cls')
                continue
            elif option == '3':
                create_window("Preview Avatar in-game clothing", html='<!DOCTYPE html><html><head><style>body{margin:0;padding:0;}</style></head><body><iframe src="https://ingame.clothing" width="100%" height="1000"></iframe></body></html>')
                start()
