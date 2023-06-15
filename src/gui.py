import json

import tkinter
import tkinter.messagebox
import customtkinter

from src.launch import Launch

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.theme_mode = customtkinter.get_appearance_mode()
        self.title_color = ["gray75", "gray30"] #LightMode, DarkMode

        # Import block filters

        self.filtering_list = []

        with open("./blocks.json") as f:
            self.filtering_list = [x[0] for x in json.loads(f.read())]

        # Window Title and Settings

        self.title("Image2MCBlock")
        self.resizable(True, True)
        self.geometry("600x386")
        self.grid_columnconfigure(0, weight=1)

        ############################
        # Input and Output Section #
        ############################

        self.io_frame = customtkinter.CTkFrame(self)
        self.io_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="new")
        self.io_frame.grid_columnconfigure(0, weight=1)

        self.io_frame_title = customtkinter.CTkLabel(self.io_frame, text="Input and Output", fg_color=self.title_color, corner_radius=2)
        self.io_frame_title.grid(row=0, column=0, columnspan=4, padx=0, pady=0, sticky="new")

        self.input_file = customtkinter.CTkEntry(self.io_frame, placeholder_text="Path to File")
        self.input_file.grid(row=1, column=0, columnspan=2, padx=(10, 5), pady=(10, 10), sticky="new")

        self.input_file_button = customtkinter.CTkButton(self.io_frame, text="Browse", command=lambda: self.browseFiles("Input Image", self.input_file))
        self.input_file_button.grid(row=1, column=3, padx=(0, 10), pady=(10, 10), sticky="e")

        self.output_file = customtkinter.CTkEntry(self.io_frame, placeholder_text="Output File")
        self.output_file.grid(row=2, column=0, columnspan=2, padx=(10, 5), pady=(0, 10), sticky="new")

        self.output_file_button = customtkinter.CTkButton(self.io_frame, text="Browse", command=lambda: self.saveFiles("Output File", self.output_file))
        self.output_file_button.grid(row=2, column=3, padx=(0, 10), pady=(0, 10), sticky="e")

        ####################
        # Settings Section #
        ####################

        self.settings_frame = customtkinter.CTkFrame(self)
        self.settings_frame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="new")
        self.settings_frame.grid_columnconfigure(0, weight=1)

        self.settings_frame_title = customtkinter.CTkLabel(self.settings_frame, text="Settings", fg_color=self.title_color, corner_radius=2)
        self.settings_frame_title.grid(row=0, column=0, columnspan=4, padx=0, pady=0, sticky="new")

        self.algorithm_method = customtkinter.CTkOptionMenu(self.settings_frame, values=["abs_diff", "euclidean"])
        self.algorithm_method.grid(row=1, column=0, padx=(10, 5), pady=(10, 0), sticky="new")

        self.scale_factor = customtkinter.CTkEntry(self.settings_frame, placeholder_text="Scale Factor") # MAKE THIS SANITIZED, INTEGER INPUT
        self.scale_factor.grid(row=1, column=1, padx=(0, 10), pady=(10, 10), sticky="new")

        ########################
        # Atlas Inputs Section #
        ########################

        self.atlas_frame = customtkinter.CTkFrame(self)
        self.atlas_frame.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="new")
        self.atlas_frame.grid_columnconfigure(0, weight=1)

        self.atlas_frame_title = customtkinter.CTkLabel(self.atlas_frame, text="Atlas Inputs", fg_color=self.title_color, corner_radius=2)
        self.atlas_frame_title.grid(row=0, column=0, columnspan=4, padx=0, pady=0, sticky="new")

        self.atlaspng_input_file = customtkinter.CTkEntry(self.atlas_frame, placeholder_text="Path to PNG Atlas")
        self.atlaspng_input_file.grid(row=1, column=0, columnspan=2, padx=(10, 5), pady=(10, 10), sticky="new")

        self.atlaspng_input_file_button = customtkinter.CTkButton(self.atlas_frame, text="Browse", command=lambda: self.browseFiles("PNG Atlas", self.atlaspng_input_file))
        self.atlaspng_input_file_button.grid(row=1, column=3, padx=(0, 10), pady=(10, 10), sticky="e")

        self.atlastxt_input_file = customtkinter.CTkEntry(self.atlas_frame, placeholder_text="Path to TXT Atlas")
        self.atlastxt_input_file.grid(row=2, column=0, columnspan=2, padx=(10, 5), pady=(0, 10), sticky="new")

        self.atlastxt_input_file_button = customtkinter.CTkButton(self.atlas_frame, text="Browse", command=lambda: self.browseFiles("TXT Atlas", self.atlastxt_input_file))
        self.atlastxt_input_file_button.grid(row=2, column=3, padx=(0, 10), pady=(0, 10), sticky="e")
        
        #####################
        # Filtering Section #
        #####################

        self.filtering_frame = customtkinter.CTkFrame(self)
        self.filtering_frame.grid(row=1, column=1, rowspan=4, padx=(0, 10), pady=(10, 10), sticky="news")
        self.filtering_frame.grid_columnconfigure(0, weight=1)
        self.filtering_frame.grid_rowconfigure(1, weight=1)

        self.filtering_frame_title = customtkinter.CTkLabel(self.filtering_frame, text="Filtering", fg_color=self.title_color, corner_radius=2)
        self.filtering_frame_title.grid(row=0, column=0, columnspan=4, padx=0, pady=0, sticky="new")

        #self.filtering_search = customtkinter.CTkEntry(self.filtering_frame, placeholder_text="Filter Search")
        #self.filtering_search.grid(row=1, column=0, columnspan=2, padx=(10, 5), pady=(10, 10), sticky="new")

        self.filter_list = tkinter.Listbox(self.filtering_frame, relief="solid", borderwidth="0", highlightthickness="0", 
                                            bg="#333333" if self.theme_mode == "Dark" else "#EBEBEB", fg="#ffffff" if self.theme_mode == "Dark" else "#000000", 
                                            selectmode=tkinter.MULTIPLE, activestyle="none")
        self.filter_list.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="news")

        for x, filtername in enumerate(self.filtering_list):
            self.filter_list.insert(x, filtername)

        ####################

        self.submit_button = customtkinter.CTkButton(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

    def browseFiles(self, title, inputmodify):
        filename = tkinter.filedialog.askopenfilename(initialdir = "./", title = title)

        inputmodify.delete(0, tkinter.END)
        inputmodify.insert(0, filename)

    def saveFiles(self, title, inputmodify):
        filename = tkinter.filedialog.asksaveasfilename(initialdir = "./", title = title)

        inputmodify.delete(0, tkinter.END)
        inputmodify.insert(0, filename)

    def submit(self):
        input_file = self.input_file.get()
        output_file = self.output_file.get()
        scale_factor = int(self.scale_factor.get())
        method = self.algorithm_method.get()
        png_atlas_filename = self.atlaspng_input_file.get()
        txt_atlas_filename = self.atlastxt_input_file.get()

        launch = Launch("",
            scale_factor,
            method,
            png_atlas_filename,
            txt_atlas_filename)
        launch.convert(input_file, output_file)