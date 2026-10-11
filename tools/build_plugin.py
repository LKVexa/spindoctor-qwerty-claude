# SpinDoctor Qwerty 1.1.0 - Claude .plugin builder
# Copyright (C) 2026 RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. It is distributed WITHOUT ANY WARRANTY; see the LICENSE file for details.
"""Build dist/spindoctor-qwerty.plugin: the plugin as a reproducible ZIP for claude.ai / Cowork
(Customize > Plugins > Add > Upload plugin). `.claude-plugin/plugin.json` sits at the archive root, next to `.mcp.json`,
`skills/`, `commands/`, `agents/`, README.md, LICENSE, NOTICE and COPYRIGHT. Tests, tools, the marketplace file and
generated sample PDFs are left out (the plugin stays text-only). Sorted entries, fixed timestamps, no __pycache__. Also writes the SHA-256. Standard library only.

  python3 tools/build_plugin.py [OUT_DIR]
"""
import hashlib, json, os, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INCLUDE = [".claude-plugin/plugin.json", ".mcp.json", "README.md", "LICENSE", "NOTICE", "COPYRIGHT", "skills", "commands", "agents"]


def files():
    out = []
    for item in INCLUDE:
        p = os.path.join(ROOT, item)
        if os.path.isfile(p): out.append(p); continue
        for root, dirs, fs in os.walk(p):
            dirs[:] = sorted(d for d in dirs if d != "__pycache__")
            out += [os.path.join(root, f) for f in sorted(fs) if not f.endswith((".pyc", ".pyo", ".pdf"))]
    return out


def build(out_dir=os.path.join(ROOT, "dist")):
    name = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8"))["name"]
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, name + ".plugin"); fs = files()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in fs:
            arc = os.path.relpath(p, ROOT).replace(os.sep, "/")
            zi = zipfile.ZipInfo(arc, date_time=(2026, 10, 10, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = (0o755 if arc.endswith(".py") and "/scripts/" in arc else 0o644) << 16
            z.writestr(zi, open(p, "rb").read())
    h = hashlib.sha256(open(out, "rb").read()).hexdigest()
    open(out + ".sha256", "w", newline="\n").write("%s  %s\n" % (h, os.path.basename(out)))
    return out, h, len(fs)


if __name__ == "__main__":
    out, h, n = build(*(sys.argv[1:2]))
    print("%s (%d files)\nsha256 %s" % (out, n, h))
