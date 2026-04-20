import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class LogicPartner(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Logic & Syntax Partner")
        self.geometry("1200x800")

        # Layout Config
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0) 
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.label = ctk.CTkLabel(self.sidebar, text="LOGIC VAULT", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=30)

        # Mode Buttons
        self.modes = {
            "Web Dev": {"color": "#2196F3", "desc": "Focus: Request/Response & Data Flow"},
            "Game Dev": {"color": "#4CAF50", "desc": "Focus: Signals & Event Handlers"},
            "Database": {"color": "#FF9800", "desc": "Focus: Schemas & Relationships"}
        }

        for mode_name in self.modes:
            btn = ctk.CTkButton(
                self.sidebar, 
                text=mode_name, 
                fg_color="transparent", 
                border_width=1,
                command=lambda m=mode_name: self.switch_mode(m)
            )
            btn.pack(fill="x", padx=20, pady=10)

        # --- MAIN CHAT AREA ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Header for the current mode
        self.mode_header = ctk.CTkLabel(self.main_container, text="Select a Mode to Begin", font=ctk.CTkFont(size=16, slant="italic"))
        self.mode_header.pack(pady=(0, 10), anchor="w")

        self.chat_box = ctk.CTkTextbox(self.main_container, corner_radius=15, border_width=1)
        self.chat_box.pack(fill="both", expand=True, pady=10)

        self.input_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.input_frame.pack(fill="x", pady=10)

        self.user_input = ctk.CTkEntry(self.input_frame, placeholder_text="Describe the logic you want to build...", height=40)
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.send_btn = ctk.CTkButton(self.input_frame, text="Discuss", width=100)
        self.send_btn.pack(side="right")

        # --- RESOURCE PANEL ---
        self.resource_panel = ctk.CTkFrame(self, width=0)
        self.resource_panel.grid(row=0, column=2, sticky="nsew", padx=(0, 20), pady=20)
        
        self.res_title = ctk.CTkLabel(self.resource_panel, text="Reference Wing", font=ctk.CTkFont(weight="bold"))
        self.res_title.pack(pady=20)

        self.toggle_btn = ctk.CTkButton(self.main_container, text="Open Resources", command=self.toggle_res, width=120)
        self.toggle_btn.pack(anchor="ne")

        self.is_open = False

    def switch_mode(self, mode):
        self.mode_header.configure(text=f"Current Mindset: {mode} | {self.modes[mode]['desc']}", text_color=self.modes[mode]['color'])
        self.chat_box.delete("0.0", "end")
        self.chat_box.insert("0.0", f"System: Initializing {mode} environment...\nReady to map out your {mode} logic.")

    def toggle_res(self):
        if self.is_open:
            self.resource_panel.configure(width=0)
            self.toggle_btn.configure(text="Open Resources")
        else:
            self.resource_panel.configure(width=350)
            self.toggle_btn.configure(text="Close Resources")
        self.is_open = not self.is_open

if __name__ == "__main__":
    app = LogicPartner()
    app.mainloop()