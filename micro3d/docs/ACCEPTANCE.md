# Abnahmekriterien und Nachweise

## Gerüst (dieser Auftrag)

Manifest/Lock parsebar; Source-Pin offiziell verifiziert; leere Patchserie ausdrücklich ausgewiesen; Patchwerkzeug mit echten temporären Git-Repositories getestet; eigene SVGs und Herkunftsliste vorhanden. Diese Abnahme ist kein Nachweis eines Blender-Builds.

## Erster lauffähiger Fork (Cursor-Auftrag)

- Unveränderte Baseline und gepatchter Build auf dem Host kompiliert; Start durch tatsächliches Executable, `--version`, Hintergrundlauf und sichtbarer GUI-Start belegt.
- Produktname/Icons eigenständig; eigene Benutzerpfade. Parallelstart mit Original-Blender ohne Profilüberschreibung; zweiter Start erhält Einstellungen.
- Objekt anlegen, auswählen, umbenennen, verschachteln, transformieren und löschen; Objektmanager, Viewport und Attribute synchron; Undo/Redo korrekt.
- Navigation: Orbit/Pan/Zoom, Auswahl rahmen, Perspektive/Orthografie; die mitgelieferte Blender-Keymap bleibt auswählbar. Physische Maus-, Trackpad- und DPI-Prüfungen nur als bestanden werten, wenn sie auf dem jeweiligen Host ausgeführt wurden.
- .blend-Roundtrip von und zurück zu unverändertem Blender derselben Basis; ältere Dateien im Umfang der Upstream-Unterstützung. Testdaten: Mesh/Material, Animation, Modifier, Geometry Nodes, Collections, verlinkte Bibliothek mit Overrides und gepackte Textur. Verglichen werden Objektzahlen, stabile benannte Eigenschaften, Links und ausgewertete Szene/Render. Keine still verlorenen Daten.
- Test-Add-on registrieren/abmelden, Operator und Panel ausführen, Modal-Kontext testen. .blend mit deaktiviertem µ3D-Modul bleibt benutzbar.
- Leere Szene speichern, neu öffnen, CPU-Testrender. Benutzerdefinierte Startup-/Layout-Dateien nur in µ3D-Profil.
- Source-Patches aus sauberem Pin rekonstruierbar; vollständiger Host-Dependency-/Toolchain-Lock und Buildbericht mit Befehlen, Versionen, Hashes, Fehlern und offenen Punkten.

## UI-Kandidat

Belegt am 11.10.2026 mit `dist\windows-ui-candidate\micro3D.exe`: Fensteranzeige µ3D, Splash und About mit dem vorhandenen roten Logo, Lizenz- und Credit-Texte bleiben. Arbeitsablauf über Operatoren: Würfel, Umbenennen, Parent, Collection, Transform, Komponenten, Material, Modifier, zwei Keyframes, Speichern, erneutes Öffnen, CPU-Render. Layout wird beim Öffnen nicht erzwungen und durch den Wiederherstellungsbefehl ohne Objektverlust zurückgesetzt. Navigationspreset wechselt und bleibt über einen Neustart. Roundtrip der unveränderten Baseline meldet `ROUNDTRIP_OK 507`. Add-on, Profiltrennung und CPU-Render erneut `SMOKE_OK`.

Offen: kein physischer Maus- oder Trackpad-Durchlauf, keine gemessene Windows-Skalierung, kein Linux, kein macOS, keine Bitidentität. Der bisherige Stand `dist\windows-x64` und die Baseline bleiben erhalten.

## Plattformfreigabe

Windows x64, Linux x64, macOS arm64 jeweils native GUI-/Datei-/Add-on-Smokes und Clean-Rebuild. Eine erfolgreiche Windows-Kompilierung ist kein Linux-/macOS-Nachweis. Nicht verfügbare Plattformen explizit als ungetestet ausweisen. Retina/HiDPI, Unicode-Pfade, Leerzeichen und eigenes Profil prüfen.

## Späterer C4D-Importer

Kein C4D-Schreiben erforderlich. Import versioniert und best effort: unterstützte Inhalte dokumentieren; unbekannte Tags, Generatoren, Materialien, Animation oder fehlende Plugins im Bericht nennen; Originaldatei nie überschreiben. Nur legal verfügbare Spezifikationen/SDKs und freigegebene Testdateien verwenden. Oxyd und eine Prozessanbindung bleiben separate Folgeaufträge.
