import tkinter as tk
#import keyboard
import sys
import os
sys.path.append(os.getcwd())
from builder.builder import *
from solution.maze import Point, BonusType
from tkinter import messagebox
from solution.creatures import *


class RectApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.game=None
        self.person=None
        
        director=Director()
        director.procesar(os.getcwd() + '\\json\\ProyectoMaze10room5beasts copy.json')
        self.game=director.getGame()

        self.title("Laberinto rectangular")
        self.geometry("1150x900")
        self.menubar = tk.Menu(self)
        
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Salir", command=self.quit)
        
        self.drawmenu = tk.Menu(self.menubar, tearoff=0)
        self.drawmenu.add_command(label="Lanzar creatures", command=self.game.launchThreads)
        self.drawmenu.add_command(label="Parar creatures", command=self.game.stopThreads)
        
        self.menubar.add_cascade(label="Archivo", menu=self.filemenu)  
        self.menubar.add_cascade(label="Bichos", menu=self.drawmenu)
        
        self.config(menu=self.menubar)

        self.toolbar = tk.Frame(self)
        self.b1 = tk.Button(self.toolbar, text="Lanzar bichos", command=self.button1_click)
        self.b2 = tk.Button(self.toolbar, text="Parar bichos", command=self.button2_click)
        self.b3 = tk.Button(self.toolbar, text="Abrir puertas", command=self.button3_click)
        self.b4 = tk.Button(self.toolbar, text="Cerrar puertas", command=self.button4_click)
        
        self.b1.pack(side=tk.LEFT)
        self.b2.pack(side=tk.LEFT) 
        self.b3.pack(side=tk.LEFT)
        self.b4.pack(side=tk.LEFT)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
       

        self.canvas = tk.Canvas(self, width=1100, height=650, bg="white")
        self.canvas.pack(expand=True)
        # Load and scale images
        self.player_image = tk.PhotoImage(file="images/player_img.png").subsample(4)
        self.aggressive_beast_image = tk.PhotoImage(file="images/agressive_beast.png").subsample(8)
        self.lazy_beast_image = tk.PhotoImage(file="images/lazy_beast.png").subsample(5)
        
        self.fat_beast_image = tk.PhotoImage(file="images/fat_beast.png").subsample(3)
        self.healer_beast_image = tk.PhotoImage(file="images/healer_beast.png").subsample(2)
        
        self.strong_player_image = tk.PhotoImage(file="images/strong_player.png").subsample(7)
        self.titan_player_image = tk.PhotoImage(file="images/titan_player.png").subsample(3)
       # Load bonus images
        self.hp_bonus_image = tk.PhotoImage(file="images/hp_bonus.png").subsample(14)
        self.power_bonus_image = tk.PhotoImage(file="images/hp_bonus.png").subsample(14)
        
        self.floorhole_image = tk.PhotoImage(file="images/floorhole_image.png").subsample(14)

        
        self.mostrarLaberinto()
        self.agregarPersonaje()
        self.dibujarLaberinto()

       
    def mostrarLaberinto(self):
        self.calcularPosicion()
        self.normalizar()
        self.calcularDimensiones()
        self.asignarPuntosReales()
    
    def calcularPosicion(self):
        if not(self.game):
            return
        h1=self.game.getRoom(1)
        h1.setPoint(Point(0,0))
        h1.calcularPosicion()

    def normalizar(self):
        minX=0
        minY=0
        for h in self.game.maze.children:
            if h.getPoint().x<minX:
                minX=h.getPoint().x
            if h.getPoint().y<minY:
                minY=h.getPoint().y
        for h in self.game.maze.children:
            point=h.getPoint()
            h.setPoint(Point(point.x+abs(minX),point.y+abs(minY)))
    
    def change_character_type(self, new_type):
        self.person.change_character_type(new_type)
        self.update_character_stats()
        self.update_character_image()

    def update_character_stats(self):
        self.delete_character_stats_from_canvas()
        self.draw_character_stats()

    def delete_character_stats_from_canvas(self):
        self.canvas.delete("lives")
        self.canvas.delete("power")

    def calcularDimensiones(self):
        maxX = 0
        maxY = 0
        for h in self.game.maze.children:
            if h.getPoint().x > maxX:
                maxX = h.getPoint().x
            if h.getPoint().y > maxY:
                maxY = h.getPoint().y
        maxX += 1
        maxY += 1
        self.ancho = (1050 / maxX)
        self.alto = (600 / maxY)

    def asignarPuntosReales(self):
        origen=Point(10,10)
        for h in self.game.maze.children:
            x=origen.x+h.getPoint().x*self.ancho
            y=origen.y+h.getPoint().y*self.alto
            h.setPoint(Point(x,y))
            h.setExtent(Point(self.ancho,self.alto))           
    
    def agregarPersonaje(self):
        self.person = self.game.person
        self.person_lives = self.person.life
        self.person_power = self.person.power

    def dibujarLaberinto(self):
        if not(self.game):
            return
        self.game.maze.accept(self)
        self.draw_character()
        self.draw_beasts()
        self.draw_bonuses() 
        self.handle_bonuses()
        self.draw_traps() 
        self.handle_traps() 
        self.draw_floorholes() 

    def draw_rect(self, x1, y1, width, height, door_type="normal"):
        x2 = x1 + width
        y2 = y1 + height
        
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
        
        if door_type == "spiked":
            # Draw spikes on the door
            spike_length = min(width, height) / 10
            for i in range(5):  # Draw 5 spikes
                spike_x = x1 + (i + 1) * width / 6
                self.canvas.create_line(spike_x, y1, spike_x, y1 + spike_length, fill="red", width=2)
                self.canvas.create_line(spike_x, y2, spike_x, y2 - spike_length, fill="red", width=2)

    def visitRoom(self,room):
        self.draw_rect(room.getPoint().x,room.getPoint().y,room.getExtent().x,room.getExtent().y)
        
    def button1_click(self):
        self.game.launchThreads()

    def button2_click(self):
        self.game.stopThreads()

    def button3_click(self):
        self.game.openDoors()

    def button4_click(self):
        self.game.closeDoors()

    def animate_sprite(self):
        # Código para animar un sprite en el canvas
        pass

    def keypress(self, event):
        """Recieve a keypress and move the ball by a specified amount"""
        print(event)
        if event.char == 'w':
            app.person.goNorth()
            self.update_character_and_beasts()
            self.draw_character_and_beasts()
        elif event.char == 's':
            app.person.goSouth()
            self.update_character_and_beasts()
            self.draw_character_and_beasts()
        elif event.char == 'a':
            app.person.goWest()
            self.update_character_and_beasts()
            self.draw_character_and_beasts()
        elif event.char == 'd':
            app.person.goEast()
            self.update_character_and_beasts()
            self.draw_character_and_beasts()
        elif event.char == 'e':
            self.attack_beast()
        elif event.char == 'r':
            print("Attempting to use Titan's ultimate")
            self.use_titan_ultimate()
        else:
            pass
        self.update_character_and_beasts()
        self.draw_character_and_beasts()


    def use_titan_ultimate(self):
        status = self.game.check_ultimate_status()
        if status == "ready":
            if self.game.use_titan_ultimate():
                self.delete_all_beasts_from_gui()
                messagebox.showinfo("Victory", "The Titan's ultimate ability has destroyed all beasts! You win!")
                self.quit()
        elif status == "not ready":
            messagebox.showinfo("Ultimate Not Ready", "The Titan's ultimate ability has already been used.")
        else:
            messagebox.showinfo("No Ultimate", "This character doesn't have an ultimate ability.")

    
    def change_character_type(self, new_type):
        # Check if the player is in the spawn room
        spawn_room = self.game.getRoom(1)
        if self.person.position == spawn_room:
            self.character_type = new_type
            self.update_character_stats()
        else:
            print("You can only change your character type in the spawn room.")

    def draw_character(self):
        # Clear the previous circle
        self.delete_character_from_canvas()

        # Get the position of the character's room
        room = self.person.position
        x = room.getPoint().x + room.getExtent().x / 7  # Position the character on the left side
        y = room.getPoint().y + room.getExtent().y / 10
        radius = min(room.getExtent().x, room.getExtent().y) / 8  # Make the character smaller

         # Draw the new character image at the updated position
        if self.person.isNormal():
            self.character_image = self.canvas.create_image(
                x, y, image=self.player_image, anchor=tk.NW, tags="character"
            )
        elif self.person.isStrong():
            self.character_image = self.canvas.create_image(
                x, y, image=self.strong_player_image, anchor=tk.NW, tags="character"
            )
        elif self.person.isTitan():
            self.character_image = self.canvas.create_image(
                x, y, image=self.titan_player_image, anchor=tk.NW, tags="character"
            )

        self.draw_character_stats()
    def delete_all_beasts_from_gui(self):
        # Remove all beast images and stats from the canvas
        self.canvas.delete("beast")
        self.canvas.delete("lives")
        self.canvas.delete("power")
        # Redraw the character to ensure it's still visible
        self.draw_character()

    def delete_character_from_canvas(self):
        self.canvas.delete("character")
        self.canvas.delete("lives")
        self.canvas.delete("power")

    def update_character_image(self):
        self.delete_character_from_canvas()
        self.draw_character()
   
    def draw_character_stats(self):
        # Get the position of the character's room
        room = self.person.position
        x = room.getPoint().x + room.getExtent().x / 3
        y = room.getPoint().y + room.getExtent().y / 2
        radius = min(room.getExtent().x, room.getExtent().y) / 8

        # Draw the lives text
        lives_text = f"Lives: {self.person.life}"
        self.canvas.create_text(x + radius + 50, y - radius - 10, text=lives_text, fill="black", font=("Arial", 12), tags="lives")

        # Draw the power text
        power_text = f"Power: {self.person.power}"
        self.canvas.create_text(x + radius + 50, y + radius + 10, text=power_text, fill="black", font=("Arial", 12), tags="power")

    def delete_beasts_from_canvas(self, beast):
            self.canvas.delete("cross1"+str(beast.position.num))
            self.canvas.delete("cross2"+str(beast.position.num))
            self.canvas.delete("lives"+str(beast.position.num))
            self.canvas.delete("power"+str(+beast.position.num))
    
    def draw_beasts(self):
        self.canvas.delete("beast")
        for beast in self.game.beasts:
            room = beast.position
            self.delete_beasts_from_canvas(beast)
            x = room.getPoint().x + room.getExtent().x * 4 / 6.5  # Position the cross on the right side
            y = room.getPoint().y + room.getExtent().y / 2
            size = min(room.getExtent().x, room.getExtent().y) / 8  # Make the cross smaller

            # Draw the beast image
            if beast.isAggressive():
                beast_image = self.aggressive_beast_image
            if beast.isLazy():
                beast_image = self.lazy_beast_image
            if beast.isFat():
                beast_image = self.fat_beast_image
                x += 20  # Shift the x-coordinate to the right
                y -= size 
            if beast.isHealer():
                beast_image = self.healer_beast_image

            self.canvas.create_image(
                x, y, image=beast_image, anchor=tk.CENTER, tags="beast"
            )
            # Draw the lives and power text
            lives_text = f"Lives: {beast.life}"
            power_text = f"Power: {beast.power}"
            self.canvas.create_text(x + size + 70, y - size + 5, text=lives_text, fill="black", font=("Arial", 12), tags="lives"+str(beast.position.num))
            self.canvas.create_text(x + size + 70, y + size + 15, text=power_text, fill="black", font=("Arial", 12), tags="power"+str(beast.position.num))

    def attack_beast(self):
        # Get the current room and the beast in that room
        current_room = self.person.position
        beast = self.game.findBeast(current_room)

        if beast:
        # Check if the beast is a Healer Beast
            if beast.isHealer():
                # Healer Beast restores 5 HP to the player
                heal_amount = 5
                self.person.life += heal_amount
                print(f"Healer beast healed the player for {heal_amount} HP!")
                self.game.beasts.remove(beast)
                self.delete_beasts_from_canvas(beast)
               
            else:
                # Character attacks the beast
                beast.life -= self.person.power
                print(f"Character attacked the beast! Beast's remaining life: {beast.life}")

                # Beast attacks the character
                if beast.life > 0:
                    self.person.life -= beast.power
                    print(f"Beast attacked the character! Character's remaining life: {self.person.life}")
                    if self.person.life <= 0:
                        self.delete_character_from_canvas()
                        messagebox.showwarning("Game Over", "The character was killed!")
                        print(f"Game Over", "The character was killed!")
                        exit()
                else:
                    self.game.beasts.remove(beast)
                    self.delete_beasts_from_canvas(beast)
                    if len(self.game.beasts) == 0:
                        messagebox.showinfo("Congratulations", "You have defeated all the beasts and won the game.")
                        exit()

            # Update the character's lives and power display
            self.person_lives = self.person.life

            # Redraw the character and beasts
            self.draw_character()
            self.draw_beasts()
        else:
            print("No beast in the current room.")


    def draw_bonuses(self):
        self.canvas.delete("bonus")  # Clear any previously drawn bonuses
        for room in self.game.maze.children:
            for bonus in room.children:
                if isinstance(bonus, BonusType):
                    x, y = self.get_room_center(room)
                    bonus_type = "HP" if isinstance(bonus, BonusHP) else "Power"
                    bonus_value = bonus.bonus_value
                    bonus_image = self.hp_bonus_image if bonus_type == "HP" else self.power_bonus_image
                    
                    self.canvas.create_image(x, y, image=bonus_image, anchor=tk.CENTER, 
                                             tags=(f"bonus_{room.num}", "bonus"))
                    self.canvas.create_text(x, y + 50, text=f"{bonus_type}: +{bonus_value}", 
                                            fill="black", font=("Arial", 12), 
                                            tags=(f"bonus_{room.num}", "bonus"))

    def handle_bonuses(self):
        current_room = self.person.position
        bonuses_to_remove = []
        for child in current_room.children:
            if isinstance(child, BonusType):
                child.apply_bonus(self.person)
                bonuses_to_remove.append(child)
        
        # Remove bonuses from the room and update GUI
        for bonus in bonuses_to_remove:
            current_room.removeChild(bonus)
            self.canvas.delete(f"bonus_{current_room.num}")
        
        # Redraw character stats to reflect new values
        self.update_character_stats()

    def draw_traps(self):
        self.canvas.delete("trap")  # Clear any previously drawn traps
        for room in self.game.maze.children:
            for trap in room.children:
                if isinstance(trap, Trap):
                    x, y = self.get_room_center(room)
                    radius = min(room.getExtent().x, room.getExtent().y) / 8
                    trap_damage = trap.damage_value
                    trap_text = f"Trap: -{trap_damage} Damage"

                    # Draw the trap icon
                    trap_icon_size = radius * 2
                    trap_icon_x = x - trap_icon_size / 2
                    trap_icon_y = y - trap_icon_size / 2
                    trap_icon_color = "red"
                    self.canvas.create_rectangle(trap_icon_x, trap_icon_y, trap_icon_x + trap_icon_size, trap_icon_y + trap_icon_size, fill=trap_icon_color, outline="black", tags="trap")

                    # Draw the trap text
                    self.canvas.create_text(x, y + 35, text=trap_text, fill="black", font=("Arial", 12), tags="trap")

    def draw_floorholes(self):
        self.canvas.delete("floorhole")  # Clear any previously drawn floorholes
        for room in self.game.maze.children:
            for child in room.children:
                if isinstance(child, FloorHole):
                    x, y = self.get_room_center(room)
                    self.canvas.create_image(x, y, image=self.floorhole_image, anchor=tk.CENTER, tags=("floorhole", f"floorhole_{room.num}"))
                    self.canvas.create_text(x, y + 35, text=f"Damage: {child.damage_value}", fill="black", font=("Arial", 12), tags=("floorhole", f"floorhole_{room.num}"))

    def handle_floorholes(self):
        current_room = self.person.position
        floorholes_to_remove = []
        for child in current_room.children:
            if isinstance(child, FloorHole):
                child.apply_damage(self.person)
                floorholes_to_remove.append(child)
        
        # Remove floorholes from the room and update GUI
        for hole in floorholes_to_remove:
            current_room.removeChild(hole)
            self.canvas.delete(f"floorhole_{current_room.num}")
        
        # Redraw character stats to reflect new values
        self.update_character_stats()

    def handle_traps(self):
        current_room = self.person.position
        current_room.app = self  # Pass the RectApp instance to the current room
        for trap in current_room.children:
            if isinstance(trap, Trap):
                print(f"Trap in the current room!")
                trap.apply_damage(self.person)

    def delete_character_and_beasts_from_canvas(self):
        self.canvas.delete("character")
        self.canvas.delete("beast")
        self.canvas.delete("lives")
        self.canvas.delete("power")
        self.canvas.delete("bonus")
        self.canvas.delete("trap")
        self.canvas.delete("floorhole")  # Add this line

        

    def get_room_center(self, room):
        x = room.getPoint().x + room.getExtent().x / 2
        y = room.getPoint().y + room.getExtent().y / 2
        return x, y
    
    def update_character_and_beasts(self):
        self.handle_bonuses()
        self.handle_traps()
        self.draw_bonuses()  # Redraw remaining bonuses

    def draw_character_and_beasts(self):
        self.delete_character_and_beasts_from_canvas()
        self.draw_character()
        self.draw_beasts()
        self.update_character_and_beasts()
        self.draw_bonuses()
        self.draw_traps()
        self.draw_floorholes()  # Add this line



if __name__ == "__main__":
    app = RectApp()
    app.bind('w',app.keypress)
    app.bind('s',app.keypress)
    app.bind('d',app.keypress)
    app.bind('a',app.keypress)
    app.bind('e',app.keypress)
    app.bind('r',app.keypress)
    app.mainloop()
