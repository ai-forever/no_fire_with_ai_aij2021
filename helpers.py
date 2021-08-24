import numpy as np
import pandas as pd


def get_grid_index(df, array_of_lons, array_of_lats):
    col_n = len(array_of_lons)
    temp = df.drop_duplicates(subset=["lon_min", "lat_min"]).reset_index(drop=True)
    for (idx, row) in temp.iterrows():
        col_i = np.where(array_of_lons == row["lon_min"])[0][0]
        row_i = np.where(array_of_lats == row["lat_min"])[0][0]
        temp.loc[(temp.index == idx), "grid_index"] = row_i * col_n + col_i
    df = df.merge(
        temp[["lon_min", "lat_min", "lon_max", "lat_max", "grid_index"]],
        how="left",
        on=["lon_min", "lat_min", "lon_max", "lat_max"],
    )
    df.grid_index = df.grid_index.astype(int)
    return df


def split_string(string):
    try:
        return string.split("(")[0]
    except AttributeError:
        return string


def __get_arange(num, step=0.2):
    return np.arange(num, num + 1 + step, step)


def __get_max(row, feat):
    return row[f"temp_{feat}"][np.where(row[f"diff_{feat}"] > 0)[0].min()]


def __get_min(row, feat):
    try:
        return row[f"temp_{feat}"][np.where(row[f"diff_{feat}"] <= 0)[0].max()]
    except:
        print(row)


def add_edges_polygon(df):
    for feat in ["lon", "lat"]:
        df[f"temp_{feat}"] = df[feat].astype(int).apply(__get_arange)
        df[f"diff_{feat}"] = df[f"temp_{feat}"] - df[feat]

        df[f"{feat}_min"] = df.apply(__get_min, axis=1, feat=feat).round(1)
        df[f"{feat}_max"] = df.apply(__get_max, axis=1, feat=feat).round(1)

    df.drop(columns=["temp_lon", "diff_lon", "temp_lat", "diff_lat"], inplace=True)
    return df


def competition_metric(y_true, y_pred):
    assert (
        y_true.shape == y_pred.shape
    ), "Dataset shapes are not equal (y_true.shape != y_pred.shape)"
    assert all(
        [el in [0, 1] for el in np.unique(y_pred.values)]
    ), "Predictions should only have 0 or 1"
    y_true_sums = (
        y_true.replace(0, np.nan).fillna(axis=1, method="ffill").fillna(0).sum(axis=1)
    )
    y_pred_sums = (
        y_pred.replace(0, np.nan).fillna(axis=1, method="ffill").fillna(0).sum(axis=1)
    )
    days_error_series = y_pred_sums - y_true_sums
    days_error_series.loc[days_error_series < 0] = days_error_series[days_error_series < 0] * (-2)
    metric = days_error_series.apply(
        lambda x: round((20 ** (x / 16) - 1) / (20 - 1), 5)
    ).mean()
    return metric
