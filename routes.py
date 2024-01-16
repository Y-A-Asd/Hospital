import asyncio
import os
from colorama import Style, Fore, Back
from tortoise import Tortoise
from models import Patient, Reservation


class ExitRequest(Exception):
    pass


class BaseRouterMixin:
    async def banner(self, manager_name):

        print('=' * 30)
        print(f"{manager_name} Manager")
        print('=' * 30)

    async def menu(self, manager_name, menu_items):
        while True:
            try:
                await self.banner(manager_name)
                for i, item in enumerate(menu_items, start=1):
                    print(f"{i}. {item['label']}")

                choice = input("Enter your choice (1-{max_choice}): ".format(max_choice=len(menu_items)))  # fun:-)
                try:
                    choice = int(choice)
                    if 1 <= choice <= len(menu_items):
                        menu_item = menu_items[choice - 1]
                        args = []
                        for arg_name in menu_item["args"]:
                            arg_value = input(f"Enter {arg_name}: ")
                            args.append(arg_value)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(Fore.GREEN, "")
                        await menu_item["action"](*args)
                        print(Fore.RESET, "")
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            except ExitRequest:
                break


class BaseMenu:
    def __init__(self, manager_name, menu_items, menu_req=None):
        self.router = BaseRouterMixin()
        self.manager_name = manager_name
        self.menu_items = menu_items

    async def menu(self):
        await self.router.menu(self.manager_name, self.menu_items)
