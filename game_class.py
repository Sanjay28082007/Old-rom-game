from character_class import *
from item_class import *
from shop_class import *
from map_class import *

class Game:
    explored_paths = []

    def __init__(self, name):
        self.player = Player(name)
        self.enemies = []
        self.main_shop = Shop()
        self.game_map = Room()
        self.current_directions = {}
        self.available_directions()

    @staticmethod
    def start_game():

        filename = 'Files/game_intro.txt'

        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()

        print(f"The game starts.... ")
        print()
        print(data)

    def explore(self, direction):

        print(f"You moved {direction}")
        self.no_of_enemies()
        if self.enemies:
            print('Enemies Found')
        else:
            print('No enemies Found')


    def available_directions(self):
        rand_map = self.game_map.split_directions()

        rand_dict = {}

        for index, direction in enumerate(rand_map):
            rand_dict[index + 1] = direction

        self.current_directions = rand_dict


    def battle(self, current_enemy):
        self.player.attack(current_enemy)
        current_enemy.attack(self.player)

    @staticmethod
    def enemy_in_path():
        list_of_enemies = []
        sub_classes = Enemy.__subclasses__()
        number = random.randint(0, 3)

        for i in range(number):
            enemy_in = random.choice(sub_classes)
            list_of_enemies.append(enemy_in)

        return list_of_enemies

    def no_of_enemies(self):
        enemies = self.enemy_in_path()
        number = random.randint(1, 3)

        if enemies:
            for enemy_times in enemies:
                for _ in range(0, number):
                    self.enemies.append(enemy_times())


    def shop(self):
        return self.main_shop


    def escape(self):
        self.enemies.clear()
        self.current_directions.clear()





if __name__ == "__main__":
    game = Game('name')
    print(game.current_directions)
    _, directions = game.current_directions.popitem()
    print(_, directions)
    game.explore(directions)
    print(game.enemies)
    for enemy in game.enemies:
        print(enemy)