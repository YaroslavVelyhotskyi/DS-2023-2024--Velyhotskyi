from .maze import Maze, Room, Door, Wall, BombedWall, Bomb, North, East, South, West, Northeast, Southeast, Southwest, Northwest, Rectangle
from solution.creatures import Beast, Mode, Aggressive, Lazy, Person
from solution.threadManager import ThreadManager
import copy
import time

class Game:
    def __init__(self):
        self.maze = None
        self.beasts = []
        self.person=None
        self.prototype = None
        self.threadManager = ThreadManager()
       
    def getRoom(self, id):
        return self.maze.getRoom(id)
    
    def launchThreads(self):
        print("The creatures start to move...")
        for beast in self.beasts:
            self.threadManager.addThread(beast)
        if self.person:
            self.threadManager.addThreadPerson(self.person)
        
        self.threadManager.start()

    def stopThreads(self):
        print("The creatures are stopped...")
        self.threadManager.stop()


    def check_ultimate_status(self):
        if self.person.isTitan():
            return "ready" if self.person.ultimate_available else "not ready"
        return "not available"

    def use_titan_ultimate(self):
        if self.person.use_ultimate():
            print("The Titan's ultimate ability destroys all beasts!")
            self.beasts.clear()
            return True
        return False

    
    def makeWall(self):
        return Wall()
    
    def makeDoor(self,room1, room2):
        door=Door(room1, room2)
        return door

    def makeRoom(self, id):
        room=Room(id)
        room.form=self.makeForm(id)
        room.addOrientation(self.makeNorth())
        room.addOrientation(self.makeEast())
        room.addOrientation(self.makeSouth())
        room.addOrientation(self.makeWest())
        room.north=self.makeWall()
        room.east=self.makeWall()
        room.south=self.makeWall()
        room.west=self.makeWall()
        return room

    def makeForm(self,num):
        return Rectangle(num)

    def makeNorth(self):
        return North().get_instance()

    def makeEast(self):
        return East.get_instance()
    
    def makeSouth(self):
        return South().get_instance()
    
    def makeWest(self):
        return West().get_instance()
    
    def makeSoutheast(self):
        return Southeast().get_instance()

    def makeSouthwest(self):
        return Southwest().get_instance()

    def makeNortheast(self):
        return Northeast().get_instance()

    def makeNorthwest(self):
        return Northwest().get_instance()
      
    def createMaze2Room(self):
        maze = Maze()
        self.maze = maze
        room1 = Room(1)
        room2 = Room(2)

        door=Door(room1, room2)

        room1.south = door  
        room2.north = door

        self.maze.addRoom(room1)
        self.maze.addRoom(room2)

    def create4Room4BeastFM(self):
        room1 = self.makeRoom(1)
        room2 = self.makeRoom(2)
        room3 = self.makeRoom(3)
        room4 = self.makeRoom(4)
        
        door12 = self.makeDoor(room1, room2)
        door13 = self.makeDoor(room1, room3)
        door24 = self.makeDoor(room2, room4)
        door34 = self.makeDoor(room3, room4)
        
        room1.south = door12
        room2.north = door12
        
        room1.east = door13
        room3.west = door13
        
        room2.east = door24
        room4.west = door24
        
        room3.south = door34
        room4.north = door34
        
        maze = Maze()
                
        maze.addRoom(room1)
        maze.addRoom(room2)
        maze.addRoom(room3)
        maze.addRoom(room4)
        self.maze = maze

        beast1 = self.makeAggressiveBeast(room1)
        beast2 = self.makeLazyBeast(room2)  
        beast3 = self.makeAggressiveBeast(room3)
        beast4 = self.makeLazyBeast(room4)
       
        self.addBeast(beast1)
        self.addBeast(beast2)
        self.addBeast(beast3)
        self.addBeast(beast4)

        return maze


    def createMaze2RoomFM(self):
        room1 = self.makeRoom(1)
        room2 = self.makeRoom(2)
        door = self.makeDoor(room1, room2)
        maze = Maze()
        self.maze = maze
        self.maze.addRoom(room1)
        self.maze.addRoom(room2)
      
        room1.south = door 
        room2.north = door

        return maze
    
    def addPerson(self, character):
        self.person = character
        self.person.game = self
        if self.maze is not None:
            self.maze.enter(self.person)
            

    def addBeast(self, beast):
        beast.num=len(self.beasts)+1
        beast.game=self
        self.beasts.append(beast)        

    def removeBeast(self, beast):
        self.beasts.remove(beast)
    
    def makeAggressiveBeast(self,room):
        beast = Beast(Aggressive())
        beast.power = 3  # Set the power value for aggressive beasts
        beast.position = room
        return beast
    
    def makeLazyBeast(self, room):
        beast = Beast(Lazy())
        beast.power = 1  # Set the power value for lazy beasts
        beast.position = room
        return beast
    
    def print(self):
        print("Game")
    
    def findPerson(self,unCont):
        if self.person.position ==unCont:
            return self.person
        else:
            return None
    
    def findBeast(self,unCont):
        for beast in self.beasts:
            if beast.position == unCont:
                return beast
        else:
            return None
    
    def openDoors(self):
        print("Opening all doors...")
        abrirPuertas=lambda each: each.open()
        #eval('add(3,4)',{'__builtins__':None},dispatcher)
        self.maze.recorrer(abrirPuertas)

    def closeDoors(self):
        print("Closing all doors...")
        cerrarPuertas=lambda each: each.close()

        self.maze.recorrer(cerrarPuertas)
    
    def cloneMaze(self):
        return copy.deepcopy(self.prototype)
      

# BombedGame.py
class BombedGame(Game):
  def makeWall(self):
    return BombedWall()

  def print(self):
    print("BombedGame")

