import os
import gc
import torch
import numpy as np
import torch.nn as nn
import geopandas as gpd
import cfgrib
import helpers


def prepare_cities(path_to_input, lat_min, lat_max, lon_min, lon_max, step):
    array_of_lats = np.arange(lat_min, lat_max, step).round(1)
    array_of_lons = np.arange(lon_min, lon_max, step).round(1)
    cities_df = gpd.read_file(os.path.join(path_to_input, "city_town_village.geojson"))
    cities_df = cities_df[
        ["admin_level", "name", "population", "population:date", "place", "geometry"]
    ]
    cities_df = cities_df[cities_df.place != "city_block"].reset_index(drop=True)
    cities_df["lon"] = cities_df["geometry"].x
    cities_df["lat"] = cities_df["geometry"].y

    cities_df.loc[cities_df.lon < 0, "lon"] += 360
    cities_df.loc[cities_df.population.notna(), "population"] = (
        cities_df[cities_df.population.notna()]
        .population.apply(helpers.split_string)
        .str.replace(" ", "")
        .astype(int)
    )
    cities_df = helpers.add_edges_polygon(cities_df)
    cities_df = cities_df[
        (cities_df.lon_max <= lon_max)
        & (cities_df.lon_min >= lon_min)
        & (cities_df.lat_min >= lat_min)
        & (cities_df.lat_max <= lat_max)
    ].reset_index(drop=True)
    cities_df = helpers.get_grid_index(cities_df, array_of_lons, array_of_lats)
    cities_df.rename(columns={"lon": "city_lon", "lat": "city_lat"}, inplace=True)
    return cities_df


def parse_dims(ds):
    times = ds[0].indexes["time"]
    latitudes = ds[0].indexes["latitude"]
    longitudes = ds[0].indexes["longitude"]
    return times, latitudes, longitudes


def parse_cube(ds):
    features_values = {}
    for ds_part in ds:
        for feature_name in ds_part.data_vars.variables:
            features_values[feature_name] = ds_part[feature_name].data
    return features_values


def save_to_tensors(ds, path_to_pooling, file_name):
    for ds_part in ds:
        for feature_name in ds_part.keys():
            feat_tensor = feat_to_tensor(ds_part[feature_name].data)
            make_max_pool_feats(feat_tensor, path_to_pooling, file_name, feature_name)
            make_avg_pool_feats(feat_tensor, path_to_pooling, file_name, feature_name)
            del feat_tensor
            gc.collect()


def feat_to_tensor(feat_numpy):
    feat_tensor = torch.from_numpy(feat_numpy).unsqueeze(1)
    feat_tensor = nn.functional.pad(feat_tensor, (0, 0, 1, 0), mode="replicate")
    feat_tensor = torch.flip(feat_tensor, [2])
    return feat_tensor


def make_avg_pool_feats(feat_tensor, path_to_pooling, file_name, feat_name):
    feat_tensor = nn.functional.avg_pool2d(feat_tensor, kernel_size=3, stride=2)
    feat_tensor = feat_tensor.reshape(feat_tensor.shape[0], -1)
    torch.save(
        feat_tensor,
        os.path.join(path_to_pooling, f"{file_name}_avg_pool_{feat_name}.pt"),
    )
    del feat_tensor


def make_max_pool_feats(feat_tensor, path_to_pooling, file_name, feat_name):
    feat_tensor = nn.functional.max_pool2d(feat_tensor, kernel_size=3, stride=2)
    feat_tensor = feat_tensor.reshape(feat_tensor.shape[0], -1)
    torch.save(
        feat_tensor,
        os.path.join(path_to_pooling, f"{file_name}_max_pool_{feat_name}.pt"),
    )
    del feat_tensor


def make_pool_features(path_to_gribs, file_name, path_to_pooling):
    if not os.path.exists(path_to_pooling):
        os.mkdir(path_to_pooling)
    ds = cfgrib.open_datasets(os.path.join(path_to_gribs, f"{file_name}.grib"))
    save_to_tensors(ds, path_to_pooling, file_name)
