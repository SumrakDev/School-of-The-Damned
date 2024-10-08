import random
from dataclasses import dataclass, field
from data_for_items import medic_names, weapon_names, misc_names
from data_game_loc import united_list

@dataclass
class Objects:
    name: str = "None"
    image: str = "None"
    type_obj: str = "None"
    id: int = 0

    def set_type(self, type: str):
        self.__dict__["type_obj"] = type


@dataclass
class Trait(Objects):
    trigger: str = "None"
    text: str = "None"
    trait_contaiment: dict = field(default_factory=lambda: {})

    def triger_changer(self, new_trigger: str):
        self.__dict__["trait_trigger"] = new_trigger

    def __post_init__(self):
        self.set_type("Trait")


@dataclass
class Monster(Objects):
    monster_descrip: str = "None"

    def generate_monster(self):
        start: str = random.choice(["Ужасное",
                                    "Отвратительное",
                                    "Мерзкое"])
        head_count: str = random.choice(["одноголовое",
                                         "двуголове",
                                         "трехголовое"])
        hands_count: str = random.choice(["двумя",
                                          "тремя",
                                          "шестью"])
        type_hand: str = random.choice(["руками",
                                        "щупальцами",
                                        "отростками"])
        descrip: str = "{} {} существо с {} {}".format(start,
                                                       head_count,
                                                       hands_count,
                                                       type_hand)
        self.__dict__["monster_descrip"] = descrip
        self.__dict__["name"] = ("Тварь " +
                                          str(random.randrange(1, 99)))

    def __post_init__(self):
        self.set_type("Monster")
        self.generate_monster()

    def get_index(self, new_index: int):
        self.__dict__["index"] = new_index


@dataclass
class Item(Objects):
    type_item: str = "None"
    action_item: str = "Item was used"

    def generate_item(self):
        self.__dict__["type_item"] = random.choice(["Weapon",
                                                    "Medicine",
                                                    "Misc"])
        if self.type_item == "Weapon":
            self.__dict__["name"] = random.choice(weapon_names)
        elif self.type_item == "Misc":
            self.__dict__["name"] = random.choice(misc_names)
        elif self.type_item == "Medicine":
            self.__dict__["name"] = random.choice(medic_names)

    def __post_init__(self):
        self.set_type("Item")
        self.generate_item()

    def get_index(self, new_index: int):
        self.__dict__["index"] = new_index


@dataclass
class Player(Objects):
    player_traits: dict = field(default_factory=lambda: {})
    player_action: dict = field(default_factory=lambda: {})
    player_inventory: dict = field(default_factory=lambda: {})

    def get_trait(self, new_trait: Trait):
        self.player_traits[new_trait.trait_name] = new_trait

    def remove_trait(self, lose_trait: Trait):
        del self.player_traits[lose_trait.trait_name]

    def return_traits(self):
        return self.player_traits

    def get_item(self, item: Item):
        self.player_inventory[item.name] = Item()


@dataclass
class Location(Objects):
    connection: list = field(default_factory=lambda: [])
    loc_content: dict = field(default_factory=lambda: {})

    def content_prepare(self):
        self.loc_content["NPC"] = []
        self.loc_content["Item"] = []
        self.loc_content["Monster"] = []
        self.loc_content["Events"] = []

    def add_content(self, obj: Objects):
        for key in self.loc_content.keys():
            if obj.type_obj == key:
                self.loc_content[key].append(obj)

    def generate_name(self, name: str):
        self.__dict__['name'] = name

    def create_id(self):
        self.__dict__["id"] = random.randrange(1, 10000)

    def full_celar_loc(self):
        self.loc_content.clear()

    def __post_init__(self):
        self.set_type("Location")
        self.create_id()
        self.content_prepare()

    def create_connection(self, locations: list):
        self.__dict__["connection"] = locations

    def return_connection(self):
        return self.connection


@dataclass
class Game:
    monsters_count: int = 3
    items_count: int = 3
    game_data: list = field(default_factory=lambda: [])
    game_map: dict = field(default_factory=lambda: {})
    player: Player = field(default_factory=Player)

    def create_monster(self):
        for i in range(self.monsters_count):
            self.game_data.append(Monster())

    def create_item(self):
        for i in range(self.items_count):
            self.game_data.append(Item())

    def create_loc(self):
        for i in range(0, len(united_list)):
            location = Location()
            location.generate_name(united_list[i])
            self.game_map[location.name] = location

    def __post_init__(self):
        self.create_monster()
        self.create_item()
        self.create_loc()

    def generate_content(self):
        for obj in self.game_data:
            [self.game_map[loc_key].add_content(obj) for loc_key in self.game_map.keys()]

    def __str__(self):
        location = [self.game_map[loc] for loc in self.game_map.keys()]
        return f"""Общая дата: {[obj.name for obj in self.game_data]}
Карта: {[obj for obj in self.game_map.keys()]}
////////////////////////////
Локация: {location[0].name}
    Монстры: {[obj.name for obj in location[0].loc_content["Monster"]]}
    Предметы: {[ obj.name for obj in location[0].loc_content["Item"]]}"""


game = Game()
print(game)
