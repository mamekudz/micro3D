# Verbindliche Projektregeln: micro3D / µ3D

Diese Regeln gelten für Menschen, Claude, Cursor und andere Coding-Agenten. Bei Konflikten Aufgabe und Regeln konkret benennen; keine stillen Ausnahmen. Ein erfolgreicher Build darf nicht erfunden werden.

## Produkt und Umfang

1. µ3D ist ein eigenständiger nativer Blender-Fork mit eigenen Executables für Windows, Linux und macOS. Kein bloß umbenannter Download, kein extern gestartetes Original-Blender als Endprodukt.
2. Bedienziel: nachvollziehbare Objekthierarchie, kontextbezogene Attribute und direkt auffindbare Werkzeuge; die Bedienung ist eigenständig und objektzentriert. Keine pixelgenaue Nachbildung fremder Oberflächen und keine kopierten Drittanbieter-Assets, Icons, Texte, Themes, Screenshots, Quellcodes oder Markenaufmachung.
3. Phase 1 enthält Branding, Build/Packaging, Patching und UI-Grundlayout. JS/TS-first API und µGulp bleiben vorbereitete spätere Module. Oxyd, zusätzliche Dateiformat-Importer, externe Programmanbindung und Sprite-Export sind ausdrücklich nicht Teil von Phase 1.

## Architektur

4. Blender bleibt C/C++-Kern mit bestehender Python/bpy-Integration. Keine TS-Neuschreibung des Kerns, kein Electron-Frontend über dem Viewport. JS/TS-first beschreibt später die öffentliche Automations-API, nicht die interne Implementierungssprache.
5. Änderungen zuerst in eigenen Python-UI-Modulen, Keymaps, App-Templates und Build-Overlays prüfen. Native Patches nur für notwendige Produktidentität, Konfigurationsisolation oder belegte UI-Lücken. App-Template allein erfüllt nicht das Fork-Ziel.
6. Keine globale Ersetzung von `Blender`/`blender`. `bpy`, RNA/DNA, Operator-IDs, .blend-Format, Versionsabfragen und Python-Paketnamen bleiben kompatibel. Upstream-Copyrights bleiben erhalten.
7. Objektmanager basiert auf Outliner/Datenmodell; Attribute auf RNA/Properties. Keine zweite Objektwelt. Auswahl, Undo/Redo, Depsgraph und Speichern müssen konsistent bleiben.
8. UI funktioniert ohne Node, Netzwerk oder µGulp. Spätere externe Commands gehen validiert über eine versionierte Bridge auf den Blender-Hauptthread, niemals direkt aus einem Socket-Thread an bpy.
9. Eigene Konfigurations-, Cache- und Extension-Verzeichnisse. Bestehende Blender-Installation nicht überschreiben. Übernahme von Nutzereinstellungen nur ausdrücklich und nachvollziehbar. Stock-Blender-Keymap als Rückfalloption.

## Upstream und Patches

10. Offizieller Ursprung: https://projects.blender.org/blender/blender.git. Source-Basis ausschließlich vollständiger Commit aus `upstream/lock.json`. 5.3 ist zunächst Beta; keine Stabilitätsgarantie.
11. Jede Änderung am Upstream muss als kleiner, thematisch isolierter Patch in `patches/series.json` geführt werden. Pflichtfelder: ID, Datei, Zweck, Kategorie, Tests, Upstream-Strategie. SHA-256 und Reihenfolge werden im Lock geprüft. Keine versteckten lokalen Änderungen.
12. Keine Fuzzy-Anwendung, keine automatische Konfliktauflösung, kein stiller Patch-Refresh. Bei Konflikt abbrechen; neuen Upstream in frischem Arbeitsverzeichnis prüfen. Niemals Nutzeränderungen durch reset/clean löschen.
13. Source-Pin, Patchserie und Build-Inputs gemeinsam reviewen. Dependencies einschließlich Git-LFS-Inhalten, Submodulen, Compiler, SDK, CMake, Build-Flags und Packaging-Werkzeugen je Plattform festschreiben. `make update` gehört nur zur kontrollierten Auflösung, nicht in einen eingefrorenen Release-Build.
14. `bootstrap` ist kein Release-Lock. Erst nach vollständigen Plattform-Locks, erfolgreichem Clean-Rebuild und Abnahmetests auf `ready` wechseln. Bitidentische Reproduzierbarkeit gesondert messen; Signaturen/Notarisierung getrennt betrachten.
15. Allgemeine Fehlerkorrekturen upstream-fähig halten; Branding und Produktlayout lokal halten. Sicherheitsrelevante Upstream-Änderungen priorisieren. Keine automatische Hintergrundaktualisierung im Produkt.

## Lizenz, Herkunft, Recht

16. Neue eigene Code-/Dokumentations-/Platzhalterdateien stehen unter GPL-3.0-or-later. Unveränderte und geänderte Fremddateien behalten ihre Lizenzhinweise. Blender-Binärdistribution nach der offiziellen GPL-3.0-or-later-Vorgabe, Abhängigkeiten separat erfassen.
17. Releases enthalten vollständige Lizenztexte, Notices, Änderungsvermerk, Build-Informationen sowie passenden Corresponding Source einschließlich eigener Patches und benötigter Build-Skripte. Ein Link nur auf Blender-Upstream genügt für unseren geänderten Build nicht.
18. Eigene Icons aus dokumentierten geometrischen Quellen erstellen; keine Extraktion oder Nachzeichnung fremder Icons. `branding/assets.json` pflegen. Blender-Logo nicht als Produktlogo verwenden. Markenhinweise dürfen keine Unterstützung durch andere Hersteller oder die Blender Foundation suggerieren.
19. micro3D/µ3D ist ein Arbeitsname ohne durchgeführte Markenfreigabe. Vor öffentlicher Vermarktung Namens-, Design- und Gesamteindrucksprüfung vorsehen. Keine Aussage rechtlicher Unangreifbarkeit.
20. Prozessgrenzen sind keine automatische GPL-Ausnahme. Lizenzlage der späteren µGulp-Anbindung und etwaiger SDKs vor Distribution prüfen. Keine proprietären Drittanbieter-Bibliotheken oder SDKs ohne gesonderte Rechteprüfung.

## Entwicklung und Abnahme

21. Pro Änderung klarer Zweck, begrenzter Diff, passende Tests und nachvollziehbare Build-Ausgabe. Geheimnisse, Zertifikate und Nutzerszenen nicht einchecken. Keine Paket-/Softwareinstallation ohne die jeweils nötige Berechtigung.
22. Patchwerkzeuge fail-closed: falscher Commit, Hashabweichung, unbekannte Patchdatei, Pfad außerhalb des Repos und schmutziger Source-Baum brechen ab.
23. Windows x64, Linux x64 und macOS arm64 sind primäre Ziele. Andere Architekturen nur mit eigener Upstream-/Dependency-/CI-Prüfung. Keine Intel-macOS-Unterstützung versprechen, wenn sie für den 5.3-Pin nicht nachgewiesen ist.
24. Kompatibilität bedeutet getestete Add-ons für dieselbe Blender-Basisversion. Keine pauschale Zusage für alle Blender-Versionen oder geschlossene Binär-Add-ons.
25. Arbeit erst als abgeschlossen markieren, wenn die jeweiligen Kriterien in `docs/ACCEPTANCE.md` belegt sind. Fehlende Plattformtests, Dependencies oder Toolchains offen dokumentieren.

## Ergänzter verbindlicher Dateivertrag

26. `.blend` bleibt das native Lese- und Schreibformat. Bestehende Blender-Dateien müssen innerhalb der Upstream-Kompatibilität ohne zusätzliche µ3D-Einschränkungen lesbar, editierbar und speicherbar bleiben. Roundtrips mit Original-Blender derselben Basisversion sind Pflicht. Keine Szenendaten zugunsten des UI-Layouts entfernen oder proprietär ersetzen.
27. `.c4d` ist ausschließlich ein späteres optionales Best-effort-Importformat. C4D-Dateien schreiben ist keine Anforderung. Unvollständige Konvertierung muss einen konkreten Importbericht liefern; keine stillen Datenverluste.

## Vom Nutzer vorgegebene Logo-Grundlage

28. Der Dongleware-Wuerfel aus `branding/dongleware-cube-reference.png` ist die vom Nutzer gewaehlte Produktlogo-Grundlage. Roter Entwurf: `branding/dongleware-cube-red.png`; Hinweise in `branding/LOGO.md`. Diese nutzerbereitgestellten Dateien sind keine im Projekt erfundenen GPL-Platzhalter; ihre Rechte nicht pauschal umdeklarieren. Eigene UI-Icons bleiben davon getrennt.

## Projektpfad, Logo und Entwicklungswerkzeuge

29. Das Projektverzeichnis ist die Wurzel dieses Bestands. Bestehende microGulp-Steuerdateien erhalten. Gulp fuer Einrichtung, Icon-Erzeugung und Quellbackup ist Entwicklungsinfrastruktur; die spaetere Produkt-API zu microGulp bleibt davon getrennt.
30. Aktive Logo-Master sind branding/micro3D-logo.svg und branding/micro3D-app.svg: einfarbige rote Flaechen und transparenter Hintergrund. Die ausdruecklich vom Nutzer beauftragte Vektorableitung ersetzt den Rasterentwurf als Produktlogo.
31. Spaeter microCSS ueber die versionierte API integrieren, insbesondere Bildsequenzen fuer CSS-Animationen. modules/microcss/README.md ist die Zielvorgabe; Sequenz-/Sprite-Export bleibt ausserhalb von Phase 1.

32. Informationen zu lokal installierter Referenzsoftware und interne Produktvergleiche gehören nicht in veröffentlichbare Projektdateien. Dateiformat- und Interoperabilitätsanforderungen ausschließlich sachlich und im jeweiligen Modul dokumentieren.

## Eigenständiger öffentlicher Auftritt

33. README, UI-Texte, eigene Codekommentare, Prompts, Commit-Nachrichten und sonstige neue Git-Inhalte beschreiben das Produkt eigenständig, ohne konkurrierende Hersteller-/Produktnamen als Bedienvorbild oder Werbevergleich. Eng begrenzte Ausnahmen: sachlich notwendige Dateiformat-Import-/Interoperabilitätsangaben und rechtlich erforderliche Lizenz-, Copyright- und Herkunftshinweise. Fremde Pflichtangaben bleiben erhalten; keine Umschreibung bestehender Git-Historie.

34. CLAUDE.md, AGENTS.md und Cursor-Prompts sind wie README als veröffentlichbar zu behandeln. Vor Commit und Veröffentlichung deren vollständigen Inhalt auf interne Referenzsoftware, Produktvergleiche und private Bestandsangaben prüfen und solche Passagen entfernen; eine geplante spätere Bereinigung reicht nicht. Ausnahmen aus Regel 33 einzeln begründen.

## Geplante KI-Steuerung und MCP (spätere Ausbaustufe)

35. Diese Planung erweitert den aktuellen Phase-1-Auftrag nicht. Laufende Branding-, UI- und Build-Arbeiten zuerst wie beauftragt abschließen. Jetzt keine MCP-Dienste starten, Add-ons installieren, Ports öffnen oder KI-/npm-Runtimes hinzufügen. Umsetzung erst in einem nachfolgenden ausdrücklich beauftragten Arbeitsschritt.

36. Als erster späterer Schritt ist ein begrenzter Kompatibilitätstest der offiziellen Blender-Lab-MCP-Anbindung vorgesehen (Quelle: https://www.blender.org/lab/mcp-server/). Vor Verwendung aktuellen Quellstand, Lizenz, Voraussetzungen und Sicherheitsverhalten prüfen und Versionen festschreiben. Kompatibilität zum gepinnten µ3D-Build ist eine zu prüfende Annahme, keine bereits nachgewiesene Eigenschaft. Vorzugsweise Add-on und externer Adapter; kein nativer Patch ohne belegten Bedarf.

37. Den ersten MCP-Test mit separatem µ3D-Profil, kopierten Testszenen und isolierter Umgebung ohne sensible Daten durchführen. Szenenabfrage, Objekterstellung, Materialänderung, Vorschau-Render, Undo/Redo und .blend-Speichern samt erneutem Öffnen prüfen. Ergebnisse, Einschränkungen, Client-/Add-on-/Server-Versionen und getestete Plattform dokumentieren. Unbeschränkte Python-Ausführung ist keine sichere Sandbox; ein bloßer Localhost-Zugang schützt nicht vor deren Dateisystem- oder Netzwerkzugriffen.

38. Für die Produktintegration eine gemeinsame versionierte Automations-API entwickeln: MCP-Adapter, späteres eigenes µGulp-npm-Modul und microCSS verwenden denselben Befehls- und Jobvertrag. `modules/api/contracts.ts` ist bislang ein Entwurf, kein laufender Dienst. Öffentliche API JS/TS-first, Blender-seitige Ausführung über Python/bpy auf dem Hauptthread. Keine zweite Szenenverwaltung und keine Pflicht zu Node, KI-Client oder Netzwerk für den normalen Editorbetrieb. Ein eingebauter Chat ist keine Voraussetzung.

39. Definierte, validierte Befehle für Szenen-/Objektabfrage, Auswahl, Objekterstellung und -bearbeitung, Materialien, Kameras, Speichern und Renderaufträge schrittweise ergänzen. Fähigkeiten und Protokollversion aushandeln, stabile Objektkennungen und strukturierte Fehler vorsehen. Szenenzustand und Vorschauen ermöglichen der KI die Kontrolle ihrer Ergebnisse. Bestehende .blend-Daten und Add-on-Kompatibilität gemäß den bisherigen Regeln erhalten.

40. Automationszugang standardmäßig deaktiviert und ausdrücklich aktivierbar gestalten. Lokale Kommunikation mit authentifiziertem Verbindungsaufbau, Eingabeprüfung und begrenzten Dateipfad-/Ausgaberechten vorsehen; keine Geheimnisse protokollieren. Unbeschränktes Python/eval und beliebige Shell-Befehle nicht als normalen Produktzugang anbieten. Vor Änderungen reversible Abläufe mit geeignetem Undo oder Sicherungspunkt vorsehen; Dateischreibvorgänge und externe Nebenwirkungen sind nicht automatisch durch Undo rückgängig zu machen. Szenentexte und importierte Daten dürfen keine Berechtigungen erweitern.

41. Längere Aufträge benötigen Job-ID, Status, nachvollziehbaren Fortschritt, Fehlerbericht, Zeitlimit und kooperativen Abbruch. Bei nicht sofort abbrechbaren Operationen den tatsächlichen Zustand melden; keinen erfolgreichen Abbruch vortäuschen. Verbindungsausfall und Wiederverbindung dürfen Änderungen nicht unbemerkt doppelt ausführen. Tests umfassen Erfolg, ungültige Eingaben, fehlende Berechtigung, Abbruch, Verbindungsfehler und .blend-Roundtrip.

42. Das eigene npm-Modul für die spätere µGulp-Produktanbindung ist ausdrücklich geplant, aber weder implementiert noch veröffentlicht. Paketname, Lizenz, Abhängigkeiten und Versionsstrategie vor Umsetzung festlegen. Die bestehende Repository-Integration über `gulp-mu-gulp-api` ist davon getrennt. microCSS soll später über dieselbe API Bildsequenzen anfordern; Sequenz-/Sprite-Export und zusätzliche Dateiformat-Importer bleiben außerhalb von Phase 1.

43. Bedienanforderungen und Abnahmetests eigenständig anhand konkreter Abläufe beschreiben: Auswahlwechsel, Objekthierarchie, kontextbezogene Attribute, Navigation und Undo. Interne Vergleichsnotizen, Namen oder Versions-/Installationsangaben fremder Referenzsoftware nicht in diese Datei oder andere veröffentlichbare Projektinhalte aufnehmen; keine fremden Assets oder Oberflächen kopieren. Regeln 32 bis 34 gelten unverändert.
