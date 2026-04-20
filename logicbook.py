import customtkinter as ctk

# Set the appearance and theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class LogicPlatform(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Logic & Syntax Partner")
        self.geometry("1100x700")

        # --- Grid Configuration ---
        # Column 0: Sidebar, Column 1: Main Chat, Column 2: Expandable Panel
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0) # Hidden/Small by default
        self.grid_rowconfigure(0, weight=1)

        # --- 1. SIDEBAR (The Umbrellas) ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="PROJECT VAULT", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20, padx=20)

        # Umbrella Buttons
        self.btn_web = ctk.CTkButton(self.sidebar, text="Web Development", fg_color="transparent", anchor="w")
        self.btn_web.pack(fill="x", padx=10, pady=5)
        
        self.btn_game = ctk.CTkButton(self.sidebar, text="Game Development", fg_color="transparent", anchor="w")
        self.btn_game.pack(fill="x", padx=10, pady=5)

        self.btn_db = ctk.CTkButton(self.sidebar, text="Databases", fg_color="transparent", anchor="w")
        self.btn_db.pack(fill="x", padx=10, pady=5)

        # --- 2. MAIN SECTION (The Conversation) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.chat_display = ctk.CTkTextbox(self.main_frame, corner_radius=10)
        self.chat_display.pack(fill="both", expand=True, pady=(0, 10))
        self.chat_display.insert("0.0", "System: Select an umbrella to begin your logic session...")

        self.input_area = ctk.CTkEntry(self.main_frame, placeholder_text="Discuss your project design here...")
        self.input_area.pack(fill="x", side="bottom")

        # --- 3. EXPANDABLE PANEL (The Resources) ---
        self.resource_panel = ctk.CTkFrame(self, width=0) # Width 0 makes it "hidden"
        self.resource_panel.grid(row=0, column=2, sticky="nsew", padx=(0, 20), pady=20)
        
        self.res_label = ctk.CTkLabel(self.resource_panel, text="Resources", font=ctk.CTkFont(weight="bold"))
        self.res_label.pack(pady=10)
        
        # Toggle Button for the Resource Panel
        self.toggle_btn = ctk.CTkButton(self.main_frame, text="Toggle Resources", command=self.toggle_resources)
        self.toggle_btn.pack(side="top", anchor="ne", pady=5)

        self.panel_open = False

    def toggle_resources(self):
        if self.panel_open:
            self.resource_panel.configure(width=0)
            self.grid_columnconfigure(2, weight=0)
        else:
            self.resource_panel.configure(width=300)
            self.grid_columnconfigure(2, weight=0) # Keep it fixed width
        self.panel_open = not self.panel_open

if __name__ == "__main__":
    app = LogicPlatform()
    app.mainloop()