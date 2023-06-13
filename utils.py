from sys import platform
import os


def cls():
    if platform == "win32":
        os.system("cls")
    else:
        os.system("clear")

def input_yes_no(question: str) -> bool:
    return input(f"{question} [Y/n]: ").lower() in ["yeah", "yes", "y", ""]

def create_if_not_exists(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def list_dir(path: str) -> list:
    if not path_exists(path):
        os.makedirs(path)
    return os.listdir(path)
        
def path_exists(path: str) -> bool:
    return os.path.exists(path)

def field_name_from(property_name: str) -> str:
    return property_name.replace('_', ' ')