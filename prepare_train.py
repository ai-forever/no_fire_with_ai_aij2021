from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, MultiPolygon
from countryinfo import CountryInfo
import pandas as pd
import numpy as np
import helpers


def load_and_prepare_targets(path):
    df = pd.read_csv(path, parse_dates=["dt"])
    df = df.drop_duplicates(subset=["dt", "lon", "lat"]).reset_index(drop=True)
    df = helpers.add_edges_polygon(df)
    df = df.drop_duplicates(
        subset=["dt", "lon_min", "lon_max", "lat_min", "lat_max"]
    ).reset_index(drop=True)
    return df


def make_grid(df, array_of_lats, array_of_lons, step):
    mesh = np.meshgrid(array_of_lons, array_of_lats)
    grid_df = pd.DataFrame(
        np.vstack([mesh[0].ravel(), mesh[1].ravel()]).T, columns=["lon_min", "lat_min"]
    )
    grid_df["lon_max"] = grid_df["lon_min"] + step
    grid_df["lat_max"] = grid_df["lat_min"] + step
    grid_df[["lon_min", "lat_min", "lon_max", "lat_max"]] = grid_df[
        ["lon_min", "lat_min", "lon_max", "lat_max"]
    ].round(1)
    return grid_df


def add_check_for_land(grid_df, targets):
    grid_df["is_land"] = 0
    land = (
        targets[["lon_min", "lon_max", "lat_min", "lat_max"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    grid_df = grid_df.merge(
        land,
        how="left",
        on=["lon_min", "lon_max", "lat_min", "lat_max"],
        indicator=True,
    )
    grid_df.loc[(grid_df._merge == "both"), "is_land"] = 1
    grid_df.drop(columns=["_merge"], inplace=True)
    return grid_df


def make_and_prepare_grid_df(targets, array_of_lons, array_of_lats, step):
    grid_df = make_grid(targets, array_of_lats, array_of_lons, step)
    grid_df = helpers.get_grid_index(grid_df, array_of_lons, array_of_lats)
    grid_df = add_check_for_land(grid_df, targets)
    return grid_df


def explode_dates(targets, df, start_date="2018-01-01"):
    dates = pd.date_range(start_date, targets["dt"].max())
    s = pd.Series(dtype="object")
    for idx in range(df.shape[0]):
        s.at[idx] = dates
    df["dt"] = s
    df = df.explode("dt")
    return df


def get_infire(targets, df):
    df = df.merge(
        targets[
            [
                "lon_min",
                "lat_min",
                "lon_max",
                "lat_max",
                "dt",
                "type_id",
                "type_name",
                "lon",
                "lat",
            ]
        ],
        how="left",
        on=["lon_min", "lat_min", "lon_max", "lat_max", "dt"],
    )
    df.loc[df.type_name.isna(), "infire"] = 0
    df.infire = df.infire.fillna(1).astype(int)
    return df


def build_targets(df, count_targets=8):
    for i in range(1, count_targets + 1):
        df[f"infire_day_{i}"] = df.groupby(
            ["lon_min", "lat_min", "lon_max", "lat_max"]
        ).infire.shift(-i)
    return df


def make_df_only_land(grid_df, targets, start_date):
    df = grid_df[grid_df.is_land == 1].reset_index(drop=True)
    df = explode_dates(targets, df, start_date)
    df = get_infire(targets, df)
    df = build_targets(df)

    is_ones = df[
        (df["infire"] == 1)
        | (df["infire_day_1"] == 1)
        | (df["infire_day_2"] == 1)
        | (df["infire_day_3"] == 1)
        | (df["infire_day_4"] == 1)
        | (df["infire_day_5"] == 1)
        | (df["infire_day_6"] == 1)
        | (df["infire_day_7"] == 1)
        | (df["infire_day_8"] == 1)
    ]

    np.random.seed(1)
    only_zeros = df[
        (df["infire"] == 0)
        & (df["infire_day_1"] == 0)
        & (df["infire_day_2"] == 0)
        & (df["infire_day_3"] == 0)
        & (df["infire_day_4"] == 0)
        & (df["infire_day_5"] == 0)
        & (df["infire_day_6"] == 0)
        & (df["infire_day_7"] == 0)
        & (df["infire_day_8"] == 0)
    ]

    only_zeros = only_zeros.sample(is_ones.shape[0] // 3).reset_index(drop=True)

    df = pd.concat([is_ones, only_zeros]).sort_values(by=["grid_index", "dt"])
    df.dropna(subset=[f"infire_day_{i}" for i in range(1, 9)], inplace=True)
    df[[f"infire_day_{i}" for i in range(1, 9)]] = df[
        [f"infire_day_{i}" for i in range(1, 9)]
    ].astype(int)
    df.reset_index(drop=True, inplace=True)

    df["is_land"] = True
    df_is_land = df[
        [
            "dt",
            "lon_min",
            "lat_min",
            "lon_max",
            "lat_max",
            "lon",
            "lat",
            "grid_index",
            "type_id",
            "type_name",
            "is_land",
        ]
        + [f"infire_day_{i}" for i in range(1, 9)]
    ]
    return df_is_land


def make_df_not_land(grid_df, targets, df_is_land, start_date):
    df = grid_df[grid_df.is_land == 0].reset_index(drop=True)

    np.random.seed(17)
    df = explode_dates(targets, df, start_date)
    df = df.sample(df_is_land.shape[0]).reset_index(drop=True)
    df[[f"infire_day_{i}" for i in range(1, 9)]] = 0
    df[["lon", "lat", "type_id", "type_name"]] = np.nan
    df["is_land"] = False
    df_not_land = df[
        [
            "dt",
            "lon_min",
            "lat_min",
            "lon_max",
            "lat_max",
            "lon",
            "lat",
            "grid_index",
            "type_id",
            "type_name",
            "is_land",
        ]
        + [f"infire_day_{i}" for i in range(1, 9)]
    ]
    return df_not_land


def is_point_within_Russia(point, borders) -> bool:
    polygon = MultiPolygon(borders)
    return boolean_point_in_polygon(point, polygon)


def add_russia_flag_to_point(df, borders):
    df["lat_center"] = ((df["lat_max"] + df["lat_max"]) / 2).round(1)
    df["lon_center"] = ((df["lon_min"] + df["lon_max"]) / 2).round(1)
    temp = df[["lat_center", "lon_center"]].drop_duplicates()
    temp["is_point_within_Russia"] = temp.apply(
        lambda x: is_point_within_Russia(
            Point((x["lon_center"], x["lat_center"])), borders
        ),
        axis=1,
    )
    df = df.merge(temp, how="left")
    return df


def make_train(path, array_of_lons, array_of_lats, step, start_date):
    # Подготавливаем сырые данные от МЧС/ Создаем границы для точки пожара с шагом 0.2
    targets = load_and_prepare_targets(path)

    # Создаем ячейки для сетки с шагом 0.2 на 0.2, добавляем grid_index, добавляем флаг суша/не суша
    # Считаем за сушу те ячейки, которые когда-либо горели
    grid_df = make_and_prepare_grid_df(targets, array_of_lons, array_of_lats, step)

    # Объединяем ячейки на суше с таргетами, берем все пожары и случайно те даты, в которых не было пожаров
    df_is_land = make_df_only_land(grid_df, targets, start_date)

    # Объединяем ячейки не на суше с таргетами, берем точно такое же кол-во строк
    # как и в df_is_land, проставляем в таргеты нули
    df_not_land = make_df_not_land(grid_df, targets, df_is_land, start_date)
    train = (
        pd.concat([df_is_land, df_not_land])
        .sort_values(by=["grid_index", "dt"])
        .reset_index(drop=True)
    )

    # Убираем ячейки не из России
    country = CountryInfo("Russia")
    russia = country.geo_json()
    borders = russia["features"][0]["geometry"]["coordinates"]
    train = add_russia_flag_to_point(train, borders)
    train = train[train.is_point_within_Russia == True].reset_index(drop=True)
    train.drop(
        ["lat_center", "lon_center", "is_point_within_Russia"], axis=1, inplace=True
    )
    return train
