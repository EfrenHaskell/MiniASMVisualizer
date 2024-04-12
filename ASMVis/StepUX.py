from tkinter import *
from tkinter import filedialog, PhotoImage
from Simulation import *
from os.path import exists
import Visualizer as v
import Grammar as grm

"""
Author: Efren Haskell
Last Update: 4/8/2024
StepUX class creates a UI for Assembly visualization and Syntax checking for Brandeis University Cosi 131
"""


interface = Tk()
interface.title("CS131 Assembly Visualizer")
interface.geometry("440x400")
interface.resizable(False, False)
bg_color = "#F3FCF6"
interface['background'] = bg_color
emul = Simulation()
make_preset = Tk()
make_preset['background'] = bg_color
make_preset.geometry("400x440")
make_preset.resizable(False, False)
make_preset.withdraw()
preset_frame = LabelFrame(make_preset)
scrollbar = Scrollbar(preset_frame)
scrollbar.pack(side=RIGHT, fill=Y)
preset_list = Listbox(preset_frame, yscrollcommand=scrollbar.set)


def editor_close():
    make_preset.withdraw()


def close_all():
    make_preset.destroy()
    interface.destroy()


make_preset.protocol("WM_DELETE_WINDOW", editor_close)
interface.protocol("WM_DELETE_WINDOW", close_all)


def home():
    """The home method initializes GUI elements and styling for home page"""
    page_elements = []
    for i in range(3):
        page_elements.append(Label(interface, bg=bg_color))
    labelFrame = LabelFrame(interface, bg="white")
    page_elements.append(labelFrame)
    page_elements.append(Label(labelFrame, text="Welcome to the CS131 Assembly Simulator!", font=('Courier', 13), bg="white"))
    descriptor = "This application can be used to:\n - Check the syntax of your assembly programs\n - Check the semantics of your assembly code\n - Visualize the CPU processing assembly"
    page_elements.append(Label(labelFrame, text=descriptor, font=('Courier', 10), bg="white"))
    descriptor = "Hit the start button below to begin using the program!"
    page_elements.append(Label(labelFrame, text=descriptor, font=('Courier', 9), bg="white"))
    page_elements.append(Label(interface, bg=bg_color))
    page_elements.append(Button(interface, text="Start", bg="white", font=('Courier', 16), command=lambda params=("file_input", page_elements): redirect(params)))
    page_elements.append(Label(interface, bg=bg_color))
    for element in page_elements:
        element.pack()


def redirect(params):
    """"The redirect method routes page names to page initialization methods"""
    route: str = params[0]
    elements = params[1]
    for element in elements:
        element.destroy()
    if route == "file_input":
        file_input()
    elif route == "set_up":
        set_up()
    elif route == "option_page":
        option_page()
    elif route == "syntax_checker":
        syntax_checker()
    elif route == "visualize":
        visualize()


def file_input():
    """"The file_input method initializes GUI elements and styling for file input page"""
    # TODO: Clean up GUI elements, especially page_elements references for set_path 
    page_elements = []
    for i in range(3):
        page_elements.append(Label(interface, bg=bg_color))
    labelFrame = LabelFrame(interface, bg="white")
    page_elements.append(labelFrame)
    page_elements.append(Label(labelFrame, text="Input File Below", font=('Courier', 13), bg="white"))
    descriptor = "Please input the file path you want to visualize.\nOr use the browse button to find a file."
    page_elements.append(Label(labelFrame, text=descriptor, font=('Courier', 10), bg="white"))
    page_elements.append(Label(labelFrame, font=('Arial', 10), bg="white"))
    page_elements.append(Label(interface, font=('Arial', 9), bg=bg_color))
    for element in page_elements:
        element.pack()
    page_elements.append(Label(interface, text="Path: ", font=('Courier', 10), bg=bg_color))
    page_elements[-1].pack(anchor="nw", padx=20)
    page_elements.append(Entry(interface, bg="white", font=('Courier', 10)))
    entry_index = len(page_elements)-1
    page_elements[-1].pack(anchor="nw", padx=20)
    page_elements.append(Label(interface, text="", bg=bg_color))
    page_elements[-1].pack(side="left", anchor="nw", padx=7)
    page_elements.append(Button(interface, text="Browse", bg="white", height=1, font=('Courier', 9), command=lambda: browse_files(page_elements[entry_index])))
    page_elements[-1].pack(side="left", anchor="nw")
    page_elements.append(Label(interface, text="", bg=bg_color))
    page_elements.append(Label(interface, text="Go to next Page:", font=('Courier', 9), bg=bg_color))
    page_elements.append(Button(interface, text="Next", bg="white", font=('Courier', 9), command=lambda params=("set_up", page_elements): redirect(params)))
    page_elements.append(Button(interface, text="Submit", height=1, bg="white", font=('Courier', 9), command=lambda params=(page_elements[entry_index],
                                                                                 page_elements[entry_index+3],
                                                                                 page_elements[entry_index+4],
                                                                                 page_elements[entry_index+5]): set_path(params)))
    page_elements[-1].pack(side="left", anchor="nw")
    page_elements.append(Label(interface, text="", bg=bg_color))
    page_elements[-1].pack()
    page_elements[entry_index+3].pack(anchor="nw", padx=20)


def browse_files(entry):
    """The browse_files method creates a file dialog box for MiniASM file lookup"""
    file_path = filedialog.askopenfilename()
    entry.delete(0, END)
    entry.insert(0, file_path)


def alert(text: str):
    # Currently unused code
    # TODO: provide more descriptive error messages with alert boxes
    ############################################################
    pop_up = Tk()
    pop_up.title("Alert")
    pop_up.geometry("200x50")
    Label(pop_up, text=text, font=('Arial', 12)).pack()


def set_path(params):
    """The set_path method determines whether or not an entry input is an existant file"""
    entry = params[0]
    element = params[1]
    button_label = params[2]
    button = params[3]
    path = entry.get()
    path_valid = exists(path)
    entry.delete(0, END)
    v.file_nm = path
    if path_valid:
        length = len(path)
        if length > 35:
            length -= 15
            path = path[0:3] + "..." + path[length:]
        element.config(text=f"Path set to: {path}", font=('Courier', 9))
        button_label.pack()
        button.pack()
    else:
        element.config(text=f"Path does not exist", font=('Courier', 9))


def list_presets(preset_type):
    """The list_presets method initializes a list box to display memory and disk preset values"""
    preset_list.delete(0, END)
    presets.deiconify()
    for key, val in emul.history[preset_type].items():
        preset_list.insert(END, preset_type + ": " + key+"->"+val)
    preset_list.pack(fill=BOTH)
    scrollbar.config(command=preset_list.yview)
    presets.mainloop()


def make_new_preset(preset_type):
    """The make_new_preset method initializes a preset editor window for memory and disk presets
    It allows for both edit/create and delete functionality
    Preset elements are identifiable by an address parameter
    Elements are saved as address, data pairs
    """
    make_preset.title(f"Make {preset_type} Preset")
    make_preset.deiconify()
    for i in range(2):
        Label(make_preset, bg=bg_color).pack()
    labelFrame1 = LabelFrame(make_preset, bg="white")
    labelFrame2 = LabelFrame(make_preset, bg="white")
    Label(make_preset, text="Preset Editor", font=('Courier', 14), bg=bg_color).pack()
    Label(make_preset, bg=bg_color).pack()
    labelFrame1.pack(anchor="w", padx=15)
    Label(labelFrame1, text="Address:", bg="white").pack(side="left", padx=2, pady=2)
    e = Entry(labelFrame1)
    e.pack(side="left", padx=2, pady=2)
    Label(labelFrame1, text="Value:", bg="white").pack(side="left", padx=2, pady=2)
    e1 = Entry(labelFrame1)
    e1.pack(side="left", padx=2, pady=2)
    Button(make_preset, text="Set preset", bg="white", command=lambda params=(preset_type,e,e1): create(params)).pack(anchor="nw", padx=15, pady=2)
    Label(make_preset, bg=bg_color).pack()
    labelFrame2.pack(anchor="w", padx=15)
    Label(labelFrame2, text="Address:", bg="white").pack(side="left", padx=2, pady=2)
    e = Entry(labelFrame2)
    e.pack(side="left", padx=2, pady=2)
    Button(make_preset, text="Delete preset", bg="white", command=lambda params=(preset_type,e): delete(params)).pack(anchor="nw", padx=15, pady=2)
    Label(make_preset, bg=bg_color).pack()
    preset_frame.pack()
    preset_list.pack()
    refresh_history(preset_type)
    make_preset.mainloop()


def refresh_history(preset_type):
    """The refresh_history method clears the preset list-box and refills it with the simulation base history values"""
    preset_list.delete(0,END)
    for key, val in emul.history[preset_type].items():
        preset_list.insert(END, preset_type + ": " + key+"->"+val)

def create(params):
    """The create method handles preset creation"""
    address: str = params[1].get()
    data: str = params[2].get()
    location: str = params[0]
    emul.set_base(location, address, data)
    refresh_history(location)
    params[1].delete(0,END)
    params[2].delete(0,END)


def delete(params):
    """The create method handles preset deletion"""
    address: str = params[1].get()
    location: str = params[0]
    emul.remove_base(location, address)
    refresh_history(location)
    params[1].delete(0,END)


def set_up():
    """The set_up method initializes a window for preset creation options"""
    page_elements = []
    for i in range(3):
        page_elements.append(Label(interface, bg=bg_color))
    labelFrame = LabelFrame(interface, bg="white")
    page_elements.append(labelFrame)
    page_elements.append(Label(labelFrame, text="Set Up Presets", font=('Courier', 12), bg="white"))
    page_elements.append(Label(labelFrame, text="Set values for Memory and Disk addresses\nto be used by Visualizer", font=('Courier', 9), bg="white"))
    page_elements.append(Label(labelFrame, font=('Courier', 11), bg="white"))
    page_elements.append(Label(labelFrame, text="Memory Presets:", font=('Courier', 11), bg="white"))
    page_elements.append(Button(labelFrame, text="Add memory presets", font=('Courier', 11), command=lambda: make_new_preset("memory"), bg="white"))
    page_elements.append(Label(labelFrame, font=('Courier', 11), bg="white"))
    page_elements.append(Label(labelFrame, text="Disk Presets:", font=('Courier', 11), bg="white"))
    page_elements.append(Button(labelFrame, text="Add disk presets", font=('Courier', 11), command=lambda: make_new_preset("memory"), bg="white"))
    page_elements.append(Label(labelFrame, font=('Courier', 11), bg="white"))
    for element in page_elements:
        element.pack()
    page_elements.append(Label(interface, text="\t", font=('Courier', 11), bg=bg_color))
    page_elements[-1].pack(side="left")
    page_elements.append(Button(interface, text="Back", font=('Courier', 11), bg="white", command=lambda params=("file_input", page_elements): redirect(params)))
    page_elements[-1].pack(side="left")
    page_elements.append(Label(interface, text="\t", font=('Courier', 11), bg=bg_color))
    page_elements[-1].pack(side="right")
    page_elements.append(Button(interface, text="Next", font=('Courier', 11), bg="white", command=lambda params=("option_page", page_elements): redirect(params)))
    page_elements[-1].pack(side="right")
    


def syntax_checker():
    """The syntax_checker method initializes a window displaying the result of a syntax check run on file input"""
    page_elements = []
    for i in range(3):
        page_elements.append(Label(interface, bg=bg_color))
    labelFrame = LabelFrame(interface, bg="white")
    page_elements.append(labelFrame)
    page_elements.append(Label(labelFrame, text="Output:", font=('Courier', 14), bg="white"))
    page_elements.append(Label(labelFrame, bg="white"))
    try:
        message = v.start(emul)[0]
    except Exception as e:
        message = e
    page_elements.append(Label(labelFrame, text=message, bg="white", font=('Courier', 12)))
    page_elements.append(Label(interface, bg=bg_color))
    page_elements.append(Button(interface, text="Back", font=('Courier', 12), bg="white", command=lambda params=("option_page", page_elements): redirect(params)))
    for element in page_elements:
        element.pack()


def display_step(param_vals):
    """The display_step method initializes window elements displaying CPU state after running a specific line of MiniASM.
    MiniASM semantics parsing also provides addressing modes for load, store, read and write instructions,
    presents equivalent expressions for arithmetic operations and primary bus motions
    """
    index: int = param_vals[1]
    token_set = param_vals[0][index]
    token_string = "String Line: " + " ".join(token_set)
    next_index: int = emul.simulate_step(index)
    emul.log_index(index)
    log_string = emul.make_log_string(index)
    length: int = param_vals[2]
    page_elements = []
    title = Label(interface, text="ASM Visual", font=('Courier', 14), bg=bg_color)
    title.pack(anchor="nw", padx=5, pady=5)
    pc = "x"
    if index > 0:
        pc += f"+{4*index}"
    first_line: str = f"Line {index+1}, PC = {pc}"
    if token_set[0] in emul.label_map:
        first_line += f", Label = {token_set[0]}"
    subtitle = Label(interface, text=first_line, font=('Courier', 13), bg=bg_color)
    subtitle.pack(anchor="nw", padx=5, pady=5)
    labelFrame1 = LabelFrame(interface, bg="white")
    labelFrame1.pack(side="left", padx=10, pady=10)
    labelFrame2 = LabelFrame(interface, bg="white")
    labelFrame2.pack(side="right", padx=10, pady=10)
    page_elements.append(Label(labelFrame1, text="Element Breakdown:", font=('Courier', 10), bg="white"))
    page_elements.append(Label(labelFrame1, text=token_string, font=('Courier', 8), bg="white"))
    num_elements = 0
    for element in log_string:
        page_elements.append(Label(labelFrame1, text=element, font=('Courier', 8), bg="white"))
        num_elements += 1
    page_elements.append(Label(labelFrame2, text="Registers:", font=('Courier', 10), bg="white"))
    labelFrames = [LabelFrame(labelFrame2, bg="white", width=10, height=2), LabelFrame(labelFrame2, bg="white", width=10, height=2), LabelFrame(labelFrame2, bg="white", width=10, height=2)]
    '''
    for frame in labelFrames:
        frame.pack(padx=1, pady=1)
        '''
    scroll1 = Scrollbar(labelFrames[0],orient="vertical")
    scroll2 = Scrollbar(labelFrames[1])
    scroll3 = Scrollbar(labelFrames[2])
    reg_list = Listbox(labelFrames[0], yscrollcommand=scroll1.set, width=10, height=3)
    scroll1.pack(side="right", fill="y")
    mem_list = Listbox(labelFrames[1], yscrollcommand=scroll2.set, width=10, height=3)
    scroll2.pack(side="right", fill="y")
    disk_list = Listbox(labelFrames[2], yscrollcommand=scroll3.set, width=10, height=3)
    scroll3.pack(side="right", fill="y")
    for element in emul.history["registers"].items():
        reg_list.insert(END, f"{element[0]} -> {element[1]}")
    page_elements.append(labelFrames[0])
    page_elements.append(reg_list)
    page_elements.append(Label(labelFrame2, text="Disk:", font=('Courier', 10), bg="white"))
    for element in emul.history["disk"].items():
        disk_list.insert(END, f"{element[0]} -> {element[1]}")
    page_elements.append(labelFrames[1])
    page_elements.append(disk_list)
    page_elements.append(Label(labelFrame2, text="Memory:", font=('Courier', 10), bg="white"))
    for element in emul.history["memory"].items():
        disk_list.insert(END, f"{element[0]} -> {element[1]}")
    page_elements.append(labelFrames[2])
    page_elements.append(mem_list)
    for i in range(4-num_elements):
        page_elements.append(Label(labelFrame1, bg="white", width=42, font=('Courier', 8)))
    if index == 0 and emul.index_log[-1] == 0:
        page_elements.append(Label(labelFrame1, bg="white", text=" ", font=('Courier', 15)))
    else:
        page_elements.append(Button(labelFrame1, font=('Courier', 10), text="< Back", bg="white", command=lambda params=(param_vals[0], index, length, page_elements): revert_step(params)))
    if "halt" in token_set:
        page_elements.append(Label(labelFrame1, font=('Courier', 15), text=" ", bg="white"))
    else:
        page_elements.append(Button(labelFrame1, font=('Courier', 10), text="Next >", bg="white", command=lambda params=(param_vals[0], next_index, length, page_elements): transition_display(params)))
    page_elements.append(Button(labelFrame1, font=('Courier', 10), text="Back to Options", bg="white", command=lambda params=("option_page", page_elements): redirect(params)))
    for element in page_elements:
        element.pack(anchor="w", padx=2, pady=2)
    page_elements.append(title)
    page_elements.append(subtitle)
    page_elements.append(labelFrame1)
    page_elements.append(labelFrame1)
    page_elements.append(labelFrame2)
    page_elements.append(scroll1)
    page_elements.append(scroll2)
    page_elements.append(scroll3)


def revert_step(params):
    """The revert_step method calls simulation revert_step method"""
    index = emul.revert_step(params[1])
    transition_display((params[0],index,params[2],params[3]))


def transition_display(params):
    """Handles switching between steps to be displayed"""
    param_vals = (params[0], params[1],params[2])
    page_elements = params[3]
    for element in page_elements:
        element.destroy()
    display_step(param_vals)


def visualize():
    """Handles initialization of visualizer by calling the start method from Visualizer class"""
    page_elements = []
    token_sets = v.start(emul)[1]
    length = len(token_sets)
    if length > 0:
        index = 0
        display_step((token_sets, index, length))
    else:
        page_elements.append(Label(interface))
        page_elements.append(Label(interface, text="Program did not assemble properly", font=('Arial', 12)))
        page_elements.append(Button(interface, text="Back", command=lambda params=("option_page", page_elements): redirect(params)))
        for element in page_elements:
            element.pack()


def history_clear(params):
    """The history_clear method, resets data structures for Simulator functions"""
    emul.history = {
        "registers": defaultdict(str),
        "memory": defaultdict(str),
        "disk": defaultdict(str)
    }
    emul.base_cache = {
        "memory": defaultdict(str),
        "disk": defaultdict(str)
    }
    emul.label_map = defaultdict()
    emul.operation_log = []
    emul.index_log = [0]
    emul.curr_line = 0
    emul.cache_log = []
    redirect(params)


def history_reset():
    """The history_clear method, resets data structures for Simulator functions,
    Sets the memory and disk values to the base_cache elements
    """
    emul.history = {
        "registers": defaultdict(str),
        "memory": emul.base_cache["memory"],
        "disk": emul.base_cache["disk"]
    }
    emul.label_map = defaultdict()
    emul.operation_log = []
    emul.index_log = [0]
    emul.curr_line = 0
    emul.cache_log = []


def option_page():
    """The option_page method initializes window elements for Chech Syntax and Visualizer options"""
    page_elements = []
    for i in range(3):
        page_elements.append(Label(interface, bg=bg_color))
    labelFrame = LabelFrame(interface, bg="white")
    page_elements.append(labelFrame)
    page_elements.append(Label(labelFrame, text="Choose an Option Below", font=('Courier', 14), bg="white", padx=20, pady=20))
    page_elements.append(Label(labelFrame, text="Syntax Checker", bg="white", font=('Courier', 11)))
    page_elements.append(Button(labelFrame, text="Check Syntax", font=('Courier', 12), bg="white", command=lambda params=("syntax_checker", page_elements): redirect(params)))
    page_elements.append(Label(labelFrame, bg="white", font=('Courier', 11)))
    page_elements.append(Label(labelFrame, text="Semantics Checker\nand Visualizer", bg="white", font=('Courier', 11)))
    page_elements.append(Button(labelFrame, text="Run Visualizer", font=('Courier', 12), bg="white", command=lambda params=("visualize", page_elements): redirect(params)))
    page_elements.append(Label(labelFrame, bg="white"))
    #page_elements.append(Label(interface, bg=bg_color))
    for element in page_elements:
        element.pack()
    page_elements.append(Button(interface, text="Process New File", font=('Courier', 11), bg="white", command=lambda params=("file_input", page_elements): history_clear(params)))
    page_elements.append(Button(interface, text="Reset History", font=('Courier', 11), bg="white", command=history_reset))
    page_elements[-2].pack(anchor="nw", padx=80, pady=5)
    page_elements[-1].pack(anchor="nw", padx=80, pady=5)


if __name__ == "__main__":
    home()
    interface.mainloop()
