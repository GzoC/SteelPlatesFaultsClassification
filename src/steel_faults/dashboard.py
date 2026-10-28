"""Local demonstration on measured features; no images or machine actuation."""

import os
from pathlib import Path

import pandas as pd
import streamlit as st

from steel_faults.inference import Predictor
from steel_faults.schema import CLASSES


def render():
    st.set_page_config(page_title="Steel Defect Study", page_icon="🔎", layout="wide")
    st.caption("CALIDAD INDUSTRIAL · DATOS · CLASIFICACIÓN")
    st.title("Siete tipos de defecto, una evaluación trazable")
    st.info(
        "Todos los ejemplos UCI son defectos. Este modelo no distingue una pieza sana ni autoriza su aceptación o rechazo."
    )
    directory = Path(os.environ.get("MODEL_DIR", "var/model"))
    try:
        predictor = Predictor(directory)
    except (OSError, ValueError, KeyError):
        st.error(
            "Modelo local no disponible o incompatible. Ejecuta steel-faults train antes de abrir la demo."
        )
        return
    m = predictor.manifest
    demo, evaluation, upload = st.tabs(["Explorar un caso", "Evaluación", "Consultar CSV"])
    with demo:
        st.caption(
            "Casos del conjunto de prueba. La etiqueta observada se revela junto al resultado; no entra al modelo."
        )
        example = st.selectbox(
            "Observación UCI", m["examples"], format_func=lambda e: f"Fila {e['row'] + 1}"
        )
        with st.expander("Ver las 27 características medidas"):
            st.dataframe(
                pd.Series(example["features"], name="Valor").rename_axis("Característica"),
                width="stretch",
            )
        result = predictor.predict(pd.DataFrame([example["features"]]))[0]
        a, b, c = st.columns(3)
        a.metric("Clase propuesta", result["class"])
        b.metric("Clase observada", example["observed"])
        c.metric("Margen entre primeras clases", f"{result['margin']:.2f}")
        if result["review"]:
            st.warning(
                "Revisión sugerida: puntuaciones poco separadas o valores fuera del rango de entrenamiento."
            )
        else:
            st.info(
                "Sin marca de revisión por esta regla. No equivale a certeza ni a aprobación de calidad."
            )
        if result["outside_training_range"]:
            st.write("Fuera de rango observado:", result["outside_training_range"])
        st.bar_chart(pd.Series(result["scores"], name="Puntuación"), horizontal=True)
        st.caption(
            "Puntuaciones sin calibración probabilística. Revisión sugerida si máximo <0,60, margen <0,15 o algún valor sale del rango de entrenamiento."
        )
        st.subheader("Qué información usa el modelo")
        st.write(
            "Las 27 características describen geometría, luminosidad y acero. No se procesa una fotografía. Las etiquetas de defecto están excluidas."
        )
        st.dataframe(
            pd.DataFrame(m["validation_permutation_importance"][:10]),
            hide_index=True,
            width="stretch",
        )
        st.caption(
            "Importancia global por permutación en validación: caída de macro-F1 al desordenar una característica. No es una explicación causal ni individual de este caso."
        )
    with evaluation:
        st.subheader("Comparación con una referencia simple")
        st.write(
            f"Modelo elegido con macro-F1 de validación: {m['selected']}. Prueba reservada: {m['split']['test']['rows']} observaciones."
        )
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Modelo": name,
                        "Macro-F1": r["macro_f1"],
                        "Accuracy": r["accuracy"],
                        "Marcadas por puntuación": r["review"]["flagged"],
                    }
                    for name, r in m["test"].items()
                ]
            ),
            hide_index=True,
            width="stretch",
        )
        chosen = m["test"][m["selected"]]
        st.subheader("Resultados por tipo de defecto")
        st.dataframe(pd.DataFrame(chosen["per_class"]).T.loc[CLASSES], width="stretch")
        st.caption(
            "Matriz: filas observadas, columnas propuestas. No hay clase sin defecto; no se pueden evaluar decisiones de aceptación/rechazo de piezas con este dataset."
        )
        st.dataframe(
            pd.DataFrame(chosen["confusion_matrix"], index=CLASSES, columns=CLASSES),
            width="stretch",
        )
        st.write(
            "Partición aleatoria estratificada 60/20/20, semilla 42. No acredita generalización por tiempo, planta o lote: faltan esos identificadores."
        )
        st.caption(
            "La marca de revisión del informe usa solo puntuación/margen. En consulta también se marca cualquier característica fuera del rango observado al entrenar."
        )
    with upload:
        st.subheader("Consultar características medidas")
        st.write(
            "CSV con exactamente las 27 columnas del ejemplo, hasta 100 filas y 2 MB. Se procesa localmente y no se guarda en disco."
        )
        st.download_button(
            "Descargar ejemplo de entrada",
            pd.DataFrame([e["features"] for e in m["examples"]]).to_csv(index=False).encode(),
            "steel-example.csv",
            "text/csv",
        )
        file = st.file_uploader("CSV de características", type=["csv"])
        if file is not None:
            try:
                if file.size > 2_000_000:
                    raise ValueError("Máximo 2 MB")
                frame = pd.read_csv(file)
                rows = predictor.predict(frame)
                result = pd.DataFrame(
                    [{k: v for k, v in row.items() if k != "scores"} for row in rows]
                )
                st.dataframe(result, hide_index=True, width="stretch")
                st.download_button(
                    "Exportar resultados",
                    result.to_csv(index=False).encode(),
                    "steel-results.csv",
                    "text/csv",
                )
            except (ValueError, pd.errors.ParserError) as exc:
                st.error(f"Entrada inválida: {exc}")
    st.caption(
        "Fuente: Steel Plates Faults / UCI · DOI 10.24432/C5J88N · CC BY 4.0 · Demostrador educativo"
    )


if __name__ == "__main__":
    render()
