from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # TYPE_CHECKING is False at runtime so the importing won't happen that time rather type hints works here
    from character_class import Character

from character_class import Slot

class Item(ABC):
    """
    Class Attributes:
        item (list[Item]): Contains the list of the Items.

    Attributes:
        name (str): Name of the item
        description (str): A short description
        _weight (float): How heavy the item is
        _value (int): Gold value of the item

    Methods:
        __str__: Nicely format item info
        use(): Base method to define item usage (overridden in subclasses)
        add_item(): adds the item to the respective subclasses and adds to the item list.
    """

    item = []

    def __init__(self, name, item_type, weight, value, description): # add weapon type here
        self.name = name
        self._weight = weight
        self._value = value
        self.description = description
        self.weapon_type = item_type

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, change_value):
        print(f"Weight: {self.weight} cannot be changed to {change_value}")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, change_value):
        print(f"Value: {self.value} cannot be changed to {change_value}")

    @abstractmethod
    def use(self, character: 'Character') -> bool:
        """Checks if the Item is present in Player object's inventory

        :param character: The character object to equip the item

        :returns The boolean value after checking
        """
        if self in character.inventory:
            print(f"\U0001F525 Upgrade !")
            return True
        else:
            print("The item is not present in the inventory")
            return False

    def __str__(self) -> str:
        """Used to display the Details of the Item"""

        return f"""{self.name}:
            Name: {self.name}
            Item Type: {self.weapon_type.capitalize()}
            Weight: {self.weight}
            Value: {self.value}
            Description: {self.description}"""


class Weapon(Item):
    """
    Attributes:
        damage (int): How much damage it deals
        weapon_type (str): The type of weapon (e.g., "sword", "bow", etc.)

    Methods:
        use(): Attacks with the weapon (calls player.attack or returns damage value)
    """
    item = []

    def __init__(self, name, item_type, damage, weight, value, description):
        super().__init__(name=name, weight=weight, item_type=item_type, value=value, description=description)
        self.damage = damage
        self.weapon_type = item_type

    def use(self, character: 'Character') -> None:
        """
        Equips the weapon to the Player object and then provides the buffs to the Player object.

        :param character: The Player object to equip and give buffs

        """
        value = super().use(character)

        if value:
            temp = character.attack_power
            character.attack_power += self.damage
            print(f"{character.name} attack power increased from {temp} to {character.attack_power}!")

    def __repr__(self):
        return (f"Weapon(Name: {self.name}, Item_type: {self.weapon_type}, Damage: {self.damage}"
                f"Weight: {self.weight}, Value: {self.value}, Description: {self.description})")


class Armor(Item):
    """
    Attributes:
        defense (int): How much damage it can reduce
        slot (str): Where it's worn: "head", "chest", etc.

    Methods:
        equip(): Adds to player's defense
        use(): Alias for equip()
    """
    item = []

    def __init__(self, name, item_type, defense, slot, weight, value, description):
        super().__init__(name=name, weight=weight, item_type=item_type, value=value, description=description)
        self.defense = defense
        self.slot = slot
        self.weapon_type = item_type

    def equip(self, character: 'Character'):
        """
        Equips the weapon to the Player object and then provides the buffs to the Player object.

        :param character: The Player object to equip and give buffs

        """
        value = super().use(character)

        available_slot = None

        for slots in Slot:
            if slots.value == self.slot:
                available_slot = slots

        if value:
            if character.slot.get(available_slot) is None:
                temp = character.defense
                character.defense += self.defense
                character.slot[available_slot] = self.name
                print(f"{character.name} defense has been increased from {temp} to {character.defense}!")
            else:
                print(f"The slot has been already filled with the item {character.slot[available_slot]}")

    def use(self, character):
        """Alias for equip function"""

        self.equip(character)

    def __repr__(self):
        return (f"Armor(Name: {self.name}, Item_type: {self.weapon_type}, Defense: {self.defense}"
                f"Weight: {self.weight}, Value: {self.value}, Description: {self.description})")


class Potion(Item):
    """
    Attributes:
        effect (str): What the potion does (e.g., "heal", "mana")
        magnitude (int): How much it heals or boosts

    Methods:
        use(): Applies the effect to the player (e.g., restore health)
    """
    item = []

    def __init__(self, name, item_type, effect, magnitude, weight, value, description):
        super().__init__(name=name, weight=weight, item_type=item_type, value=value, description=description)
        self.effect = effect
        self.magnitude = magnitude
        self.weapon_type = item_type

    def equip(self, user: 'Character'):
        if self.effect == 'heal':
            user.health += self.magnitude
            print(f"{self.magnitude} of health is restored using Health Potion")
            print(f"Health: {user.health}")
        if self.effect == 'buff':
            user.attack_power += self.magnitude

    def use(self, user):
        self.equip(user)

    def __repr__(self):
        return (f"Potion(Name: {self.name}, Item_type: {self.weapon_type}, Effect: {self.effect}"
                f"Magnitude: {self.magnitude}, Weight: {self.weight}, Value: {self.value}, Description: {self.description})")


class Special(Item):
    item = []

    def __init__(self, name, item_type, use, weight, value, description):
        super().__init__(name=name, weight=weight, item_type=item_type, value=value, description=description)
        self.type = item_type
        self.use = use
        self.weapon_type = item_type

    def use(self, character: 'Character'):
        pass

    def __repr__(self):
        return (f"Special(Name: {self.name}, Item_type: {self.weapon_type}, Use: {self.use}"
                f"Weight: {self.weight}, Value: {self.value}, Description: {self.description})")


if __name__ == "__main__":
    pass
