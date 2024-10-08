init python:
    import random
    from gameplay import Trait, Monster, Item, Player, Location, Game

screen map:
    frame:
        vbox:
            for location_key in main_game.game_loc.keys():
                textbutton "[location_key]" action (Function(game.go_to_location, location_key),
                                                    Jump("location_label"))

screen location:
    python:
        name = test_loc.name
        items_loc = [item.name for item in test_loc.loc_content["Item"]]
        monsters_loc = [monster.name for monster in test_loc.loc_content["Monster"]]

    frame:
        vbox:
            text "Имя локации: [test_loc.name]"
            text "Предметы локации: [items_loc]"
            text "Монстры локации: [monsters_loc]"
            text "ID локации:[test_loc.id]"


label start:

    python:
        monsters_count = renpy.input("Введите число монстров", length = 2)
        items_count = renpy.input("ВВедите число предметов", length = 2)
        monsters_num = int(monsters_count)
        items_num = int(items_count)
        game = Game(monsters_count= monsters_num, items_count=items_num)
        game.generate_content()
        image = "bg cafeteria"
        main_game = game

    "Калибровка связи..."

    "Стабилизация соеднинения..."

    
    python:
        test_loc = random.choice([location for location in game.game_map.values()])

    image location_image:
        Frame("[image]")

    "Доступность данных...1 процент"

    "Загрузка..."

    jump location_label


label location_label:
    scene location_image with dissolve
    
    call screen location


label map_label:

    call screen map