# Resultado reproducible

Modelo elegido por macro-F1 de validación: **forest**.

| Modelo | Macro-F1 validación | Macro-F1 prueba | Accuracy prueba |
|---|---:|---:|---:|
| majority | 0.0733 | 0.0736 | 0.3470 |
| logistic | 0.6390 | 0.6635 | 0.6530 |
| forest | 0.8109 | 0.8080 | 0.7789 |

## Resultado por clase del modelo elegido

| Clase | Recall | F1 | N |
|---|---:|---:|---:|
| Pastry | 0.6452 | 0.6780 | 31 |
| Z_Scratch | 0.9474 | 0.9474 | 38 |
| K_Scatch | 0.8354 | 0.9103 | 79 |
| Stains | 0.8571 | 0.8571 | 14 |
| Dirtiness | 0.8182 | 0.8571 | 11 |
| Bumps | 0.6790 | 0.6667 | 81 |
| Other_Faults | 0.7778 | 0.7394 | 135 |

Regla de revisión por puntuación/margen: 169 casos marcados; cobertura sin marca 56.6%. La marca adicional por rango se aplica en consulta y no está incluida en esta cifra.

Las siete clases corresponden a defectos. No se estima aceptación/rechazo de piezas ni detección de piezas sanas. El costo ilustrativo uniforme de confundir tipos sería el número de errores (suma fuera de la diagonal); no representa costos industriales reales.

Partición aleatoria estratificada, sin identificadores de tiempo/lote/planta. No se usó SMOTE. Puntuaciones sin calibración y pocos ejemplos de las clases raras limitan la interpretación.

Generado por scripts/publish_report.py desde var/model/manifest.json. La matriz completa, particiones, rangos y versiones se encuentran en evaluation.json.
