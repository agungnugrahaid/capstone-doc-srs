#!/bin/sh
# Regenerate SAPA.vpp and PNG exports with Visual Paradigm (Community Edition 18) in headless mode.
# Requires the sapa.gen plugin in ~/Library/Application Support/VisualParadigm/plugins/sapa.gen
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
DIAG="$HERE/.."
WORK="${TMPDIR:-/tmp}/sapa-vp"
APP="/Applications/Visual Paradigm.app/Contents/Resources/app"
JAVA="/Applications/Visual Paradigm.app/Contents/Resources/jre.bundle/Contents/Home/bin/java"
CP=".:../lib/vpplatform.jar:../lib/jniwrap.jar:../lib/winpack.jar:../ormlib/orm.jar:../ormlib/orm-core.jar"
for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20; do CP="$CP:../lib/lib$i.jar"; done
vp() { cls="$1"; shift; (cd "$APP/bin" && "$JAVA" -Xmx2048m -Djava.awt.headless=${HEADLESS:-true} -cp "$CP" "$cls" "$@" 2>&1 | grep -E "sapa.gen|Saved|rror" || true); }

mkdir -p "$WORK" "$DIAG/png"
rm -f "$WORK"/*.vpp*
python3 "$HERE/build_specs.py" "$WORK/sapa.tsv" ${1:-all}
printf '<?xml version="1.0" encoding="UTF-8"?>\n<Project Name="SAPA" UmlVersion="2.x" Xml_structure="simple"><Models/><Diagrams/></Project>\n' > "$WORK/empty.xml"
vp com.vp.cmd.ImportXML -project "$WORK/base.vpp" -file "$WORK/empty.xml"
vp com.vp.cmd.Plugin -project "$WORK/base.vpp" -pluginid sapa.gen -pluginargs "'$WORK/sapa.tsv' '$WORK/SAPA.vpp'"
rm -rf "$WORK/png" && mkdir -p "$WORK/png"
HEADLESS=false vp com.vp.cmd.ExportDiagramImage -project "$WORK/SAPA.vpp" -out "$WORK/png" -diagram '*' -type png_with_background
cp "$WORK/SAPA.vpp" "$DIAG/SAPA.vpp"
cp "$WORK"/png/*.png "$DIAG/png/"
ls "$DIAG/png"
