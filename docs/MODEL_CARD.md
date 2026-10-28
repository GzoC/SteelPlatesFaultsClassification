# Modelo y límites de decisión

Objetivo: identificar uno de siete tipos de defecto a partir de 27 características medidas. Se clasifica una observación ya defectuosa. No se detectan defectos directamente en imágenes y no hay clase sana para calcular falsas aceptaciones o rechazos de piezas.

Se comparan clase mayoritaria, regresión logística con estandarización y balance de clases, y Random Forest con 300 árboles, mínimo2 muestras por hoja y balance por bootstrap. Parámetros fijados antes de evaluar; no se usa SMOTE. Macro-F1 de validación elige el modelo, después se consulta el holdout. No se reajusta el modelo con validación o prueba. El informe se genera automáticamente desde métricas reales, no desde conclusiones escritas a mano.

La aplicación muestra puntuaciones sin calibración probabilística, el margen entre las dos primeras clases y una regla de revisión fijada antes de evaluar: máximo inferior a0,60 o margen inferior a0,15. En consulta también marca cualquier característica fuera del rango de entrenamiento. No se afirma que una puntuación0,8 implique 80 % de certeza ni que un caso sin marca esté aprobado para liberación. El conjunto reservado permite describir cobertura y errores de esta regla, no garantizar seguridad.

La importancia por permutación se calcula en validación con tres repeticiones y pérdida de macro-F1. Es una explicación global de sensibilidad del modelo, no una explicación causal o individual. Los atributos correlacionados pueden repartirse importancia.

La matriz tiene costo ilustrativo uniforme1 por confundir tipos de defecto y0 para aciertos; su suma sería el número de errores. Sin piezas sanas, costos de reparación, severidad ni política de calidad no se estima el costo de aceptar defectuosas o rechazar conformes. Se necesitan datos adicionales de piezas sanas y una matriz de costos acordada con operación antes de tomar decisiones reales.

La partición aleatoria no acredita generalización a nuevas plantas, lotes o periodos. Hay pocas observaciones en clases raras; deben revisarse support, recall y F1, no solo accuracy. Se requieren validación externa, calibración, seguimiento de deriva y revisión de ingeniería antes de un uso operativo.

El artefacto guarda contrato, scikit-learn, hash de datos y checksum del pipeline. Solo se carga un modelo entrenado localmente y confiable. El checksum detecta corrupción; no autentica fuentes de terceros. Reentrenar ante cambio de scikit-learn y reiniciar la aplicación.
