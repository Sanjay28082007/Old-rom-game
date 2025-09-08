import random

class Room:

    def __init__(self):
        self.directions_dict = {
            'n': 'north',
            'e': 'east',
            'w': 'west',
            's': 'south'
        }

    def _swap_number(self, *args, main_list):
        same_check = self._same_number(*args)

        reverse = sorted(args)
        addition = "".join(reverse)

        if same_check:
            if addition not in main_list:
                return addition
        return False

    def _same_number(*args):
        numbers = set(args)

        return len(numbers) == len(args)

    def calculate_directions(self):
        inner_list = []
        max_depth = len(self.directions_dict)

        def recurse(current_combo):
            check = self._swap_number(*current_combo, main_list=inner_list)
            if check:
                inner_list.append(check)

            if len(current_combo) == max_depth:
                return

            for inner_direction in self.directions_dict:
                recurse(current_combo + [inner_direction])

        for direction in self.directions_dict:
            recurse([direction])

        return inner_list

    def random_directions(self):
        directions_list = self.calculate_directions()

        current_direction = random.choice(directions_list)

        return current_direction


    def split_directions(self):
        directions = self.random_directions()

        split_list = [self.directions_dict.get(direction) for direction in directions]

        return split_list



if __name__ == "__main__":
    room = Room()
    value = room.split_directions()
    print(value)




