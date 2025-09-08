from game_class import Game

main_disp = {
    1: 'Start Game',
    2: 'Quit'
}


def print_dict(dict_to_print):
    for index, choices in dict_to_print.items():
        print(f'{index}: {choices}')


def get_choice(prompt, choice_dict):
    while True:
        temp = input(prompt)
        if temp.isnumeric() and int(temp) in choice_dict:
            return int(temp)
        else:
            print("Please enter a correct choice")


battle_choice = {
    1: 'Battle',
    2: 'Use Item',
    3: 'Menu',
    4: 'Escape',
}

menu_choice = {
    1: 'Shop',
    2: 'Inventory',
    3: 'Quit',
}

shop_choice = {
    1: 'Display Item',
    2: 'Buy Item',
    3: 'Sell Item',
}



def main():
    print_dict(main_disp)
    val = get_choice('<<< ', main_disp)
    if val != 2:
        name = input("Input a name for the Player: ").strip().capitalize()
        main_game = Game(name)
        main_game.start_game()
        while True:
            print()
            directions_available = main_game.current_directions
            print(f"Available directions: ")
            print_dict(directions_available)
            walk = get_choice('Enter a number to get the directions: ', directions_available)
            if walk == 0:
                break
            direction = directions_available[walk]
            main_game.explore(direction)
            for enemy in main_game.enemies.copy():
                print_dict(battle_choice)
                print(f"Number of Enemies remaining: {len(main_game.enemies)}")
                while enemy.alive:
                    choice_battle = get_choice("Your choice: ", battle_choice)
                    if choice_battle == 1:
                        main_game.battle(enemy)
                        if not main_game.player.alive:
                            print("You died!")
                            break
                    elif choice_battle == 2:
                        main_game.player.print_items()
                        item_gonna_use = input("The item to use: ").casefold().strip().capitalize()
                        main_game.player.equip(item_gonna_use)
                    elif choice_battle == 3:
                        print_dict(menu_choice)
                        menu_chose = get_choice('Menu choice: ', menu_choice)
                        if menu_chose == 1:
                            print('You opened Shop')
                            shop = main_game.shop()
                            print_dict(shop_choice)
                            shop_chose = get_choice('Shop Menu choice: ', shop_choice)
                            if shop_chose == 1:
                                shop.display_items()
                            elif shop_chose == 2:
                                item_to_use = input("The item to buy: ").casefold().strip().capitalize()
                                shop.buy_item(item_to_use, main_game.player)
                            elif shop_chose == 3:
                                item_to_sell = input("The item to sell: ").casefold().strip().capitalize()
                                # need to write functions to sell
                                shop.sell_item(item_to_sell, main_game.player)
                        elif menu_chose == 2:
                            print("You opened Player's Inventory")
                            main_game.player.print_items()
                        elif menu_chose == 3:
                            print('Are you sure you want to quit the game? [Yes/No]: ')
                            confirmation = input().casefold().strip()
                            if confirmation == 'yes':
                                break

                    elif choice_battle == 4:
                        main_game.escape()
                        print("You escaped")
                        break

                else:
                    main_game.enemies.remove(enemy)
                main_game.explored_paths.append(direction)
                break


            main_game.escape()
            main_game.available_directions()


if __name__ == "__main__":
    main()
