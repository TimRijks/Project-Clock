# Import module
from tkinter import *
import datetime
from PIL import ImageTk, Image
import time
import sqlite3
import random

# Create object
root_hour = Tk()
root_minute = Toplevel()

# Adjust size
root_minute.attributes("-fullscreen", True)
root_hour.attributes("-fullscreen", True)
root_hour.geometry("800x480+0+0")
root_minute.geometry("800x480+800+0")

def database(Time: str):
    # Establish a connection to the database
    conn = sqlite3.connect('klok_database.db')
    count = 0

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    #cursor.execute("CREATE TABLE `Klok` (`ID` INTEGER ,`ThemaTijd` TEXT(10),`ThemaNR` INTEGER ,`Afbeelding` TEXT(2000),`TextKleur` TEXT(100),`AfbeeldingLin` TEXT(2000))")


    #for paths in tijd:

        #kleur = tijd[count]
    #    sql = f"INSERT INTO Klok(ID, ThemaTijd, ThemaNR, Afbeelding, TextKleur, AfbeeldingLin) VALUES {tijd[count]}"

    #    cursor.execute(sql)
        
    #    conn.commit()       
    #    count = count+1
     #Execute a SELECT statement
    themanr = random.randint(1,3)
    tijd = Time
    cursor.execute('SELECT AfbeeldingLIN FROM Klok WHERE ThemaNR=? AND ThemaTijd=? LIMIT 1',(themanr, Time,))

    # Fetch all rows returned by the SELECT statement
    image = cursor.fetchone()

    print(image)

    # Close the cursor and connection
    cursor.close()
    conn.close()
    return image

# Function to resize image
def resize_image(image1=None):
    # Open image to resize it
    if image1 is None:
        image = Image.open(fr"/home.timrijks/Documents/Digitale klok/Backup/firework.jpg")
    else:
        image = Image.open(image1)

    # Resize the image with width and height of root
    resized = image.resize((800, 480), Image.LANCZOS)
    # Transform it into a PhotoImage object
    return ImageTk.PhotoImage(resized)
# Create Canvas for hours
canvas_hour = Canvas(root_hour, width=800, height=480, bd=0, highlightthickness=0)
bg_hour = resize_image(image1=None)
bg_hour_id = canvas_hour.create_image(0, 0, image=bg_hour, anchor='nw')
text_hour_id = canvas_hour.create_text(400, 240, text="", font=("Arial", 280), fill="#eeff00")

canvas_hour.pack(fill="both", expand=True)

# Create Canvas for minutes
canvas_minute = Canvas(root_minute, width=800, height=480, bd=0, highlightthickness=0)
bg_minute = resize_image(image1=None)
bg_minute_id = canvas_minute.create_image(0, 0, image=bg_minute, anchor='nw')
text_minute_id = canvas_minute.create_text(400, 240, text="", font=("Arial", 280), fill="#eeff00")

canvas_minute.pack(fill="both", expand=True)

def update_time():
    now = datetime.datetime.now()
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    canvas_hour.itemconfig(text_hour_id, text=hour)
    canvas_minute.itemconfig(text_minute_id, text=minute,)
    if minute == '00' or minute == '30':
        tijd = now.strftime("%H%M")
        newimage = database(Time=tijd)
        print(newimage[0][0])
        time.sleep(1)
        canvas_minute.bg_image = resize_image(image1=newimage[0])
        canvas_minute.itemconfig(bg_minute_id, image=canvas_minute.bg_image)

        canvas_hour.bg_image = resize_image(image1=newimage[0])
        canvas_hour.itemconfig(bg_hour_id, image=canvas_hour.bg_image)
        time.sleep(59)

    root_hour.after(500, update_time)  # reschedule event in 0.5 seconds

# schedule the first call to update_time
update_time()

# Execute tkinter
root_hour.mainloop()
