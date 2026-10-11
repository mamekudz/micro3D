# Architektur und Phasen

## Entscheidungen

Native Blender-Anwendung, C/C++-Kern, Python/bpy für UI und Erweiterungen. Upstream-Datenmodell, Renderer, Abhängigkeitsgraph und Undo bleiben maßgeblich. Kein zweiter Szenengraph und keine Weboberfläche über dem Viewport. Die langfristige öffentliche Automationsschnittstelle ist JS/TS-first; Blender-Add-ons bleiben Python-basiert.

Blender 5.3 Beta ist nach Rückfrage des Nutzers die Basis. Ein festgeschriebener Release-Branch-Commit begrenzt die beweglichen Eingaben. Der Übergang auf 5.3 final wird als eigener Upstream-Update behandelt. 4.5 war eine verworfene konservative Erstwahl, keine zweite aktiv gepflegte Produktlinie.

## Dateivertrag — verbindlich

`.blend` ist das primäre native Lese- und Schreibformat. Bestehende Blender-Dateien müssen im Rahmen der Kompatibilität der gewählten Blender-Basis geöffnet, bearbeitet und gespeichert werden können. Keine Umbenennung des Formats, keine eigene Pflicht-Endung, keine inkompatible DNA-/RNA-Erweiterung für UI-Komfort. micro3D darf diese Upstream-Kompatibilität nicht zusätzlich einschränken.

Roundtrip: Original-Blender der gelockten Basis erzeugt Datei → µ3D öffnet/ändert/speichert → Original-Blender öffnet erneut. Verglichen werden Szeneninhalte, Verknüpfungen und ausgewertete Ergebnisse, nicht binäre Dateigleichheit. Die Dateien älterer unterstützter Versionen gehören in die Regressionstests. Künftige Blender-Versionen und Speichern zurück in ältere Versionen unterliegen den Upstream-Grenzen; niemals pauschal ewige Vorwärtskompatibilität behaupten.

Produktlayout standardmäßig in eigenen Benutzereinstellungen speichern. Benutzerdefinierte Properties nur optional, dokumentiert und im eigenen Namensraum; Szenen müssen ohne µ3D-Module nutzbar bleiben. Normales Öffnen respektiert gespeicherte Arbeitsbereiche entsprechend dem Benutzerwunsch; ein Layoutwechsel verändert keine Szenendaten.

`.c4d` ist später ein optionales, bestmöglich lesbares Importformat. Schreiben von C4D-Dateien ist ausdrücklich keine Anforderung. Importer müssen Versionen und unterstützte Objektarten nennen und für ausgelassene/approximierte Daten einen Importbericht liefern. Keine Behauptung vollständiger C4D-Kompatibilität. Oxyd und eine Prozessanbindung erfordern einen eigenen Folgeauftrag.

## Phase 1

A. Unveränderten gelockten Upstream auf dem Host bauen und starten; Build-Inputs erfassen.
B. Getrennte Patches für Produktidentität und Konfigurationspfade; Zielprogramme `micro3D.exe`, `micro3D`, `micro3D.app`, sichtbarer Name µ3D. Interne Blender-API-Bezeichner bleiben bestehen. Bundle-ID vor Veröffentlichung mit eigener kontrollierter Namensdomäne festlegen, keine erfundene Unternehmenszugehörigkeit.
C. Startlayout mit zentralem Viewport, Objektmanager rechts oben, Attributen rechts unten, Zeitleiste unten. Zuerst vorhandene Editor-Typen verwenden; neue Editor-Typen erst nach belegter Notwendigkeit.
D. Tests und paketierbarer Build für Windows x64, Linux x64, macOS arm64. Intel-Mac und Windows ARM nur nach gesondertem Nachweis; plattformübergreifend bedeutet nicht automatisch jede CPU.

## Spätere Module

`modules/api/` reserviert einen transportneutralen TS-Vertrag. Eine Python/native Bridge führt validierte Aufträge im Main Thread aus. Stabile IDs, Capability-Abfrage, Versionierung, Undo-Transaktionen, Abbruch, Timeouts und begrenzte Nachrichten sind Pflicht. Kein beliebiges eval, keine automatische Codeausführung beim Öffnen einer Szene. Ein späterer lokaler IPC-Kanal ist standardmäßig deaktiviert, authentifiziert und nicht öffentlich gebunden.

`modules/ugulp/` beschreibt nur den Adaptervertrag. Architektur, Protokoll und Lizenz von µGulp liegen hier noch nicht vor. Keine erfundene Integration, kein offener Port und keine Runtime-Abhängigkeit in Phase 1.

## Grenzen

Kompatibilität mit Add-ons wird gegen die gleiche Basisversion getestet: Register/Unregister, Operatoren, Panels, Modal-Tools, UI-Kontexte und Python-Pakete. Eingriffe in Layout/Keymap können kontextabhängige Add-ons beeinflussen. Benutzer können zur Blender-Keymap und einem Standardlayout wechseln. Vorhandene Blender-Einstellungen werden nicht still importiert.
