# Reproduzierbarer Fork- und Build-Plan

Stand: 11.10.2026. Source-Pin verifiziert; Build noch nicht ausgeführt. Die lokale Erstellungsumgebung hatte Git, aber Python/CMake waren nicht regulär im PATH; Tests des Gerüsts nutzen das gebündelte Python. Visual-Studio-/SDK-Verfügbarkeit wurde noch nicht ermittelt.

## 1. Source und Patchserie

`python tools/patches.py verify` prüft Manifest, Source-Pin, Patchreihenfolge und Hashes. `python tools/patches.py clone` klont in das zuvor nicht vorhandene `vendor/blender` und checkt genau den Commit aus. Ein vorhandenes Ziel wird niemals überschrieben. Submodule/Bibliotheken werden dabei noch nicht geladen. `python tools/patches.py apply --source vendor/blender` wendet die geprüfte Serie auf einen sauberen Checkout des Pins an.

Bei einem abgebrochenen Clone den Teilbaum erst untersuchen; das Werkzeug löscht ihn nicht automatisch. Für einen neuen Versuch kann er bewusst archiviert und ein neues Ziel angelegt werden.

## 2. Einmalige kontrollierte Auflösung der Build-Eingaben

Zuerst die mit dem Pin ausgelieferten CMake-Dateien, `.gitmodules`, `build_files/utils/make_update.py`, Plattformskripte und `make help` lesen. Die aktuellen Webseiten beziehen sich häufig auf main, nicht genau auf 5.3. Ihre Compilerangaben sind Orientierung, die gelockten Source-Anforderungen haben Vorrang.

Auf einem sauberen, separaten Baseline-Checkout die Upstream-Dependency-Aktualisierung verwenden. Vorher prüfen, ob der gepinnte Updater einen Modus ohne Source-Update anbietet. Danach muss HEAD unverändert dem Pin entsprechen; andernfalls abbrechen, nicht mit verschobener Source weiterbauen. Niemals ein uneingeschränktes `make update` im bereits gepatchten Release-Baum ausführen.

Je Ziel in `upstream/platforms/<target>.json` erfassen:

- vollständige Source-/Submodul-/Library-Repository-URLs und Commit-IDs, jeweils Checkout-Pfad;
- Git-LFS-OIDs bzw. SHA-256 von Archiven, Bezugsadresse und erforderliche Bibliothekspfade;
- OS-/Runner-Image-Version oder Container-Digest, CPU-Architektur;
- Compiler, Linker, SDK, Python, CMake, Generator und Packaging-Werkzeuge mit exakten Versionen;
- vollständige Configure-/Build-/Install-Befehle, CMake-Cache-Optionen, Buildtyp und relevante Umgebungsvariablen;
- Upstream-Commit-Zeit als SOURCE_DATE_EPOCH, Pfadnormalisierung und Versionsmetadatenstrategie;
- Testbefehle und Artefakt-Prüfsummen, ohne Zugangsdaten oder private absolute Benutzerpfade.

Diese Dateien mit SHA-256 in `lock.json.platformLocks` registrieren. Beim Replay ausschließlich diese Inhalte auschecken/laden, Hashes und LFS-Verfügbarkeit prüfen. Kein Netzwerk-Update auf Branch-HEAD. Für Release-Status muss Cursor den Plattform-Lock-Replay und die Vollständigkeitsprüfung implementieren; das gelieferte Werkzeug verwaltet zunächst Source und Patches.

## 3. Plattform-Builds

Windows x64: Visual Studio 2022 mit Desktop-C++-Workload, passendem Windows SDK, CMake, Git und Git LFS. Die aktuelle allgemeine Blender-Doku nennt VS 17.14.14 als x64-Minimum; das am Pin gegenprüfen. Upstream `make.bat` aus einer passenden Entwicklerumgebung verwenden oder CMake direkt konfigurieren. INSTALL-Target bauen, sonst können DLLs/Ressourcen fehlen. Ziel ist ein vollständiges portables Verzeichnis mit `micro3D.exe`, nicht nur eine kopierte EXE.

Linux x64: passender GCC/Clang, CMake, Make/Ninja, Git LFS und X11/Wayland-Entwicklungsabhängigkeiten. Aktuelle Doku empfiehlt vorkompilierte Bibliotheken; Runtime-glibc-Basis explizit wählen und testen. Die Doku nennt aktuell GCC 14 als Minimum. Keine Systembibliotheken unbemerkt in einen vermeintlich gepinnten Build mischen.

macOS arm64: vollständiges Xcode samt Metal-Werkzeugen, SDK, CMake und Git LFS. Die einfache Build-Seite erwähnt auch Command Line Tools, die Dependency-Doku weist auf Metal-Werkzeuge aus vollem Xcode hin; daher vollständiges Xcode als Planungsbasis. Blender 5.3 setzt laut Kompatibilitätshinweisen macOS 13+ voraus. Deployment-Target im Lock erfassen. App-Bundle mit eigenen Ressourcen, korrekten Bibliothekspfaden und Plist erzeugen. Signierung/Notarisierung ist ein separater Release-Schritt mit eigenen Berechtigungen.

## 4. Konkretes CMake-Muster

Die folgenden Befehle sind Muster nach erfolgreicher Dependency-Auflösung, keine hier verifizierten Build-Befehle. Generator und CMake-Optionen am Pin prüfen. Source-/Build-/Install-Verzeichnisse getrennt halten.

```text
cmake -S vendor/blender -B build/host -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=<absoluter-dist-Pfad>
cmake --build build/host --config Release --parallel <RAM-gerechte-Anzahl>
cmake --install build/host --config Release
```

Windows alternativ das vom Generator bereitgestellte INSTALL-Target über `cmake --build build/host --target INSTALL --config Release`. Erst Baseline, dann Branding, dann Layout testen. CPU-Rendering muss funktionieren; CUDA/OptiX/HIP/oneAPI erst mit explizit gelockten SDKs aktivieren. Lite-/Headless-Build allein erfüllt den GUI-Abnahmetest nicht.

## 5. Wiederholung und Distribution

Zwei frische Checkouts mit demselben Lock bauen. Source-, Patch-, Dependency- und Cache-Eingaben vergleichen. Funktionsgleiche Reproduktion und Bitidentität getrennt ausweisen. Zeitstempel, Buildpfade und Signaturen können Bytes verändern; keinen bitreproduzierbaren Build behaupten, bevor die Hashes tatsächlich verglichen wurden.

Release-Paket: native Anwendung, Ressourcen, Lizenztexte, Drittanbieterhinweise, Build-Info, Prüfsummen und passender vollständiger Quellstand einschließlich Patches/Buildskripten. Nur freigegebene eigene Produktlogos verwenden. Installationspakete dürfen bestehende Blender-Zuordnungen und Benutzerdaten nicht ungefragt übernehmen. Erst portable Pakete, danach Installer.

CI-Plan: leichte Patch-/Schema-Prüfungen pro Änderung, native Builds je primärem OS auf explizit versionierten Runnern, GPU-/GUI-Smoke auf realen Maschinen; Signierung separat. Keine fiktiv grüne CI-Datei vor vorhandenen Dependency-Locks.
