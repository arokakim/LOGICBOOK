import customtkinter as ctk
from database_mgr import DatabaseManager

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class LogicPartner(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()

        self.title("Logic & Syntax Partner")
        self.geometry("1200x850")

        # Layout Config
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0) 
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.label = ctk.CTkLabel(self.sidebar, text="LOGIC VAULT", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=30)

        self.modes = {
            "Web Dev": {"color": "#2196F3", "desc": "Focus: Python/Django Data Flow"},
            "Game Dev": {"color": "#4CAF50", "desc": "Focus: Python/Godot Event Logic"},
            "Database": {"color": "#FF9800", "desc": "Focus: SQL & Schema Structure"}
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

        # --- MAIN AREA ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.mode_header = ctk.CTkLabel(self.main_container, text="Select an Umbrella to View Snippets", font=ctk.CTkFont(size=16, slant="italic"))
        self.mode_header.pack(pady=(0, 10), anchor="w")

        """
        # Create a frame for the list of titles (The "Master" view)
        self.list_frame = ctk.CTkScrollableFrame(self.main_container, width=250)
        self.list_frame.pack(side="left", fill="y", padx=(0, 10))

        # The archive_display now sits to the right (The "Detail" view)
        self.archive_display.pack(side="right", fill="both", expand=True)
        """
        # 1. THE ARCHIVE VIEW
        self.search_bar = ctk.CTkEntry(self.main_container, placeholder_text="🔍 Search titles in this umbrella...")
        self.search_bar.pack(fill="x", pady=(0, 10))
        # This tells Python: "Every time I let go of a key, run the search function"
        self.search_bar.bind("<KeyRelease>", lambda event: self.run_search())

        self.archive_display = ctk.CTkTextbox(self.main_container, corner_radius=15, border_width=1)
        self.archive_display.pack(fill="both", expand=True, pady=10)

        # 2. THE ENTRY FORM
        self.entry_label = ctk.CTkLabel(self.main_container, text="Add New Logic to Vault", font=("Arial", 12, "bold"))
        self.entry_label.pack(anchor="w", pady=(10, 0))
        
        self.form_bg = ctk.CTkFrame(self.main_container)
        self.form_bg.pack(fill="x", pady=10)

        # Entry (Supports placeholder_text)
        self.input_title = ctk.CTkEntry(self.form_bg, height=35, placeholder_text="Snippet Title (e.g. 'Django View Logic')")
        self.input_title.pack(fill="x", padx=10, pady=5)

        # Textbox (Manual placeholder)
        self.input_pseudo = ctk.CTkTextbox(self.form_bg, height=60)
        self.input_pseudo.insert("0.0", "--- LOGIC (Pseudo-code) ---")
        self.input_pseudo.pack(fill="x", padx=10, pady=5)

        self.input_code = ctk.CTkTextbox(self.form_bg, height=120)
        self.input_code.insert("0.0", "--- SYNTAX (Python Code) ---")
        self.input_code.pack(fill="x", padx=10, pady=5)

        # Control Row
        self.control_row = ctk.CTkFrame(self.form_bg, fg_color="transparent")
        self.control_row.pack(fill="x", padx=10, pady=5)

        self.current_category = ctk.StringVar(value="Web Dev")
        self.cat_menu = ctk.CTkOptionMenu(self.control_row, values=list(self.modes.keys()), variable=self.current_category)
        self.cat_menu.pack(side="left")

        self.save_btn = ctk.CTkButton(self.control_row, text="Save to Archive", command=self.save_logic, fg_color="#1f538d")
        self.save_btn.pack(side="right")

        self.resource_panel = ctk.CTkFrame(self, width=0)
        self.resource_panel.grid(row=0, column=2, sticky="nsew", padx=(0, 20), pady=20)
        
        self.toggle_btn = ctk.CTkButton(self.main_container, text="Open Resources", command=self.toggle_res, width=120)
        self.toggle_btn.pack(anchor="ne")

        self.is_open = False
        self.active_mode = None

    def save_logic(self):
        title = self.input_title.get()
        pseudo = self.input_pseudo.get("0.0", "end").strip()
        code = self.input_code.get("0.0", "end").strip()
        umbrella = self.current_category.get()
        
        if title and code:
            self.db.add_snippet(umbrella, title, pseudo, code)
            
            # Clear fields and reset manual "placeholders"
            self.input_title.delete(0, "end")
            self.input_pseudo.delete("0.0", "end")
            self.input_pseudo.insert("0.0", "--- LOGIC (Pseudo-code) ---")
            self.input_code.delete("0.0", "end")
            self.input_code.insert("0.0", "--- SYNTAX (Python Code) ---")
            
            if self.active_mode == umbrella:
                self.switch_mode(umbrella)

    def switch_mode(self, mode):
        self.active_mode = mode
        self.mode_header.configure(text=f"Current Mindset: {mode} | {self.modes[mode]['desc']}", text_color=self.modes[mode]['color'])
        
        self.archive_display.delete("0.0", "end")
        # UPDATED: We now select pseudo_code as well
        self.db.cursor.execute("SELECT title, pseudo_code, code_block FROM snippets WHERE umbrella = ?", (mode,))
        rows = self.db.cursor.fetchall()
        
        if not rows:
            self.archive_display.insert("0.0", f"No snippets found in {mode} yet.")
        else:
            for title, pseudo, code in rows:
                # Formatting the output with significant space
                self.archive_display.insert("end", f"TITLE: {title.upper()}\n")
                self.archive_display.insert("end", f"LOGIC: {pseudo}\n")
                self.archive_display.insert("end", f"\nCODE:\n{code}\n")
                self.archive_display.insert("end", f"{'='*50}\n\n") # Massive separator

    def toggle_res(self):
        if self.is_open:
            self.resource_panel.configure(width=0)
            self.toggle_btn.configure(text="Open Resources")
        else:
            self.resource_panel.configure(width=350)
            self.toggle_btn.configure(text="Close Resources")
        self.is_open = not self.is_open

    def run_search(self):
        search_term = self.search_bar.get()
        mode = self.active_mode
        
        # Clear the current display
        self.archive_display.delete("0.0", "end")
        
        # Ask the brain for filtered results
        rows = self.db.search_snippets(mode, search_term)
        
        if not rows:
            self.archive_display.insert("0.0", "No matches found.")
        else:
            for title, pseudo, code in rows:
                self.archive_display.insert("end", f"TITLE: {title.upper()}\n")
                self.archive_display.insert("end", f"LOGIC: {pseudo}\n")
                self.archive_display.insert("end", f"\nCODE:\n{code}\n")
                self.archive_display.insert("end", f"{'='*50}\n\n")

if __name__ == "__main__":
    app = LogicPartner()
    app.mainloop()