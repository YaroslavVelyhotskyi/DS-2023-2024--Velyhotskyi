# beast.pyclass Beast:
import time
import threading

class Creature:
    def __init__(self):
        self.position = None
        self.game=None
        self.life=None
        self.power=None
    
    def goNorth(self):
        self.position.goNorth(self)
    def goEast(self):
        self.position.goEast(self)
    def goSouth(self):
        self.position.goSouth(self)
    def goWest(self):
        self.position.goWest(self)
    def attack(self):
        enemy = self.findEnemy()
        if enemy:
            enemy.isAttackedBy(self)

    def findEnemy(self):
        pass

    def isAttackedBy(self, other):
        pass

class CharacterType:
    def __init__(self):
        self.life = 0
        self.power = 0

    def set_stats(self, person):
        person.life = self.life
        person.power = self.power

    def isNormal(self):
        return False

    def isStrong(self):
        return False
    
    def isTitan(self):
        return False

class NormalType(CharacterType):

    def __init__(self):
        super().__init__()
        self.life = 20
        self.power = 1

    def __str__(self):
        return "Normal Character"

    def isNormal(self):
        return True

class StrongType(CharacterType):
    def __init__(self):
        super().__init__()
        self.life = 30
        self.power = 3

    def __str__(self):
        return "Strong Character"

    def isStrong(self):
        return True

class TitanType(CharacterType):
    def __init__(self):
        super().__init__()
        self.life = 50
        self.power = 20

    def __str__(self):
        return "Titan Character"

    def isTitan(self):
        return True


class Person(Creature):
    def __init__(self, name, character_type):
        super().__init__()
        self.name = name
        self.character_type = character_type
        self.ultimate_available = self.isTitan()  # Set to True if Titan, False otherwise
        self.character_type.set_stats(self)

    def __str__(self):
        return f"{self.name} ({self.character_type.__class__.__name__})"

    def change_character_type(self, new_type):
        self.character_type = new_type
        self.character_type.set_stats(self)
    
    def isTitan(self):
        return self.character_type.isTitan()
    
    def ultimate_status(self):
        if hasattr(self, 'ultimate_available'):
            return "ready" if self.ultimate_available else "not ready"
        return "not available"

    def set_as_titan(self):
        if self.isTitan():
            self.ultimate_available = True

    def use_ultimate(self):
        if self.isTitan() and self.ultimate_available:
            print(f"{self.name} uses the Titan's ultimate ability!")
            self.ultimate_available = False
            return True
        return False
    
    def isStrong(self):
        return self.character_type.isStrong()

    def isNormal(self):
        return self.character_type.isNormal()

    def findEnemy(self):
        return self.game.findBeast(self.position)

    def start(self, stop_event):
        self.run(stop_event)

    def run(self, stop_event):
        while self.life > 0 and not stop_event.is_set():
            self.walkRandom()
            beast = self.findEnemy()
            if beast:
                self.attack_beast(beast, stop_event)
            time.sleep(1)
            
    def stop(self):
        print(self , " is stopped")
        exit(0)

    def walk(self, character):
        character.walkRandom()

    def run(self, stop_event):
        while self.life > 0 and not stop_event.is_set():
            self.walkRandom()
            beast = self.findEnemy()
            if beast:
                self.attack_beast(beast, stop_event)
            time.sleep(1)

    def walkRandom(self):
        self.position.walkRandom(self)

    def attack_beast(self, beast, stop_event):
        print(f"{self} HP: {self.life}, Beast HP: {beast.life}")
        while beast.life > 0 and self.life > 0 and not stop_event.is_set():
            # Player attacks the beast
            beast.life = max(0, beast.life - self.power)
            print(f"{self} attacked the beast! Beast's remaining HP: {beast.life}")
            if beast.life <= 0:
                print("The beast has been defeated!")
                if beast.isHealer():
                    self.heal_from_healer_beast(beast)
                self.game.removeBeast(beast)
                if not self.game.beasts:
                    print("GAME OVER! Congratulations! All beasts have been defeated!")
                    self.game.stopThreads()
                    return

            # Beast attacks the player
            if beast.life > 0:  # Ensure the beast can only attack if it is still alive
                self.life = max(0, self.life - beast.power)
                print(f"Beast attacked {self}! {self}'s remaining HP: {self.life}")
                if self.life <= 0:
                    print(f"GAME OVER! {self} has been defeated!")
                    self.game.stopThreads()
                    return
            
            time.sleep(1)  # Adding a sleep to control the pace of the game

    def isAttackedBy(self, other):
        self.life -= other.power
        print(f"{self} is attacked by {other}")
        if self.life <= 0:
            print(f"{self} is dead, GAME OVER")
            self.game.stopThreads()
        else:
            print(f"{self}'s life is now {self.life}")

    def heal_from_healer_beast(self, healer_beast):
            heal_amount = healer_beast.mode.heal_amount
            self.life += heal_amount
            print(f"The defeated Healer beast healed the player for {heal_amount} HP!")
            print(f"Player's HP is now {self.life}")

class Beast(Creature):
    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.num=0

        self.mode.set_stats(self)

    def __str__(self):
        template='Beast-{0.mode}{0.num}'
        return template.format(self)
    
    
    
    def isAggressive(self):
        return self.mode.isAggressive()

    def isLazy(self):
        return self.mode.isLazy()
    
    def isFat(self):
        return self.mode.isFat()

    def isHealer(self):
        return self.mode.isHealer()

    
    def act(self):
        self.mode.act(self)
    
    def walkRandom(self):
        self.position.walkRandom(self)
    
    #def attack(self):
    #    self.position.attack(self)
    
    def start(self, stop_event):
        self.mode.act(self, stop_event)

    def stop(self):
        print(self , " is stopped")
        exit(0)

    
    def findEnemy(self):
        return self.game.findPerson(self.position)

class Mode:
    def __init__(self):
        pass
    def __str__(self):    
        pass
    def isAggressive(self):
        return False
    def isLazy(self):
        return False
    def isFat(self):
        return False
    def isHealer(self):
        return False

    def set_stats(self, beast):
        beast.life = self.life
        beast.power = self.power


    def act(self, beast, stop_event):
        while beast.life > 0 and not stop_event.is_set():
            self.sleep(beast)
            self.walk(beast)
            self.attack(beast)
        time.sleep(1)


    def walk(self, beast):
        beast.walkRandom()
        time.sleep(1)

    def sleep(self, beast):
        print(f"{beast} is sleeping")
        time.sleep(1)

    def attack(self, beast):
        beast.attack()
        time.sleep(1)
      

class Aggressive(Mode):
    def __init__(self):
        super().__init__()
        self.life = 20
        self.power = 3

    def __str__(self):
        return "Aggressive"
    
    def isAggressive(self):
        return True

    def print(self):
        print("Aggressive beast")

class Lazy(Mode):
    def __init__(self):
        super().__init__()
        self.life = 10
        self.power = 1
    
    def __str__(self):    
        return "Lazy"
    
    def print(self):
        print("Lazy beast")

    def isLazy(self):
        return True
    
class FatBeast(Mode):
    def __init__(self):
        super().__init__()
        self.life = 20
        self.power = 1

    def __str__(self):
        return "Fat"

    def print(self):
        print("Fat beast")

    def isFat(self):
        return True

class HealerBeast(Mode):
    def __init__(self):
        super().__init__()
        self.heal_amount = 5  # Adjust the heal amount as needed
        self.life = 1
        self.power = 0

    def __str__(self):
        return "Healer"

    def print(self):
        print("Healer beast")

    def isHealer(self):
        return True
