# Datos y atribución

Fuente: Buscema, M., Terzi, S. y Tastle, W. (2010), **Steel Plates Faults**, UCI Machine Learning Repository, DOI [10.24432/C5J88N](https://doi.org/10.24432/C5J88N). [Ficha oficial](https://archive.ics.uci.edu/dataset/198/steel+plates+faults), consultada el 28 de octubre de 2026. Licencia del dataset: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Código: MIT.

Los archivos originales `Faults.NNA` y `Faults27x7_var` se obtuvieron del [ZIP oficial](https://archive.ics.uci.edu/static/public/198/steel%2Bplates%2Bfaults.zip) y se conservan sin modificar bytes. Git no convierte sus saltos de línea.

| Archivo | SHA256 |
|---|---|
| Faults.NNA | 08994f5b0185a8e6cc22afe9910fd36834990fb1ca30852ed79012a832fbff55 |
| Faults27x7_var | 887dbfa140b48877b706865ef277550dc0203699243c600e24bfe8b090a9a953 |

1.941 observaciones, 27 entradas y siete indicadores de clase mutuamente excluyentes. Se conserva la grafía original `K_Scatch`. Las clases son Pastry, Z_Scratch, K_Scatch, Stains, Dirtiness, Bumps y Other_Faults. **No hay clase sana**. No asumir que las 1.941 filas representan piezas independientes de lotes distintos: faltan identificadores de lote/planta y fechas verificables. No se añaden unidades que la fuente no especifica.

La partición es aleatoria estratificada 60/20/20 con semilla42. No hay duplicados exactos en las 27 entradas; el entrenamiento rechaza duplicados si aparecen para exigir una revisión del corte. Eso no descarta correlación entre piezas del mismo lote no identificado. Las etiquetas se excluyen explícitamente de las características; cada transformación aprende solo de entrenamiento.

El CSV anterior de 5.000 filas/12 columnas no corresponde a esta fuente documentada. Su origen no pudo acreditarse. Se retiró del árbol actual junto con el notebook de conclusiones inconsistentes después de preservar el historial en `0637de3a8f94bfac3caececd8700a9e8287574fb` y un bundle completo. No se reutilizan sus resultados ni se atribuyen a UCI.
