# Importing the required plugins to make our script work
import requests
import time
from colorama                   import init, Fore, Style
import os
import subprocess
import secrets
import random
from pypresence                 import Presence
import tempfile
import atexit
import sys
import json
from ctypes                     import wintypes
import threading
from queue                      import Queue
from ctypes                     import windll
from functools                  import partial
from pystyle                    import Write, Colors
import getpass
import tls_client
import pygame

pygame.mixer.init()
generated_urls = []  # List to store generated URLs
urls_lock = threading.Lock()  # Lock to synchronize access to generated_urls list

# Variables
genStartTime = int(time.time())
locked = 0
exit_flag = False
output_lock = threading.Lock()  # Lock to synchronize access to console output
red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT


with requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all", stream=True) as response:
            response.raise_for_status()
            os.system('clear' if os.name == 'posix' else 'cls')
            print(f"({Fore.YELLOW}+{Style.RESET_ALL}) Scraping proxies ")
            with open("proxies.txt", "w") as f:
                for line in response.iter_lines():
                    if line:
                        f.write(line.decode('utf-8') + '\n')
            os.system('clear' if os.name == 'posix' else 'cls')

def set_cmd_title(title):
    if os.name == 'posix':
        # Unix-like system
        print(f'\033]0;{title}\007', end='', flush=True)
    elif os.name == 'nt':
        # Windows
        windll.kernel32.SetConsoleTitleW(title)

def update_console_title():
    while True:
        set_cmd_title(f"Promo Gen | Valid links: {locked}")
        time.sleep(1)  # Adjust the sleep duration as needed

try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        threads_count = config.get('threads', 1)  # Default to 1 if not specified in config
except json.JSONDecodeError:
    threads_count = 1  # Default to 1 if config.json doesn't exist or is malformed
except FileNotFoundError:
    # Handle the case where config.json is not found
    print(f"\r({Fore.RED}+{Style.RESET_ALL}) config.json not found, make sure it is accessible from the script.")
    time.sleep(1)
    sys.exit()

class Proxy:
    chrome_version = random.randint(115, 121)
    def get_session(self):
        session = tls_client.Session(
            client_identifier=f"chrome{self.chrome_version}",
            random_tls_extension_order=True,
        )

        with open("proxies.txt", "r") as f:
            proxies = f.read().splitlines()
            if proxies:
                proxy = random.choice(proxies)
                session.proxies = {
                    "http": "http://" + proxy,
                    "https": "http://" + proxy
                }
                return session
            else:
                return session

def status():
    global locked  # Declare 'locked' as a global variable
    try:
        client_id = "1205602865754677283"
        RPC = Presence(client_id)
        RPC.connect()

        last_clear_time = time.time()

        def update_discord_presence():
            while True:
                RPC.update(
                    large_image="hi",
                    large_text="Discord Promo gen",
                    details=f"Link generated: {locked}",
                    start=int(genStartTime),
                    buttons=[{"label": "Buy Now!", "url": "https://nitroseller0.sellix.io"}]
                )
                time.sleep(0.1)  # Wait for 0.1 seconds between updates

        current_time = time.time()

        if current_time - last_clear_time >= 200:
            os.system('cls')
            last_clear_time = current_time

        time.sleep(1)
        discord_presence_thread = threading.Thread(target=update_discord_presence)
        discord_presence_thread.daemon = True
        discord_presence_thread.start()

    except Exception as e:
        print(e)

status()  # Corrected the function call

# Initialize Colorama
init(autoreset=True)

# Functions including random Header and PUID generator
def random_accept_language():
    languages = ['en-US,en;q=0.9', 'fr-FR,fr;q=0.9', 'es-ES,es;q=0.9', 'de-DE,de;q=0.9', 'zh-CN,zh;q=0.9']
    return random.choice(languages)

def random_sec_ch_ua():
    browsers = ['"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"']
    return random.choice(browsers)

def random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
    ]
    return random.choice(user_agents)
 
def generate_partner_user_id(length=64):
    return secrets.token_hex(length // 2)  # Divided by 2 as each byte is two hex digits

# Clears the cmd for a better and cleaner preview. Supports all OS
os.system('clear' if os.name == 'posix' else 'cls')


# Function to generate the raw string of discord promo link
def generate_discord_url(session):
    base_url = 'https://api.discord.gx.games/v1/direct-fulfillment'
    headers = {
        'authority': 'api.discord.gx.games',
        'accept': '*/*',
        'accept-language': random_accept_language(),
        'content-type': 'application/json',
        'origin': 'https://www.opera.com',
        'referer': 'https://www.opera.com/',
        'sec-ch-ua': random_sec_ch_ua(),
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': random_user_agent()
    }
    data = {
        'partnerUserId': generate_partner_user_id()
    }
    try:    
            # Prints the PUID (partnerUserId) for debugging purposes
            # with output_lock:
            #    dataprint = data['partnerUserId']
            #    print(f"({Fore.MAGENTA}+{Style.RESET_ALL}) PUID Used: {dataprint}")

            # Extract the raw string of the link and add it into a promo link
            response = requests.post(base_url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            token = response.json().get('token')
            return f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}"
    except requests.RequestException as e:
            return f"Error: {str(e)}"
    
# Saves the links into a file
def save_url_to_file(url, filename):
    with open(filename, 'a') as file:
        file.write(url + "\n")

# Makes the URL shorter in the CMD so it doesn't flood.
def truncate_url(url, max_length=120):
    return url if len(url) <= max_length else url[:max_length] + "..."
def start_main_menu_music():
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load('data/music.mp3')
        pygame.mixer.music.play()

    except pygame.error as e:
        print(f"Error: {e}")

def stop_main_menu_music():
    try:
        pygame.mixer.music.stop()
        pygame.quit()

    except pygame.error as e:
        print(f"Error: {e}")

start_main_menu_music()
# ASCII Art in color that will appear in CMD
username = getpass.getuser()
Write.Print(f"""
\t\t  ▄▀▀▀▀▄   ▄▀▀▄▀▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄  ▄▀▀█▄       ▄▀▀▄ ▀▄  ▄▀▀█▀▄    ▄▀▀▀█▀▀▄  ▄▀▀▄▀▀▀▄  ▄▀▀▀▀▄       ▄▀▀█▄▄▄▄  ▄▀▀▄  ▄▀▄  ▄▀▀▄▀▀▀▄  ▄▀▀▀▀▄    ▄▀▀▀▀▄   ▄▀▀█▀▄    ▄▀▀▀█▀▀▄ 
\t\t  █      █ █   █   █ ▐  ▄▀   ▐ █   █   █ ▐ ▄▀ ▀▄     █  █ █ █ █   █  █  █    █  ▐ █   █   █ █      █     ▐  ▄▀   ▐ █    █   █ █   █   █ █    █    █      █ █   █  █  █    █  ▐ 
\t\t  █      █ ▐  █▀▀▀▀    █▄▄▄▄▄  ▐  █▀▀█▀    █▄▄▄█     ▐  █  ▀█ ▐   █  ▐  ▐   █     ▐  █▀▀█▀  █      █       █▄▄▄▄▄  ▐     ▀▄▀  ▐  █▀▀▀▀  ▐    █    █      █ ▐   █  ▐  ▐   █     
\t\t  ▀▄    ▄▀    █        █    ▌   ▄▀    █   ▄▀   █       █   █      █        █       ▄▀    █  ▀▄    ▄▀       █    ▌       ▄▀ █     █          █     ▀▄    ▄▀     █        █      
\t\t    ▀▀▀▀    ▄▀        ▄▀▄▄▄▄   █     █   █   ▄▀      ▄▀   █    ▄▀▀▀▀▀▄   ▄▀       █     █     ▀▀▀▀        ▄▀▄▄▄▄       █  ▄▀   ▄▀         ▄▀▄▄▄▄▄▄▀ ▀▀▀▀    ▄▀▀▀▀▀▄   ▄▀       
\t\t           █          █    ▐   ▐     ▐   ▐   ▐       █    ▐   █       █ █         ▐     ▐                 █    ▐     ▄▀  ▄▀   █           █                █       █ █         
\t\t           ▐          ▐                              ▐        ▐       ▐ ▐                                 ▐         █    ▐    ▐           ▐                ▐       ▐ ▐          
        
                                                                                        Welcome {username} | discord.gg/bestnitro  
                                                                                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""", Colors.blue_to_cyan, interval=0.0000)


# Choice prompt
print(f"{Fore.MAGENTA}Press 1:{Style.RESET_ALL} to generate an infinite amount of codes.\n{Fore.RED}Press 2:{Style.RESET_ALL} to generate a specific amount.")
Write.Print(f"\n{username}@promogen ~> ", Colors.blue_to_cyan, interval=0.000); opc = input(magenta).lower()
# Variables 
filename = 'promos.txt' # Will create a txt file in the directory where the script is ran. Change it for personalized path/name.
retry_delay = 5


def generate_and_save_link(session):
    global locked, exit_flag, retry_delay
    try:
        console_title_thread = threading.Thread(target=update_console_title)
        console_title_thread.daemon = True
        console_title_thread.start()

        while not exit_flag.is_set():
            try:
                result = generate_discord_url(session)
                with urls_lock:
                    if result and not result.startswith("Error"):
                        locked += 1
                        save_url_to_file(result, filename)
                        print(f"({Fore.GREEN}+{Style.RESET_ALL}) URL: {truncate_url(result)}")
                    else:
                        print(f"({Fore.RED}+{Style.RESET_ALL}) {result} Waiting {retry_delay} seconds before retrying...")
                time.sleep(retry_delay)
            except KeyboardInterrupt:
                stop_main_menu_music()
                exit_flag.set()
                break  # Exit the loop on KeyboardInterrupt
    except KeyboardInterrupt:
        stop_main_menu_music()
        pass
        
exit_flag = threading.Event()


# Modified logic for generating and checking the links
if opc == '1':
    stop_main_menu_music()
    os.system('clear' if os.name == 'posix' else 'cls')
    try:
        threads = []
        main_obj = Proxy()  # Instantiate your class
        for _ in range(threads_count):
            thread = threading.Thread(target=generate_and_save_link, args=(main_obj.get_session(),))
            thread.daemon = True
            thread.start()
            threads.append(thread)

        # Wait for KeyboardInterrupt
        for thread in threads:
            thread.join()

    except SystemExit:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"({Fore.YELLOW}+{Style.RESET_ALL}) Loop stopped by user.")  
        sys.exit()  


elif opc == '2':
    num = int(input("Enter the number of codes to generate: "))
    stop_main_menu_music()
    os.system('clear' if os.name == 'posix' else 'cls')
    for _ in range(num):
        result = generate_discord_url()
        locked += 1
        if result and not result.startswith("Error"):
            save_url_to_file(result, filename)
            print(f"({Fore.GREEN}+{Style.RESET_ALL}) URL: {truncate_url(result)}")
        else:
           
            print(f"({Fore.RED}+{Style.RESET_ALL}) {result} Error encountered.")
else:
    print(f"{Fore.RED}Invalid choice. Exiting.{Style.RESET_ALL}")

subprocess.run(["python", "main.py"])
