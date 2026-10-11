<p align="center">
  <img src="../micro3d/branding/micro3D-logo.svg" alt="µ3D™ Logo" width="106" height="120">
</p>

<h1 align="center">µ3D™</h1>

<p align="center">
  <a href="https://microgulp.dev/de/ready/">
    <img src="../micro3d/branding/microgulp-ready.png" alt="µGulp Ready" width="110">
  </a>
</p>

Eigenständiger Blender-Fork mit einer klaren, objektorientierten Bedienung. Technischer Name und Executables: `micro3D`; Anzeigename: **µ3D™**. Ein eigenständiges Projekt auf Blender-Basis, kein offizielles Produkt und kein offizieller Spiegel der Blender Foundation.

## Stand

Entwicklungsstand vom 11.10.2026: Windows x64 ist lokal gebaut und technisch geprüft. Oberfläche und Mausnavigation werden weiter überarbeitet; die gestalterische Abnahme ist noch offen. Hier wird noch kein fertiger Binärdownload angeboten.

Basis: Blender **5.3.0 Beta**, Commit `a6f145b151fa8562a478ed2c381ab945e7bcac72`. Der Entwicklungszweig `micro3d` enthält die angewendete Patchserie. Der Lock bleibt `bootstrap`: Linux und macOS sind nicht getestet, Signierung und bitidentische Reproduktion sind nicht nachgewiesen. Ein Upstream-Upgrade erfolgt ausdrücklich, nicht automatisch.

`.blend` bleibt das native Lese- und Schreibformat. Blender-Datenmodell, Python/bpy und Add-on-Schnittstellen bleiben Grundlage; Kompatibilität wird anhand konkreter Tests geprüft.

## Einstieg und Repository-Struktur

Der Repository-Stamm enthält den Blender-Quellbaum. Unsere Steuerdateien, UI-Module, Patches und Dokumentation liegen unter [`micro3d/`](../micro3d/). Befehle für das separate lokale Steuerprojekt sind nicht automatisch Befehle für den Repository-Stamm dieses Forks.

1. [Hinweise zum Fork und zur Patchserie](../micro3d/README.md) lesen.
2. Mit Python 3.11+ vom Repository-Stamm `python micro3d/tools/patches.py verify` ausführen.
3. [Build-Plan](../micro3d/docs/BUILD.md), [Architektur](../micro3d/docs/ARCHITECTURE.md) und [Bedienung](../micro3d/docs/CONTROLS.md) beachten. Der Build-Plan enthält auch frühe Gerüsthinweise; diese sind kein aktueller Abnahmenachweis.

Die Patchserie nicht noch einmal auf den bereits gepatchten Entwicklungszweig anwenden. Für eine Rekonstruktion einen separaten sauberen Checkout des Pins verwenden und die Steuerdateien separat bereithalten. Der Fork allein enthält nicht sämtliche externen Build-Abhängigkeiten.

**Git LFS:** Historische Upstream-Dateien können LFS-Zeiger enthalten. Für den initialen GitHub-Clone gegebenenfalls `GIT_LFS_SKIP_SMUDGE=1` setzen; das überspringt nur den Download und ersetzt keine benötigten Build-Dateien. Erforderliche Inhalte aus dem offiziellen Blender-Ursprung anhand der gelockten IDs beziehen und prüfen. Fehlende LFS-Inhalte nicht als vollständigen Checkout behandeln.

## Entwicklungsziele

Phase 1: eigener nativer Build, Produktidentität, isolierte Konfiguration, Patchpipeline, verständliches UI-Grundlayout und Mausnavigation. Später: gemeinsame JS/TS-Automations-API, MCP-Anbindung, eigenes µGulp-npm-Modul und microCSS-Integration. Zusätzliche Importer und Sequenz-/Sprite-Export sind spätere Ausbaustufen, keine bereits verfügbaren Funktionen.

**µGulp Ready:** Das Badge gilt für die Entwicklungs-Tasks des lokalen Steuerprojekts. Dessen Projektprüfung meldet Fortschritt über `gulp-mu-gulp-api` und ist auch per CLI ausführbar. Es bezeichnet keine bereits verfügbare Runtime-Anbindung des Editors und kein veröffentlichtes µ3D-npm-Paket. Die Fork-Quellen sind unter `micro3d/` angeordnet; Einrichtung und Prüfung des vollständigen lokalen Steuerprojekts sind von einem reinen Quellclone zu unterscheiden.

## Herkunft und Lizenz

Offizieller Blender-Ursprung: https://projects.blender.org/blender/blender.git. Die GitHub-Fork-Beziehung zu `blender/blender` dokumentiert die Herkunft.

Neue eigene Projektdateien stehen unter GPL-3.0-or-later, soweit ihre Herkunftshinweise nichts anderes festlegen. Fremde Bestandteile behalten ihre Lizenz- und Urheberhinweise. Siehe [Blender-Lizenzinformationen](../COPYING), [Autoren](../AUTHORS) und [Lizenz des Steuerprojekts](../micro3d/LICENSE). Die bisherige [Upstream-README](../README.upstream.md) bleibt als Herkunftsdokument erhalten.
