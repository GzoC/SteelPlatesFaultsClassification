"""Generate conclusions from the measured manifest, without editing metrics by hand."""

import json
from pathlib import Path

manifest = json.loads(Path("var/model/manifest.json").read_text(encoding="utf-8"))
output = Path("reports")
output.mkdir(exist_ok=True)
(output / "evaluation.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
lines = [
    "# Resultado reproducible",
    "",
    f"Modelo elegido por macro-F1 de validación: **{manifest['selected']}**.",
    "",
    "| Modelo | Macro-F1 validación | Macro-F1 prueba | Accuracy prueba |",
    "|---|---:|---:|---:|",
]
for name, result in manifest["test"].items():
    lines.append(
        f"| {name} | {manifest['validation'][name]['macro_f1']:.4f} | {result['macro_f1']:.4f} | {result['accuracy']:.4f} |"
    )
lines += [
    "",
    "## Resultado por clase del modelo elegido",
    "",
    "| Clase | Recall | F1 | N |",
    "|---|---:|---:|---:|",
]
selected = manifest["test"][manifest["selected"]]
for name in manifest["classes"]:
    result = selected["per_class"][name]
    lines.append(
        f"| {name} | {result['recall']:.4f} | {result['f1-score']:.4f} | {int(result['support'])} |"
    )
lines += [
    "",
    f"Regla de revisión por puntuación/margen: {selected['review']['flagged']} casos marcados; cobertura sin marca {selected['review']['coverage']:.1%}. La marca adicional por rango se aplica en consulta y no está incluida en esta cifra.",
    "",
    "Las siete clases corresponden a defectos. No se estima aceptación/rechazo de piezas ni detección de piezas sanas. El costo ilustrativo uniforme de confundir tipos sería el número de errores (suma fuera de la diagonal); no representa costos industriales reales.",
    "",
    "Partición aleatoria estratificada, sin identificadores de tiempo/lote/planta. No se usó SMOTE. Puntuaciones sin calibración y pocos ejemplos de las clases raras limitan la interpretación.",
    "",
    "Generado por scripts/publish_report.py desde var/model/manifest.json. La matriz completa, particiones, rangos y versiones se encuentran en evaluation.json.",
]
(output / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(output / "RESULTS.md")
