import os
import torch
import numpy as np
import pandas as pd
from datetime import timedelta
from sklearn.neighbors import KDTree


def add_pool_feats_to_group(group, pool_feats, feature_name, lag, times, year):
    if year not in group["dt"].dt.year.unique():
        return group
    dt = group["dt"].dt.date.values[0] - timedelta(days=lag)
    time_index = np.where(times == dt)[0]
    if len(time_index) != 0:
        grid_indexes = group.grid_index.values
        group[[f"{feature_name}_lag{lag}"]] = (
            pool_feats[time_index[0]][grid_indexes].numpy().T
        )
    return group


def add_pooling_features(df, path_to_pooling, count_lag):
    for file_name in [el for el in os.listdir(path_to_pooling) if el.endswith("pt")]:
        year = int(file_name.split("_")[1])
        feature_name = "_".join(file_name.split("_")[2:]).split(".")[0]
        if year in df["dt"].dt.year.unique():
            times = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31").date
            pool_feats = torch.load(os.path.join(path_to_pooling, file_name))
            for lag in range(count_lag + 1):
                df = df.groupby(["dt", df["dt"].dt.year]).apply(
                    add_pool_feats_to_group,
                    pool_feats,
                    feature_name,
                    lag,
                    times,
                    year,
                )
    return df


def add_cat_date_features(df):
    df["month"] = df["dt"].dt.month
    df["day"] = df["dt"].dt.day
    df["weekofyear"] = df["dt"].dt.weekofyear
    df["dayofweek"] = df["dt"].dt.week
    return df


def add_geo_features(df, cities_df):
    df = df.copy()
    temp = df.drop_duplicates(subset=["grid_index"])
    feats_from_cities_df = [
        "name",
        "population",
        "population:date",
        "place",
        "city_lon",
        "city_lat",
    ]
    temp = temp.merge(
        cities_df[feats_from_cities_df + ["grid_index"]], how="left", on=["grid_index"]
    )
    temp = (
        temp.sort_values(by=["population"], ascending=False)
        .drop_duplicates(subset=["grid_index"], keep="first")
        .reset_index(drop=True)
    )
    temp.loc[temp.place.notna(), "distance_to_nearest_city"] = 0
    for dim in ["lon", "lat"]:
        temp[f"{dim}_center"] = temp[[f"{dim}_min", f"{dim}_max"]].mean(axis=1)

    kd_tree = KDTree(cities_df[["city_lon", "city_lat"]])

    indices_list = []
    distances_list = []
    ind_list = []
    for (ind, row) in temp[temp.place.isna()].iterrows():
        indices, distances = kd_tree.query_radius(
            [[row["lon_center"], row["lat_center"]]],
            5,
            return_distance=True,
            sort_results=True,
        )
        if len(distances[0]) > 0:
            distances_list.append(distances[0][0])
            indices_list.append(indices[0][0])
            ind_list.append(ind)

    temp.loc[temp.index.isin(ind_list), "distance_to_nearest_city"] = distances_list
    temp.loc[temp.index.isin(ind_list), feats_from_cities_df] = cities_df.iloc[
        indices_list, :
    ][feats_from_cities_df].values

    df = df.merge(
        temp[feats_from_cities_df + ["grid_index", "distance_to_nearest_city"]],
        how="left",
        on="grid_index",
    )
    df.place = df.place.fillna("nan")
    return df
