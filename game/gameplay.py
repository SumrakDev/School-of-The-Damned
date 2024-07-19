import random
from dataclasses import dataclass, field
from game.data_for_items import medic_names, weapon_names, misc_names


@dataclass
class Trait:
    trait_name: str = "None"
    type_obj: str = "Trait"
    trait_trigger: str = "None"
    trait_text: str = "None"
    trait_contaiment: dict = field(default_factory=lambda: {})

    def triger_changer(self, new_trigger: str):
        self.__dict__["trait_trigger"] = new_trigger


@dataclass
class Monster:
    name: str = "None"
    type_obj: str = "Monster"
    image: str = ""
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
        self.__dict__["monster_banme"] = ("Тварь " +
                                          str(random.randrange(1, 99)))

    def __post_init__(self):
        self.generate_monster()

    def get_index(self, new_index: int):
        self.__dict__["index"] = new_index


@dataclass
class Item:
    name: str = "None"
    type_obj: str = "Item"
    image: str = ""
    type_item: str = "None"
    action_item: str = "Item was used"

    def generate_item(self):
        self.__dict__["type_item"] = random.choice(["Weapon",
                                                    "Medicine",
                                                    "Misc"])
        if self.type_item == "Weapon":
            self.__dict__["item_name"] = random.choice(weapon_names)
        elif self.type_item == "Misc":
            self.__dict__["item_name"] = random.choice(misc_names)
        elif self.type_item == "Medicine":
            self.__dict__["item_name"] = random.choice(medic_names)

    def __post_init__(self):
        self.generate_item()

    def get_index(self, new_index: int):
        self.__dict__["index"] = new_index


@dataclass
class Player:
    name: str = "None"
    type_obj: str = "Player"
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
        self.player_inventory[item.item_name] = Item()


@dataclass
class Location:
    name: str = "None"
    type_obj: str = "Location"
    id: int = 0
    image: str = "None"
    connection: list = field(default_factory=lambda: [])
    loc_content: dict = field(default_factory=lambda: {})

    def content_prepare(self):
        self.loc_content["NPC"] = []
        self.loc_content["Items"] = []
        self.loc_content["Monsters"] = []
        self.loc_content["Events"] = []

    def create_id(self):
        self.__dict__["id"] = random.randrange(1, 10000)

    def full_celar_loc(self):
        self.loc_content.clear()

    def __post_init__(self):
        self.create_id()
        self.content_prepare()

    def create_connection(self, locations: list):
        self.__dict__["connection"] = locations

    def return_connection(self):
        return self.connection


@dataclass
class Game:
    monsters: int = 3
    items: int = 3
    game_data: list = field(default_factory=lambda: [])
    game_map: list = field(default_factory=lambda: [])
    game_loc: dict = field(default_factory=lambda: {})
    player: Player = field(default_factory=Player)
    current_location: Location = field(default_factory=Location)

    def create_game_items(self):
        for i in range(self.items):
            item = Item()
            self.game_data.append(item)

    def create_game_monsters(self):
        for i in range(self.monsters):
            monster = Monster()
            self.game_data.append(monster)

    def create_objects(self):
        npc: dict = {}
        items: dict = {}
        monsters: dict = {}
        events: dict = {}

        for obj in self.game_data:
            if obj.type_obj == "NPC":
                npc[obj.name] = obj
            elif obj.type_obj == "Item":
                items[obj.name] = obj
            elif obj.type_obj == "Monster":
                monsters[obj.name] = obj
            elif obj.type_obj == "Event":
                events[obj.name] = obj

        work_list = [npc, items, monsters, events]
        self.game_data.clear()
        self.__dict__["game_data"] = work_list

    def prepare_map(self):
        locations = {}
        for location in self.game_map:
            locations[location.name] = location
        self.__dict__["game_loc"] = locations

    def __post_init__(self):
        self.create_game_items()
        self.create_game_monsters()
        self.create_objects()

    def get_random_value(self, dictionary):
        keys = list(dictionary.keys())
        random_key_index = random.randint(0, len(keys) - 1)
        return dictionary[keys[random_key_index]]

    def fill_loc(self):
        item = self.get_random_value(self.game_data[1])
        monster = self.get_random_value(self.game_data[2])
        self.current_location.loc_content["Items"].append(item)
        self.current_location.loc_content["Monsters"].append(monster)

    def go_to_location(self, location: str):
        self.__dict__["current_location"] = self.game_loc[location]
        self.fill_loc()
