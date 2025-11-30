import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import glob
import threading

class ORMGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenSim (O)RM Map Generator")
        self.root.geometry("600x400")
        
        # Variablen
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.progress = tk.DoubleVar()
        self.status = tk.StringVar(value="Bereit")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Hauptframe
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Root-Fenster Grid-Konfiguration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Titel
        title_label = ttk.Label(main_frame, text="OpenSim (O)RM Map Generator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Eingabe-Verzeichnis Auswahl
        ttk.Label(main_frame, text="Eingabe-Verzeichnis:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_dir, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Durchsuchen", command=self.browse_input_dir).grid(row=1, column=2, pady=5)
        
        # Ausgabe-Verzeichnis Auswahl
        ttk.Label(main_frame, text="Ausgabe-Verzeichnis:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_dir, width=50).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Durchsuchen", command=self.browse_output_dir).grid(row=2, column=2, pady=5)
        
        # Optionen
        options_frame = ttk.LabelFrame(main_frame, text="Optionen", padding="5")
        options_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)
        
        self.use_height_for_ao = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Height Map für AO verwenden (falls AO fehlt)", 
                       variable=self.use_height_for_ao).grid(row=0, column=0, sticky=tk.W)
        
        self.overwrite_existing = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Existierende ORM-Maps überschreiben", 
                       variable=self.overwrite_existing).grid(row=1, column=0, sticky=tk.W)
        
        # Fortschrittsbalken
        ttk.Label(main_frame, text="Fortschritt:").grid(row=4, column=0, sticky=tk.W, pady=(10, 0))
        progress_bar = ttk.Progressbar(main_frame, variable=self.progress, length=500)
        progress_bar.grid(row=5, column=0, columnspan=3, sticky="ew", pady=5)
        
        # Status-Anzeige
        status_label = ttk.Label(main_frame, textvariable=self.status)
        status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="ORM-Maps generieren", 
                  command=self.start_generation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Beenden", 
                  command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Log-Ausgabe
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=8, column=0, columnspan=3, sticky="nsew", pady=10)
        
        self.log_text = tk.Text(log_frame, height=8, width=70)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Grid-Konfiguration
        main_frame.columnconfigure(1, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(8, weight=1)
    
    def browse_input_dir(self):
        directory = filedialog.askdirectory(title="Eingabe-Verzeichnis auswählen")
        if directory:
            self.input_dir.set(directory)
            # Automatisch Output-Verzeichnis vorschlagen
            if not self.output_dir.get():
                self.output_dir.set(os.path.join(directory, "ORM_Maps"))
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Ausgabe-Verzeichnis auswählen")
        if directory:
            self.output_dir.set(directory)
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_generation(self):
        if not self.input_dir.get() or not self.output_dir.get():
            messagebox.showerror("Fehler", "Bitte Eingabe- und Ausgabe-Verzeichnis auswählen!")
            return
        
        # In separatem Thread ausführen, um GUI nicht zu blockieren
        thread = threading.Thread(target=self.generate_orm_maps)
        thread.daemon = True
        thread.start()
    
    def generate_orm_maps(self):
        try:
            input_dir = self.input_dir.get()
            output_dir = self.output_dir.get()
            
            self.status.set("Suche Texturen...")
            self.progress.set(0)
            self.log_text.delete(1.0, tk.END)
            
            # Alle Albedo-Texturen finden (case-insensitive und mit Unterordnern)
            albedo_files = []
            for pattern in ["*_albedo.png", "*_Albedo.png", "*_ALBEDO.png"]:
                albedo_files.extend(glob.glob(os.path.join(input_dir, pattern)))
                albedo_files.extend(glob.glob(os.path.join(input_dir, "**", pattern), recursive=True))
            
            # Duplikate entfernen
            albedo_files = list(set(albedo_files))
            
            if not albedo_files:
                self.log("Keine _albedo.png Dateien gefunden!")
                self.log(f"Durchsuchtes Verzeichnis: {input_dir}")
                
                # Zeige verfügbare PNG-Dateien zur Diagnose
                all_pngs = glob.glob(os.path.join(input_dir, "*.png"))
                if all_pngs:
                    self.log(f"\nGefundene PNG-Dateien ({len(all_pngs)}):")
                    for png in all_pngs[:5]:  # Zeige erste 5
                        self.log(f"  - {os.path.basename(png)}")
                    if len(all_pngs) > 5:
                        self.log(f"  ... und {len(all_pngs) - 5} weitere")
                
                self.status.set("Fehler: Keine Texturen gefunden")
                return
            
            self.log(f"Gefunden: {len(albedo_files)} Textur-Sets")
            self.log("=" * 50)
            
            processed = 0
            errors = 0
            
            for i, albedo_file in enumerate(albedo_files):
                base_name = os.path.basename(albedo_file).replace("_albedo.png", "")
                
                # Fortschritt aktualisieren
                progress_percent = (i / len(albedo_files)) * 100
                self.progress.set(progress_percent)
                self.status.set(f"Verarbeite: {base_name}")
                
                # ORM-Map generieren
                success = self.create_single_orm_map(input_dir, output_dir, base_name)
                
                if success:
                    processed += 1
                else:
                    errors += 1
            
            # Abschluss
            self.progress.set(100)
            self.status.set("Fertig!")
            self.log("=" * 50)
            self.log(f"Erfolgreich verarbeitet: {processed}")
            self.log(f"Fehler: {errors}")
            self.log(f"ORM-Maps gespeichert in: {output_dir}")
            
            messagebox.showinfo("Fertig", f"Verarbeitung abgeschlossen!\nErfolgreich: {processed}\nFehler: {errors}")
            
        except Exception as e:
            self.log(f"FEHLER: {str(e)}")
            self.status.set("Fehler aufgetreten")
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{str(e)}")
    
    def create_single_orm_map(self, input_dir, output_dir, base_name):
        try:
            # Datei-Pfade
            ao_file = os.path.join(input_dir, f"{base_name}_ao.png")
            roughness_file = os.path.join(input_dir, f"{base_name}_roughness.png")
            metallic_file = os.path.join(input_dir, f"{base_name}_metallic.png")
            height_file = os.path.join(input_dir, f"{base_name}_height.png")
            
            # Output-Pfad
            output_file = os.path.join(output_dir, f"{base_name}_ORM.png")
            
            # Überspringen falls bereits existiert
            if os.path.exists(output_file) and not self.overwrite_existing.get():
                self.log(f"Übersprungen (existiert): {base_name}")
                return True
            
            # Falls AO fehlt und Height Map verwendet werden soll
            if self.use_height_for_ao.get() and not os.path.exists(ao_file) and os.path.exists(height_file):
                self.log(f"  Verwende Height Map für AO: {base_name}")
                ao_file = height_file
            
            # Überprüfen ob alle benötigten Dateien existieren
            missing_files = []
            for file_path in [ao_file, roughness_file, metallic_file]:
                if not os.path.exists(file_path):
                    missing_files.append(os.path.basename(file_path))
            
            if missing_files:
                self.log(f"FEHLER {base_name}: Fehlende Dateien - {', '.join(missing_files)}")
                return False
            
            # Bilder laden und verarbeiten
            ao_img = Image.open(ao_file).convert("L")
            roughness_img = Image.open(roughness_file).convert("L")
            metallic_img = Image.open(metallic_file).convert("L")
            
            # Auf gemeinsame Größe bringen
            sizes = [img.size for img in [ao_img, roughness_img, metallic_img]]
            target_size = max(sizes, key=lambda x: x[0] * x[1])
            
            if ao_img.size != target_size:
                ao_img = ao_img.resize(target_size, Image.Resampling.LANCZOS)
            if roughness_img.size != target_size:
                roughness_img = roughness_img.resize(target_size, Image.Resampling.LANCZOS)
            if metallic_img.size != target_size:
                metallic_img = metallic_img.resize(target_size, Image.Resampling.LANCZOS)
            
            # (O)RM Map kombinieren
            orm_map = Image.merge("RGB", (ao_img, roughness_img, metallic_img))
            
            # Speichern
            os.makedirs(output_dir, exist_ok=True)
            orm_map.save(output_file, "PNG")
            
            self.log(f"ERFOLG: {base_name} ({target_size[0]}x{target_size[1]})")
            return True
            
        except Exception as e:
            self.log(f"FEHLER {base_name}: {str(e)}")
            return False

def main():
    root = tk.Tk()
    ORMGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
