import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import glob
import threading

class ORMGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenSim (O)RM Map Tools")
        self.root.geometry("1200x900")
        
        # Variablen
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.progress = tk.DoubleVar()
        self.status = tk.StringVar(value="Bereit")
        self.current_texture_index = 0
        self.texture_list = []
        
        # Preview Images
        self.preview_images = {}
        self.normal_preview_widget = None
        self.combined_preview_widget = None
        
        # Optionen
        self.use_height_for_ao = tk.BooleanVar(value=True)
        self.overwrite_existing = tk.BooleanVar(value=False)
        self.fill_missing_maps = tk.BooleanVar(value=False)  # Standard: AUS
        
        self.setup_ui()
    
    def setup_ui(self):
        # Hauptframe
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Root-Fenster Grid-Konfiguration
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Titel
        title_label = ttk.Label(main_frame, text="OpenSim (O)RM Map Tools", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Linke Seite: Steuerung
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # Eingabe-Verzeichnis
        ttk.Label(control_frame, text="Eingabe-Verzeichnis:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(control_frame, textvariable=self.input_dir, width=40).grid(row=1, column=0, pady=5)
        ttk.Button(control_frame, text="Durchsuchen", command=self.browse_input_dir).grid(row=1, column=1, pady=5, padx=5)
        
        # Ausgabe-Verzeichnis
        ttk.Label(control_frame, text="Ausgabe-Verzeichnis:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(control_frame, textvariable=self.output_dir, width=40).grid(row=3, column=0, pady=5)
        ttk.Button(control_frame, text="Durchsuchen", command=self.browse_output_dir).grid(row=3, column=1, pady=5, padx=5)
        
        # Optionen
        options_frame = ttk.LabelFrame(control_frame, text="Optionen", padding="5")
        options_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)
        
        ttk.Checkbutton(options_frame, text="Height für AO verwenden", 
                       variable=self.use_height_for_ao).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Checkbutton(options_frame, text="Existierende überschreiben", 
                       variable=self.overwrite_existing).grid(row=1, column=0, sticky=tk.W)
        
        ttk.Checkbutton(options_frame, text="Fehlende Maps automatisch auffüllen", 
                       variable=self.fill_missing_maps).grid(row=2, column=0, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Texturen laden", command=self.load_textures).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Fehlende Maps", command=self.generate_missing_maps).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="ORM generieren", command=self.start_generation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="GLTF generieren", command=self.generate_gltf).pack(side=tk.LEFT, padx=5)
        
        # Fortschritt
        ttk.Label(control_frame, text="Fortschritt:").grid(row=6, column=0, sticky=tk.W, pady=(10, 0))
        progress_bar = ttk.Progressbar(control_frame, variable=self.progress, length=400)
        progress_bar.grid(row=7, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Status
        status_label = ttk.Label(control_frame, textvariable=self.status)
        status_label.grid(row=8, column=0, columnspan=2, pady=5)
        
        # Log
        log_frame = ttk.LabelFrame(control_frame, text="Log", padding="5")
        log_frame.grid(row=9, column=0, columnspan=2, sticky="nsew", pady=10)
        
        self.log_text = tk.Text(log_frame, height=8, width=50)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Rechte Seite: Vorschau
        preview_frame = ttk.LabelFrame(main_frame, text="Material Vorschau", padding="10")
        preview_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        
        # Navigation
        nav_frame = ttk.Frame(preview_frame)
        nav_frame.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        ttk.Button(nav_frame, text="◄ Zurück", command=self.prev_texture).pack(side=tk.LEFT, padx=5)
        self.texture_label = ttk.Label(nav_frame, text="Keine Texturen geladen")
        self.texture_label.pack(side=tk.LEFT, padx=20)
        ttk.Button(nav_frame, text="Vor ►", command=self.next_texture).pack(side=tk.LEFT, padx=5)
        
        # Zeile 1: ORM-Komponenten (Original-Reihenfolge)
        ttk.Label(preview_frame, text="Ambient Occlusion", font=("Arial", 9, "bold")).grid(row=1, column=0, pady=5)
        self.ao_preview = ttk.Label(preview_frame, text="Keine Vorschau", relief="solid", width=25)
        self.ao_preview.grid(row=2, column=0, padx=5, pady=5)
        
        ttk.Label(preview_frame, text="Roughness", font=("Arial", 9, "bold")).grid(row=1, column=1, pady=5)
        self.roughness_preview = ttk.Label(preview_frame, text="Keine Vorschau", relief="solid", width=25)
        self.roughness_preview.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(preview_frame, text="Metallic", font=("Arial", 9, "bold")).grid(row=1, column=2, pady=5)
        self.metallic_preview = ttk.Label(preview_frame, text="Keine Vorschau", relief="solid", width=25)
        self.metallic_preview.grid(row=2, column=2, padx=5, pady=5)
        
        # Zeile 2: Emission und ORM Map
        ttk.Label(preview_frame, text="Emission Map", font=("Arial", 10, "bold")).grid(row=3, column=0, pady=(20, 5))
        self.emission_preview = ttk.Label(preview_frame, text="Keine Vorschau", relief="solid", width=25)
        self.emission_preview.grid(row=4, column=0, padx=5, pady=5)
        
        ttk.Label(preview_frame, text="ORM Map (kombiniert)", font=("Arial", 10, "bold")).grid(row=3, column=1, columnspan=2, pady=(20, 5))
        self.orm_preview = ttk.Label(preview_frame, text="Noch nicht generiert", relief="solid", width=25)
        self.orm_preview.grid(row=4, column=1, columnspan=2, padx=5, pady=5)
        
        # Zeile 3: Normal Map, Albedo, Alle Bestandteile (NEU - nebeneinander)
        ttk.Label(preview_frame, text="Normal Map", font=("Arial", 9, "bold")).grid(row=5, column=0, pady=(20, 5))
        self.normal_preview = ttk.Label(preview_frame, text="Keine Vorschau", relief="solid", width=25)
        self.normal_preview.grid(row=6, column=0, padx=5, pady=5)
        
        ttk.Label(preview_frame, text="Albedo/Base Color", font=("Arial", 9, "bold")).grid(row=5, column=1, pady=(20, 5))
        self.albedo_preview = ttk.Label(preview_frame, text="Keine Vorschau", relief="solid", width=25)
        self.albedo_preview.grid(row=6, column=1, padx=5, pady=5)
        
        ttk.Label(preview_frame, text="Alle Bestandteile", font=("Arial", 9, "bold")).grid(row=5, column=2, pady=(20, 5))
        self.combined_preview = ttk.Label(preview_frame, text="Keine Vorschau", relief="solid", width=25)
        self.combined_preview.grid(row=6, column=2, padx=5, pady=5)
        
        # Grid-Konfiguration
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        control_frame.rowconfigure(9, weight=1)
    
    def browse_input_dir(self):
        directory = filedialog.askdirectory(title="Eingabe-Verzeichnis auswählen")
        if directory:
            self.input_dir.set(directory)
            self.output_dir.set(directory)
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Ausgabe-Verzeichnis auswählen")
        if directory:
            self.output_dir.set(directory)
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def load_textures(self):
        if not self.input_dir.get():
            messagebox.showerror("Fehler", "Bitte Eingabe-Verzeichnis auswählen!")
            return
        
        thread = threading.Thread(target=self._load_textures_thread)
        thread.daemon = True
        thread.start()
    
    def _load_textures_thread(self):
        input_dir = self.input_dir.get()
        self.status.set("Suche Texturen...")
        self.log_text.delete(1.0, tk.END)
        
        # Alle Albedo-Texturen finden
        albedo_files = []
        albedo_suffixes = [
            "albedo", "Albedo", "ALBEDO",
            "alb", "Alb", "ALB",
            "base", "Base", "BASE",
            "basecolor", "BaseColor", "BASECOLOR",
            "color", "Color", "COLOR",
            "col", "Col", "COL",
            "diffuse", "Diffuse", "DIFFUSE",
            "diff", "Diff", "DIFF"
        ]
        extensions = ["png", "jpg", "jpeg", "jp2"]
        
        for suffix in albedo_suffixes:
            for ext in extensions:
                for sep in ["_", "-"]:
                    pattern = f"*{sep}{suffix}.{ext}"
                    albedo_files.extend(glob.glob(os.path.join(input_dir, pattern)))
                    albedo_files.extend(glob.glob(os.path.join(input_dir, "**", pattern), recursive=True))
                    
                    # Polyhaven: *_diff_1k.jpg, *_diff_2k.jpg, etc.
                    for res in ["1k", "2k", "4k", "8k", "16k"]:
                        pattern_res = f"*{sep}{suffix}_{res}.{ext}"
                        albedo_files.extend(glob.glob(os.path.join(input_dir, pattern_res)))
                        albedo_files.extend(glob.glob(os.path.join(input_dir, "**", pattern_res), recursive=True))
        
        albedo_files = list(set(albedo_files))
        
        if not albedo_files:
            self.log("Keine Texturen gefunden!")
            self.status.set("Fehler: Keine Texturen gefunden")
            return
        
        # Extrahiere Base-Namen
        self.texture_list = []
        for albedo_file in albedo_files:
            base_name = os.path.basename(albedo_file)
            for suffix in albedo_suffixes:
                for ext in extensions:
                    for sep in ["_", "-"]:
                        # Standard: material_diff.jpg
                        full_suffix = f"{sep}{suffix}.{ext}"
                        if base_name.endswith(full_suffix):
                            base_name = base_name[:-(len(full_suffix))]
                            self.texture_list.append({
                                'base_name': base_name,
                                'albedo_file': albedo_file,
                                'dir': os.path.dirname(albedo_file)
                            })
                            break
                        
                        # Polyhaven: material_diff_1k.jpg
                        for res in ["1k", "2k", "4k", "8k", "16k"]:
                            full_suffix_res = f"{sep}{suffix}_{res}.{ext}"
                            if base_name.endswith(full_suffix_res):
                                base_name = base_name[:-(len(full_suffix_res))]
                                self.texture_list.append({
                                    'base_name': base_name,
                                    'albedo_file': albedo_file,
                                    'dir': os.path.dirname(albedo_file)
                                })
                                break
                        else:
                            continue
                        break
                    else:
                        continue
                    break
                else:
                    continue
                break
        
        self.current_texture_index = 0
        self.log(f"Gefunden: {len(self.texture_list)} Textur-Sets")
        self.status.set(f"{len(self.texture_list)} Texturen geladen")
        
        if self.texture_list:
            self.show_current_texture()
    
    def show_current_texture(self):
        if not self.texture_list:
            return
        
        texture_info = self.texture_list[self.current_texture_index]
        base_name = texture_info['base_name']
        texture_dir = texture_info['dir']
        
        self.texture_label.config(text=f"Textur {self.current_texture_index + 1}/{len(self.texture_list)}: {base_name}")
        
        # Finde Textur-Dateien
        normal_file = self.find_texture_file_with_ogl(texture_dir, base_name, [
            "normal", "Normal", "NORMAL",
            "NormalGL", "NormalDX",  # AmbientCG
            "nor_gl", "nor_dx",  # Polyhaven
            "norrmal",  # Tippfehler
            "norm", "Norm",
            "NRM", "Nrm", "nrm",  # CGBookcase, Poliigon
            "nor", "Nor", "NOR"  # FreePBR
        ])
        ao_file = self.find_texture_file(texture_dir, base_name, [
            "ao", "AO", "Ao",
            "ambient", "Ambient", "AMBIENT",
            "occlusion", "Occlusion", "OCCLUSION",
            "AmbientOcclusion",  # AmbientCG
            "ambientOcclusion",  # 3dtextures.me
            "Occlusionc", "ambient-occlusion"  # Tippfehler in Texturen
        ])
        roughness_file = self.find_texture_file(texture_dir, base_name, [
            "roughness", "Roughness", "ROUGHNESS",
            "rough", "Rough", "ROUGH",
            "roughnness",  # Tippfehler in Texturen
            "rgh", "RGH",
            "REFL", "Refl", "refl",  # CGBookcase, Poliigon (Roughness Map)
            "gloss", "Gloss", "GLOSS"  # TextureCan, Poliigon (inverted roughness)
        ])
        metallic_file = self.find_texture_file(texture_dir, base_name, [
            "metallic", "Metallic", "METALLIC",
            "metal", "Metal", "METAL",
            "metalic",  # Tippfehler in Texturen
            "metallness", "Metallness",
            "metalness", "Metalness",
            "mtl", "MTL",
            "Metalness",  # cc0textures
            "specular", "Specular", "SPECULAR"  # Legacy PBR (Textures.com, TextureCan)
        ])
        height_file = self.find_texture_file(texture_dir, base_name, [
            "height", "Height", "HEIGHT",
            "disp", "Disp", "DISP",
            "displacement", "Displacement", "DISPLACEMENT",  # AmbientCG
            "bump", "Bump", "BUMP"
        ])
        emission_file = self.find_texture_file(texture_dir, base_name, [
            "emission", "Emission", "EMISSION",
            "emissive", "Emissive", "EMISSIVE",
            "emiss", "Emiss", "emis", "Emis", "emi", "Emi",
            "glow", "Glow", "GLOW"
        ])
        
        # Falls AO fehlt, Height verwenden
        if not ao_file and height_file and self.use_height_for_ao.get():
            ao_file = height_file
        
        # ORM Datei prüfen
        output_dir = self.output_dir.get() or os.path.join(texture_dir, "ORM_Maps")
        orm_file = os.path.join(output_dir, f"{base_name}_ORM.png")
        
        # Zeige Previews
        self.show_preview_image(normal_file, self.normal_preview, "Normal fehlt")
        self.show_preview_image(texture_info['albedo_file'], self.albedo_preview, "Albedo fehlt")
        self.show_preview_image(ao_file, self.ao_preview, "AO fehlt")
        self.show_preview_image(roughness_file, self.roughness_preview, "Roughness fehlt")
        self.show_preview_image(metallic_file, self.metallic_preview, "Metallic fehlt")
        self.show_preview_image(emission_file, self.emission_preview, "Emission fehlt")
        
        # Erstelle kombinierte Preview (alle Bestandteile)
        self.create_combined_preview(texture_info['albedo_file'], normal_file, ao_file, 
                                    roughness_file, metallic_file, height_file, emission_file)
        
        if os.path.exists(orm_file):
            self.show_preview_image(orm_file, self.orm_preview, "ORM Map")
        else:
            self.orm_preview.config(image='', text="Noch nicht generiert")
    
    def find_texture_file(self, directory, base_name, suffixes):
        extensions = ["png", "jpg", "jpeg", "jp2"]
        for suffix in suffixes:
            for sep in ['_', '-']:
                for ext in extensions:
                    # Standard: material_rough.jpg
                    path = os.path.join(directory, f"{base_name}{sep}{suffix}.{ext}")
                    if os.path.exists(path):
                        return path
                    
                    # Polyhaven: material_rough_1k.jpg
                    for res in ["1k", "2k", "4k", "8k", "16k"]:
                        path_res = os.path.join(directory, f"{base_name}{sep}{suffix}_{res}.{ext}")
                        if os.path.exists(path_res):
                            return path_res
        return None
    
    def find_texture_file_with_ogl(self, directory, base_name, suffixes):
        """Spezielle Suche für Normal-Maps die oft -ogl oder Nummern haben"""
        extensions = ["png", "jpg", "jpeg", "jp2"]
        
        # Erst normale Suche (inkl. Polyhaven-Auflösungen)
        result = self.find_texture_file(directory, base_name, suffixes)
        if result:
            return result
        
        # Dann mit -ogl und Nummern
        import glob as glob_mod
        for suffix in suffixes:
            for sep in ['_', '-']:
                for ext in extensions:
                    # Polyhaven: material_nor_gl_1k.jpg (with underscore before resolution)
                    for res in ["1k", "2k", "4k", "8k", "16k"]:
                        # Pattern: *_nor_gl_1k.jpg
                        pattern = os.path.join(directory, f"{base_name}{sep}{suffix}_{res}.{ext}")
                        matches = glob_mod.glob(pattern)
                        if matches:
                            return matches[0]
                    
                    # Mit -ogl Suffix: material_normal-ogl.jpg
                    pattern = os.path.join(directory, f"{base_name}{sep}{suffix}*-ogl.{ext}")
                    matches = glob_mod.glob(pattern)
                    if matches:
                        return matches[0]
                    
                    # Mit Nummern: material_normal4.jpg
                    pattern = os.path.join(directory, f"{base_name}{sep}{suffix}[0-9].{ext}")
                    matches = glob_mod.glob(pattern)
                    if matches:
                        return matches[0]
        
        return None
    
    def show_preview_image(self, file_path, label_widget, fallback_text):
        if not file_path or not os.path.exists(file_path):
            label_widget.config(image='', text=fallback_text)
            return
        
        try:
            img = Image.open(file_path)
            img.thumbnail((200, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            # Speichere Referenz
            label_widget.image = photo
            label_widget.config(image=photo, text='')
        except Exception as e:
            label_widget.config(image='', text=f"Fehler: {str(e)[:20]}")
    
    def create_combined_preview(self, albedo_file, normal_file, ao_file, 
                               roughness_file, metallic_file, height_file, emission_file=None):
        """Erstellt eine kombinierte Vorschau - zeigt wie das Material aussehen würde"""
        try:
            # Lade Basis-Textur (Albedo)
            if not albedo_file or not os.path.exists(albedo_file):
                self.combined_preview.config(image='', text="Albedo fehlt")
                return
            
            base_img = Image.open(albedo_file).convert('RGB')
            width, height = base_img.size
            
            # Erstelle Pixel-Arrays für Verarbeitung
            import numpy as np
            albedo_data = np.array(base_img, dtype=np.float32) / 255.0
            
            # Lade AO und multipliziere mit Albedo (dunkelt Schatten ab)
            if ao_file and os.path.exists(ao_file):
                ao_img = Image.open(ao_file).convert('L').resize((width, height), Image.Resampling.LANCZOS)
                ao_data = np.array(ao_img, dtype=np.float32) / 255.0
                albedo_data *= ao_data[:, :, np.newaxis]
            
            # Simuliere Roughness-Effekt (weichere Albedo bei hoher Roughness)
            if roughness_file and os.path.exists(roughness_file):
                rough_img = Image.open(roughness_file).convert('L').resize((width, height), Image.Resampling.LANCZOS)
                rough_data = np.array(rough_img, dtype=np.float32) / 255.0
                # Leichtes Blur für raue Bereiche simulieren
                roughness_factor = 0.85 + (rough_data * 0.15)
                albedo_data *= roughness_factor[:, :, np.newaxis]
            
            # Simuliere Metallic-Effekt (metallische Bereiche reflektieren mehr)
            if metallic_file and os.path.exists(metallic_file):
                metal_img = Image.open(metallic_file).convert('L').resize((width, height), Image.Resampling.LANCZOS)
                metal_data = np.array(metal_img, dtype=np.float32) / 255.0
                # Metallische Bereiche sind glänzender (heller)
                metallic_boost = 1.0 + (metal_data * 0.3)
                albedo_data *= metallic_boost[:, :, np.newaxis]
            
            # Addiere Emission (selbstleuchtend, unabhängig von Beleuchtung)
            if emission_file and os.path.exists(emission_file):
                emission_img = Image.open(emission_file).convert('RGB').resize((width, height), Image.Resampling.LANCZOS)
                emission_data = np.array(emission_img, dtype=np.float32) / 255.0
                # Emission wird addiert (nicht multipliziert) - leuchtet selbst
                albedo_data += emission_data * 0.5  # 50% Stärke für bessere Sichtbarkeit
            
            # Konvertiere zurück zu Bild
            result_data = np.clip(albedo_data * 255.0, 0, 255).astype(np.uint8)
            result_img = Image.fromarray(result_data, mode='RGB')
            
            # Skaliere für Vorschau
            result_img.thumbnail((200, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(result_img)
            
            # Speichere Referenz (verhindert Garbage Collection)
            self.combined_preview.image = photo  # type: ignore
            self.combined_preview.config(image=photo, text='')
            
        except Exception as e:
            self.combined_preview.config(image='', text=f"Fehler: {str(e)[:30]}")
    
    def prev_texture(self):
        if not self.texture_list:
            return
        self.current_texture_index = (self.current_texture_index - 1) % len(self.texture_list)
        self.show_current_texture()
    
    def next_texture(self):
        if not self.texture_list:
            return
        self.current_texture_index = (self.current_texture_index + 1) % len(self.texture_list)
        self.show_current_texture()
    
    def start_generation(self):
        if not self.input_dir.get() or not self.output_dir.get():
            messagebox.showerror("Fehler", "Bitte Eingabe- und Ausgabe-Verzeichnis auswählen!")
            return
        
        if not self.texture_list:
            messagebox.showwarning("Warnung", "Bitte zuerst Texturen laden!")
            return
        
        thread = threading.Thread(target=self.generate_orm_maps)
        thread.daemon = True
        thread.start()
    
    def generate_missing_maps(self):
        """Generiert nur fehlende Einzeltexturen (AO, Roughness, Metallic) als separate Dateien"""
        if not self.texture_list:
            messagebox.showwarning("Warnung", "Bitte zuerst Texturen laden!")
            return
        
        if not self.input_dir.get():
            messagebox.showerror("Fehler", "Bitte Eingabe-Verzeichnis auswählen!")
            return
        
        thread = threading.Thread(target=self._generate_missing_maps_thread)
        thread.daemon = True
        thread.start()
    
    def _generate_missing_maps_thread(self):
        """Thread-Funktion für Generierung fehlender Maps"""
        try:
            self.status.set("Generiere fehlende Maps...")
            self.progress.set(0)
            
            generated = 0
            skipped = 0
            
            for i, texture_info in enumerate(self.texture_list):
                base_name = texture_info['base_name']
                texture_dir = texture_info['dir']
                output_dir = self.output_dir.get() or texture_dir
                
                progress_percent = (i / len(self.texture_list)) * 100
                self.progress.set(progress_percent)
                self.status.set(f"Prüfe: {base_name}")
                
                # Prüfe welche Maps fehlen
                ao_file = self.find_texture_file(texture_dir, base_name, ["ao", "AO", "ambient", "occlusion"])
                roughness_file = self.find_texture_file(texture_dir, base_name, ["roughness", "rough", "ROUGH"])
                metallic_file = self.find_texture_file(texture_dir, base_name, ["metallic", "metal", "METAL"])
                
                # Bestimme Zielgröße
                reference_img = None
                if texture_info['albedo_file']:
                    reference_img = Image.open(texture_info['albedo_file'])
                
                if reference_img:
                    target_size = reference_img.size
                else:
                    target_size = (1024, 1024)
                
                created_maps = []
                
                # Erstelle fehlende AO
                if not ao_file:
                    ao_img = Image.new("L", target_size, 255)
                    ao_path = os.path.join(output_dir, f"{base_name}_ao.png")
                    os.makedirs(output_dir, exist_ok=True)
                    ao_img.save(ao_path, "PNG")
                    created_maps.append("AO")
                
                # Erstelle fehlende Roughness
                if not roughness_file:
                    rough_img = Image.new("L", target_size, 128)
                    rough_path = os.path.join(output_dir, f"{base_name}_roughness.png")
                    os.makedirs(output_dir, exist_ok=True)
                    rough_img.save(rough_path, "PNG")
                    created_maps.append("Roughness")
                
                # Erstelle fehlende Metallic
                if not metallic_file:
                    metal_img = Image.new("L", target_size, 0)
                    metal_path = os.path.join(output_dir, f"{base_name}_metallic.png")
                    os.makedirs(output_dir, exist_ok=True)
                    metal_img.save(metal_path, "PNG")
                    created_maps.append("Metallic")
                
                if created_maps:
                    self.log(f"Erstellt für {base_name}: {', '.join(created_maps)}")
                    generated += 1
                else:
                    skipped += 1
            
            self.progress.set(100)
            self.status.set("Fehlende Maps generiert!")
            self.log("=" * 50)
            self.log(f"Materialien mit erstellten Maps: {generated}, Vollständig: {skipped}")
            
            messagebox.showinfo("Fertig", f"Fehlende Maps generiert!\nBearbeitet: {generated}\nVollständig: {skipped}")
            
        except Exception as e:
            self.log(f"FEHLER: {str(e)}")
            self.status.set("Fehler aufgetreten")
            messagebox.showerror("Fehler", f"Fehler bei Map-Generierung:\n{str(e)}")
    
    def generate_orm_maps(self):
        try:
            output_dir = self.output_dir.get()
            
            self.status.set("Generiere ORM-Maps...")
            self.progress.set(0)
            
            processed = 0
            errors = 0
            
            for i, texture_info in enumerate(self.texture_list):
                base_name = texture_info['base_name']
                texture_dir = texture_info['dir']
                
                progress_percent = (i / len(self.texture_list)) * 100
                self.progress.set(progress_percent)
                self.status.set(f"Verarbeite: {base_name}")
                
                success = self.create_single_orm_map(texture_dir, output_dir, base_name)
                
                if success:
                    processed += 1
                else:
                    errors += 1
            
            self.progress.set(100)
            self.status.set("Fertig!")
            self.log("=" * 50)
            self.log(f"Erfolgreich: {processed}, Fehler: {errors}")
            
            # Zeige ORM Preview nach Generierung
            if self.texture_list:
                self.show_current_texture()
            
            messagebox.showinfo("Fertig", f"Verarbeitung abgeschlossen!\nErfolgreich: {processed}\nFehler: {errors}")
            
        except Exception as e:
            self.log(f"FEHLER: {str(e)}")
            self.status.set("Fehler aufgetreten")
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{str(e)}")
    
    def create_single_orm_map(self, input_dir, output_dir, base_name):
        try:
            # Suffix-Definitionen
            ao_suffixes = [
                "ao", "AO", "Ao",
                "ambient", "Ambient", "AMBIENT",
                "occlusion", "Occlusion", "OCCLUSION",
                "AmbientOcclusion",  # AmbientCG
                "ambientOcclusion",  # 3dtextures.me
                "Occlusionc"  # Tippfehler
            ]
            roughness_suffixes = [
                "roughness", "Roughness", "ROUGHNESS",
                "rough", "Rough", "ROUGH",
                "roughnness",  # Tippfehler
                "rgh", "RGH", "Rgh",
                "REFL", "Refl", "refl",  # CGBookcase, Poliigon
                "gloss", "Gloss", "GLOSS"  # TextureCan (inverted)
            ]
            metallic_suffixes = [
                "metallic", "Metallic", "METALLIC",
                "metal", "Metal", "METAL",
                "metalic",  # Tippfehler
                "metallness", "Metallness",
                "metalness", "Metalness",
                "mtl", "MTL", "Mtl",
                "Metalness",  # cc0textures
                "specular", "Specular", "SPECULAR"  # Legacy
            ]
            height_suffixes = [
                "height", "Height", "HEIGHT",
                "disp", "Disp", "DISP",
                "displacement", "Displacement", "DISPLACEMENT",  # AmbientCG
                "bump", "Bump", "BUMP"
            ]
            
            def find_texture_file(base, suffix_list):
                extensions = ["png", "jpg", "jpeg", "jp2"]
                for suffix in suffix_list:
                    for sep in ['_', '-']:
                        for ext in extensions:
                            # Standard: material_rough.jpg
                            path = os.path.join(input_dir, f"{base}{sep}{suffix}.{ext}")
                            if os.path.exists(path):
                                return path
                            
                            # Polyhaven: material_rough_1k.jpg
                            for res in ["1k", "2k", "4k", "8k", "16k"]:
                                path_res = os.path.join(input_dir, f"{base}{sep}{suffix}_{res}.{ext}")
                                if os.path.exists(path_res):
                                    return path_res
                return None
            
            ao_file = find_texture_file(base_name, ao_suffixes)
            roughness_file = find_texture_file(base_name, roughness_suffixes)
            metallic_file = find_texture_file(base_name, metallic_suffixes)
            height_file = find_texture_file(base_name, height_suffixes)
            
            output_file = os.path.join(output_dir, f"{base_name}_ORM.png")
            
            if os.path.exists(output_file) and not self.overwrite_existing.get():
                self.log(f"Übersprungen: {base_name}")
                return True
            
            if self.use_height_for_ao.get() and not ao_file and height_file:
                ao_file = height_file
            
            # Prüfe ob fehlende Maps automatisch aufgefüllt werden sollen
            if not self.fill_missing_maps.get():
                # Alte Logik: Fehlende Maps führen zu Fehler
                missing_files = []
                if not ao_file:
                    missing_files.append("ao")
                if not roughness_file:
                    missing_files.append("roughness")
                if not metallic_file:
                    missing_files.append("metallic")
                
                if missing_files:
                    self.log(f"FEHLER {base_name}: Fehlende Dateien - {', '.join(missing_files)}")
                    return False
            
            # Bestimme Zielgröße aus vorhandenen Dateien
            reference_img = None
            if ao_file:
                reference_img = Image.open(ao_file)
            elif roughness_file:
                reference_img = Image.open(roughness_file)
            elif metallic_file:
                reference_img = Image.open(metallic_file)
            
            # Falls alle fehlen, verwende Standardgröße
            if reference_img:
                target_size = reference_img.size
            else:
                target_size = (1024, 1024)  # Standardgröße
            
            # Lade oder erstelle AO (Standard: Weiß = keine Verdeckung)
            if ao_file and os.path.exists(ao_file):
                ao_img = Image.open(ao_file).convert("L")
                if ao_img.size != target_size:
                    ao_img = ao_img.resize(target_size, Image.Resampling.LANCZOS)
            elif self.fill_missing_maps.get():
                ao_img = Image.new("L", target_size, 255)  # Weiß = keine Ambient Occlusion
                self.log(f"INFO {base_name}: AO fehlt - verwende Weiß (255)")
            else:
                raise Exception("AO-Map fehlt")
            
            # Lade oder erstelle Roughness (Standard: Mittelgrau = semi-rough)
            if roughness_file and os.path.exists(roughness_file):
                roughness_img = Image.open(roughness_file).convert("L")
                if roughness_img.size != target_size:
                    roughness_img = roughness_img.resize(target_size, Image.Resampling.LANCZOS)
            elif self.fill_missing_maps.get():
                roughness_img = Image.new("L", target_size, 128)  # Grau = mittlere Roughness
                self.log(f"INFO {base_name}: Roughness fehlt - verwende Grau (128)")
            else:
                raise Exception("Roughness-Map fehlt")
            
            # Lade oder erstelle Metallic (Standard: Schwarz = nicht-metallisch)
            if metallic_file and os.path.exists(metallic_file):
                metallic_img = Image.open(metallic_file).convert("L")
                if metallic_img.size != target_size:
                    metallic_img = metallic_img.resize(target_size, Image.Resampling.LANCZOS)
            elif self.fill_missing_maps.get():
                metallic_img = Image.new("L", target_size, 0)  # Schwarz = nicht-metallisch
                self.log(f"INFO {base_name}: Metallic fehlt - verwende Schwarz (0)")
            else:
                raise Exception("Metallic-Map fehlt")
            
            orm_map = Image.merge("RGB", (ao_img, roughness_img, metallic_img))
            
            os.makedirs(output_dir, exist_ok=True)
            orm_map.save(output_file, "PNG")
            
            self.log(f"ERFOLG: {base_name}")
            return True
            
        except Exception as e:
            self.log(f"FEHLER {base_name}: {str(e)}")
            return False
    
    def generate_gltf(self):
        """Generiert GLTF-Dateien mit allen PBR-Texturen"""
        if not self.texture_list:
            messagebox.showwarning("Warnung", "Bitte zuerst Texturen laden!")
            return
        
        if not self.input_dir.get():
            messagebox.showerror("Fehler", "Bitte Eingabe-Verzeichnis auswählen!")
            return
        
        thread = threading.Thread(target=self._generate_gltf_thread)
        thread.daemon = True
        thread.start()
    
    def _generate_gltf_thread(self):
        """Thread-Funktion für GLTF-Generierung"""
        try:
            import json
            
            self.status.set("Generiere GLTF-Dateien...")
            self.progress.set(0)
            
            generated = 0
            errors = 0
            
            for i, texture_info in enumerate(self.texture_list):
                base_name = texture_info['base_name']
                texture_dir = texture_info['dir']
                
                progress_percent = (i / len(self.texture_list)) * 100
                self.progress.set(progress_percent)
                self.status.set(f"GLTF: {base_name}")
                
                try:
                    # Finde alle vorhandenen Texturen
                    albedo_file = texture_info['albedo_file']
                    normal_file = self.find_texture_file_with_ogl(texture_dir, base_name, [
                        "normal", "Normal", "NORMAL",
                        "NormalGL", "NormalDX",  # AmbientCG
                        "nor_gl", "nor_dx",  # Polyhaven
                        "norrmal",  # Tippfehler
                        "norm", "Norm",
                        "NRM", "Nrm", "nrm",  # CGBookcase, Poliigon
                        "nor", "Nor", "NOR"  # FreePBR
                    ])
                    emission_file = self.find_texture_file(texture_dir, base_name, [
                        "emission", "Emission", "EMISSION",
                        "emissive", "Emissive", "EMISSIVE",
                        "emiss", "Emiss",
                        "glow", "Glow", "GLOW"
                    ])
                    
                    # Prüfe ob ORM Map bereits existiert
                    output_dir = self.output_dir.get() or texture_dir
                    orm_file = os.path.join(output_dir, f"{base_name}_ORM.png")
                    
                    # Falls ORM nicht existiert und fill_missing_maps aktiv ist, erstelle sie
                    if not os.path.exists(orm_file) and self.fill_missing_maps.get():
                        self.log(f"GLTF: Erstelle fehlende ORM-Map für {base_name}")
                        success = self.create_single_orm_map(texture_dir, output_dir, base_name)
                        if not success:
                            self.log(f"WARNUNG: ORM-Erstellung fehlgeschlagen für {base_name}")
                            orm_file = None
                    elif not os.path.exists(orm_file):
                        self.log(f"WARNUNG: ORM fehlt für {base_name} (automatisches Auffüllen deaktiviert)")
                        orm_file = None
                    
                    # Erstelle Texture-Dictionary mit relativen Pfaden
                    gltf_textures = {}
                    
                    if albedo_file and os.path.exists(albedo_file):
                        rel_path = os.path.relpath(albedo_file, texture_dir)
                        gltf_textures['baseColor'] = f"./{rel_path.replace(os.sep, '/')}"
                    
                    if normal_file and os.path.exists(normal_file):
                        rel_path = os.path.relpath(normal_file, texture_dir)
                        gltf_textures['normal'] = f"./{rel_path.replace(os.sep, '/')}"
                    
                    if orm_file and os.path.exists(orm_file):
                        rel_path = os.path.relpath(orm_file, texture_dir)
                        gltf_textures['orm'] = f"./{rel_path.replace(os.sep, '/')}"
                    
                    if emission_file and os.path.exists(emission_file):
                        rel_path = os.path.relpath(emission_file, texture_dir)
                        gltf_textures['emission'] = f"./{rel_path.replace(os.sep, '/')}"
                    
                    # Erstelle GLTF JSON
                    gltf_data = self._create_gltf_structure(base_name, gltf_textures)
                    
                    # Speichere GLTF-Datei
                    gltf_file = os.path.join(texture_dir, f"{base_name}.gltf")
                    with open(gltf_file, 'w') as f:
                        json.dump(gltf_data, f, indent=2)
                    
                    self.log(f"GLTF: {base_name}.gltf")
                    generated += 1
                    
                except Exception as e:
                    self.log(f"FEHLER GLTF {base_name}: {str(e)}")
                    errors += 1
            
            self.progress.set(100)
            self.status.set("GLTF-Generierung abgeschlossen!")
            self.log("=" * 50)
            self.log(f"GLTF: {generated} erstellt, {errors} Fehler")
            
            messagebox.showinfo("Fertig", f"GLTF-Generierung abgeschlossen!\nErstellt: {generated}\nFehler: {errors}")
            
        except Exception as e:
            self.log(f"FEHLER: {str(e)}")
            self.status.set("Fehler bei GLTF-Generierung")
            messagebox.showerror("Fehler", f"GLTF-Generierung fehlgeschlagen:\n{str(e)}")
    
    def _create_gltf_structure(self, material_name, textures):
        """Erstellt GLTF 2.0 JSON-Struktur - kompatibel mit SecondLife/OpenSim"""
        gltf = {
            "asset": {
                "generator": "ORM-Maps-Viewer Python",
                "version": "2.0"
            },
            "scene": 0,
            "scenes": [{"nodes": [0]}],
            "nodes": [{"mesh": 0}],
            "meshes": [{
                "primitives": [{
                    "attributes": {
                        "POSITION": 1,
                        "TEXCOORD_0": 2
                    },
                    "indices": 0,
                    "material": 0
                }]
            }],
            "materials": [{
                "doubleSided": False,
                "name": material_name,
                "pbrMetallicRoughness": {
                    "metallicFactor": 1.0,
                    "roughnessFactor": 1.0
                },
                "alphaMode": "opaque"
            }],
            "textures": [],
            "images": [],
            "samplers": [{
                "magFilter": 9729,
                "minFilter": 9987,
                "wrapS": 33648,
                "wrapT": 33648
            }],
            "buffers": [{
                "uri": "data:application/gltf-buffer;base64,AAABAAIAAQADAAIAAAAAAAAAAAAAAAAAAACAPwAAAAAAAAAAAAAAAAAAgD8AAAAAAACAPwAAgD8AAAAAAAAAAAAAgD8AAAAAAACAPwAAgD8AAAAAAAAAAAAAAAAAAAAAAACAPwAAAAAAAAAA",
                "byteLength": 108
            }],
            "bufferViews": [
                {
                    "buffer": 0,
                    "byteOffset": 0,
                    "byteLength": 12,
                    "target": 34963
                },
                {
                    "buffer": 0,
                    "byteOffset": 12,
                    "byteLength": 96,
                    "byteStride": 12,
                    "target": 34962
                }
            ],
            "accessors": [
                {
                    "bufferView": 0,
                    "byteOffset": 0,
                    "componentType": 5123,
                    "count": 6,
                    "type": "SCALAR",
                    "max": [3],
                    "min": [0]
                },
                {
                    "bufferView": 1,
                    "byteOffset": 0,
                    "componentType": 5126,
                    "count": 4,
                    "type": "VEC3",
                    "max": [1.0, 1.0, 0.0],
                    "min": [0.0, 0.0, 0.0]
                },
                {
                    "bufferView": 1,
                    "byteOffset": 48,
                    "componentType": 5126,
                    "count": 4,
                    "type": "VEC2",
                    "max": [1.0, 1.0],
                    "min": [0.0, 0.0]
                }
            ]
        }
        
        # Füge Texturen in richtiger Reihenfolge hinzu (wie C# Reference)
        image_index = 0
        texture_index = 0
        
        # 1. Normal Map (Index 0)
        if 'normal' in textures:
            gltf['images'].append({
                "mimeType": "image/png",
                "name": f"{material_name}_normal",
                "uri": textures['normal']
            })
            gltf['textures'].append({"source": image_index})
            gltf['materials'][0]['normalTexture'] = {"index": texture_index}
            image_index += 1
            texture_index += 1
        
        # 2. Base Color / Albedo (Index 1)
        if 'baseColor' in textures:
            gltf['images'].append({
                "mimeType": "image/png",
                "name": f"{material_name}_baseColor",
                "uri": textures['baseColor']
            })
            gltf['textures'].append({"source": image_index})
            gltf['materials'][0]['pbrMetallicRoughness']['baseColorTexture'] = {"index": texture_index}
            image_index += 1
            texture_index += 1
        
        # 3. ORM Map (Index 2) - WICHTIG: Wird für metallicRoughness UND occlusion verwendet
        if 'orm' in textures:
            gltf['images'].append({
                "mimeType": "image/png",
                "name": f"{material_name}_orm",
                "uri": textures['orm']
            })
            gltf['textures'].append({"source": image_index})
            
            # ORM Format: R=Occlusion, G=Roughness, B=Metallic
            # MetallicRoughness nutzt G+B Kanäle
            gltf['materials'][0]['pbrMetallicRoughness']['metallicRoughnessTexture'] = {"index": texture_index}
            # Occlusion nutzt R Kanal
            gltf['materials'][0]['occlusionTexture'] = {"index": texture_index}
            image_index += 1
            texture_index += 1
        
        # 4. Emission Map (optional)
        if 'emission' in textures:
            gltf['images'].append({
                "mimeType": "image/png",
                "name": f"{material_name}_emission",
                "uri": textures['emission']
            })
            gltf['textures'].append({"source": image_index})
            gltf['materials'][0]['emissiveTexture'] = {"index": texture_index}
            gltf['materials'][0]['emissiveFactor'] = [1.0, 1.0, 1.0]
        
        return gltf

def main():
    root = tk.Tk()
    ORMGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
