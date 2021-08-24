import os
import time
import pickle
import warnings
import pandas as pd
import preprocessing, features_generation

warnings.simplefilter("ignore")


PATH_TO_INPUT = "input/"
PATH_TO_MODELS = "models/"
PATH_TO_OUTPUT = "output/"
PATH_TO_ADD_DATA = "additional_data/"
LAT_MIN, LAT_MAX, LON_MIN, LON_MAX, STEP = 41.0, 81.5, 19.0, 169.0, 0.2

FEATURES = [
    "avg_pool_stl1_lag0",
    "avg_pool_t2m_lag0",
    "avg_pool_d2m_lag0",
    "avg_pool_skt_lag0",
    "avg_pool_stl1_lag1",
    "avg_pool_t2m_lag1",
    "avg_pool_d2m_lag1",
    "avg_pool_skt_lag1",
    "avg_pool_stl1_lag2",
    "avg_pool_t2m_lag2",
    "avg_pool_d2m_lag2",
    "avg_pool_skt_lag2",
    "avg_pool_stl1_lag3",
    "avg_pool_t2m_lag3",
    "avg_pool_d2m_lag3",
    "avg_pool_skt_lag3",
    "avg_pool_sp_lag0",
    "avg_pool_u10_lag0",
    "avg_pool_v10_lag0",
    "avg_pool_tp_lag0",
    "avg_pool_sp_lag1",
    "avg_pool_u10_lag1",
    "avg_pool_v10_lag1",
    "avg_pool_tp_lag1",
    "avg_pool_sp_lag2",
    "avg_pool_u10_lag2",
    "avg_pool_v10_lag2",
    "avg_pool_tp_lag2",
    "avg_pool_sp_lag3",
    "avg_pool_u10_lag3",
    "avg_pool_v10_lag3",
    "avg_pool_tp_lag3",
    "max_pool_stl1_lag0",
    "max_pool_t2m_lag0",
    "max_pool_d2m_lag0",
    "max_pool_skt_lag0",
    "max_pool_stl1_lag1",
    "max_pool_t2m_lag1",
    "max_pool_d2m_lag1",
    "max_pool_skt_lag1",
    "max_pool_stl1_lag2",
    "max_pool_t2m_lag2",
    "max_pool_d2m_lag2",
    "max_pool_skt_lag2",
    "max_pool_stl1_lag3",
    "max_pool_t2m_lag3",
    "max_pool_d2m_lag3",
    "max_pool_skt_lag3",
    "max_pool_sp_lag0",
    "max_pool_u10_lag0",
    "max_pool_v10_lag0",
    "max_pool_tp_lag0",
    "max_pool_sp_lag1",
    "max_pool_u10_lag1",
    "max_pool_v10_lag1",
    "max_pool_tp_lag1",
    "max_pool_sp_lag2",
    "max_pool_u10_lag2",
    "max_pool_v10_lag2",
    "max_pool_tp_lag2",
    "max_pool_sp_lag3",
    "max_pool_u10_lag3",
    "max_pool_v10_lag3",
    "max_pool_tp_lag3",
    "population",
    "place",
    "distance_to_nearest_city",
    "month",
    "day",
    "weekofyear",
    "dayofweek",
]

if __name__ == "__main__":
    t_start = time.time()
    test, array_of_lats, array_of_lons = preprocessing.prepare_test(
        PATH_TO_INPUT, LAT_MIN, LAT_MAX, LON_MIN, LON_MAX, STEP
    )
    cities_df = preprocessing.prepare_cities(
        PATH_TO_INPUT, LAT_MIN, LAT_MAX, LON_MIN, LON_MAX, array_of_lons, array_of_lats
    )

    features_dict = {}
    grib_list = [
        el.split(".")[0]
        for el in os.listdir(os.path.join(PATH_TO_INPUT, "ERA5_data"))
        if el.startswith(("temp", "wind")) and el.endswith("2021.grib")
    ]
    for file_name in grib_list:
        preprocessing.make_pool_features(
            os.path.join(PATH_TO_INPUT, "ERA5_data"), file_name, PATH_TO_ADD_DATA
        )
    test = features_generation.add_pooling_features(test, PATH_TO_ADD_DATA, count_lag=3)
    test = features_generation.add_cat_date_features(test)
    test = features_generation.add_geo_features(test, cities_df)

    result_df = pd.DataFrame()
    models = []
    for idx in range(1, 9):
        path_to_model = os.path.join(PATH_TO_MODELS, f"model_{idx}_day.pkl")

        with open(path_to_model, "rb") as f:
            model = pickle.load(f)
            models.append(model)
    for idx, model in enumerate(models):
        result_df[f"infire_after_{idx+1}_day"] = model.predict(test[FEATURES])
    result_df.to_csv(os.path.join(PATH_TO_OUTPUT, "output.csv"), index=False)
    t_end = time.time()
    print(t_end - t_start, "ok")
