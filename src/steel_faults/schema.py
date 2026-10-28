import numpy as np
import pandas as pd

FEATURES = [
    "X_Minimum",
    "X_Maximum",
    "Y_Minimum",
    "Y_Maximum",
    "Pixels_Areas",
    "X_Perimeter",
    "Y_Perimeter",
    "Sum_of_Luminosity",
    "Minimum_of_Luminosity",
    "Maximum_of_Luminosity",
    "Length_of_Conveyer",
    "TypeOfSteel_A300",
    "TypeOfSteel_A400",
    "Steel_Plate_Thickness",
    "Edges_Index",
    "Empty_Index",
    "Square_Index",
    "Outside_X_Index",
    "Edges_X_Index",
    "Edges_Y_Index",
    "Outside_Global_Index",
    "LogOfAreas",
    "Log_X_Index",
    "Log_Y_Index",
    "Orientation_Index",
    "Luminosity_Index",
    "SigmoidOfAreas",
]
CLASSES = ["Pastry", "Z_Scratch", "K_Scatch", "Stains", "Dirtiness", "Bumps", "Other_Faults"]
SCHEMA_VERSION = 1


def validate_features(frame):
    if not isinstance(frame, pd.DataFrame) or frame.empty or frame.columns.duplicated().any():
        raise ValueError("Se requiere una tabla no vacía con columnas únicas")
    if set(frame.columns) != set(FEATURES):
        raise ValueError(
            "Se requieren exactamente las 27 características UCI, sin etiquetas ni columnas extra"
        )
    result = frame.loc[:, FEATURES].copy()
    if any(
        not pd.api.types.is_numeric_dtype(t) or pd.api.types.is_bool_dtype(t) for t in result.dtypes
    ):
        raise ValueError(
            "Las características deben ser numéricas; no se aceptan texto ni booleanos"
        )
    if not np.isfinite(result.to_numpy(dtype=float)).all():
        raise ValueError("No se aceptan valores ausentes, NaN ni infinitos")
    for low, high in [
        ("X_Minimum", "X_Maximum"),
        ("Y_Minimum", "Y_Maximum"),
        ("Minimum_of_Luminosity", "Maximum_of_Luminosity"),
    ]:
        if (result[low] > result[high]).any():
            raise ValueError(f"{low} no puede superar {high}")
    steel = result[["TypeOfSteel_A300", "TypeOfSteel_A400"]]
    if not steel.isin([0, 1]).all().all() or not steel.sum(axis=1).eq(1).all():
        raise ValueError("Selecciona un único tipo de acero A300/A400 (0/1)")
    return result
