# ORM-Maps-Tools - PBR Material für Second Life & OpenSim

## Was ist das?

**ORM-Maps-Tools** ist ein einfaches Werkzeug, um PBR-Materialien (Physically Based Rendering) für **Second Life** und **OpenSim** zu erstellen.

Im Gegensatz zu anderen PBR-GLTF-Packern können die ORM-Tools **ganze Verzeichnisse** auf einmal verarbeiten und in Second Life/OpenSim-kompatible PBR-Materialien umwandeln.

## Was macht das Programm?

- ✅ **Keine Veränderung** bestehender Texturen
- ✅ **Automatische Erkennung** aller PBR-Textur-Maps
- ✅ **Erstellt ORM-Maps** (Occlusion + Roughness + Metallic kombiniert)
- ✅ **Generiert GLTF-Dateien** für Second Life/OpenSim Upload
- ✅ **Batch-Verarbeitung** für hunderte Materialien gleichzeitig
- ✅ **Material-Vorschau** mit allen PBR-Bestandteilen

---

## Für absolute Anfänger

### Was ist PBR?

**PBR** steht für "Physically Based Rendering" - eine moderne Technik, um Materialien in 3D-Welten realistisch darzustellen.

Ein komplettes PBR-Material besteht aus mehreren **Textur-Maps**:

| Map | Beschreibung | Beispiel-Dateiname |
|-----|--------------|-------------------|
| **Albedo/Base Color** | Grundfarbe ohne Schatten | `wood_albedo.png` |
| **Normal** | Oberflächenstruktur (Rillen, Beulen) | `wood_normal.png` |
| **Roughness** | Rauheit (matt oder glänzend) | `wood_roughness.png` |
| **Metallic** | Metallisch (ja/nein) | `wood_metallic.png` |
| **AO (Ambient Occlusion)** | Schatten in Vertiefungen | `wood_ao.png` |
| **Emission** _(optional)_ | Selbstleuchtende Bereiche | `wood_emission.png` |

### Was ist eine ORM-Map?

**ORM** kombiniert drei Maps in **eine** Datei:

- **R-Kanal** (Rot) = Ambient Occlusion
- **G-Kanal** (Grün) = Roughness
- **B-Kanal** (Blau) = Metallic

Second Life und OpenSim benötigen diese kombinierte ORM-Datei zum Upload.

### Was ist eine GLTF-Datei?

Eine **GLTF-Datei** ist eine JSON-Datei, die Second Life/OpenSim sagt:

- Welche Texturen verwendet werden
- Wo diese Texturen liegen
- Wie das Material aussehen soll

**Ohne GLTF-Datei** kann Second Life/OpenSim die PBR-Maps nicht hochladen!

---

## Installation

### Voraussetzungen

- **Windows** 10/11
- **Python 3.13** oder neuer

### Python installieren (falls nicht vorhanden)

1. Download von [python.org](https://www.python.org/downloads/)
2. Installer starten
3. ✅ **Wichtig:** Häkchen bei "Add Python to PATH" setzen
4. "Install Now" klicken

### Programm starten

1. Datei `orm-maps-viewer008.py` öffnen (oder neueste Version)
2. Doppelklick auf die Datei **ODER**
3. Rechtsklick → "Öffnen mit" → "Python"

**Alternativ über Kommandozeile:**

```powershell
python orm-maps-viewer008.py
```

---

## Schritt-für-Schritt Anleitung

### Schritt 1: PBR-Texturen besorgen

**Wo bekomme ich PBR-Materialien?**

Kostenlose Quellen:

- [polyhaven.com](https://polyhaven.com/textures) - Kostenlos & hochqualitativ
- [ambientcg.com](https://ambientcg.com) - CC0 Lizenz (gemeinfrei)
- [freepbr.com](https://freepbr.com) - Große Sammlung
- [3dtextures.me](https://3dtextures.me) - Viele Varianten

**Beispiel-Download:**

1. Gehe zu polyhaven.com
2. Suche z.B. "brick wall"
3. Wähle Auflösung (z.B. 2K)
4. Download "All Maps" → ZIP-Datei
5. Entpacke die ZIP in einen Ordner

**Wichtig:** Die Dateien sollten ähnliche Namen haben:

```bash
brick_wall_albedo.png
brick_wall_normal.png
brick_wall_roughness.png
brick_wall_metallic.png
brick_wall_ao.png
```

### Schritt 2: Programm öffnen

Starte `orm-maps-viewer008.py` (siehe Installation oben)

### Schritt 3: Texturen laden

1. **"Eingabe-Verzeichnis"** auswählen
   - Klicke auf "Durchsuchen"
   - Wähle den Ordner mit deinen PBR-Texturen
   - Beispiel: `G:\Texturen\Brick_Wall`

2. **"Ausgabe-Verzeichnis"** auswählen (optional)
   - Standardmäßig wird `ORM_Maps` im gleichen Ordner erstellt
   - Du kannst es ändern, wenn du willst

3. **Klicke "Texturen laden"**
   - Das Programm sucht automatisch alle PBR-Maps
   - Du siehst die Anzahl gefundener Materialien

### Schritt 4: Material-Vorschau prüfen

**Vorschau-Bereiche:**

- **Zeile 1:** Ambient Occlusion | Roughness | Metallic
- **Zeile 2:** Emission Map | ORM Map (kombiniert)
- **Zeile 3:** Normal Map | Albedo/Base Color | Alle Bestandteile

**Navigation:**

- `◄ Zurück` / `Vor ►` - Zwischen Materialien wechseln
- Die Vorschau zeigt, wie das Material aussehen wird

### Schritt 5: ORM-Maps generieren

1. **Klicke "ORM generieren"**
   - Das Programm kombiniert AO + Roughness + Metallic
   - Erstellt `material_ORM.png` Dateien
   - Zeigt Fortschritt im Log

**Was passiert:**

```bash
✅ brick_wall_ORM.png erstellt in ORM_Maps/
✅ wood_floor_ORM.png erstellt in ORM_Maps/
✅ metal_plate_ORM.png erstellt in ORM_Maps/
```

### Schritt 6: GLTF-Dateien generieren

1. **Klicke "GLTF generieren"**
   - Das Programm erstellt `.gltf` Dateien
   - Referenziert alle vorhandenen Texturen
   - Kein Kopieren, nur Verlinkung!

**Was passiert:**

```bash
✅ brick_wall.gltf erstellt
✅ wood_floor.gltf erstellt
✅ metal_plate.gltf erstellt
```

### Schritt 7: Upload in Second Life / OpenSim

**Wichtig:** Du musst die GLTF-Datei **UND** alle Texturen hochladen!

#### Variante A: Einzelnes Material hochladen

1. Öffne Second Life Viewer (Firestorm empfohlen)
2. **Inventory** → Rechtsklick → "Upload" → "Material"
3. Wähle die `.gltf` Datei (z.B. `brick_wall.gltf`)
4. Second Life lädt automatisch alle referenzierten Texturen

#### Variante B: Bulk Upload (mehrere Materialien)

1. Markiere alle `.gltf` Dateien in einem Ordner
2. Ziehe sie gleichzeitig ins Second Life Fenster
3. Alle Materialien werden hochgeladen

**Kosten:**

- Pro Textur: 10 L$
- GLTF-Datei: 10 L$
- Beispiel: 1 Material mit 4 Texturen = 50 L$

---

## Häufige Probleme & Lösungen

### Problem: "Keine Texturen gefunden"

**Ursache:** Dateinamen stimmen nicht überein

**Lösung:**

- Prüfe, ob die Dateien konsistente Namen haben
- Alle Maps müssen den gleichen **Base-Namen** haben
- Beispiel OK: `wood_albedo.png`, `wood_normal.png`
- Beispiel FEHLER: `wood_color.png`, `plank_normal.png`

### Problem: "GLTF ungültig" beim Upload

**Ursache:** Texturen fehlen oder Pfade stimmen nicht

**Lösung:**

1. Öffne die `.gltf` Datei mit einem Texteditor
2. Prüfe die `"uri"` Einträge
3. Stelle sicher, alle Texturen liegen am richtigen Ort
4. GLTF und Texturen müssen im **gleichen Ordner** sein

### Problem: "AO fehlt" oder "Roughness fehlt"

**Ursache:** Nicht alle Maps vorhanden

**Lösung:**

- ORM-Maps benötigen **alle drei**: AO, Roughness, Metallic
- Option: "Height für AO verwenden" aktivieren (nutzt Height-Map als AO)
- Oder: Fehlende Maps manuell aus Base Color generieren (andere Tools)

### Problem: Material sieht in Second Life anders aus

**Ursache:** Second Life rendert anders als Vorschau

**Lösung:**

- Normal Maps: Stelle sicher, es ist **OpenGL-Format** (nicht DirectX)
- Dateiname mit `-ogl` Suffix (z.B. `wood_normal-ogl.png`)
- Helligkeit/Kontrast der Maps anpassen
- In Second Life: Material-Editor öffnen und Werte tweaken

---

## Tipps für beste Ergebnisse

### 1. Konsistente Dateinamen

✅ **GUT:**

```bash
leather_albedo.png
leather_normal.png
leather_roughness.png
leather_metallic.png
leather_ao.png
```

❌ **SCHLECHT:**

```bash
leather_color.png
Leather-Normal-Map.png
leather_rough.jpg
metal.png
```

### 2. Gleiche Auflösungen

- Alle Maps sollten die **gleiche Größe** haben
- Empfohlen: 1024×1024 oder 2048×2048
- Second Life Maximum: 1024×1024 (höhere Auflösungen werden runterskaliert)

### 3. Speicherplatz sparen

Second Life Limits:

- Inventory Speicher ist begrenzt
- Pro Textur Upload-Gebühr (10 L$)

**Tipp:** Nutze 1024×1024 statt 4K für Second Life Upload

### 4. Material-Presets

Typische Werte für verschiedene Materialien:

| Material | Roughness | Metallic | AO |
|----------|-----------|----------|-----|
| Poliertes Metall | 0.1 - 0.3 | 1.0 | 0.8 - 1.0 |
| Raues Holz | 0.7 - 0.9 | 0.0 | 0.5 - 0.8 |
| Matte Plastik | 0.4 - 0.6 | 0.0 | 0.7 - 1.0 |
| Stein/Beton | 0.6 - 0.8 | 0.0 | 0.4 - 0.7 |
| Glänzender Lack | 0.1 - 0.2 | 0.0 | 0.8 - 1.0 |

---

## Erweiterte Funktionen

### Height für AO verwenden

- Aktiviere "Height für AO verwenden"
- Nutzt Height-Map (Displacement) als Ambient Occlusion
- Nützlich wenn keine dedizierte AO-Map vorhanden

### Existierende überschreiben

- Aktiviere "Existierende überschreiben"
- Generiert ORM-Maps neu, auch wenn sie schon existieren
- Nützlich nach Änderungen an den Quell-Maps

### Batch-Verarbeitung

**Beispiel:** 100 Materialien auf einmal

- Ordner-Struktur:

```bash
PBR_Textures/
├── Material_001/
│   ├── mat001_albedo.png
│   ├── mat001_normal.png
│   └── ...
├── Material_002/
└── Material_003/
```

- Wähle `PBR_Textures` als Eingabe-Verzeichnis
- Klicke "Texturen laden" (sucht rekursiv)
- Klicke "ORM generieren"
- Klicke "GLTF generieren"
- Fertig! Alle 100 Materialien sind bereit

---

## Unterstützte Dateiformate

### Eingabe-Texturen

- `.png` (empfohlen)
- `.jpg` / `.jpeg`
- `.jp2` (JPEG 2000)

### Ausgabe

- **ORM-Maps:** `.png` (unkomprimiert)
- **GLTF:** `.gltf` (JSON-Text, lesbar)

---

## Unterstützte Namenskonventionen

Das Programm erkennt viele Varianten automatisch:

### Albedo / Base Color

`_albedo`, `_alb`, `_base`, `_basecolor`, `_color`, `_col`, `_diffuse`, `_diff`

### Normal Map

`_normal`, `_nrm`, `_norm`, `_normalmap`, `_normal-ogl`

### Roughness

`_roughness`, `_rough`, `_rgh`

### Metallic

`_metallic`, `_metal`, `_mtl`

### Ambient Occlusion

`_ao`, `_ambient`, `_occlusion`, `_ambientocclusion`

### Emission (optional)

`_emission`, `_emissive`, `_emiss`, `_glow`

### Height / Displacement (optional)

`_height`, `_disp`, `_displacement`, `_bump`

---

## Workflow-Beispiel von A-Z

### Szenario: Backstein-Wand für Second Life

**Ausgangssituation:** Du hast ein kostenloses PBR-Material von polyhaven.com heruntergeladen.

#### 1. Material herunterladen

- URL: `https://polyhaven.com/a/brick_wall_002`
- Format: 2K PNG
- Download "All Maps"
- Entpacken nach `D:\SecondLife\Textures\Brick_Wall_002\`

#### 2. Dateien prüfen

```bash
D:\SecondLife\Textures\Brick_Wall_002\
├── brick_wall_002_diff_2k.png    (Albedo)
├── brick_wall_002_nor_gl_2k.png  (Normal)
├── brick_wall_002_rough_2k.png   (Roughness)
├── brick_wall_002_ao_2k.png      (AO)
└── brick_wall_002_disp_2k.png    (Height/Displacement)
```

#### 3. Umbenennen (optional, aber empfohlen)

Für Second Life besser 1024×1024:

```bash
brick_wall_albedo.png
brick_wall_normal-ogl.png
brick_wall_roughness.png
brick_wall_ao.png
```

**Tools zum Skalieren:**

- IrfanView (kostenlos)
- GIMP (kostenlos)
- Photoshop

Batch-Resize in IrfanView:

- File → Batch Conversion
- Output Format: PNG
- Advanced: Resize 1024×1024

#### 4. ORM-Maps-Tools starten

```powershell
python orm-maps-viewer008.py
```

#### 5. Texturen laden

- Eingabe-Verzeichnis: `D:\SecondLife\Textures\Brick_Wall_002\`
- Ausgabe-Verzeichnis: (Standard nutzen)
- "Texturen laden" klicken

**Log-Ausgabe:**

```bash
Gefunden: 1 Textur-Sets
```

#### 6. Vorschau prüfen

- Alle Maps werden angezeigt
- "Alle Bestandteile" zeigt kombinierte Vorschau
- Prüfe, ob alles korrekt aussieht

#### 7. ORM generieren

- "ORM generieren" klicken
- Warte auf "Erfolgreich: 1"

**Erstellt:**

```bash
D:\SecondLife\Textures\Brick_Wall_002\ORM_Maps\
└── brick_wall_ORM.png
```

#### 8. GLTF generieren

- "GLTF generieren" klicken
- Warte auf "GLTF: 1 erstellt"

**Erstellt:**

```bash
D:\SecondLife\Textures\Brick_Wall_002\
└── brick_wall.gltf
```

#### 9. Second Life Upload

1. Öffne Firestorm Viewer
2. Login in Second Life
3. Inventory → Rechtsklick → Upload → Material
4. Wähle `brick_wall.gltf`
5. Upload bestätigen (50 L$ = 5 Texturen)
6. Material erscheint im Inventory

#### 10. Material anwenden

1. Erstelle oder wähle ein Objekt (z.B. Cube)
2. Rechtsklick → Edit
3. Texture-Tab → Material-Dropdown
4. Wähle dein hochgeladenes Material
5. Fertig! Die Wand hat jetzt PBR-Rendering

---

## Häufig gestellte Fragen (FAQ)

### Muss ich alle Maps haben?

**Minimum:**

- Albedo/Base Color (Pflicht)
- Normal Map (empfohlen)
- AO + Roughness + Metallic (für ORM-Map)

**Optional:**

- Emission (für leuchtende Bereiche)
- Height (kann als AO verwendet werden)

### Kostet das Upload Geld?

**Ja**, Second Life Upload-Gebühren:

- Pro Textur: 10 L$
- GLTF-Datei: 10 L$
- Beispiel: Material mit Albedo + Normal + ORM = 40 L$

### Kann ich bestehende Texturen neu verpacken?

**Ja!** Das ist der Hauptzweck:

- Vorhandene PBR-Maps aus dem Internet
- Alte Texturen mit neuen Maps ergänzen
- Batch-Konvertierung ganzer Bibliotheken

### Was ist mit Copyright?

**Achtung Copyright!**

- Nur Texturen hochladen, die du verwenden darfst
- CC0 / Public Domain ist sicher
- Commercial Licenses beachten
- Nicht in Second Life hochladen: Copyrighted Texturen ohne Lizenz

**Sichere Quellen:**

- Polyhaven.com (CC0)
- AmbientCG.com (CC0)
- Eigene Fotografien
- Selbst erstellte Texturen

### Funktioniert das auch für OpenSim?

**Ja!** Das GLTF-Format ist kompatibel mit:

- Second Life (offizieller Viewer)
- Firestorm Viewer
- OpenSim Grids
- Andere SL-kompatible Viewer

---

## Support & Feedback

### Bei Problemen

1. **Log prüfen:** Unten im Programm-Fenster
2. **Dateinamen prüfen:** Müssen konsistent sein
3. **Python-Version:** Mindestens 3.13

### Verbesserungsvorschläge

Dieses Tool ist Open Source und kann erweitert werden:

- Automatische Skalierung auf 1024×1024
- Weitere Material-Presets
- Integration mit anderen Viewern
- GUI-Verbesserungen

---

## Zusammenfassung

**In 3 Minuten:**

1. ✅ PBR-Texturen herunterladen (polyhaven.com)
2. ✅ ORM-Maps-Tools starten
3. ✅ "Texturen laden" → Ordner wählen
4. ✅ "ORM generieren" klicken
5. ✅ "GLTF generieren" klicken
6. ✅ In Second Life hochladen

**Fertig!** Deine PBR-Materialien sind upload-bereit.

---

## Glossar

| Begriff | Bedeutung |
|---------|-----------|
| **PBR** | Physically Based Rendering - Realistische Material-Darstellung |
| **ORM** | Occlusion + Roughness + Metallic kombiniert in RGB-Kanälen |
| **GLTF** | Graphics Library Transmission Format - 3D-Szenen & Materialien |
| **Albedo** | Grundfarbe ohne Beleuchtung |
| **Normal Map** | Fake-Geometrie für Oberflächendetails |
| **Roughness** | Rauheit (matt vs. glänzend) |
| **Metallic** | Metallisch (0 = Nicht-Metall, 1 = Metall) |
| **AO** | Ambient Occlusion - Schatten in Ecken/Vertiefungen |
| **Emission** | Selbstleuchtende Bereiche (z.B. Neonlicht) |

---

**Viel Erfolg mit deinen PBR-Materialien in Second Life!** 🎨✨
