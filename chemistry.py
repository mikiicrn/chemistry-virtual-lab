from tkinter import *
from tkinter import ttk, Toplevel, Frame, Scrollbar, RIGHT, Y
from turtle import TK
from PIL import Image, ImageTk
import time
import tkinter.filedialog as filedialog
import csv
import random

LIGHT_GREEN = "#90EE90" 
GREEN = "#37FD12" 
RED ="#ED2939"
YELLOW = "#FFFF99"       
ORANGE = "#FFA500"
BACKGROUND_COLOR = "#bec3e6"
LIGHT_BLUE = "#ADD8E6"
PALE_YELLOW = "#FFFFE0" 
SOFT_ORANGE = "#FFDAB9" 
TEXT_COLOR = "#333333"  
HEADING_COLOR = "#005A9C" 

VOLTMETER = "assets/voltmeter.png"
BOTTLE = "assets/bottle.png"
FE = "assets/FE.png"
ZN = "assets/ZN.png"
AL = "assets/AL.png"
CU = "assets/CU.png"
TRAY = "assets/tray.png"
CONTAINER = "assets/container.png"
DISTILLEDWATER = "assets/distilledWater.png"
SANDPAPER = "assets/sandpaper.png"
SOLUTIONDROP = "assets/waterdrop.png"
PAPERFILTER = "assets/paper.png"
GLASS = "assets/glass.png"
ELECTRODE = "assets/referenceElectrode.png"
SALTBRIDGE1 = "assets/saltbridge1.png"
SALTBRIDGE2 = "assets/saltbridge2.png"
SALTBRIDGE3 = "assets/saltbridge3.png"

# class for the voltage input window
class VoltageInputDialog:
    def __init__(self, parent):
        self.dialog = Toplevel(parent)
        self.dialog.title("Introducere valori tensiune")
        self.dialog.geometry("600x400")
        self.dialog.config(bg=BACKGROUND_COLOR)
        
        self.values = {}
        self.create_widgets()
        
        # display the modal window (blocks interaction with the main window)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
    def create_widgets(self):
        metals = ["Fe", "Cu", "Zn", "Al"]
        solutions = ["NaOH", "NaCl", "H2SO4"]
        
        # frame for grid
        main_frame = Frame(self.dialog, bg=BACKGROUND_COLOR)
        main_frame.pack(padx=20, pady=20)
        
        # labels solutions
        Label(main_frame, text="Metal/Soluție", bg=BACKGROUND_COLOR, font=('Times', 12, 'bold')).grid(row=0, column=0, padx=5, pady=5)
        for j, solution in enumerate(solutions, 1):
            Label(main_frame, text=solution, bg=BACKGROUND_COLOR, font=('Times', 12, 'bold')).grid(row=0, column=j, padx=5, pady=5)
        
        # fields for each metal/solution
        self.entries = {}
        for i, metal in enumerate(metals, 1):
            Label(main_frame, text=metal, bg=BACKGROUND_COLOR, font=('Times', 12, 'bold')).grid(row=i, column=0, padx=5, pady=5)
            metal_entries = {}
            for j, solution in enumerate(solutions, 1):
                entry = Entry(main_frame, width=10)
                entry.grid(row=i, column=j, padx=5, pady=5)
                metal_entries[solution] = entry
            self.entries[metal] = metal_entries
        
        
        Button(self.dialog, text="Salvează", command=self.save_values, 
               bg=GREEN, font=('Times', 12, 'bold')).pack(pady=20)
        
        
        Label(self.dialog, text="Introduceti valorile tensiunii pentru fiecare combinatie metal-solutie",
              bg=BACKGROUND_COLOR, font=('Times', 10)).pack(pady=10)
        
    def save_values(self):
        try:
            for metal, solutions in self.entries.items():
                metal_values = {}
                for solution, entry in solutions.items():
                    value = float(entry.get())
                    metal_values[solution] = value
                self.values[metal] = metal_values
            self.dialog.destroy()
        except ValueError:
            TK.messagebox.showerror("Eroare", "Va rugam introduceti doar valori numerice!")

# dictionary
expVoltage = {}

window = Tk()
window.minsize(width=1920, height=1080)
window.title("Protectia catodica cu anozi de sacrificiu")
window.config(bg=BACKGROUND_COLOR)

# open window for enter the values
voltage_dialog = VoltageInputDialog(window)
window.wait_window(voltage_dialog.dialog)

# update the dictionary 
expVoltage = voltage_dialog.values

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
PIL_paperfilter_image = Image.open(PAPERFILTER)
PIL_glass_image = Image.open(GLASS)
PIL_electrode_image = Image.open(ELECTRODE)
PIL_saltbridge1_image = Image.open(SALTBRIDGE1)
PIL_saltbridge2_image = Image.open(SALTBRIDGE2)
PIL_saltbridge3_image = Image.open(SALTBRIDGE3)

main_canvas = Canvas(window, width=1920, height=1080, bg=BACKGROUND_COLOR, highlightthickness=0)
main_canvas.place(x=0, y=0)

metal_clean_status = {
    "Fe": True,
    "Cu": True,
    "Zn": True,
    "Al": True
}

unclean_metals = []
measurements = []  # for table: catod, anod, mediu, tensiune
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

    return [resized_image, width, height]  # returns a list with the image and its attributes


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


water_ID_image = displayImage(xAxis=1170, yAxis=620, PILimageToResize=PIL_distillerWater_image, scale=0.5)
sandpaper_ID_image = displayImage(xAxis=0, yAxis=600, PILimageToResize=PIL_sandpaper_image, scale=0.6)
container1_ID_image = displayImage(xAxis=300, yAxis=300, PILimageToResize=PIL_container_image, scale=0.4)
container2_ID_image = displayImage(xAxis=500, yAxis=300, PILimageToResize=PIL_container_image, scale=0.4)
container3_ID_image = displayImage(xAxis=700, yAxis=300, PILimageToResize=PIL_container_image, scale=0.4)
voltmeter_ID_image = displayImage(xAxis=30, yAxis=10, PILimageToResize=PIL_voltmeter_image, scale=0.6)
bottle_naoh_ID_image = displayImage(xAxis=1080, yAxis=180, PILimageToResize=PIL_bottle_naoh_image, scale=0.5)
bottle_h2so4_ID_image = displayImage(xAxis=1180, yAxis=180, PILimageToResize=PIL_bottle_h2so4_image, scale=0.5)
bottle_nacl_ID_image = displayImage(xAxis=1280, yAxis=180, PILimageToResize=PIL_bottle_nacl_image, scale=0.5)
tray_ID_image = displayImage(xAxis=550, yAxis=550, PILimageToResize=PIL_tray_image, scale=0.9)
iron_ID_image = displayImage(xAxis=600, yAxis=600, PILimageToResize=PIL_FE_image, scale=0.4)
copper_ID_image = displayImage(xAxis=700, yAxis=600, PILimageToResize=PIL_CU_image, scale=0.3)
zinc_ID_image = displayImage(xAxis=750, yAxis=600, PILimageToResize=PIL_ZN_image, scale=0.4)
alluminium_ID_image = displayImage(xAxis=880, yAxis=600, PILimageToResize=PIL_AL_image, scale=0.4)
paperfilter_ID_image = displayImage(xAxis=1300, yAxis=620, PILimageToResize=PIL_paperfilter_image, scale=0.5)
glass_ID_image = displayImage(xAxis= 180, yAxis= 260, PILimageToResize = PIL_glass_image, scale = 0.4)
saltbridge1_ID_image = displayImage(xAxis = 2000, yAxis= 2000, PILimageToResize= PIL_saltbridge1_image, scale =0.6)
saltbridge2_ID_image = displayImage(xAxis = 2000, yAxis= 2000, PILimageToResize= PIL_saltbridge2_image, scale =0.5)
saltbridge3_ID_image = displayImage(xAxis = 2000, yAxis= 2000, PILimageToResize= PIL_saltbridge3_image, scale =0.6)
electrode_ID_image = displayImage(xAxis = 250, yAxis = 100, PILimageToResize= PIL_electrode_image, scale = 0.6)
main_canvas.tag_raise(bottle_h2so4_ID_image)
main_canvas.tag_raise(bottle_naoh_ID_image)
main_canvas.tag_raise(bottle_nacl_ID_image)
main_canvas.tag_raise(glass_ID_image)
main_canvas.tag_raise(iron_ID_image)
main_canvas.tag_raise(copper_ID_image)
main_canvas.tag_raise(zinc_ID_image)
main_canvas.tag_raise(alluminium_ID_image)

label_warningMetal = Label(text="", font=('Times', 14), bg=BACKGROUND_COLOR)
label_warningMetal.place(x=1140, y=450)

label_env = Label(text="Mediu coroziv selectat: N/A", font=('Times', 14), bg=BACKGROUND_COLOR)
label_env.place(x=1140, y=400)

label_metal1 = Label(text="Primul metal selectat: N/A", font=('Times', 14), bg=BACKGROUND_COLOR)
label_metal1.place(x=300, y=700)

label_metal2 = Label(text="Al doilea metal selectat: N/A", font=('Times', 14), bg=BACKGROUND_COLOR)
label_metal2.place(x=300, y=800)

label_clean = Label(text="Plăcutele sunt curate.", font=('Times', 14), fg="green", bg=BACKGROUND_COLOR)
label_clean.place(x=1100, y=550)

label_voltage = Label(text="Ultima tensiune măsurată: 0V", font=('Times', 14), bg=BACKGROUND_COLOR)
label_voltage.place(x=300, y=600)

label_info = Label(text = "", font=('Times', 14), bg = BACKGROUND_COLOR)
label_info.place(x=1140, y= 420)

label_startWarning = Label(text="""Nu putem începe! Asigurați-vă că ați folosit șmirghelul pentru a curăța plăcuțele. 
                        Studenții de dinainte au uitat!""", font=('Times', 14), fg="red", bg=BACKGROUND_COLOR)


def hideText(label):
    label.config(text = "")

def is_any_metal_unclean():
    return any(not clean for clean in metal_clean_status.values())


def unclean():
    return [key for key, clean in metal_clean_status.items() if not clean]


containerCoords = {
    "NaOH": [370, 100],  
    "H2SO4": [600, 100],
    "NaCl": [770, 100]
} 
containerDict = {
    "NaOH": container1_ID_image,   
    "H2SO4": container2_ID_image,
    "NaCl": container3_ID_image
}

"""dictionary containing the destination for each bottle moving animation
1st number: the x coordinate for the bottle
2nd number: the y coordinate for the bottle
3rd number: the x coordinate for the container
4th number: the y coordinate for the container"""
bottles = {
    bottle_h2so4_ID_image: [1180, 180, containerCoords["H2SO4"][0], containerCoords["H2SO4"][1]],
    bottle_naoh_ID_image: [1080, 180, containerCoords["NaOH"][0], containerCoords["NaOH"][1]],
    bottle_nacl_ID_image: [1280, 180, containerCoords["NaCl"][0], containerCoords["NaCl"][1]]
}

metal1 = None
metal2 = None
flagMetal = False
existentSaltbridge = []

def HideShowMetalButtons(flagMetal):
    #set the y coordinate depending if the iron's voltage alone was determined. 
    if flagMetal == True: 
        yAxis = 820
    else:
        yAxis = -1000

    #display (or not) the buttons
    buttonFe.place(x=600, y=820)
    buttonCu.place(x= 700, y= yAxis)
    buttonZn.place(x= 800, y= yAxis)
    buttonAl.place(x= 900, y= yAxis)
    
def select_environment(env):
    global environment
    global flagMetal
    global existentSaltbridge

    if not unclean_metals:
        hideX = -2000
        hideY = 2000
        for saltbridge in existentSaltbridge:
            main_canvas.coords(saltbridge, hideX, hideY)
    
    if flag == False:
        label_startWarning.place(x= 500, y = 100)
    else:
        if environment is not None and env != environment and is_any_metal_unclean():
            # restriction when trying to change the corrosive environment; 
            # operations can still be made if the environment is the same and the metal was selected once
            label_clean.config(
                text=f"Curăță toate plăcuțele înainte de a schimba mediul!\nPlăcuțe necurățate: {', '.join(unclean())}",
                fg="red"
            )
            return
        
        environment = env
        if flagMetal == False: # warning for user to start with iron.
            label_env.config(text=f"Mediu coroziv selectat: {environment}.")
            label_info.config(text="Efectuati mai întâi măsurătoarea doar pentru Fe.")
            window.after(3000, lambda:hideText(label_info))
        else: 
            label_env.config(text= f"Mediu coroziv selectat: {environment}.")
            label_info.config(text="")

        # if the corrosive environment was succesfully selected, show the user a message related to clean status
        label_clean.config(text="Plăcutele sunt curate.", fg="green")
        
        # set the variables for the animation (PIL, TK id and coordinates)
        if environment == "NaOH":
            PILbottle = PIL_bottle_naoh_image
            IDbottle = bottle_naoh_ID_image
            saltbridge = saltbridge1_ID_image

            xAxis = bottles[bottle_naoh_ID_image][2] - 100  # adjust with 100 pixels for visual precision
            yAxis = bottles[bottle_naoh_ID_image][3]
            xSalt = 230
            ySalt = 270

        elif environment == "NaCl":
            PILbottle = PIL_bottle_nacl_image
            IDbottle = bottle_nacl_ID_image
            saltbridge = saltbridge3_ID_image

            xAxis = bottles[bottle_nacl_ID_image][2] - 100
            yAxis = bottles[bottle_nacl_ID_image][3]
            xSalt = 250
            ySalt = 240
            
        else:
            PILbottle = PIL_bottle_h2so4_image
            IDbottle = bottle_h2so4_ID_image
            saltbridge = saltbridge2_ID_image
            
            xAxis = bottles[bottle_h2so4_ID_image][2] - 100
            yAxis = bottles[bottle_h2so4_ID_image][3]
            xSalt = 240
            ySalt = 245
            
        # make animation
        pour_solution(IDbottle, PILbottle, xAxis, yAxis)
        
        existentSaltbridge.append(saltbridge)

        time.sleep(1)
        window.update()

        main_canvas.coords(saltbridge, xSalt, ySalt)
        # reset the flag and restrict user's access to other metals
        flagMetal = False
        HideShowMetalButtons(flagMetal)

#text for voltmeter display
previous_ID = main_canvas.create_text(120, 55, text="0.00", font=('Times', 24), fill="black") 
conclusion = None

def calculate_corrosive(metalVoltage, metalName, corrosiveEnvironment):
    potential = referenceElectrodVoltage - metalVoltage
    ironVoltage = referenceElectrodVoltage - expVoltage["Fe"][corrosiveEnvironment]
    global conclusion

    if potential < ironVoltage:
        # the corrosive potential of the (Fe + X) sistem is bigger than the Fe's voltage in the corrosive environment selected.
        TK.messagebox.showinfo(title="Concluzia măsuratorii",
                               message=f"Metalul de asociere, {metalName} este anod de sacrificiu!")
        conclusion = "Da"
    else:
        TK.messagebox.showinfo(title="Concluzia măsurătorii",
                               message=f"Metalul de asocieire, {metalName} NU este anod de sacrificiu!")
        conclusion = "Nu"


def select_metal1(metal_input):
    if flag == False:
        label_startWarning.place(x= 500, y = 100)
    else:
        global metal1
        metal1 = metal_input
        metal_clean_status[metal1] = False #once selected, the metal is not clean anymore

        if metal1 not in unclean_metals:
            unclean_metals.append(metal1) 
        
        label_metal1.config(text=f"Primul metal selectat: {metal1}")
        label_clean.config(text="Plăcuță de Fe selectată.\nCurăță la schimbarea mediului coroziv!", fg="red")

        main_canvas.tag_raise(containerDict[environment])
        xEnd = containerCoords[environment][0]
        yEnd = containerCoords[environment][1] + 120
        move_image_smoothly(iron_ID_image, x_start= 600, y_start=600, 
                            x_end= xEnd, y_end= yEnd, duration= 1)

def getMetalID(metal_input):
    if metal_input == "Fe": 
        ID = iron_ID_image
    elif metal_input == "Zn":
        ID = zinc_ID_image
    elif metal_input == "Cu":
        ID = copper_ID_image
    else:
        ID = alluminium_ID_image
    return ID

def select_metal2(metal_input):
    if flag == False:
        label_startWarning.place(x= 500, y = 100)
    else:
        global metal2
        metal2 = metal_input
        
        # check if the selected metal has been cleaned before 
        if metal_clean_status[metal2]:
            metal_clean_status[metal2] = False
        
            if metal2 not in unclean_metals:
                unclean_metals.append(metal2)
            label_metal2.config(text=f"Al doilea metal selectat: {metal2}")
            label_clean.config(text="Plăcuță nouă selectată. Curăță după utilizare!", fg="red")

            key = getMetalID(metal_input) 
            xEnd = containerCoords[environment][0]
            yEnd = containerCoords[environment][1] + 120

            main_canvas.tag_raise(containerDict[environment])
            move_image_smoothly(key, x_start = metals[key][0], y_start= metals[key][1], 
                                x_end = xEnd, y_end= yEnd, duration = 1)
        else:
            label_metal2.config(text="Al doilea metal selectat: eroare.")
            label_clean.config(text="Plăcuța trebuie curățată mai întâi!", fg="red")

def clean(metal, metalID):
    global unclean_metals
    global metal1
    global metal2
    
    if flag == False:
        label_startWarning.place(x= 500, y = 100)
    else:
        metal_clean_status[metal] = True
        
        if metal in unclean_metals:
            unclean_metals.remove(metal)
        
        cleanAnimation(metalID, water_ID_image)
        window.update()
        time.sleep(0.5)

        # update the messages after the animation    
        label_clean.config(text=f"Plăcuța {metal} a fost curățată", fg="green")
        
        if metal is metal1:
            label_metal1.config(text="Primul metal selectat: N/A")
            metal1 = None

        if metal is metal2:
            label_metal2.config(text="Al doilea metal selectat: N/A")
            metal2 = None


def calculationHelper(metal, status):
    global measurements #list used for table contents
    voltage = expVoltage[metal][environment]
    
    # update screen message regarding the measured tension
    main_canvas.itemconfig(previous_ID, text = voltage)
    label_voltage.config(text=f"Ultima tensiune măsurată este: {voltage}V")
    
    # update the values in the table
    sacrificial_status = status
    data_to_add = (metal, sacrificial_status, environment, voltage)
    measurements.append(data_to_add)

    if metal2 is not None:
        time.sleep(0.3)
        metalID = getMetalID(metal)
        xStart, yStart = main_canvas.coords(metalID)
        move_image_smoothly(metalID, x_start= xStart, y_start= yStart, x_end= metals[metalID][0], y_end= metals[metalID][1])
        window.update()

def calculate_results():
    global flagMetal
    if flag == False:
        label_startWarning.place(x= 500, y = 100)
    else:
        if environment is None:
            label_env.config(text="Nu a fost selectat niciun \nmediu coroziv!")
        elif metal1 is None and metal2 is None:
            label_warningMetal.config(text="Selectați cele două metale (Fe + X),\nunde X poate fi (Cu, Zn, Al, -)")
            window.after(3000, lambda:hideText(label_warningMetal))
        elif metal1 is None:
            label_warningMetal.config(text="Selectați Fe ca prim metal!")
            window.after(3000, lambda:hideText(label_warningMetal))
        else:
            voltmeterValues()

            if metal2 is None:
                # if the iron plate was taken alone, set the status in the table as none. 
                calculationHelper(metal1, status= "N/A")
            else:
                # decide wether is sacrificial anode or not. 
                voltage = expVoltage[metal2][environment]
                calculate_corrosive(voltage, metal2, environment)
                status = conclusion
                calculationHelper(metal2, status)
                
        # show other buttons once iron's voltage has been calculated.
        if metal1 == "Fe" and flagMetal == False:
            flagMetal = True
            HideShowMetalButtons(flagMetal)

# erases all data in the table
def reset_data():
    global measurements
    measurements.clear()

def reset():
    global metal1, metal2, environment, previous_ID
    for metalID in metals:
        main_canvas.coords(metalID, metals[metalID][0], metals[metalID][1])
    

    main_canvas.coords(saltbridge1_ID_image, 2000, 2000)
    main_canvas.coords(saltbridge2_ID_image, 2000, 2000)
    main_canvas.coords(saltbridge3_ID_image, 2000, 2000)
    
    metal1 = None
    metal2 = None
    environment = None

    label_metal1.config(text="Primul metal selectat: N/A")
    label_metal2.config(text="Al doilea metal selectat: N/A")
    label_voltage.config(text="Ultima tensiune măsurată: 0V")
    label_env.config(text="Mediu coroziv selectat: N/A")
    main_canvas.itemconfig(previous_ID, text="0.00")

    reset_data()
    
def show_table():
    global tree, measurements
    table_window = Toplevel(window)
    table_window.title("Măsurători de tensiune")
    table_window.geometry("600x400")

    # create frame for table & scrollbar
    frame = Frame(table_window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    columns = ("Catod", "Anod de sacrificiu pt Fe", "Mediu", "Tensiune (V)")
    tree = ttk.Treeview(frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=140, anchor="center")

    for idx, (catod, anod, mediu, tensiune) in enumerate(measurements):
        tree.insert("", "end", iid=str(idx), values=(catod, anod, mediu, tensiune))

    tree.pack(fill="both", expand=True)
    scrollbar.config(command=tree.yview)

    Button(table_window, text="Exportă", command=lambda: export_to_csv(measurements)).pack(pady=10)

def export_to_csv(data):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Catod", "Anod de sacrificiu pt Fe", "Mediu", "Tensiune (V)"])
            writer.writerows(data)

def create_styled_text_window(title, file_path, window_bg, text_bg, text_fg, font_family="Arial", font_size=12, heading_size=16):
    
    styled_window = Toplevel(window)
    styled_window.title(title)
    styled_window.geometry("650x550") 
    styled_window.config(bg=window_bg)

    frame = Frame(styled_window, bg=window_bg, padx=10, pady=10)
    frame.pack(fill="both", expand=True)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    scrollbar = ttk.Scrollbar(frame)
    scrollbar.grid(row=0, column=1, sticky='ns') 
    # filling the space at scrollbar if the window is bigger than the widget. 
    
    text_widget = Text(
        frame,
        wrap="word",
        yscrollcommand=scrollbar.set,
        bg=text_bg,           
        fg=text_fg,           
        font=(font_family, font_size),
        padx=15,              
        pady=15,
    )
    text_widget.grid(row=0, column=0, sticky='ns') 
    scrollbar.config(command=text_widget.yview)
    
    text_widget.tag_configure(
        "heading",
        font=(font_family, heading_size, "bold"),
        foreground=HEADING_COLOR, 
        spacing1=10,  #space before the paragraph
        spacing2=10   #space after the paragraph
    )
    
    text_widget.tag_configure(
        "bold_text",
        font=(font_family, font_size, "bold")
    )
    
    text_widget.tag_configure(
         "italic_text",
         font=(font_family, font_size, "italic")
    )

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                    text_widget.index("end-1c") 
                    text_widget.insert("end", line)
                    text_widget.index("end-1c")

    except FileNotFoundError:
        text_widget.insert("1.0", f"eroare '{file_path}' nu a fost gasit", "heading")
    except Exception as e:
         text_widget.insert("1.0", f"eroare la citirea fișierului:\n{e}", "heading")

    text_widget.config(state="disabled") 

def show_theory():
    create_styled_text_window(
        title="Știați că...",
        file_path="text/teorie.txt",      
        window_bg=YELLOW,            
        text_bg=PALE_YELLOW,         
        text_fg=TEXT_COLOR,          
        font_family="Georgia",       
        font_size=12
    )

def show_instructions():
     create_styled_text_window(
        title="Mod de lucru",
        file_path="text/mod_lucru.txt",  
        window_bg=ORANGE,           
        text_bg=SOFT_ORANGE,        
        text_fg=TEXT_COLOR,
        font_family="Verdana",      
        font_size=11
    )
    
def oscillation(image, x, y, offset=20, count=4):
    original_y = y  # initial y coordinate

    for i in range(count):  # doing the up-down movement 'count' times
        y_start = original_y
        y_end = original_y - offset  # move the image with a certain number of pixels upper

        # start of the animation for going up
        for step in range(21):
            progress = step / 20
            current_y = y_start + (y_end - y_start) * progress  # tracking the current y coordinate
            main_canvas.coords(image, x, current_y)  # updating image's position in real time
            window.update()  # displaying the changes
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

# moving animation
def move_image_smoothly(image, x_start, y_start, x_end, y_end, duration=1.0):
    steps = 50

    for step in range(steps + 1):
        progress = step / steps # update the coefficient at each step
        current_x = x_start + (x_end - x_start) * progress # update coordinates
        current_y = y_start + (y_end - y_start) * progress

        main_canvas.coords(image, current_x, current_y) # apply the movement variables
        window.update() 
        time.sleep(duration / steps) 

#dictionary with coordinates for each plate
metals = {
    iron_ID_image: [600, 600],
    copper_ID_image: [700, 600],
    zinc_ID_image: [750, 600],
    alluminium_ID_image: [880, 600]
}

# the animation takes the metal, moves it towards the glass and then on the paper, and finally in the original pos
def cleanAnimation(metalID, waterID):
    distilledWaterX = 1230
    distilledWaterY = 600

    filterPaperX = 1350
    filterPaperY = 650

    currentX, currentY = main_canvas.coords(metalID)
    main_canvas.tag_raise(waterID) # bring the glass forwards
    move_image_smoothly(metalID, currentX, currentY, distilledWaterX, distilledWaterY)
    window.update()
    time.sleep(0.4)

    main_canvas.tag_raise(metalID)
    move_image_smoothly(metalID, distilledWaterX, distilledWaterY, filterPaperX, filterPaperY)
    time.sleep(0.3)
    move_image_smoothly(metalID, filterPaperX, filterPaperY, metals[metalID][0], metals[metalID][1])

def sand():
    # set a flag used to begin the simulation. all metals must be cleaned by the sandpaper
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
    move_image_smoothly(bottleID, bottles[bottleID][0], bottles[bottleID][1], bottles[bottleID][2],
                        bottles[bottleID][3])

    # convert the image into a rotated one
    rotated_bottleID = PILbottle.rotate(45, expand=True)

    # set the scale top 0.5, as the original bottle image had the same scale when
    scale = 0.5

    # setting up image attributes
    width = int(rotated_bottleID.width * scale)
    height = int(rotated_bottleID.height * scale)

    # getting new PIL ID for the resized image
    resized_bottleID = rotated_bottleID.resize((width, height))

    # convert the ID into a TK 'object'
    rotated_bottleTK = ImageTk.PhotoImage(resized_bottleID)

    # store the 'object' in the list so it will not be erased
    imagesList.append(rotated_bottleTK)

    main_canvas.itemconfig(bottleID, image=rotated_bottleTK)
    solutiondrop_ID_image = displayImage(xAxis, yAxis, PIL_solutiondrop_image, 0.6)

    window.update()
    time.sleep(1)
    main_canvas.delete(solutiondrop_ID_image) 

    original_PIL = PILbottle

    # redo changes and bring the bottle vertically as it was
    width = int(original_PIL.width * scale)
    height = int(original_PIL.height * scale)
    original_PIL_resized = original_PIL.resize((width, height))

    normal_imageTK = ImageTk.PhotoImage(original_PIL_resized)
    imagesList.append(normal_imageTK)

    main_canvas.itemconfig(bottleID, image=normal_imageTK)
    # bring the bottle at its initial coordinates
    move_image_smoothly(bottleID, bottles[bottleID][2], bottles[bottleID][3], bottles[bottleID][0],
                        bottles[bottleID][1])

    window.update()

#animation for voltmeter display to jump its values randomly until the final result is reached
def voltmeterValues():
    for step in range(8):
        window.update()
        time.sleep(0.2)

        random_voltage = random.random()
        random_voltage = round(random_voltage, 3)
        random_voltage_string = str(random_voltage)

        main_canvas.itemconfig(previous_ID, text=random_voltage_string)
        window.update()
    time.sleep(0.2)

# Buttons

Button(text="NaOH 0.1M", width=10, font=('times 10 bold'), command=lambda: select_environment("NaOH"),
       borderwidth=0).place(x=1097, y=300)
Button(text="H2SO4 0.1M", width=10, font=('times 10 bold'), command=lambda: select_environment("H2SO4"),
       borderwidth=0).place(x=1200, y=300)
Button(text="NaCl 1%", width=10, font=('times 10 bold'), command=lambda: select_environment("NaCl"),
       borderwidth=0).place(x=1303, y=300)

buttonFe = Button(text="Fe", width=7, font=('times 13 bold'), command=lambda: select_metal1("Fe"), borderwidth=0)
buttonCu = Button(text="Cu", width=7, font=('times 13 bold'), command=lambda: select_metal2("Cu"), borderwidth=0)
buttonZn = Button(text="Zn", width=7, font=('times 13 bold'), command=lambda: select_metal2("Zn"), borderwidth=0)
buttonAl = Button(text="Al", width=7, font=('times 13 bold'), command=lambda: select_metal2("Al"), borderwidth=0)

Button(text="Curăță Fe", width=10, command=lambda: clean("Fe", iron_ID_image)).place(x=1100, y=650)
Button(text="Curăță Cu", width=10, command=lambda: clean("Cu", copper_ID_image)).place(x= 1100, y=700)
Button(text="Curăță Zn", width=10, command=lambda: clean("Zn", zinc_ID_image)).place(x= 1100, y=750)
Button(text="Curăță Al", width=10, command=lambda: clean("Al", alluminium_ID_image)).place(x= 1100, y=800)

Button(text="Calculează", font=('times 13 bold'), command=calculate_results, bg=GREEN, fg="black", relief="groove").place(x=850, y=480)
Button(text="Resetează", font=('times 13 bold'), command=reset, bg=RED, fg="black", relief="groove").place(x=850, y=520)

Button(text="Șmirgheluire", font=('times 13 bold'), command=sand).place(x=0, y=600)

Button(text="Afișează Tabel", font=('times 13 bold'), command=show_table, bg=LIGHT_GREEN).place(x=1400, y=30)
Button(text="Știați că...", font=('times 13 bold'), command=show_theory, bg=YELLOW, fg="black", relief="groove", 
        borderwidth=1, padx=10, pady=10, width = 9).place(x=1400, y=70) #rounding with radius

Button(text="Mod de lucru", font=('times 13 bold'), bg = ORANGE, command=show_instructions).place(x=1400, y=125)

window.mainloop()