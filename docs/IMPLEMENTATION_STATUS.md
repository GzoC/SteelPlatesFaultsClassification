# Estado de implementación — 28 de octubre de 2026

Rama `codex/steel-faults-rebuild`, PR #1. Base main `0637de3a8f94bfac3caececd8700a9e8287574fb`.

Implementado: datos oficiales UCI con hashes/licencia, pipeline sin etiquetas de salida en entradas, partición 60/20/20, selección con validación, tres referencias, métricas por clase, persistencia y contrato de inferencia, demo Streamlit, notebook ejecutable, paquetes e integración continua. Histórico preservado en Git y bundle inicial.

Comprobado localmente con Python 3.12.13: 11 pruebas, Ruff, entrenamiento, notebook completo (tres celdas ejecutadas sin salida error), wheel y sdist generados. Forest seleccionado, macro-F1 prueba 0,8080. CI de push `40738084641` aprobada en commit `b216a83aa1b063443e60306a1ede7b7468b8ab77`; cualquier cambio posterior requiere comprobar su CI propia.

Vista de escritorio abierta realmente en Edge a 127.0.0.1:8503. Captura `evidence/desktop-case.png` muestra inferencia y caso incorrecto sin marca de revisión; no se oculta esa limitación. La tabla de entradas queda plegada. Se observaron dos avisos Vega sobre escalas/fit-y; ningún error en el registro consultado. Esto no constituye una validación visual completa.

Pendiente antes de entregar: comprobar cambios de observación, pestaña Evaluación, carga CSV válida/inválida y descarga, vista móvil y ausencia de desbordes; revisar avisos del gráfico; capturas finales; revisar README e informe, cerrar evidencia y comprobar CI del último commit. El PR queda borrador. No fusionar sin autorización específica para este PR. No comenzar otro repositorio antes de cerrar este.

No se validó Docker ni despliegue industrial. No hay clase sana; no se pueden afirmar decisiones de aceptación/rechazo de piezas. Registro y respaldo externos: `../STEEL_PROGRESS.md` desde la carpeta raíz del repositorio.
