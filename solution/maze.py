# mapelement.py
import random
from solution.creatures import Person, Beast
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Command:
    def __init__(self, receptor):
        self.receptor = receptor
    
    def execute(self):
        pass
    def isEnter(self):
        return False

class Open(Command):
    def execute(self):
        self.receptor.removeCommand(self)
        self.receptor.addCommand(Close(self.receptor))
        self.receptor.addCommand(Enter(self.receptor))
        self.receptor.open()

class Close(Command):
    def execute(self):
        self.receptor.removeCommand(self)
        self.receptor.addCommand(Open(self.receptor))
        self.receptor.close()

class Enter(Command):
    def execute(self):
        self.receptor.enter()
    def isEnter(self):
        return True

class MapElement:
    def __init__(self):
        self.commands = []
    
    def enter(self,someone):
        pass

    def print(self):
        print("MapElement")
    
    def isRoom(self):
        return False

    def isDoor(self):
        return False
    
    def recorrer(self,unBloque):
        pass
    def open(self):
        pass
    def close(self):
        pass
    def recorrer(self,unBloque):
        unBloque(self)
        
    def addCommand(self, command):
        self.commands.append(command)
    def removeCommand(self, command):
        self.commands.remove(command)
    def getCommands(self):
        return self.commands
    def accept(self,visitor):
        pass

class Leaf(MapElement):
    def __init__(self):
        super().__init__()
   
    def print(self):
        print("Leaf")
        

class Bonus(Leaf):
    def __init__(self, bonus_value):
        super().__init__()
        self.bonus_value = bonus_value

    def apply_bonus(self, player):
        raise NotImplementedError("Subclass must implement abstract method")

    def __str__(self):
        return f"Bonus ({self.__class__.__name__}, {self.bonus_value})"

class BonusType(Bonus):
    def __init__(self, bonus_value):
        super().__init__(bonus_value)

    def apply_bonus(self, creature):
        if isinstance(creature, Person):
            self._apply_bonus_to_person(creature)
        else:
            print(f"Warning: Attempted to apply bonus to non-Person creature: {creature}")

    def _apply_bonus_to_person(self, person):
        raise NotImplementedError("Subclass must implement abstract method")

class BonusHP(BonusType):
    def __init__(self, bonus_value):
        super().__init__(bonus_value)

    def _apply_bonus_to_person(self, person):
        person.life += self.bonus_value
        print(f"{person} HP now is {person.life}!")

class BonusPower(BonusType):
    def __init__(self, bonus_value):
        super().__init__(bonus_value)

    def _apply_bonus_to_person(self, person):
        person.power += self.bonus_value
        print(f"{person} Power now is {person.power}!")
        
class Trap(MapElement):
    def __init__(self, damage_value):
        super().__init__()
        self.damage_value = damage_value
        self.active = False
    def apply_damage(self, creature):
        if isinstance(creature, Person):
             creature.life -= self.damage_value
             print(f"{creature.name} ({creature.character_type}) took {self.damage_value} damage from the trap!")
             print(f"Player HP now is {creature.life}!")

    def __str__(self):
        return f"Trap (Damage: {self.damage_value})"

class FloorHole(MapElement):
    def __init__(self,damage_value):
        super().__init__()
        self.damage_value = damage_value

    def apply_damage(self, creature):
        if isinstance(creature, Person):
            creature.life -= self.damage_value
            print(f"{creature.name} fell in a floor hole and took {self.damage_value} damage!")
            print(f"Player HP now is {creature.life}!")

    def __str__(self):
        return f"FloorHole (Damage: {self.damage_value})"


class Container(MapElement):
    # Composite
    def __init__(self):
        super().__init__()
        self.children = []
        self.num = None    
        self.form = None    
    
    def getPoint(self):
        return self.form.getPoint()

    def setPoint(self, point):
        self.form.setPoint(point)
    def getExtent(self):
        return self.form.extent
    def setExtent(self, extent):
        self.form.extent=extent
    
    def addChild(self, component):
        self.children.append(component)

    def removeChild(self, component):
        if component in self.children:
            self.children.remove(component)
        else:
            print(f"Warning: Attempted to remove a child {component} that is not in the container")
    
    def print(self):
        print("Container")
    
    def walkRandom(self,someone):
        pass
    
    def addOrientation(self, orientation):
        #self.orientations.append(orientation)
        self.form.addOrientation(orientation)
    
    def removeOrientation(self, orientation):
        #self.orientations.remove(orientation)
        self.form.removeOrientation(orientation)
    
    def getOrientations(self):
        return self.form.orientations

    def walkRandom(self, someone):        
        orientation = self.form.getRandomOrientation()
        orientation.walkRandom(someone)
   
    def goNorth(self, someone):
        #self.north.enter(someone)
        self.form.goNorth(someone)
    def goEast(self, someone):
        #self.east.enter(someone)
        self.form.goEast(someone)
    def goSouth(self, someone):
        #self.south.enter(someone)
        self.form.goSouth(someone)
    def goWest(self, someone):
        #self.west.enter(someone)
        self.form.goWest(someone)
    def setEMinOr(self, em, orientation):
        #orientation.setEMinOr(em, self)
        self.form.setEMinOr(em, orientation)
    
    def recorrer(self, unBloque):
        unBloque(self)
        for child in self.children:
            child.recorrer(unBloque)
        self.form.recorrer(unBloque)
        #for orient in self.orientations:
        #    orient.recorrerEn(unBloque,self)
    def getCommands(self):
        lista=[]
        lista += self.commands
        for child in self.children:
            lista += child.getCommands()
        lista += self.form.getCommands()
        return lista	

    def calcularPosicion(self):
        self.form.calcularPosicion()  
    
class Maze(Container):
    def __init__(self):
        super().__init__()

    def addRoom(self, room):
        self.addChild(room)

    def enter(self,someone):
        self.children[0].enter(someone)

    def print(self):
        print("Maze")   
    
    def getRoom(self, num):
        for room in self.children:
            if room.num == num:
                return room
        return None
    def recorrer(self, unBloque):
        unBloque(self)
        for child in self.children:
            child.recorrer(unBloque)        

    def getOrientations(self):
        pass
    def accept(self, visitor):
        for child in self.children:
            child.accept(visitor)   

class Room(Container):
    def __init__(self, num):
        super().__init__()
        self.num=num

    def enter(self, creature):
        creature.position = self

        # Now use self instead of current_room
        if isinstance(creature, Person):
            items_to_remove = []
            for child in self.children:
                if isinstance(child, BonusType):
                    print(f"Applying bonus to player: {child}")
                    child.apply_bonus(creature)
                    items_to_remove.append(child)
                elif isinstance(child, Trap):
                    print(f"Applying trap to player: {child}")
                    child.apply_damage(creature)
                    items_to_remove.append(child)
                elif isinstance(child, FloorHole):
                    child.apply_damage(creature)
                    items_to_remove.append(child)
                

            # Remove bonuses after the loop
            for bonus in items_to_remove:
                self.removeChild(bonus)
        elif isinstance(creature, Beast):
            print(f"Beast {creature} entered room {self.num}")
        else:
            print(f"Unknown creature type {type(creature)} entered room {self.num}")

  # Remove the bonus from the room
                        
    def print(self):
        print("Room")

    def isRoom(self):
        return True
    
    def __str__(self):
        return "Room-" + str(self.num)    
    def accept(self, visitor):
        visitor.visitRoom(self)


class Leaf(MapElement):
    def __init__(self):
        super().__init__()
    
    def print(self):
        print("Leaf")

class Tunnel(Leaf):
    def __init__(self):
        super().__init__()
        self.maze = None

    def enter(self,someone):
        print(str(someone) + " enter Tunnel"+"\n")
        self.maze=someone.game.cloneMaze()
        self.maze.enter(someone)

class Decorator(Leaf):
    def __init__(self):
        super().__init__()
        self.comp = None
    
    def print(self):
        print("Decorator")

class Bomb(Decorator):
    def __init__(self):
        super().__init__()
        self.active = False

    def print(self):
        print("Bomb")

    def enter(self, someone):
        print(someone + " walked into a bomb"+"\n")

class Wall(MapElement):
    def __init__(self):
        pass
    
    def print(self):
        print("Wall")

    def enter(self, someone):
        print(someone , " walked into a wall \n")

    def calcularPosicionDesde(self,aForm,aPoint):
        pass
# bombedwall.py

class BombedWall(Wall):
    def __init__(self):
        super().__init__()
        self.active = False
    
    def print(self):
        print("BombedWall")

# door.py

class Door(MapElement):
    def __init__(self, side1, side2):
        super().__init__()
        self.side1 = side1
        self.side2 = side2
        self.opened = False
        self.visited = False
    
    def enter(self,someone):
        if (self.opened):
            if someone.position == self.side1:
                self.side2.enter(someone)
            else:
                self.side1.enter(someone)
        else:
            print("The door "+str(self)+" is locked")
    def __str__(self):
        return "Puerta-"+str(self.side1)+"-"+str(self.side2)
    
    def open(self):
        print("Opening the door between "+str(self.side1)+" and "+str(self.side2))
        self.opened = True
    
    def close(self):
        print("Closing the door between "+str(self.side1)+" and "+str(self.side2))
        self.opened = False

    def isDoor(self):
        return True
    def calcularPosicionDesde(self,aForm,aPoint):
        if self.visited:
            return  
        self.visited = True
        if aForm.num==self.side1.num:
            self.side2.setPoint(aPoint)
            self.side2.calcularPosicion()
        else:
            self.side1.setPoint(aPoint)
            self.side1.calcularPosicion()

class SpikedDoor(Door):
    def __init__(self, side1, side2):
        super().__init__(side1, side2)
        self.damage = 1

    def enter(self, creature):
        if self.opened:
            if isinstance(creature, Person):
                print(f"{creature} enters through a spiked door and takes {self.damage} damage!")
                creature.life -= self.damage
                print(f"Player HP now is {creature.life}!")
            super().enter(creature)  # Use the parent class's enter method
        else:
            print("The spiked door is locked")

    def __str__(self):
        return f"SpikedDoor-{self.side1}-{self.side2}"

class Orientation:
    def __init__(self):
        pass
    def walkRandom(self, someone):
        pass
    def setEMinOr(self, em, aContainer):
        pass
    def recorrerEn(self, unBloque, aContainer):
        pass
    def getCommands(self,aForm):
        pass
    def calcularPosicionDesde(self,aForm):
        pass

class North(Orientation):
    _instance = None
    def __init__(self):
        if not North._instance:
            super().__init__()
            North._instance = self
    def setEMinOr(self, em, aContainer):
        aContainer.north = em

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = North()
        return cls._instance

    def print(self):
        print("North")
    
    def walkRandom(self, someone):
        someone.goNorth()

    def recorrerEn(self, unBloque, aContainer):
        aContainer.north.recorrer(unBloque)
    
    def getCommands(self,aForm):
        return aForm.north.getCommands()
    def calcularPosicionDesde(self, aForm):
        unPunto=Point(aForm.point.x,aForm.point.y-1)
        aForm.north.calcularPosicionDesde(aForm,unPunto)

class South(Orientation):
    _instance = None
    def __init__(self):
        if not South._instance:
            super().__init__()  
            South._instance = self

    @staticmethod 
    def get_instance():
        if not South._instance:
            South()
        return South._instance
    
    def print(self):
        print("South")
    
    def walkRandom(self, someone):
        someone.goSouth()
    
    def setEMinOr(self, em, aContainer):
        aContainer.south = em
    
    def recorrerEn(self, unBloque, aContainer):
        aContainer.south.recorrer(unBloque)

    def getCommands(self,aForm):
        return aForm.south.getCommands()
    def calcularPosicionDesde(self, aForm):
        unPunto=Point(aForm.point.x,aForm.point.y+1)
        aForm.south.calcularPosicionDesde(aForm,unPunto)

class East(Orientation):
    _instance = None
    def __init__(self):
        raise RuntimeError('Call instance() instead')
        # if not East._instance:
        #     super().__init__()
        #     East._instance = self

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            print('Creating new instance')
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
        return cls._instance
    
    def walkRandom(self, someone):
        someone.goEast()
    
    def setEMinOr(self, em, aContainer):
        aContainer.east = em
    # @staticmethod
    # def get_instance():
    #     if not East._instance:
    #         East()
    #     return East._instance
    
    # def print(self):
    #     print("East")
    def recorrerEn(self, unBloque, aContainer):
        aContainer.east.recorrer(unBloque)
    def getCommands(self,aForm):
        return aForm.east.getCommands()
    def calcularPosicionDesde(self, aForm):
        unPunto=Point(aForm.point.x+1,aForm.point.y)
        aForm.east.calcularPosicionDesde(aForm,unPunto)

class West(Orientation):
    _instance = None
    def __init__(self):
        if not West._instance:
            super().__init__()
            West._instance = self

    @staticmethod
    def get_instance():
        if not West._instance:
            West()
        return West._instance
    
    def print(self):
        print("West")
    
    def walkRandom(self, someone):
        someone.goWest()

    def setEMinOr(self, em, aContainer):
        aContainer.west = em

    def recorrerEn(self, unBloque, aContainer):
        aContainer.west.recorrer(unBloque)

    def getCommands(self,aForm):
        return aForm.west.getCommands()
    def calcularPosicionDesde(self, aForm):
        unPunto=Point(aForm.point.x-1,aForm.point.y)
        aForm.west.calcularPosicionDesde(aForm,unPunto)

class Northeast(Orientation):
    _instance = None
    
    def __init__(self):
        if not Northeast._instance:
            super().__init__()
            Northeast._instance = self

    @staticmethod
    def get_instance():
        if not Northeast._instance:
            Northeast()
        return Northeast._instance

    def print(self):
        print("Northeast")

    def walkRandom(self, someone):
        someone.goNortheast()

    def setEMinOr(self, em, aContainer):
        aContainer.northeast = em

    def recorrerEn(self, unBloque, aContainer):
        aContainer.northeast.recorrer(unBloque)
        
class Northwest(Orientation):
    _instance = None
    
    def __init__(self):
        if not Northwest._instance:
            super().__init__()
            Northwest._instance = self

    @staticmethod
    def get_instance():
        if not Northwest._instance:
            Northwest()
        return Northwest._instance

    def print(self):
        print("Northwest")

    def walkRandom(self, someone):
        someone.goNorthwest()

    def setEMinOr(self, em, aContainer):
        aContainer.northwest = em

    def recorrerEn(self, unBloque, aContainer):
        aContainer.northwest.recorrer(unBloque)
        
class Southeast(Orientation):
    _instance = None
    
    def __init__(self):
        if not Southeast._instance:
            super().__init__()
            Southeast._instance = self

    @staticmethod
    def get_instance():
        if not Southeast._instance:
            Southeast()
        return Southeast._instance

    def print(self):
        print("Southeast")

    def walkRandom(self, someone):
        someone.goSoutheast()

    def setEMinOr(self, em, aContainer):
        aContainer.southeast = em

    def recorrerEn(self, unBloque, aContainer):
        aContainer.southeast.recorrer(unBloque)
        
class Southwest(Orientation):
    _instance = None
    
    def __init__(self):
        if not Southwest._instance:
            super().__init__()
            Southwest._instance = self

    @staticmethod
    def get_instance():
        if not Southwest._instance:
            Southwest()
        return Southwest._instance

    def print(self):
        print("Southwest")

    def walkRandom(self, someone):
        someone.goSouthwest()

    def setEMinOr(self, em, aContainer):
        aContainer.southwest = em

    def recorrerEn(self, unBloque, aContainer):
        aContainer.southwest.recorrer(unBloque)


class Form:
    def __init__(self):
        self.orientations = []
        self.point = None
        self.extent=None
        self.num=None

    def addOrientation(self, orientation):
        self.orientations.append(orientation)   
    def removeOrientation(self, orientation):
        self.orientations.remove(orientation)
    def getRandomOrientation(self):
        return random.choice(self.orientations)
    def setEMinOr(self, em, orientation):
        orientation.setEMinOr(em, self)
    def recorrer(self,unBloque):
        for orient in self.orientations:
            orient.recorrerEn(unBloque,self)
    def getCommand(self):
        lista=[]
        for orient in self.orientations:
            lista += orient.getCommandFrom(self)
        return lista
    def setPoint(self,point):
        self.point=point
    def getPoint(self):
        return self.point
    def calcularPosicion(self):
        for orient in self.orientations:
            orient.calcularPosicionDesde(self)

class Rectangle(Form):
    def __init__(self,num):
        super().__init__()
        self.num=num
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.addAllOrientations()

    def addAllOrientations(self):
        self.addOrientation(North.get_instance())
        self.addOrientation(South.get_instance())
        self.addOrientation(East.get_instance())
        self.addOrientation(West.get_instance())
    def goNorth(self, someone):
        self.north.enter(someone)
    def goEast(self, someone):
        self.east.enter(someone)
    def goSouth(self, someone):
        self.south.enter(someone)
    def goWest(self, someone):
        self.west.enter(someone)

class Hexagon(Form):
    def __init__(self):
        super().__init__()
        self.north = None
        self.northeast = None
        self.southeast = None
        self.south = None
        self.southwest = None
        self.northwest = None
        self.addAllOrientations()
    def addAllOrientations(self):
        self.addOrientation(North.get_instance())
        self.addOrientation(Northeast.get_instance())
        self.addOrientation(Southeast.get_instance())
        self.addOrientation(South.get_instance())
        self.addOrientation(Southwest.get_instance())
        self.addOrientation(Northwest.get_instance())

    def goNorth(self, someone):
        self.north.enter(someone)

    def goNortheast(self, someone):
        self.northeast.enter(someone)

    def goSoutheast(self, someone):
        self.southeast.enter(someone)

    def goSouth(self, someone):
        self.south.enter(someone)

    def goSouthwest(self, someone):
        self.southwest.enter(someone)

    def goNorthwest(self, someone):
        self.northwest.enter(someone)


