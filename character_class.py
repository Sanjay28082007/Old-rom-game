import difflib
import random
from enum import Enum

from colorama import Fore


class Slot(Enum):
    HEAD = 'head'
    CHEST = 'chest'
    LEG = 'leg'
    HAND = 'hand'


class Character:
    """
    Builds the Character of the Game

    Attributes:
        name (str): The name of the Character
        health (int): The health of the Character
        _attack_power (int): The attack value of the Character
        _life (int): The life value of the Character
        defense (int): The defense value of the Character
        inventory (list[Item]): The list of Item of the inventory items

    Methods:
        take_damage_self(): Inflicts damage to itself when other Character object is attacking it.

        attack(): Attacks the target maybe the Player or Enemy object

    """


    def __init__(self, name, health, attack_power, inventory):
        self.name = name
        self._health = health
        self.full_health = health
        self._attack_power = attack_power
        self._life = 3
        self.defense = 0
        self.inventory = inventory
        self.slot = {
            Slot.HEAD: None,
            Slot.CHEST: None,
            Slot.LEG: None,
            Slot.HAND: None
        }
        self.alive = True

    @property
    def health(self):
        if self._health >= 0:
            return self._health
        raise ValueError(f"Health cannot be negative")

    @health.setter
    def health(self, value):
        if value >= 0:
            self._health = value

    @property
    def attack_power(self):
        return self._attack_power

    @attack_power.setter
    def attack_power(self, value):
        if 0 <= value <= 1000:
            self._attack_power = value
        else:
            print(f"Attack power can be increased only up to 500 so it is added instead of {value} for {self.name}")
            self._attack_power += 500

    @property
    def life(self):
        if self._life >= 0:
            return self._life
        else:
            self._life = 0
            return self._life

    @life.setter
    def life(self, value):
        if value >= 0:
            self._life = value

    def attack(self, target: 'Character') -> None:
        """Attacks the target object to inflict damage.
            This calls the take_damage methods for further processing and
            sets the amount of damage by using the attack_power of the attack object."""

        amount = self.attack_power
        target.take_damage_self(self, amount)

    def take_damage_self(self, attacker, amount: int) -> None:
        """
        Inflicts damage to the self by the amount of the damage by the Character.
        Also reduces the life of the Character object if the character health is 0.

        Restores the health after eliminating a life but the damage still tingers
        and reduces further the health after restoring to full health too.

        If the Character's life is 0 and health becomes 0 after taking damage,
        then displays the Character has been killed.


        :param attacker:
        :param self: The self object to take damage
        :param amount: The amount of damage to be taken by the self. Usually be the attack_power of the attacker(self).

        """
        reduced_health = self.health - (amount - self.defense)
        temp = self.health
        if self.alive:
            print(f"{attacker.name} attacked {self.name}")
        if reduced_health >= 0:
            self.health = reduced_health
            print(f"{self.name} took the amount of the damage {amount} and heath from {temp} to {reduced_health}")
            print("-" * 80)
        elif self.alive and reduced_health <= 0:
            if self.life != 0:
                self.life -= 1
                self.health = self.full_health
                print("Health restored by a life")
                print(f"Remaining lives: {self.life}")
                reduced_health = abs(reduced_health)  # removing the negative sign to reduce again
                self.health -= reduced_health
                print(f"Health reduced further due to negative health and becomes {self.health}")
                print("=" * 25, f"{self.name} lost a life", "=" * 25)

            else:
                print(Fore.RED, f"\t{self.name} has been killed by {attacker.name}", Fore.RESET)
                self.health = 0
                self.alive = False

    def equip(self, item: str):
        value = True

        for items in self.inventory:
            if items.name.casefold() == item.casefold():
                items.use(self)
                break
            else:
                value = False
        return value

    def print_items(self):
        print(f"{self.name}'s Inventory contains: ")
        for index, items in enumerate(self.inventory):
            print(f"\t{index + 1}: {items.name}")

    @staticmethod
    def chance_event(onset, offset):
        rand_int = random.randint(onset, offset)

        if rand_int % offset == 0:
            return True
        return False

    def __str__(self) -> str:
        """Returns the name, health, attack_power of the Character"""
        return f"""
        Name: {self.name}
        Health: {self.health}
        Attack Power: {self.attack_power}
        """


class Player(Character):
    """
    Attributes:
        name (str): The name of the Player
        health (int): The health of the Player
        _attack_power (int): The attack power of the Player
        inventory (list[Item]): The list of Item objects
        experience (int): The experience level of the Player
        level (int): The level of the Player
        slot (dict[str: Any]): The slot of the Player to equip Item objects which can be bought from the Shop.
        level_dict (dict[int: int]): The level and the experience needed to level up for levels from 1 to 100.

    Methods:
        attack(): attacks the target object. The Target object can be anything.
            If the Target object dies then the Player gets an experience of 1000 and
            calls the function for level up to for levelling up.

        level_up(): Checks if the current experience is more than the required experience to level up
            as the details is in level_dict. If current experience is equal to or more than the required
            experience, then levels up and shows the required experience to get to the next level.
            It contains an upgrader_level functions which takes care of the buffing of the Player
            after level up. Finally, prints the details of the Player.

        upgrader_level(): Buffs the Player's health by times of 10 and then the
            Player's attack_power by times of 8.

        __str__(): Prints the Details of the Player object.
    """
    obj_lists_player = []

    def __init__(self, name):
        super().__init__(name=name, health=100, attack_power=30, inventory=[])
        self.experience = 0
        self.level = 1
        self.level_dict = {level: level * 3000 for level in range(1, 101)}
        self.obj_lists_player.append(self)
        self.same_name()

    def equip(self, item: str):

        not_found = super().equip(item=item)

        if not not_found:
            print(f"The specified item '{item.title()}' Not Found in the inventory. Buy the item from the shop")

            items_inventory_names = [item_names.name.casefold() for item_names in self.inventory]
            suggestions = difflib.get_close_matches(item, items_inventory_names)

            if suggestions:
                print(f"Do you mean {suggestions[0].title()}?")
                confirmation = input("Confirmation: ").strip().casefold()
                if confirmation == 'yes':
                    self.equip(suggestions[0])
            else:
                print(f'Item Not found')

    def attack(self, target: 'Enemy') -> None:
        """
        Attacks the target object, Uses the superclasses attack method
        and further increases the experience of the Player object by 1000 per kill and also
        calls the level_up() which is responsible for upgrading the level of the Player.

        :param target: The target object to be attacked
        """
        super().attack(target=target)
        if target.health > 0 >= target.life and target.alive:
            self.experience += 1000
            self.level_up()

        if target.alive:
            target.special_weapon()

    def level_up(self) -> None:
        """
        Responsible for Upgrading the level of the Player object if it reaches a certain criteria.
        The conditions are being contained in the level_dict. Checks if the Player is able to level up
        after some gaining of experience and also when leveling up the Player restores to full health.
        It calls the _upgrader_level() which is responsible for buffs after reaching the levels.
        Buffs include health, attack_power, life, defense, etc.

        """
        for level, experience in self.level_dict.items():
            if level >= self.level and self.experience >= experience:
                self.level += 1
                print(f"{self.name} levelled up to {self.level}")
                self.health = self.full_health
                self._upgrader_level()
                next_level = self.level_dict.get(level + 1)
                print(f"Get {next_level} to move next up next level")
                print(self.__str__())

    def _upgrader_level(self) -> None:
        """Increases the power of the Player Character after leveling up"""
        self.health += self.level * 3
        self.attack_power += self.level * 8

    def __str__(self) -> str:
        """Returns the details of the Player Character"""
        return f"""
        Name: {self.name}
        Health: {self.health}
        Life: {self.life}
        Attack Power: {self.attack_power}
        Experience: {self.experience}
        Level: {self.level}
        """

    def __repr__(self):
        return ("Player(Name: '{0.name}',  Health: {0.health}, Power: {0.attack_power}, "
                "Life: {0.life}, Experience: {0.experience}, Level: {0.level}, "
                "Inventory: List({0.inventory}))").format(self)

    def __eq__(self, other):  # used as ==
        if isinstance(other, Player):
            if other.name == self.name:
                return True
        return False

    def same_name(self):  # just give an error instead of inputting a new name
        new_lists = self.group_name()
        if new_lists:
            for first, second in new_lists:
                same_name_bool = first.__eq__(second)
                if same_name_bool:
                    print(f"Objects {first.name} of {id(first)} and {second.name} of {id(second)} "
                          f"have same names which is not allowed")
                    print(f"Below is the prompt to change the name of the object")
                    new_name = input(f"Enter a new name for the object {second.name}: ").strip().capitalize()
                    second.name = new_name

    def group_name(self):
        main_list = []
        if len(self.obj_lists_player) >= 2:
            for index in range(len(self.obj_lists_player)):
                for an_index in self.obj_lists_player:
                    first_element = self.obj_lists_player[index]
                    second_element = an_index
                    check = self.swap_check(first_element, second_element, main_list)
                    if check:
                        in_tup = (first_element, second_element)
                        main_list.append(in_tup)

        return main_list

    @staticmethod
    def swap_check(first, second, main_list):
        tup1 = first, second
        tup2 = second, first

        if tup1 or tup2 not in main_list:
            if first is second or tup2 in main_list:
                return False
        return True


class Enemy(Character):

    def __init__(self, name=None):
        if name is not None:
            super().__init__(name=name, health=35, attack_power=12, inventory=[])
        else:
            super().__init__(name='Enemy', health=35, attack_power=12, inventory=[])

    def random_weapon(self):
        from shop_class import Shop
        enemy_shop = Shop()
        # _set_choice = set(enemy_shop.enemies_weapons)
        rand_choice = random.choice(enemy_shop.enemies_weapons)
        if len(self.inventory) < 1:
            enemy_shop.buy_item(rand_choice.name, self)
            return True
        return False

    def equip_weapon(self):
        item = self.random_weapon()
        if item:
            for weapons in self.inventory:
                self.equip(weapons.name)

    def special_weapon(self):
        if self.life <= 1:
            if self.health <= (self.full_health * 90 / 100) or self.life == 0:
                self.equip_weapon()

    def __repr__(self):
        return ("Enemy(Name: '{0.name}',  Health: {0.health}, Power: {0.attack_power}, "
                "Life: {0.life}, Inventory: List({0.inventory}))").format(self)


class Goblin(Enemy):

    def __init__(self, name=None):
        if name is not None:
            super().__init__(name=name)
        else:
            super().__init__(name='Goblin')
        self.health = 15
        self.attack_power = 10
        self.life = 2

    def take_damage_self(self, attacker: Character, amount: int) -> None:

        chance = self.chance_event(1, 5)

        if not chance:
            super().take_damage_self(attacker, amount)
        else:
            print(f"{self.name} has dodged!")


class Dragon(Enemy):

    def __init__(self, name=None):
        if name is not None:
            super().__init__(name=name)
        else:
            super().__init__(name='Dragon')
        self.health = 50
        self.attack_power = 40
        self.life = 1

    def take_damage_self(self, attacker: Character, amount: int) -> None:
        amount = amount // 3
        super().take_damage_self(attacker, amount)


class Zombie(Enemy):

    def __init__(self, name=None):
        if name is not None:
            super().__init__(name=name)
        else:
            super().__init__(name='Goblin')
        self.health = 100
        self.attack_power = 20
        self.life = 3

    def take_damage_self(self, attacker: Character, amount: int) -> None:
        chances = self.chance_event(1, 8)

        super().take_damage_self(attacker, amount=amount)

        if chances:
            self.life += 1
            print(f"Zombies occasionally gets a life")
            print(f"Lives: {self.life}")


if __name__ == '__main__':
    ash = Player("Ash")
    zombie_1 = Goblin("zombie")
    ash.attack(zombie_1)
    print(zombie_1.defense)
