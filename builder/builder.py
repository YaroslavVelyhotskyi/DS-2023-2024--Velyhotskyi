import json
#import curses
import keyboard
import sys
import os
sys.path.append(os.getcwd())
from solution.game import Game
from solution.maze import Maze, Trap, Room, Door, SpikedDoor, Wall, Bomb, Rectangle, Hexagon, North, East, South, West, Northeast, Southeast, Southwest, BonusHP,BonusPower, FloorHole,Northwest,Open,Close,Enter
from solution.creatures import Beast,Aggressive,Lazy, FatBeast, HealerBeast, NormalType, StrongType, TitanType, Person
import time

class Director:
    def __init__(self):
        self.dict=None
        self.builder=None

    def procesar(self,filename):
        self.leer_archivo(filename)
        self.iniBuilder()
        self.crear_laberinto()
        self.crear_game()
        self.crear_beasts()
        self.crear_bonuses() 
        self.crear_traps()
        self.crear_holes()
        self.set_character_type()

    def set_character_type(self):
        character_type_str = self.dict.get("character_type", "normal").lower()
        if character_type_str == "normal":
            character = self.builder.makeNormalCharacter()
        elif character_type_str == "strong":
            character = self.builder.makeStrongCharacter()
        elif character_type_str == "titan":
            character = self.builder.makeTitanCharacter()
        else:
            print(f"Invalid character type: {character_type_str}. Using default (normal).")
            character = self.builder.makeNormalCharacter()

        self.builder.game.addPerson(character)
        self.person = self.builder.game.person

    def leer_archivo(self, filename):
        try:
            with open(filename) as f:
                data = json.load(f)
                self.dict= data
        except FileNotFoundError:
            print(f"File {filename} does not exist")
            return None
    
    def iniBuilder(self):
        if (self.dict['form'] == 'rectangle'):
            self.builder=LaberintoBuilder()
        elif (self.dict['form'] == 'hexagon'):
            self.builder=LaberintoHexagonalBuilder()
        else:
            print("Form not found")
            return None

    def getGame(self):
        return self.builder.getGame()

    def crear_game(self):
        if self.builder is None:
            print("Error: Builder not initialized correctly.")
            return
        self.builder.makeGame()
        self.set_character_type()

    def crear_laberinto(self):
        self.builder.makeMaze()
        
        for each in self.dict['maze']:
            self.crear_laberinto_recursivo(each, 'root')
            
        for each in self.dict['doors']:
            n1 = each[0]
            or1 = each[1]
            n2 = each[2]
            or2 = each[3]
            door_type = each[4] if len(each) > 4 else "normal"
            
            if door_type == "spiked":
                self.builder.makeSpikedDoor(n1, or1, n2, or2)
            else:
                self.builder.makeDoor(n1, or1, n2, or2)

        
    def crear_laberinto_recursivo(self, un_dic, padre):
    
        if un_dic['tipo'] == 'room':
            con = self.builder.makeRoom(un_dic['num'])
            
        if un_dic['tipo'] == 'bomb':
            self.builder.makeBombIn(padre)
        
        
        if 'hijos' in un_dic:
            for each in un_dic['hijos']:
                self.crear_laberinto_recursivo(each, con)
    
    def crear_traps(self):
        for trap in self.dict['traps']:
            damage_value = trap['damage']
            room_num = trap['posicion']
            self.builder.makeTrap(room_num, damage_value)
            print(f"Trap ({damage_value} damage) created in room {room_num}")

    def crear_bonuses(self):
        for bonus in self.dict['bonuses']:
            bonus_type = bonus['tipo']
            bonus_value = bonus['valor']
            room_num = bonus['posicion']
            self.builder.makeBonusElement(room_num, bonus_type, bonus_value)
            print(f"Bonus ({bonus_type}, {bonus_value}) placed in room {room_num}")
    
    def crear_holes(self):
        for hole in self.dict['floorHoles']:
            damage_value = hole['damage']
            room_num = hole['posicion']
            self.builder.makeFloorHole(room_num, damage_value)
            print(f"Trap ({damage_value} damage) created in room {room_num}")

    def crear_beasts(self):
        for each in self.dict['beasts']:
            modo = each['modo']
            if modo == 'Aggressive':
                self.builder.makeAggressiveBeastPosition(each['posicion'])
            elif modo == 'Lazy':
                self.builder.makeLazyBeastPosition(each['posicion'])
            elif modo == 'Fat':
                self.builder.makeFatBeastPosition(each['posicion'])
            elif modo == 'Healer':
                self.builder.makeHealerBeastPosition(each['posicion'])

class LaberintoBuilder:
    def __init__(self):
        self.game = None
        self.maze = None
        self.dict = dict

    def getGame(self):
        return self.game
    
    def makeGame(self):
        self.game = Game()
        self.game.prototype =self.maze
        self.game.maze = self.game.cloneMaze()

    def makeForm(self,num):
        return Rectangle(num)
     
    def makeMaze(self):
        self.maze= Maze()
    
    def makeWall(self):
        return Wall()
    
    def makeDoor(self, arg1, arg2, arg3=None, arg4=None):
        if arg3 is None and arg4 is None:
            # Case when called with two room objects
            room1, room2 = arg1, arg2
        else:
            # Case when called with room numbers and orientations
            room1 = self.maze.getRoom(arg1)
            room2 = self.maze.getRoom(arg3)
            or1 = getattr(self, f'make{arg2}')()
            or2 = getattr(self, f'make{arg4}')()

        door = Door(room1, room2)

        if arg3 is not None and arg4 is not None:
            # Set orientations only if they are provided
            room1.setEMinOr(door, or1)
            room2.setEMinOr(door, or2)

        return door

    def makeSpikedDoor(self, arg1, arg2, arg3=None, arg4=None):
        if arg3 is None and arg4 is None:
            # Case when called with two room objects
            room1, room2 = arg1, arg2
        else:
            # Case when called with room numbers and orientations
            room1 = self.maze.getRoom(arg1)
            room2 = self.maze.getRoom(arg3)
            or1 = getattr(self, f'make{arg2}')()
            or2 = getattr(self, f'make{arg4}')()

        door = SpikedDoor(room1, room2)
        print(f"Created SpikedDoor between rooms {room1} and {room2}")  # Debug print

        if arg3 is not None and arg4 is not None:
            # Set orientations only if they are provided
            room1.setEMinOr(door, or1)
            room2.setEMinOr(door, or2)

        return door

    def makeBombIn(self, room):
        bomb=Bomb()
        room.addChild(bomb)
        return bomb
    
    def makeTrap(self, room_num, damage_value):
        room = self.game.getRoom(room_num)
        trap = Trap(damage_value)
        room.addChild(trap)
        print(f"Trap ({damage_value} damage) placed in room {room_num}")

    def makeFloorHole(self, room_num,damage_value):
        room = self.game.getRoom(room_num)
        hole = FloorHole(damage_value)
        room.addChild(hole)
        print(f"FloorHole ({damage_value} damage) placed in room {room_num}")

    def makeBonusElement(self, room_num, bonus_type, bonus_value):
        room = self.game.getRoom(room_num)
        if bonus_type == "HP":
            bonus_element = BonusHP(bonus_value)
        elif bonus_type == "Power":
            bonus_element = BonusPower(bonus_value)
        else:
            raise ValueError(f"Unknown bonus type: {bonus_type}")
        room.addChild(bonus_element)
        print(f"Bonus ({bonus_type}, {bonus_value}) created in room {room_num}")


    def makeRoom(self, num):
        room=Room(num)
        room.form=self.makeForm(num)
    # room.addOrientation(self.makeNorth())
        # room.addOrientation(self.makeEast())
        # room.addOrientation(self.makeSouth())
        # room.addOrientation(self.makeWest())
        for each in room.getOrientations():
            each.setEMinOr(self.makeWall(), room.form)
        self.maze.addRoom(room)
        return room

    def makeNorth(self):
        return North().get_instance()

    def makeEast(self):
        return East.get_instance()
    
    def makeSouth(self):
        return South().get_instance()
    
    def makeWest(self):
        return West().get_instance()
    
    def makeDoor(self, un_num, una_or_string, otro_num, otra_or_string):
        lado1 = self.maze.getRoom(un_num)
        lado2 = self.maze.getRoom(otro_num)
        
        or1 = getattr(self, 'make'+una_or_string)()
        or2 = getattr(self, 'make'+otra_or_string)()
        
        pt = Door(lado1, lado2)
        pt.addCommand(Open(pt))
        lado1.setEMinOr(pt,or1) 
        lado2.setEMinOr(pt,or2)

    
    def makeNormalCharacter(self):
        character_type = NormalType()
        character = Person("Pepe", character_type)
        character.power = 1
        character.life = 20
        return character

    def makeStrongCharacter(self):
        character_type = StrongType()
        character = Person("Pepe", character_type)
        character.power = 3
        character.life = 30
        return character
    
    def makeTitanCharacter(self):
        character_type = TitanType()
        character = Person("Pepe", character_type)
        character.power = 20
        character.life = 50
        return character
    
    def makeAggressiveBeast(self):
        beast = Beast(Aggressive())
        beast.power = 3  # Set the power value for lazy beasts
        return beast
    
    def makeLazyBeast(self):
        beast = Beast(Lazy())
        beast.power = 1  # Set the power value for lazy beasts
        return beast

    def makeFatBeast(self):
        beast = Beast(FatBeast())
        beast.power = 1  # Set a low power value for Fat Beasts
        beast.life = 20  # Set a higher life value for Fat Beasts
        return beast

    def makeHealerBeast(self):
        beast = Beast(HealerBeast())
        beast.power = 0  # Set a moderate power value for Healer Beasts
        beast.life = 1  # Set a standard life value for Healer Beasts
        return beast

    def makeAggressiveBeastPosition(self, num):
        room = self.game.getRoom(num)
        beast = self.makeAggressiveBeast()
        beast.position = room
        self.game.addBeast(beast)

    def makeLazyBeastPosition(self, num):
        room = self.game.getRoom(num)
        beast = self.makeLazyBeast()
        beast.position = room
        self.game.addBeast(beast)

    def makeFatBeastPosition(self, num):
        room = self.game.getRoom(num)
        beast = self.makeFatBeast()
        beast.position = room
        self.game.addBeast(beast)

    def makeHealerBeastPosition(self, num):
        room = self.game.getRoom(num)
        beast = self.makeHealerBeast()
        beast.position = room   
        self.game.addBeast(beast)

class LaberintoHexagonalBuilder(LaberintoBuilder):
    def makeForm(self):
        return Hexagon()
    
    def makeRoom(self):
        room = Room()
        room.form = self.makeForm()                           
        for each in room.getOrientations():
            each.setEMinOr(self.makeWall(), room.form)
        self.maze.addRoom(room)
        return room
      

def main(): #stdscr

    director=Director()
    director.procesar(os.getcwd()+'\\json\\maze6room6beasts.json')
    game=director.getGame()
    game.addPerson("Pepe")
    person=game.person
    game.openDoors()
    game.launchThreds()
    
    while True:
        if keyboard.is_pressed('q'):
            break  # Exit the program
        elif keyboard.is_pressed("w"):  # curses.KEY_UP:
            person.goNorth()
            time.sleep(0.5)  # Add a delay after moving the character
        elif keyboard.is_pressed("s"):  # curses.KEY_DOWN:
            person.goSouth()
            time.sleep(0.5)  # Add a delay after moving the character
        elif keyboard.is_pressed("a"):  # curses.KEY_LEFT:
            person.goWest()
            time.sleep(0.5)  # Add a delay after moving the character
        elif keyboard.is_pressed("d"):  # curses.KEY_RIGHT:
            person.goEast()
            time.sleep(0.5)  # Add a delay after moving the character
        elif keyboard.is_pressed("enter"):  # curses.KEY_ENTER or key in [10, 13]:
            person.attack()
            time.sleep(0.5)  # Add a delay after attacking

    game.stopThreds()
#main()


