# Arbeitsplatz

µ3D lädt das Add-on `micro3d_layout` und das App-Template `micro3d` mit dem Windows-Build. Die Oberfläche braucht weder Node noch ein Netzwerk.

Der Arbeitsplatz besteht aus dem zentralen 3D-Viewport, dem Objektmanager oben rechts, den Attributen unten rechts und der Zeitleiste unten. Die Bereiche bleiben die vorhandenen Editoren und lassen sich an den Trennlinien verändern. „Restore µ3D layout“ stellt diese Anordnung wieder her, ohne Szenenobjekte zu ändern und ohne die übrigen Einstellungen zurückzusetzen. Eine geöffnete `.blend`-Datei behält ihr gespeichertes Layout.

Der Objektmanager zeigt die View Layer. Parent-Beziehungen stehen unter dem übergeordneten Objekt. Eine Collection ist ein eigener Eintrag. Auswahl im Manager und in der Ansicht bleibt synchron. Umbenennen nutzt den Objektnamen. Drei getrennte Schalter unterscheiden vorübergehendes Ausblenden, Deaktivieren in Ansichtsfenstern und Ausschluss vom Rendern.

Die Seitenleiste µ3D und das Menü µ3D im Ansichtskopf enthalten beschriftete Befehle für Auswahl, Rahmenauswahl, Verschieben, Drehen, Skalieren, Einrahmen, Perspektive/Orthografie, Objekt- und Komponentenmodus sowie Parent und Collection. Die Attributfelder schreiben Ort, Drehung und Skalierung des aktiven Objekts. Mehrfachauswahl, fehlende Auswahl, verlinkte oder überschriebene Daten und gemeinsam genutzte Daten werden dort benannt. Die vorhandenen Eigenschaften für Objekt, Material und Modifier bleiben im Attribut-Editor.

Die Navigation steht in `docs/CONTROLS.md`. Das Preset lässt sich auf die mitgelieferte Blender-Tastaturbelegung zurückschalten. Die Wahl bleibt im µ3D-Profil über einen Neustart erhalten.

Prüfablauf, Screenshots und Grenzen: `docs/UI-REPORT.md`.
