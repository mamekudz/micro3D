# Patchserie

Absichtlich leer: keine erfundenen oder ungeprüften Upstream-Patches. Vorgesehene getrennte Änderungen:

1. `product-identity`: native Executable-/Bundle-Namen, Fenstertitel, Plattformressourcen, eigene Icons.
2. `config-isolation`: eigene Benutzerpfade und sichere Koexistenz mit Blender.
3. `ui-bootstrap`: Installation/Start eigener UI-Module und reproduzierbare Startansicht.

Weitere native Layout-Patches nur nach belegter Grenze der vorhandenen Python-/Editor-APIs. Je Patch ein Eintrag in series.json mit `id`, `file` (relativ zum Projektstamm), `purpose`, `category`, `tests` und `upstreamStrategy`. Dann `python tools/patches.py lock-patches` ausführen und Manifest-/Lock-Diff reviewen.

Beispielwerte: ID `product-identity`, Datei `patches/0001-product-identity.patch`, Kategorie `branding`, Tests `windows-launch,linux-launch,macos-launch`, Strategie `local-only`. Dateien als normale Git-Diffs aus einem sauberen Upstream-Checkout exportieren. Binärpatches sind im ersten Schritt nicht vorgesehen; SVG-Quellen separat halten, Plattformicons deterministisch erzeugen.

`apply` benötigt exakt den gelockten Commit und einen sauberen Git-Baum. Es prüft die gesamte Serie vor der Anwendung. Keine 3-way-/Fuzzy-Merges. Nach Anwendung bleiben die Änderungen zur Prüfung uncommitted. Ein erneuter Aufruf auf diesem Baum muss abbrechen.
