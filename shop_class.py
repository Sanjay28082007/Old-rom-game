import difflib
import json

from item_class import *

class Shop:
    """Shop contains all the Item to be used in the Game, Players can buy and use it.

    Attributes:
        data_dict (list[dict]): The list of the Item obtained from the function get_items()
            which retrieves data from items.json file
        class_alias (dict[str:class]): Contains the name of the Classes as string for using it as alias for processing.

    Methods:
        add_items(): Adds items from the data_dict to their respective classes.
        display_items(): Displays the items. If weapon_type parameter is given
            then it returns the specified Items of that type.
        buy_item(): Buys the item using the coins of the Player and adds it to the Player's inventory
    """
    _items_to_buy = []
    _items_to_buy_names = []

    def __init__(self):
        self.data_dict = get_items()
        self.class_alias = {
            'weapon': Weapon,
            'armor': Armor,
            'potion': Potion,
        }
        self._add_items()
        self.enemies_weapons = Weapon.item + Armor.item + Potion.item

    def _add_items(self) -> None:
        """Adds Item object from the data_dict to the respective classes"""
        for items in self.data_dict:
            type_weapon = items.get('type')
            class_name = self.class_alias.get(type_weapon)
            if class_name is None:
                class_name = Special

            obj = class_name(*items.values())
            obj.item.append(obj)
            self._items_to_buy.append(obj)
            self._get_items_name()

    def display_items(self, weapon_type: str = None) -> None:
        """Displays the Item objects from the Classes item list

        :param: weapon_type: The type of the weapon specifically to display.
            if not given, then displays all the Items.

        """
        for items in self._items_to_buy:
            if weapon_type is not None:
                if items.weapon_type.casefold() == weapon_type.casefold():
                    print(items)
            else:
                print(items)

    def buy_item(self, weapon: str, character: 'Character') -> None:
        """Buys the Item object and adds it to the Character's inventory

        :param: weapon: The name of the weapon to buy using the coins (coins will be added later)
        :param: character: The Character object to add the item to.

        """
        for new_item in self._items_to_buy:
            if new_item.name.casefold() == weapon.casefold():
                character.inventory.append(new_item)
                print(f"{new_item.name} is added to {character.name}'s inventory")
                break

        else:
            print(f"The specified item '{weapon.title()}' does not match any items in the shop")

            item_to_buy_names = [item_names.casefold() for item_names in self._items_to_buy_names]
            suggestions = difflib.get_close_matches(weapon, item_to_buy_names)

            if suggestions:
                print(f"Did you mean {suggestions[0].title()}?")
                confirmation = input("Confirmation: ").strip().casefold()
                if confirmation == 'yes':
                    self.buy_item(suggestions[0], character)
                else:
                    print(f'Nothing is added')
            else:
                print(f"No matches found")

    def _get_items_name(self):
        for item in self._items_to_buy:
            name = item.name
            if name not in self._items_to_buy_names:
                self._items_to_buy_names.append(name)

    def sell_item(self):
        pass


def get_items() -> list:
    filename = 'Files/items.json'

    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    pass
