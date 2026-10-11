# Bedienung

µ3D startet mit einem eigenen Navigationspreset. Die mitgelieferte Blender-Tastaturbelegung bleibt im Menü µ3D und in den Add-on-Einstellungen auswählbar. Der Wechsel speichert die Einstellung im µ3D-Profil und bleibt nach einem Neustart erhalten. Ein erneutes Laden des Add-ons registriert die Fallback-Geste nicht doppelt.

## Ansicht

| Aktion | Geste |
| --- | --- |
| Auswählen | Linksklick |
| Zur Auswahl hinzufügen oder daraus entfernen | Umschalt + Linksklick |
| Ansicht drehen | Alt + Linksklick ziehen |
| Ansicht verschieben | Alt + mittlere Maustaste, ersatzweise Strg + Alt + Linksklick |
| Zoom | Mausrad oder Alt + Rechtsklick ziehen |
| Auswahl einrahmen | Taste F oder der Befehl „Frame selection“ |
| Perspektive und Orthografie | Nummernblock 5 oder der Befehl „Perspective / Orthographic“ |

Die Ersatzgeste für das Verschieben der Ansicht braucht keine mittlere Maustaste. Trackpad-Gesten sind in der Tastaturbelegung vorhanden und auf diesem Rechner nicht mit einem Trackpad geprüft. Objekte lassen sich auch per Klick-Ziehen verschieben, sobald das Werkzeug „Move“ aktiv ist.

## Werkzeuge und Komponenten

Die häufigen Werkzeuge stehen beschriftet im Menü µ3D des 3D-Ansichtskopfes und in der Seitenleiste µ3D. Dieselben Werkzeuge sind zusätzlich über Tasten erreichbar:

| Aktion | Taste |
| --- | --- |
| Rahmenauswahl | Q |
| Verschieben | W |
| Drehen | E |
| Skalieren | R |

Während Verschieben, Drehen oder Skalieren akzeptiert die Eingabe eine Zahl. X, Y oder Z beschränken die Aktion auf eine Achse. Die Seitenleiste zeigt Ort, Drehung und Skalierung des aktiven Objekts als Zahlenfelder. Diese Felder schreiben die normalen Objekteigenschaften und erzeugen Undo-Schritte.

Komponentenmodus und Objektmodus sind beschriftete Befehle. Bei einem Mesh wechseln die Befehle „Points“, „Edges“ und „Faces“ die Komponente; die Tasten 1, 2 und 3 tun dasselbe. Andere Objekttypen ohne Komponentenmodus melden das, statt still eine falsche Bearbeitung zu starten.

## Objektmanager und Layout

Der Objektmanager zeigt die View Layer. Ein Parent ist die Hierarchie unter einem Objekt. Eine Collection ist ein eigener Eintrag und kein Parent. Der Befehl „Parent to active object“ setzt den Parent. Der Befehl „New collection for selection“ legt eine Collection an und ändert den Parent nicht.

Drei getrennte Schalter unterscheiden die Sichtbarkeit: vorübergehend in der Ansicht ausblenden, in Ansichtsfenstern deaktivieren und vom Rendern ausschließen. Die Auswahl im Objektmanager folgt der Auswahl in der Ansicht.

„Restore µ3D layout“ stellt Viewport, Objektmanager, Attribute und Zeitleiste wieder her. Der Befehl ändert keine Szenenobjekte und setzt die übrigen Einstellungen nicht zurück. Eine gespeicherte .blend-Datei behält ihr Layout, solange die Ladeoption die Oberfläche mitlädt. Das Produktlayout wird nicht bei jedem Öffnen erzwungen.

Neue Profile erhalten das µ3D-App-Template, das Add-on und das Navigationspreset. Die Modifikatortasten werden über den plattformabhängigen Teil der Tastaturbelegung abgebildet. Auf diesem Windows-Stand ist Strg die getestete Modifikatortaste.
