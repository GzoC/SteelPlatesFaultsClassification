# Validación ejecutada

28 de octubre de 2026. Código de aplicación y experimento: `1a4311115f264f684b39e11972de04b0e5e12d10`. Los cambios posteriores de esta entrega añaden evidencia/documentación. No se atribuye uso en planta ni validación Docker.

## Reproducción y CI

- Windows, Python 3.12.13, entorno de `uv.lock`: entrenamiento, 11 pruebas pytest, Ruff y notebook ejecutados. Macro-F1 de prueba 0,8080; la selección del modelo se hizo con validación.
- [CI 40780867344](https://github.com/GzoC/SteelPlatesFaultsClassification/actions/runs/40780867344) aprobada para ese código en Python 3.11/3.13: pruebas, estilo, entrenamiento, informe, notebook, wheel/sdist e instalación/entrenamiento del wheel fuera del checkout.
- Wheel y sdist reconstruidos localmente. El notebook Windows terminó con avisos de zmq/selector y permisos del perfil Jupyter, sin celdas con salida de error; no se presenta como ejecución sin avisos.

## Recorridos reales de navegador

La revisión empezó en Edge y terminó en el navegador integrado. Este último permitió cargar archivos locales sin cambiar permisos de la extensión de Edge ni de Windows. Un bloqueo inicial del control nativo no se cuenta como prueba aprobada; las filas siguientes describen las comprobaciones posteriores completadas.

| Recorrido | Resultado observado |
|---|---|
| Cambiar de fila 97 a 169 | Other_Faults/Pastry con revisión cambia a Z_Scratch/Z_Scratch, margen 0,71, sin marca |
| Evaluación | Comparación de modelos, métricas por clase y matriz con 389 observaciones visibles |
| CSV válido | Siete filas procesadas y botón de exportación disponible |
| Exportar resultados | Archivo descargado; clases, puntuaciones y marcas de las siete filas coinciden con Predictor local |
| Columna de etiqueta extra | Mensaje de contrato inválido; exportación anterior desaparece |
| CSV de 105 filas | Rechazado por máximo de 100 observaciones |
| CSV solo con cabecera | Rechazado como tabla vacía |
| Recuperación | Tras los errores, un CSV válido vuelve a producir resultados y no deja alertas anteriores |
| Móvil 390 × 844 | Controles apilados, gráfico legible y pestañas operables; sin desborde horizontal de documento/main |
| Escritorio 1280 × 900 | Controles, resultado y gráfico visibles; sin desborde horizontal de documento/main |
| Consola final | Sin avisos ni errores en el registro consultado del navegador integrado |

Las tablas anchas usan su propio desplazamiento. No se afirma una auditoría completa de accesibilidad, compatibilidad con todos los navegadores ni una prueba de carga/concurrencia. La prueba de tamaño se limita a las filas del CSV; no se atribuye prueba de archivos de más de 2 MB.

## Evidencias

- [Inferencia en escritorio](evidence/desktop-case.png)
- [Matriz y límites](evidence/desktop-evaluation.png)
- [CSV procesado](evidence/csv-valid.png) y [entrada rechazada](evidence/csv-rejected.png)
- [Vista móvil](evidence/mobile-case.png) y [puntuaciones móviles](evidence/mobile-scores.png)

Las capturas muestran la aplicación ejecutada, no maquetas. El modelo puede equivocarse incluso sin marca de revisión. Las siete clases son defectos: no hay datos de piezas sanas para evaluar una decisión de aceptación/rechazo.
