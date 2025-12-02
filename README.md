# ORM-Maps-Viewer - Benutzerhandbuch

## Was ist ORM?

**ORM** steht für **Occlusion, Roughness, Metallic** - ein Standard-Texturformat in der 3D-Grafik und Game-Engine-Entwicklung.

### Die drei Kanäle erklärt

- **🔴 R (Red) = Occlusion (AO - Ambient Occlusion)**
  - Beschreibt, wie viel indirektes Licht eine Oberfläche erhält
  - Dunkle Bereiche = weniger Licht (z.B. Ecken, Ritzen)
  - Helle Bereiche = mehr Licht (offene Flächen)

- **🟢 G (Green) = Roughness (Rauheit)**
  - Bestimmt, wie glatt oder rau eine Oberfläche ist
  - Hell = rau (diffuse Reflexionen, matt)
  - Dunkel = glatt (scharfe Reflexionen, glänzend)

- **🔵 B (Blue) = Metallic (Metallisch)**
  - Definiert, ob eine Oberfläche metallisch ist
  - Weiß = metallisch (Metalle wie Eisen, Gold)
  - Schwarz = nicht-metallisch (Holz, Stoff, Kunststoff)

### Warum ORM?

Game-Engines wie **Unreal Engine**, **Unity** und **Godot** verwenden ORM-Maps, um mehrere Material-Eigenschaften in **einer einzigen Textur** zu speichern:

- ✅ **Speicherplatzersparnis** - 3 Maps in 1 Datei
- ✅ **Bessere Performance** - Weniger Texture-Lookups
- ✅ **Standard-Format** - Kompatibel mit allen modernen Engines

---

## Was kann der ORM-Maps-Viewer?

Der **ORM-Maps-Viewer** ist ein Tool zur **visuellen Überprüfung** und **Qualitätskontrolle** von ORM-Texturen:

### Hauptfunktionen

1. **📁 ORM-Maps laden und anzeigen**
   - Unterstützt PNG, JPG, JPEG, JP2 Formate
   - Zeigt alle drei Kanäle getrennt an

2. **🔍 Einzelkanal-Ansicht**
   - **Rot-Kanal** = Ambient Occlusion
   - **Grün-Kanal** = Roughness
   - **Blau-Kanal** = Metallic
   - **Vollbild** = Kombinierte ORM-Map

3. **✅ Qualitätsprüfung**
   - Überprüfen Sie, ob die Maps korrekt gepackt wurden
   - Identifizieren Sie Fehler oder Artefakte
   - Vergleichen Sie verschiedene ORM-Versionen

4. **💾 Export-Möglichkeiten**
   - Extrahieren Sie einzelne Kanäle als Graustufenbilder
   - Speichern Sie modifizierte ORM-Maps

---

## Anleitung: ORM-Maps-Viewer benutzen

### 1. Programm starten

**Windows:**

```bash
Doppelklick auf: ORM-Maps-Viewer.exe
```

**Python (Entwicklung):**

```bash
python orm-maps-viewer.py
```

### 2. ORM-Textur laden

1. Klicken Sie auf **"ORM-Map laden"**
2. Navigieren Sie zu Ihrer ORM-Textur
3. Wählen Sie die Datei (z.B. `Material_ORM.png`)
4. Klicken Sie auf **"Öffnen"**

### 3. Kanäle anzeigen

Nach dem Laden sehen Sie **4 Vorschau-Bereiche**:

```bash
┌─────────────┬─────────────┐
│ AO (Rot)    │ Roughness   │
│             │ (Grün)      │
├─────────────┼─────────────┤
│ Metallic    │ Vollbild    │
│ (Blau)      │ (ORM)       │
└─────────────┴─────────────┘
```

#### Einzelne Kanäle verstehen

🔴 AO-Kanal (Oben Links)

- Zeigt Schattierungen durch Umgebungsverdeckung
- Dunkle Bereiche = Schatten in Ecken/Ritzen
- Helle Bereiche = offene Flächen

🟢 Roughness-Kanal (Oben Rechts)

- Zeigt Oberflächenrauheit
- Hell = raue, matte Oberfläche
- Dunkel = glatte, glänzende Oberfläche

🔵 Metallic-Kanal (Unten Links)

- Zeigt metallische Bereiche
- Weiß = Metall
- Schwarz = Nicht-Metall

🌈 Vollbild (Unten Rechts)

- Die kombinierte ORM-Map wie sie in der Engine verwendet wird
- Alle Kanäle zusammen in RGB

### 4. Qualitätskontrolle durchführen

Prüfen Sie jeden Kanal auf:

- ✅ **Korrekte Zuordnung** - Sind die richtigen Maps in den richtigen Kanälen?
- ✅ **Keine Artefakte** - Keine unerwünschten Flecken oder Rauschen?
- ✅ **Richtige Helligkeitswerte** - Sind die Bereiche korrekt hell/dunkel?
- ✅ **Konsistenz** - Passen die Kanäle zusammen?

### 5. Einzelne Kanäle exportieren (Optional)

Falls Sie einen Kanal als separate Graustufentextur benötigen:

1. Klicken Sie auf **"Kanal exportieren"**
2. Wählen Sie den gewünschten Kanal (AO, Roughness oder Metallic)
3. Geben Sie einen Dateinamen ein
4. Klicken Sie auf **"Speichern"**

---

## Typische Anwendungsfälle

### 1. Nach ORM-Generierung prüfen

Nach der Erstellung einer ORM-Map mit dem **ORM-Map-Generator**:

```bash
orm-maps-generator.py → Material_ORM.png → orm-maps-viewer.py
```

1. Laden Sie die generierte ORM-Map
2. Prüfen Sie alle drei Kanäle visuell
3. Stellen Sie sicher, dass keine Fehler aufgetreten sind

### 2. Heruntergeladene Assets überprüfen

Bei gekauften oder heruntergeladenen 3D-Assets:

1. Öffnen Sie die mitgelieferte ORM-Map
2. Überprüfen Sie, ob die Kanäle korrekt sind
3. Vergleichen Sie mit den Albedo/Base-Color-Texturen

### 3. Eigene ORM-Maps erstellen

Wenn Sie manuell in Photoshop/GIMP ORM-Maps erstellen:

1. Erstellen Sie RGB-Bild mit 3 Kanälen
2. Laden Sie es im Viewer
3. Prüfen Sie, ob die Zuordnung stimmt:
   - Rot = AO
   - Grün = Roughness
   - Blau = Metallic

### 4. Fehlersuche bei Rendering-Problemen

Wenn Materialien in Ihrer Engine falsch aussehen:

1. Exportieren Sie die ORM-Map aus der Engine
2. Öffnen Sie sie im Viewer
3. Identifizieren Sie den problematischen Kanal
4. Korrigieren Sie die Original-Textur

---

## Tastenkombinationen

| Tastenkombination | Funktion |
|-------------------|----------|
| **Strg + O** | ORM-Map laden |
| **Strg + S** | Kanal exportieren |
| **Strg + R** | Ansicht aktualisieren |
| **Strg + W** | Fenster schließen |
| **F11** | Vollbildmodus |
| **ESC** | Vollbild beenden |

---

## Unterstützte Dateiformate

### Import (Laden)

- ✅ PNG (empfohlen)
- ✅ JPG/JPEG
- ✅ JP2 (JPEG 2000)
- ✅ TGA
- ✅ BMP

### Export (Speichern)

- ✅ PNG (verlustfrei, empfohlen)
- ✅ JPG (mit Qualitätseinstellung)
- ✅ TGA

---

## Technische Details

### Farbkanal-Zuordnung

```bash
ORM-Map (RGB)
├── R (Red)   → AO (Ambient Occlusion)
├── G (Green) → Roughness
└── B (Blue)  → Metallic
```

### Wertebereich

- **0-255** (8-bit pro Kanal)
- **0 = Schwarz** (Minimum)
- **255 = Weiß** (Maximum)

### Empfohlene Auflösungen

- **512x512** - Eco
- **1024x1024** - Standard
- **2048x2048** - High Quality

---

## System-Anforderungen

### Minimum

- Windows 10 oder höher
- 2 GB RAM
- Bildschirmauflösung: 1280x720

### Empfohlen

- Windows 11
- 4 GB RAM oder mehr
- Bildschirmauflösung: 1920x1080 oder höher

---

Viel Erfolg mit Ihren PBR-Materialien! 🎨✨
