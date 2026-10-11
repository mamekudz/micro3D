# Produktlogo und App-Icons

Aktiver Master: `micro3D-logo.svg`, drei geschlossene Polygonflaechen in #E6A2A2, #C65353 und #8F202D. Keine Verlaeufe, Rastereinbettungen oder Hintergrundflaeche. Auch die Trennfugen sind transparent. `micro3D-app.svg` ist dieselbe Geometrie mittig auf einer quadratischen 160x160-Zeichenflaeche mit Rand.

`npm run icons` erzeugt daraus deterministisch PNGs von 16 bis 1024 Pixel, ein Windows-ICO mit sieben Groessen und ein macOS-ICNS. Dateien unter `generated/` sind direkt fuer Packaging nutzbar. Container und Transparenz werden getestet; die Darstellung im macOS-Dock ist mangels Mac noch nicht visuell getestet. Linux verwendet SVG oder PNG. Der Build muss die Dateien noch in die jeweiligen nativen Ressourcen einbinden.

Die beiden alten PNGs bleiben als nutzerbereitgestellte Referenz und verworfener Imagegen-Rasterentwurf erhalten; `product.svg` ist nur der fruehere unabhaengige Platzhalter. Die neuen SVGs sind explizit vom Nutzer beauftragte Vektorableitungen des Dongleware-Wuerfels, keine eigene Erfindung. Rechte der Vorlage werden nicht durch die GPL-Angabe des Projektgeruests ersetzt. Siehe assets.json.
