from tkinter import *
from turtle import TK
from PIL import Image, ImageTk
import tkinter

BACKGROUND_COLOR = "#bec3e6"
VOLTMETER = "voltmeter.png"
BOTTLE = "bottle.png"
FE = "FE.png"
ZN = "ZN.png"
AL = "AL.png"
CU = "CU.png"
TRAY = "tray.png"
CONTAINER = "container.png"
DISTILLEDWATER = "distilledWater.png"
SANDPAPER = "sandpaper.png"
SOLUTIONDROP = "waterdrop.png"
PAPER = "paper.png"
# DISPLAY = "white.png"

window = Tk()
window.minsize(width=1920, height=1080)
window.title("Protecția catodică cu anozi de sacrificiu")
window.config(bg=BACKGROUND_COLOR)

imagesList = []
PIL_voltmeter_image = Image.open(VOLTMETER)
PIL_bottle_naoh_image = Image.open(BOTTLE)
PIL_bottle_h2so4_image = Image.open(BOTTLE)
PIL_bottle_nacl_image = Image.open(BOTTLE)
PIL_FE_image = Image.open(FE)
PIL_CU_image = Image.open(CU)
PIL_ZN_image = Image.open(ZN)
PIL_AL_image = Image.open(AL)
PIL_tray_image = Image.open(TRAY)
PIL_container_image = Image.open(CONTAINER)
PIL_distillerWater_image = Image.open(DISTILLEDWATER)
PIL_sandpaper_image = Image.open(SANDPAPER)
PIL_solutiondrop_image = Image.open(SOLUTIONDROP)
PIL_paper_image = Image.open(PAPER)
PIL_paper = PIL_paper_image.rotate(90, expand = True)
# PIL_display_image = Image.open(DISPLAY)

main_canvas = Canvas(window, width=1920, height=1080, bg=BACKGROUND_COLOR, highlightthickness=0)
main_canvas.place(x=0, y=0)

dictionary = {
    "FE": {"NaOH": 0.42, "NaCl": 0.512, "H2SO4": 0.482},
    "CU": {"NaOH": 0.238, "NaCl": 0.483, "H2SO4": 0.477},
    "ZN": {"NaOH": 0.516, "NaCl": 0.936, "H2SO4": 0.796},
    "AL": {"NaOH": 1.11, "NaCl": 0.658, "H2SO4": 0.622}
}

metal_clean_status = {
    "FE": True,
    "CU": True,
    "ZN": True,
    "AL": True
}

unclean_metals = []
environment = None
metal1 = None
metal2 = None
flag = False

referenceElectrodVoltage = 0.266

def ResizeImage(PILimageToResize, scale):
    # set the new width and height based on the given scale
    width = int(PILimageToResize.width * scale)
    height = int(PILimageToResize.height * scale)

    # proceed the resize
    resized_image = PILimageToResize.resize((width, height))
    
    return [resized_image, width, height] #returns a list with the image and its attributes

# this function takes a PIL image and it converts it into a Tk one, in order to be displayed on the tk window
def displayImage(xAxis, yAxis, PILimageToResize, scale):
    image_list = ResizeImage(PILimageToResize, scale)

    # converting into Tk image
    imageToDisplay = ImageTk.PhotoImage(image_list[0])
    
    # keep the tk image into a list in order not to be erased by the garbage collector
    imagesList.append(imageToDisplay)

    # place the image on the main canvas
    imageID = main_canvas.create_image(xAxis, yAxis, image=imageToDisplay, anchor="nw")
    return imageID

water_ID_image = displayImage(xAxis = 1150, yAxis = 600, PILimageToResize = PIL_distillerWater_image, scale = 0.6)
sandpaper_ID_image = displayImage(xAxis = 0, yAxis= 600, PILimageToResize = PIL_sandpaper_image, scale = 0.6)
container1_ID_image = displayImage(xAxis = 300, yAxis= 300, PILimageToResize = PIL_container_image, scale = 0.4)
container2_ID_image = displayImage(xAxis = 500, yAxis= 300, PILimageToResize = PIL_container_image, scale = 0.4)
container3_ID_image = displayImage(xAxis = 700, yAxis= 300, PILimageToResize = PIL_container_image, scale = 0.4)
voltmeter_ID_image = displayImage(xAxis = 50, yAxis= 200, PILimageToResize = PIL_voltmeter_image, scale = 0.6)
bottle_naoh_ID_image = displayImage(xAxis = 1080, yAxis = 180, PILimageToResize = PIL_bottle_naoh_image, scale = 0.5)
bottle_h2so4_ID_image = displayImage(xAxis = 1180, yAxis = 180, PILimageToResize = PIL_bottle_h2so4_image, scale = 0.5)
bottle_nacl_ID_image = displayImage(xAxis = 1280, yAxis = 180, PILimageToResize = PIL_bottle_nacl_image, scale = 0.5)
tray_ID_image = displayImage(xAxis = 550, yAxis = 550, PILimageToResize = PIL_tray_image, scale = 0.9)
iron_ID_image = displayImage(xAxis = 600, yAxis = 600, PILimageToResize = PIL_FE_image, scale = 0.4)
copper_ID_image = displayImage(xAxis = 700, yAxis = 600, PILimageToResize = PIL_CU_image, scale = 0.3)
zinc_ID_image = displayImage(xAxis = 750, yAxis = 600, PILimageToResize = PIL_ZN_image, scale = 0.4)
alluminium_ID_image = displayImage(xAxis = 880, yAxis = 600, PILimageToResize = PIL_AL_image, scale = 0.4)
paperfilter_ID_image = displayImage(xAxis = 1350, yAxis = 650, PILimageToResize = PIL_paper, scale = 0.4) 
# display_ID_image = displayImage(xAxis = 75, yAxis = 230, PILimageToResize = PIL_display_image, scale = 0.76)

label_warningMetal = Label(text = "", font = ('Times', 14), bg = BACKGROUND_COLOR)
label_warningMetal.place(x = 1140, y = 450)

label_env = Label(text="Mediu coroziv selectat: N/A", font=('Times', 14), bg=BACKGROUND_COLOR)
label_env.place(x=1140, y=400)

label_metal1 = Label(text="Primul metal selectat: N/A", font=('Times', 14), bg=BACKGROUND_COLOR)
label_metal1.place(x=300, y=700)

label_metal2 = Label(text="Al doilea metal selectat: N/A", font=('Times', 14), bg=BACKGROUND_COLOR)
label_metal2.place(x=300, y=800)

label_clean = Label(text="Plăcutele sunt curate.", font=('Times', 14), fg="green", bg=BACKGROUND_COLOR)
label_clean.place(x=500, y=100)

label_voltage = Label(text= "Ultima tensiune măsurată: ", font=('Times', 14), bg=BACKGROUND_COLOR)
label_voltage.place(x=500, y=200)

label_clean.place(x=1000, y=510)
label_voltage.place(x=450, y=505)

label_startWarning = Label(text = """Nu putem începe! Asigurați-vă că ați folosit șmirghelul pentru a curăța plăcuțele. 
                        Studenții de dinainte au uitat!""", font=('Times', 14), fg="red", bg=BACKGROUND_COLOR)

def is_any_metal_unclean():
    return any(not clean for clean in metal_clean_status.values())

def unclean():
    return [key for key, clean in metal_clean_status.items() if not clean]

"""dictionary containing the destination for each bottle moving animation
1st number: the x coordinate for the bottle
2nd number: the y coordinate for the bottle
3rd number: the x coordinate for the container"""
bottles = {
    bottle_h2so4_ID_image: [1180, 180, 600, 100],
    bottle_naoh_ID_image: [1080, 180, 370, 100],
    bottle_nacl_ID_image: [1280, 180, 770, 100]
}   

def select_environment(env):
    # if flag == False: 
    #     label_startWarning.place(x= 500, y = 100)
    # else:
    global environment
    if environment is not None and env != environment and is_any_metal_unclean():
        label_clean.config(
            text=f"Curăță toate plăcuțele înainte de a schimba mediul!\nPlăcuțe necurățate: {', '.join(unclean())}",
            fg="red"
        )
        return
    environment = env
    label_env.config(text=f"Mediu coroziv selectat: {environment}")
    label_clean.config(text="Plăcutele sunt curate.", fg="green")
    if environment == "NaOH":
        PILbottle = PIL_bottle_naoh_image
        IDbottle = bottle_naoh_ID_image
        xAxis = bottles[bottle_naoh_ID_image][2] - 100 #adjust with 100 pixels for visual precision
        yAxis = bottles[bottle_naoh_ID_image][3]
    elif environment == "NaCl":
        PILbottle = PIL_bottle_nacl_image
        IDbottle = bottle_nacl_ID_image
        xAxis = bottles[bottle_nacl_ID_image][2] - 100
        yAxis = bottles[bottle_nacl_ID_image][3]
    else:
        PILbottle = PIL_bottle_h2so4_image
        IDbottle = bottle_h2so4_ID_image
        xAxis = bottles[bottle_h2so4_ID_image][2] - 100
        yAxis = bottles[bottle_h2so4_ID_image][3]
    pour_solution(IDbottle, PILbottle, xAxis, yAxis)

previous_ID = main_canvas.create_text(135, 245, text = "0.00", font = ('Times', 24), fill = "black")    

def calculate_corrosive(metalVoltage, metalName, corrosiveEnvironment):
    potential = referenceElectrodVoltage - metalVoltage
    ironVoltage = dictionary["FE"][corrosiveEnvironment]
    if potential > ironVoltage: 
        # the corrosive potential of the (Fe + X) sistem is bigger than the Fe's voltage in the corrosive environment selected. 
        TK.messagebox.showinfo(title = "Concluzia măsuratorii", message = f"Metalul de asociere, {metalName} este anod de sacrificiu!")
    else: 
        TK.messagebox.showinfo(title = "Concluzia măsurătorii", message = f"Metalul de asocieire, {metalName} NU este anod de sacrificiu!")

def select_metal1(metal_input):
    # if flag == False: 
    #     label_startWarning.place(x= 500, y = 100)
    # else:   
        global metal1
        metal1 = metal_input
        metal_clean_status[metal1] = False
        if metal1 not in unclean_metals:
            unclean_metals.append(metal1)
        label_metal1.config(text=f"Primul metal selectat: {metal1}")
        label_clean.config(text="Plăcuță de Fe selectată.\nCurăță la schimbarea mediului coroziv!", fg="red")

def select_metal2(metal_input):
    # if flag == False: 
    #     label_startWarning.place(x= 500, y = 100)
    # else:   
        global metal2
        metal2 = metal_input
        if metal_clean_status[metal2]:
            metal_clean_status[metal2] = False
            if metal2 not in unclean_metals:
                unclean_metals.append(metal2)
            label_metal2.config(text=f"Al doilea metal selectat: {metal2}")
            label_clean.config(text="Plăcuță nouă selectată. Curăță după utilizare!", fg="red")
        else:
            label_metal2.config(text="Al doilea metal selectat: eroare.")
            label_clean.config(text="Plăcuța trebuie curățată mai întâi!", fg="red")

def clean(metal, metalID):
    # if flag == False: 
        # label_startWarning.place(x= 500, y = 100)
    # else:   
        global unclean_metals
        metal_clean_status[metal] = True
        if metal in unclean_metals:
            unclean_metals.remove(metal)
        cleanAnimation(metalID, water_ID_image)
        window.update()
        time.sleep(0.5)
        label_clean.config(text=f"Plăcuța {metal} a fost curățată", fg="green")
        if metal is metal1:
            label_metal1.config(text="Primul metal selectat: N/A")
        elif metal is metal2:
            label_metal2.config(text = "Al doilea metal selectat: N/A")

def calculate_results():
    # if flag == False: 
        # label_startWarning.place(x= 500, y = 100)
    # else:   
        if environment is None:
            label_env.config(text = "Nu a fost selectat niciun mediu coroziv!")
        elif metal1 is None and metal2 is None:
            label_warningMetal.config(text = "Selectați cele două metale (Fe + X),\nunde X poate fi (Cu, Zn, Al, -)")
        elif metal1 is None:
            label_warningMetal.config(text = "Selectați Fe ca prim metal!")
        else:
            voltmeterValues()
            if metal2 is None:
                main_canvas.itemconfig(previous_ID, text = dictionary[metal1][environment])
                label_voltage.config(text = f"Ultima tensiune măsurată este: {dictionary[metal1][environment]}V")
            else:
                main_canvas.itemconfig(previous_ID, text = dictionary[metal2][environment])
                label_voltage.config(text = f"Ultima tensiune măsurată este: {dictionary[metal2][environment]}V")
                calculate_corrosive(dictionary[metal2][environment], metal2, environment)

def reset():
    global metal1, metal2
    metal1 = None
    metal2 = None
    label_metal1.config(text = "Primul metal selectat: N/A")
    label_metal2.config(text = "Al doilea metal selectat: N/A")

import time

def oscillation(image, x, y, offset=20, count=4):
    original_y = y #initial y coordinate
    
    for i in range(count): # doing the up-down movement 'count' times
        y_start = original_y
        y_end = original_y - offset #move the image with a certain number of pixels upper
        
        # start of the animation for going up
        for step in range(21): 
            progress = step / 20
            current_y = y_start + (y_end - y_start) * progress #tracking the current y coordinate
            main_canvas.coords(image, x, current_y) #updating image's position in real time
            window.update() # displaying the changes
            time.sleep(0.02) 
        
        # the image arrived up, now we are setting it to do the same animation on the road down. 
        y_start = original_y - offset
        y_end = original_y
        
        for step in range(21): 
            progress = step / 20
            current_y = y_start + (y_end - y_start) * progress
            main_canvas.coords(image, x, current_y)
            window.update()
            time.sleep(0.02) 

def move_image_smoothly(image, x_start, y_start, x_end, y_end, duration=1.0):
    steps = 50 
    
    for step in range(steps + 1):
        progress = step / steps
        current_x = x_start + (x_end - x_start) * progress
        current_y = y_start + (y_end - y_start) * progress
        
        main_canvas.coords(image, current_x, current_y)
        window.update()
        time.sleep(duration / steps)
     
metals = {
    iron_ID_image: [600, 600],
    copper_ID_image: [700, 600],
    zinc_ID_image: [750, 600],
    alluminium_ID_image: [880, 600]
}

def cleanAnimation(metalID, waterID):
    distilledWaterX = 1230
    distilledWaterY = 600

    filterPaperX = 1350
    filterPaperY = 650

    main_canvas.tag_raise(waterID)
    move_image_smoothly(metalID, metals[metalID][0], metals[metalID][1], distilledWaterX, distilledWaterY)
    window.update()
    time.sleep(0.4)

    main_canvas.tag_raise(metalID)
    move_image_smoothly(metalID, distilledWaterX, distilledWaterY, filterPaperX, filterPaperY)
    time.sleep(0.3)
    move_image_smoothly(metalID, filterPaperX, filterPaperY, metals[metalID][0], metals[metalID][1])
    
def sand():
    global flag
    flag = True
    label_startWarning.config(text="")

    for metal in metals:
        if metal is not iron_ID_image:
            # move the metal on the sandpaper
            move_image_smoothly(metal, metals[metal][0], metals[metal][1], 600, 600)

            # make the metal move up and down to give the cleaning effect
            oscillation(metal, 20, 650)
        
            # move the metal back on the plate
            move_image_smoothly(metal, 600, 600, metals[metal][0], metals[metal][1])

            window.update()
            time.sleep(0.3)
            cleanAnimation(metal, water_ID_image)    

def pour_solution(bottleID, PILbottle, xAxis, yAxis):
    # before pouring, the bottle must be placed near the container. the parameters are integers from a dictionary
    move_image_smoothly(bottleID, bottles[bottleID][0], bottles[bottleID][1], bottles[bottleID][2], bottles[bottleID][3])

    # convert the image into a rotated one
    rotated_bottleID = PILbottle.rotate(45, expand = True)
    
    # set the scale top 0.5, as the original bottle image had the same scale when 
    scale = 0.5
    
    # setting up image attributes
    width = int(rotated_bottleID.width* scale)
    height = int(rotated_bottleID.height * scale)

    # getting new PIL ID for the resized image
    resized_bottleID = rotated_bottleID.resize((width, height))

    # convert the ID into a TK 'object'
    rotated_bottleTK = ImageTk.PhotoImage(resized_bottleID)

    # store the 'object' in the list so it will not be erased
    imagesList.append(rotated_bottleTK)

    main_canvas.itemconfig(bottleID, image = rotated_bottleTK)
    solutiondrop_ID_image = displayImage(xAxis, yAxis, PIL_solutiondrop_image, 0.6)

    window.update()
    time.sleep(1)
    main_canvas.delete(solutiondrop_ID_image)

    original_PIL = PILbottle 

    width = int(original_PIL.width * scale)
    height = int(original_PIL.height * scale)
    original_PIL_resized = original_PIL.resize((width, height))

    normal_imageTK = ImageTk.PhotoImage(original_PIL_resized)
    imagesList.append(normal_imageTK) 

    main_canvas.itemconfig(bottleID, image=normal_imageTK)
    move_image_smoothly(bottleID, bottles[bottleID][2], bottles[bottleID][3], bottles[bottleID][0], bottles[bottleID][1])

    window.update()

import random
def voltmeterValues():
    previous_string = "0.00V"
    # previous_ID = main_canvas.create_text(135, 245, text = previous_string, font = ('Times', 24), fill = "black")
    for step in range(8): 
        window.update()
        time.sleep(0.2)

        random_voltage = random.random()
        random_voltage = round(random_voltage, 3)
        random_voltage_string = str(random_voltage)

        main_canvas.itemconfig(previous_ID, text = random_voltage_string)
        window.update()

# Buttons

Button(text="NaOH 0.1M", width=10, font=('times 10 bold'), command=lambda: select_environment("NaOH"), borderwidth=0).place(x=1097, y=300)
Button(text="H2SO4 0.1M", width=10, font=('times 10 bold'), command=lambda: select_environment("H2SO4"), borderwidth=0).place(x=1200, y=300)
Button(text="NaCl 1%", width=10, font=('times 10 bold'), command=lambda: select_environment("NaCl"), borderwidth=0).place(x=1303, y=300)

Button(text="FE", width=7, font=('times 13 bold'), command=lambda: select_metal1("FE"), borderwidth=0).place(x=600, y=820)
Button(text="CU", width=7, font=('times 13 bold'), command=lambda: select_metal2("CU"), borderwidth=0).place(x=700, y=820)
Button(text="ZN", width=7, font=('times 13 bold'), command=lambda: select_metal2("ZN"), borderwidth=0).place(x=800, y=820)
Button(text="AL", width=7, font=('times 13 bold'), command=lambda: select_metal2("AL"), borderwidth=0).place(x=900, y=820)

Button(text="Curăță FE", width=10, command=lambda: clean("FE", iron_ID_image)).place(x=1100, y=650)
Button(text="Curăță CU", width=10, command=lambda: clean("CU", copper_ID_image)).place(x=1100, y=700)
Button(text="Curăță ZN", width=10, command=lambda: clean("ZN", zinc_ID_image)).place(x=1100, y=750)
Button(text="Curăță AL", width=10, command=lambda: clean("AL", alluminium_ID_image)).place(x=1100, y=800)

Button(text="Calculează", font=('times 13 bold'), command=calculate_results).place(x=850, y=480)
Button(text="Resetează", font=('times 13 bold'), command=reset).place(x=850, y=520)

Button(text= "Șmirgheluire", font=('times 13 bold'), command=sand).place(x=0, y=600)

window.mainloop()