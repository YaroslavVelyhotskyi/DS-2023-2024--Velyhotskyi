import unittest
import sys
import os
sys.path.append(os.getcwd())
from solution.game import Game
from solution.creatures import Person, NormalType, Beast, Aggressive, Lazy, FatBeast, HealerBeast, NormalType, StrongType, TitanType
from solution.maze import SpikedDoor, BonusHP, BonusPower, Trap, FloorHole


class TestGame(unittest.TestCase):
    
    def test_createRoom_returns_room_with_walls(self):
        game = Game()
        room = game.makeRoom(1)
        self.assertIsNotNone(room.north)
        self.assertIsNotNone(room.south)
        self.assertIsNotNone(room.east)
        self.assertIsNotNone(room.west)

    def test_createRoom_returns_room_with_correct_id(self):
        game = Game()
        room = game.makeRoom(5)
        self.assertEqual(room.num, 5)
        
    def test_createRoom_returns_different_rooms(self):
        game = Game()
        room1 = game.makeRoom(1)
        room2 = game.makeRoom(2)
        self.assertNotEqual(room1, room2)

    def test_spikedDoor_with_person(self):
        game = Game()
        room1 = game.makeRoom(1)
        room2 = game.makeRoom(2)
        
        character_type = NormalType()  # Assuming NormalType is defined somewhere
        person = Person("Pepe", character_type)
        
        spiked_door = SpikedDoor(room1, room2)
        spiked_door.open()
        
        initial_person_life = person.life 
        spiked_door.enter(person)
        
        expected_life_after_damage = initial_person_life - spiked_door.damage
        self.assertEqual(person.life, expected_life_after_damage)


    def test_apply_HP_bonus(self):
        game = Game()
        room = game.makeRoom(1)
        character_type = NormalType()
        person = Person("Pepe", character_type)
        initial_life = person.life

        hp_bonus = BonusHP(10) 
        room.addChild(hp_bonus)
        hp_bonus.apply_bonus(person)
        expected_life = initial_life + 10
        self.assertEqual(person.life, expected_life)

    def test_apply_Power_bonus(self):
        game = Game()
        room = game.makeRoom(1)
        character_type = NormalType()
        person = Person("Pepe", character_type)
        initial_power = person.power

        power_bonus = BonusPower(5) 
        room.addChild(power_bonus)

        power_bonus.apply_bonus(person)
        expected_power = initial_power + 5
        self.assertEqual(person.power, expected_power)

    def test_apply_Trap_damage(self):
        self.trap = Trap(10)  # Create a Trap instance with damage value 10
        self.person = Person("Pepe", NormalType())  # Create a Person instance for testing

        initial_life = self.person.life
        self.trap.apply_damage(self.person)
        expected_life = initial_life - self.trap.damage_value
        self.assertEqual(self.person.life, expected_life)

    def test_apply_FloorHole_damage(self):
        self.hole = FloorHole(2)  # Create a Trap instance with damage value 10
        self.person = Person("Pepe", NormalType())  # Create a Person instance for testing

        initial_life = self.person.life
        self.hole.apply_damage(self.person)
        expected_life = initial_life - self.hole.damage_value
        self.assertEqual(self.person.life, expected_life)


    def test_normal_type(self):
        person = Person("Normal", NormalType())
        self.assertTrue(person.isNormal())
        self.assertFalse(person.isStrong())
        self.assertFalse(person.isTitan())
        self.assertEqual(person.life, 20)
        self.assertEqual(person.power, 1)

    def test_strong_type(self):
        person = Person("Strong", StrongType())
        self.assertFalse(person.isNormal())
        self.assertTrue(person.isStrong())
        self.assertFalse(person.isTitan())
        self.assertEqual(person.life, 30)
        self.assertEqual(person.power, 3)

    def test_titan_type(self):
        person = Person("Titan", TitanType())
        self.assertFalse(person.isNormal())
        self.assertFalse(person.isStrong())
        self.assertTrue(person.isTitan())
        self.assertEqual(person.life, 50)
        self.assertEqual(person.power, 20)

    def test_change_character_type(self):
        person = Person("Changeable", NormalType())
        self.assertTrue(person.isNormal())
        person.change_character_type(StrongType())
        self.assertTrue(person.isStrong())
        self.assertEqual(person.life, 30)
        self.assertEqual(person.power, 3)
    
    def test_aggressive_beast(self):
        beast = Beast(Aggressive())
        self.assertTrue(beast.isAggressive())
        self.assertFalse(beast.isLazy())
        self.assertFalse(beast.isFat())
        self.assertFalse(beast.isHealer())
        self.assertEqual(beast.power, 3)

    def test_lazy_beast(self):
        beast = Beast(Lazy())
        self.assertFalse(beast.isAggressive())
        self.assertTrue(beast.isLazy())
        self.assertFalse(beast.isFat())
        self.assertFalse(beast.isHealer())
        self.assertEqual(beast.power, 1)

    def test_fat_beast(self):
        beast = Beast(FatBeast())
        self.assertFalse(beast.isAggressive())
        self.assertFalse(beast.isLazy())
        self.assertTrue(beast.isFat())
        self.assertFalse(beast.isHealer())
        self.assertEqual(beast.power, 1)
        self.assertEqual(beast.life, 20)

    def test_healer_beast(self):
        beast = Beast(HealerBeast())
        self.assertFalse(beast.isAggressive())
        self.assertFalse(beast.isLazy())
        self.assertFalse(beast.isFat())
        self.assertTrue(beast.isHealer())
        self.assertEqual(beast.power, 0)
        self.assertEqual(beast.life, 1)


if __name__ == '__main__':
    unittest.main()