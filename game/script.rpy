init python:
    import random
    from gameplay import Trait, Monster, Item, Player, Location, Game

screen map:
    frame:
        vbox:
            for location_key, location_value in main_game.game_loc.items():
                textbutton "[location_key]" action (Function(game.go_to_location, location_key),
                                                    Jump("location_label"))

screen location:

    frame:
        vbox:
            text "[main_game.current_location.name]"
            text "[main_game.current_location.type_obj]"
            text "[main_game.current_location.image]"
            text "[main_game.current_location.id]"
            textbutton "Перейти в другую локацию" action Jump("map_label")


label start:

    python:
        cafeteria = Location(name="Столовая",
                            image="bg cafeteria.png",
                            connection=["Столовая"])
        school_map = [cafeteria]
        game = Game(monsters=3, items=3, game_map=school_map)
        main_game = game

    "Калибровка связи..."

    "Стабилизация соеднинения..."

    
    python:
        game.prepare_map()
        game_map = list(game.game_loc.keys())
        game.go_to_location(random.choice(game_map))

    image location_image:
        Frame("[main_game.current_location.image]")

    "Доступность данных...1 процент"

    "Загрузка..."

    jump location_label


label location_label:
    scene location_image with dissolve

    python:
        items = game.current_location.loc_content["Items"]
    
    call screen location


label map_label:

    call screen map