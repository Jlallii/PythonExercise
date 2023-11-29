#
# Youtube link for a video that shows how the program works: https://www.youtube.com/watch?v=zhwHguGAYzw
# Oamk sharepoint link for the video: https://oamk-my.sharepoint.com/personal/t1laja03_students_oamk_fi/_layouts/15/stream.aspx?id=%2Fpersonal%2Ft1laja03%5Fstudents%5Foamk%5Ffi%2FDocuments%2FTeht%C3%A4v%C3%A48%2Emp4&referrer=OneDriveForBusiness&referrerScenario=OpenFile

import tkinter as tk
import winsound
import time
import numpy as np
import threading
from typing import List



ikkuna=tk.Tk()
ikkuna.title("Exercise 8")
ikkuna.geometry("700x700")
ikkuna.configure(bg='blue')


# add five buttons to the top line of the window
koristetta=tk.Label(ikkuna,text="").grid(row=0,column=0)
point_button=[]
for i in range(5):
    button_temp=tk.Button(ikkuna,text="Points: "+str(5*(i)),padx=40)
    button_temp.grid(row=0,column=i+1)
    point_button.append(button_temp)
def i_suppose_i_have_earned_so_much_points(amount_of_points):
    points_mod=int(amount_of_points/5)
    for i in range(5):
        point_button[i].configure(bg='gray')
    time.sleep(1)
    point_button[0].configure(bg='green')    
    for i in range(points_mod):
        point_button[i+1].configure(bg='green')
        winsound.Beep(440+i*100,500)




class Monkey:
    def __init__(self, frequency, island):
        self.frequency = frequency
        self.island = island
        self.alive = True
        self.swimming = False
        self.sound_thread = threading.Thread(target=self.monkey_sound)
        self.sound_thread.start()
        self.thread = threading.Thread(target=self.monkey_behavior)
        self.thread.start()
        self.visual_representation = None
        self.swim_direction = None

    def swim_sound(self):
        winsound.PlaySound('KOULU\Python\Failure.wav', winsound.SND_FILENAME)

    def monkey_sound(self):
        while self.alive:
            if not self.swimming:
                winsound.Beep(self.frequency, 500)
            time.sleep(10)


    def go_swimming(self):
        direction = np.random.choice(["N", "S", "E", "W"])
        self.swim_direction = direction
        self.create_visual_representation()
        self.swimming = True
        winsound.PlaySound('KOULU\Python\Swim.wav', winsound.SND_FILENAME)  # You can adjust this sound effect or use the swim_sound method
        return direction
    
    def monkey_behavior(self):
        while self.alive:
            if self.swimming:
                # 1% chance for the monkey to survive
                if np.random.randint(100) == 0:
                    self.alive = False
                    self.swim_sound()
                    self.stop_behaviours()
                time.sleep(1)  # wait for 1 second since it's checking every second
            else:
                # check if monkey dies of laughter while on the island
                if np.random.randint(100) == 0:  # 1% chance
                    self.alive = False
                    self.laugh()
                    self.stop_behaviours()
                    self.island.remove_monkey(self)
                time.sleep(10)  # wait for 10 seconds

    def stop_behaviours(self):
        self.stop_sound()
        self.destroy_visual_representation()

    def create_visual_representation(self):
        # Start location based on swimming direction
        if self.swim_direction == "N":
            x, y = self.island.x + self.island.width / 2, self.island.y - 30
        elif self.swim_direction == "S":
            x, y = self.island.x + self.island.width / 2, self.island.y + self.island.height + 10
        elif self.swim_direction == "E":
            x, y = self.island.x + self.island.width + 10, self.island.y + self.island.height / 2
        elif self.swim_direction == "W":
            x, y = self.island.x - 30, self.island.y + self.island.height / 2
        self.visual_representation = tk.Label(self.island.ikkuna, text="a", bg="yellow", fg="black")
        self.visual_representation.place(x=x, y=y)

    def move_visual_representation(self, new_x, new_y):
        if self.visual_representation:
            self.visual_representation.place(x=new_x, y=new_y)

    def destroy_visual_representation(self):
        if self.visual_representation:
            self.visual_representation.destroy()
            self.visual_representation = None

    def laugh(self):
        winsound.PlaySound('KOULU\Python\Laugh.wav', winsound.SND_FILENAME)


    def stop_sound(self):
        self.alive = False

class NewIsland:

    def __init__(self, ikkuna):
        self.ikkuna = ikkuna
        self.islands = []
        self.monkeys = []
        self.name_counter = 0
        self.last_monkey_sent_time = 0
        self.move_monkeys()


    def new_island(self):
        max_tries = 100 # maximum number of tries to find a suitable location
        for _ in range(max_tries):
            width, height = np.random.randint(90, 210), np.random.randint(90, 210)
            x, y = np.random.randint(50, 650 - width), np.random.randint(50, 650 - height)

            if not self.island_overlaps(x, y, width, height):
                self.name_counter += 1
                island_name = "S" + str(self.name_counter)
                button = tk.Button(self.ikkuna, bg="goldenrod", text=island_name)
                button.place(x=x, y=y, width=width, height=height)

                new_island = Island(x, y, width, height, button, island_name, self.ikkuna)
                self.islands.append(new_island)

                if island_name == "S1":
                    new_island.add_piers()

                monkeys = [Monkey(np.random.randint(200, 1000), new_island) for _ in range(10)]
                for monkey in monkeys:
                    new_island.add_monkey(monkey, update_display=False) # delete this later
                new_island.update_count_display()# this too
                self.monkeys.extend(monkeys)
                break
        else:
            lbl_error = tk.Label(self.ikkuna, text="No space for a new island", bg="red", fg="white")
            lbl_error.place(x=350, y=350, anchor="center")
            print("Could not find a suitable location for a new island")
            lbl_error.after(3000, lbl_error.destroy)
    
    def island_overlaps(self, x, y, width, height):
        for island in self.islands:
            ix, iy, iw, ih = island.x, island.y, island.width, island.height
            if x < ix + iw and x + width > ix and y < iy + ih and y + height > iy:
                return True
        return False
    
    def clear_all(self):
        # Destroy all islands and their piers
        for island in self.islands:
            if isinstance(island.piers, list):
                for pier in island.piers:
                    pier.destroy()
            island.button.destroy()

        #stop all monkeys
        for monkey in self.monkeys:
            monkey.destroy_visual_representation()
            monkey.stop_sound()

        #reset lists
        self.islands = []
        self.monkeys = []
        self.name_counter = 0

    def send_monkey_swimming(self):
        #identify the s1 island
        s1_island = None
        for island in self.islands:
            if island.name == "S1":
                s1_island = island
                break

        if not s1_island:
            print("No S1 island found!")
            return
        
        if s1_island.piers:
            s1_monkeys = [monkey for monkey in self.monkeys if monkey.island == s1_island and not monkey.swimming]
        
            if not s1_monkeys:
                print("No monkeys available on S1 island for a swim!")
                return
        
    
        monkey_to_swim = np.random.choice(s1_monkeys)
        direction = monkey_to_swim.go_swimming()
        s1_island.remove_monkey(monkey_to_swim)

        lbl_monkey_swimming = tk.Label(self.ikkuna, text=f"Monkey from S1 left swimming from the {direction}", bg="red", fg="white")
        lbl_monkey_swimming.place(x=235, y= 150)
        lbl_monkey_swimming.after(3000, lbl_monkey_swimming.destroy)

    def initiate_swimming_process(self, island):
        #send monkey swimming every 10 seconds
        self.ikkuna.after(10000, self.send_random_monkey_swimming)

    def send_random_monkey_swimming(self):
        current_time = time.time()
        if current_time - self.last_monkey_sent_time < 10:
            return
        
        self.last_monkey_sent_time = current_time
        # Getting islands that have both piers and monkeys
        islands_with_piers = [island for island in self.islands if island.piers and island.monkeys]
        
        if not islands_with_piers:
            return
        
        # Choosing a random island from the list
        random_island = np.random.choice(islands_with_piers)
        
        # Getting the monkeys that are on this island and not swimming
        available_monkeys = [monkey for monkey in self.monkeys if monkey.island == random_island and not monkey.swimming]
        
        if available_monkeys:
            monkey_to_swim = np.random.choice(available_monkeys)
            direction = monkey_to_swim.go_swimming()
            random_island.remove_monkey(monkey_to_swim)

            lbl_monkey_swimming = tk.Label(self.ikkuna, text=f"Monkey from {random_island.name} left swimming from the {direction}", bg="red", fg="white")
            lbl_monkey_swimming.place(x=235, y= 150)
            lbl_monkey_swimming.after(3000, lbl_monkey_swimming.destroy)

            # After the label disappears, find a new island for the monkey
            lbl_monkey_swimming.after(2000, lambda: self.find_new_island_for_monkey(monkey_to_swim, direction))

    def move_monkeys(self):
        for monkey in self.monkeys:
            if monkey.swimming:
                if monkey.swim_direction == "N":
                    x, y = monkey.visual_representation.winfo_x(), monkey.visual_representation.winfo_y() - 10
                elif monkey.swim_direction == "S":
                    x, y = monkey.visual_representation.winfo_x(), monkey.visual_representation.winfo_y() + 10
                elif monkey.swim_direction == "E":
                    x, y = monkey.visual_representation.winfo_x() + 10, monkey.visual_representation.winfo_y()
                elif monkey.swim_direction == "W":
                    x, y = monkey.visual_representation.winfo_x() - 10, monkey.visual_representation.winfo_y()

                    monkey.move_visual_representation(x, y)
            ikkuna.after(1000, self.move_monkeys)  # Move monkeys every second


    def find_new_island_for_monkey(self, monkey, direction):
        if direction == 'N':
            valid_islands = [island for island in self.islands if island.y < monkey.island.y]
        elif direction == 'S':
            valid_islands = [island for island in self.islands if island.y > monkey.island.y]
        elif direction == 'E':
            valid_islands = [island for island in self.islands if island.x > monkey.island.x]
        elif direction == 'W':
            valid_islands = [island for island in self.islands if island.x < monkey.island.x]
        else:
            valid_islands = []

        if valid_islands:
            closest_island = min(valid_islands, key=lambda island: abs(island.x - monkey.island.x) + abs(island.y - monkey.island.y))
            if not closest_island.piers:
                closest_island.add_piers()

            monkey.destroy_visual_representation()
            closest_island.add_monkey(monkey)
            monkey.island = closest_island
            monkey.swimming = False

            if len(closest_island.piers) == 0:
                closest_island.add_piers()
                self.send_random_monkey_swimming()



class Island:

    def __init__(self, x, y, width, height, button, name, ikkuna):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button = button
        self.name = name
        self.ikkuna = ikkuna
        self.monkeys = []
        self.piers = []

        self.first_monkey_added = False
        self.first_update = True

    def add_piers(self):
        #if self.name == "S1":
        # North pier
        self.piers.append(Pier(self.ikkuna, self.x + (self.width / 2) - 10, self.y - 20, "N"))
        # South pier
        self.piers.append(Pier(self.ikkuna, self.x + (self.width / 2) - 10, self.y + self.height, "S"))
        # East pier
        self.piers.append(Pier(self.ikkuna, self.x + self.width, self.y + (self.height / 2) - 10, "E"))
        # West pier
        self.piers.append(Pier(self.ikkuna, self.x - 20, self.y + (self.height / 2) - 10, "W"))

    def add_monkey(self, monkey, update_display=True):
        self.monkeys.append(monkey)
        if update_display:
            self.update_count_display()

    def remove_monkey(self, monkey):
        if monkey in self.monkeys:
            self.monkeys.remove(monkey)
        self.update_count_display()

    def update_count_display(self):
        self.button.after(0, self._update_count_display)

    def _update_count_display(self):
        # Display the current monkey count on the button
        current_text = self.button.cget("text")
        name_part = current_text.split(':')[0]
        self.button.config(text="{}: {}".format(name_part, len(self.monkeys)))

class Pier:
    def __init__(self, ikkuna, x, y, direction):
        self.direction = direction  # can be 'N', 'S', 'E', or 'W'
        self.x = x
        self.y = y
        self.ikkuna = ikkuna
        
        if direction == "N":
            self.pier = tk.Button(self.ikkuna, bg="darkgray", text="N")
        elif direction == "S":
            self.pier = tk.Button(self.ikkuna, bg="darkgray", text="S")
        elif direction == "E":
            self.pier = tk.Button(self.ikkuna, bg="darkgray", text="E")
        elif direction == "W":
            self.pier = tk.Button(self.ikkuna, bg="darkgray", text="W")
        self.pier.place(x=x, y=y, width=20, height=20)

    def destroy(self):
        self.pier.destroy()
def auto_swim():
    island_manager.send_random_monkey_swimming()
    ikkuna.after(10000, auto_swim)


def on_closing():
    for monkey in island_manager.monkeys:
        monkey.stop_sound()
    ikkuna.quit()

island_manager = NewIsland(ikkuna)

def clear_window():
    island_manager.clear_all()


i_suppose_i_have_earned_so_much_points(20)

swim_btn = tk.Button(ikkuna, text="Send Monkey Swimming", command=island_manager.send_monkey_swimming)
swim_btn.place(x = 5, y= 670)
clear_btn = tk.Button(ikkuna, text="Clear Window", command=clear_window)
clear_btn.place(x=148, y=670)

island_btn = tk.Button(ikkuna, text="New Island", command=island_manager.new_island)
island_btn.place(x=233, y=670)

auto_swim()

ikkuna.protocol("WM_DELETE_WINDOW", on_closing)
ikkuna.mainloop()
