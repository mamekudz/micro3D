# µ3D-Steuerdateien in diesem Fork

Repository: https://github.com/mamekudz/micro3D, Zweig `micro3d`, Parent `blender/blender`.

Dieser Zweig steht auf dem Blender-Commit `a6f145b151fa8562a478ed2c381ab945e7bcac72` (5.3.0 Beta) und enthält die angewendete Patchserie. Der Lock bleibt `bootstrap`. Die offizielle Upstream-URL bleibt `https://projects.blender.org/blender/blender.git`.

`micro3d/` liegt neben dem Blender-Quellbaum. `tools/patches.py` sucht Lock und Patches im übergeordneten Verzeichnis dieser Datei, also in `micro3d/`.

## Patchserie prüfen

Im Quellbaum:

```
python micro3d/tools/patches.py verify
```

## Patchserie auf einem sauberen Pin erneut anwenden

`apply` verlangt einen sauberen Checkout genau auf dem festgeschriebenen Commit. Der Zweig `micro3d` ist dafür bereits gepatcht; `apply` bricht dort erwartungsgemäß ab.

```
git checkout --detach a6f145b151fa8562a478ed2c381ab945e7bcac72
python micro3d/tools/patches.py apply --source .
```

Der Build selbst folgt `micro3d/docs/BUILD.md`. `upstream/platforms/windows-x64.json` zeichnet den geprüften Windows-Stand auf. Das dort genannte Replay-Werkzeug liegt nicht in diesem Overlay, weil es Bibliotheken außerhalb des Quellbaums auflöst. Eine bitidentische Reproduktion ist nicht gemessen.

Neue eigene Dateien in `micro3d/` stehen unter GPL-3.0-or-later. Unveränderte und geänderte Upstream-Dateien behalten ihre Lizenzhinweise.
