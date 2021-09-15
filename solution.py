import os
import time
import pickle
import pathlib
import logging
import warnings
import pandas as pd
import preprocessing, features_generation

warnings.simplefilter("ignore")

logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d,%H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


BASE_DIR = pathlib.Path(__file__).parent
PATH_TO_INPUT = BASE_DIR / "input/"
PATH_TO_MODELS = BASE_DIR / "models/"
PATH_TO_OUTPUT = BASE_DIR / "output/"
PATH_TO_ADD_DATA = BASE_DIR / "additional_data/"
LAT_MIN, LAT_MAX, LON_MIN, LON_MAX, STEP = 41.0, 81.5, 19.0, 169.0, 0.2

FEATURES = [
    "max_pool_ssro_lag0",
    "max_pool_ssro_lag1",
    "max_pool_ssro_lag2",
    "max_pool_ssro_lag3",
    "max_pool_ssr_lag0",
    "max_pool_ssr_lag1",
    "max_pool_ssr_lag2",
    "max_pool_ssr_lag3",
    "max_pool_t2m_lag0",
    "max_pool_t2m_lag1",
    "max_pool_t2m_lag2",
    "max_pool_t2m_lag3",
    "avg_pool_sshf_lag0",
    "avg_pool_sshf_lag1",
    "avg_pool_sshf_lag2",
    "avg_pool_sshf_lag3",
    "avg_pool_lai_lv_lag0",
    "avg_pool_lai_lv_lag1",
    "avg_pool_lai_lv_lag2",
    "avg_pool_lai_lv_lag3",
    "max_pool_strd_lag0",
    "max_pool_strd_lag1",
    "max_pool_strd_lag2",
    "max_pool_strd_lag3",
    "avg_pool_stl1_lag0",
    "avg_pool_stl1_lag1",
    "avg_pool_stl1_lag2",
    "avg_pool_stl1_lag3",
    "max_pool_evabs_lag0",
    "max_pool_evabs_lag1",
    "max_pool_evabs_lag2",
    "max_pool_evabs_lag3",
    "max_pool_evavt_lag0",
    "max_pool_evavt_lag1",
    "max_pool_evavt_lag2",
    "max_pool_evavt_lag3",
    "max_pool_sro_lag0",
    "max_pool_sro_lag1",
    "max_pool_sro_lag2",
    "max_pool_sro_lag3",
    "avg_pool_pev_lag0",
    "avg_pool_pev_lag1",
    "avg_pool_pev_lag2",
    "avg_pool_pev_lag3",
    "max_pool_ro_lag0",
    "max_pool_ro_lag1",
    "max_pool_ro_lag2",
    "max_pool_ro_lag3",
    "avg_pool_ssro_lag0",
    "avg_pool_ssro_lag1",
    "avg_pool_ssro_lag2",
    "avg_pool_ssro_lag3",
    "max_pool_pev_lag0",
    "max_pool_pev_lag1",
    "max_pool_pev_lag2",
    "max_pool_pev_lag3",
    "avg_pool_ssrd_lag0",
    "avg_pool_ssrd_lag1",
    "avg_pool_ssrd_lag2",
    "avg_pool_ssrd_lag3",
    "max_pool_e_lag0",
    "max_pool_e_lag1",
    "max_pool_e_lag2",
    "max_pool_e_lag3",
    "max_pool_lai_lv_lag0",
    "max_pool_lai_lv_lag1",
    "max_pool_lai_lv_lag2",
    "max_pool_lai_lv_lag3",
    "avg_pool_sro_lag0",
    "avg_pool_sro_lag1",
    "avg_pool_sro_lag2",
    "avg_pool_sro_lag3",
    "max_pool_v10_lag0",
    "max_pool_v10_lag1",
    "max_pool_v10_lag2",
    "max_pool_v10_lag3",
    "max_pool_d2m_lag0",
    "max_pool_d2m_lag1",
    "max_pool_d2m_lag2",
    "max_pool_d2m_lag3",
    "avg_pool_evatc_lag0",
    "avg_pool_evatc_lag1",
    "avg_pool_evatc_lag2",
    "avg_pool_evatc_lag3",
    "avg_pool_strd_lag0",
    "avg_pool_strd_lag1",
    "avg_pool_strd_lag2",
    "avg_pool_strd_lag3",
    "avg_pool_d2m_lag0",
    "avg_pool_d2m_lag1",
    "avg_pool_d2m_lag2",
    "avg_pool_d2m_lag3",
    "max_pool_str_lag0",
    "max_pool_str_lag1",
    "max_pool_str_lag2",
    "max_pool_str_lag3",
    "avg_pool_fal_lag0",
    "avg_pool_fal_lag1",
    "avg_pool_fal_lag2",
    "avg_pool_fal_lag3",
    "avg_pool_sp_lag0",
    "avg_pool_sp_lag1",
    "avg_pool_sp_lag2",
    "avg_pool_sp_lag3",
    "avg_pool_slhf_lag0",
    "avg_pool_slhf_lag1",
    "avg_pool_slhf_lag2",
    "avg_pool_slhf_lag3",
    "max_pool_sshf_lag0",
    "max_pool_sshf_lag1",
    "max_pool_sshf_lag2",
    "max_pool_sshf_lag3",
    "avg_pool_tp_lag0",
    "avg_pool_tp_lag1",
    "avg_pool_tp_lag2",
    "avg_pool_tp_lag3",
    "avg_pool_str_lag0",
    "avg_pool_str_lag1",
    "avg_pool_str_lag2",
    "avg_pool_str_lag3",
    "max_pool_skt_lag0",
    "max_pool_skt_lag1",
    "max_pool_skt_lag2",
    "max_pool_skt_lag3",
    "avg_pool_t2m_lag0",
    "avg_pool_t2m_lag1",
    "avg_pool_t2m_lag2",
    "avg_pool_t2m_lag3",
    "avg_pool_ssr_lag0",
    "avg_pool_ssr_lag1",
    "avg_pool_ssr_lag2",
    "avg_pool_ssr_lag3",
    "max_pool_evatc_lag0",
    "max_pool_evatc_lag1",
    "max_pool_evatc_lag2",
    "max_pool_evatc_lag3",
    "avg_pool_u10_lag0",
    "avg_pool_u10_lag1",
    "avg_pool_u10_lag2",
    "avg_pool_u10_lag3",
    "max_pool_tp_lag0",
    "max_pool_tp_lag1",
    "max_pool_tp_lag2",
    "max_pool_tp_lag3",
    "avg_pool_evabs_lag0",
    "avg_pool_evabs_lag1",
    "avg_pool_evabs_lag2",
    "avg_pool_evabs_lag3",
    "max_pool_ssrd_lag0",
    "max_pool_ssrd_lag1",
    "max_pool_ssrd_lag2",
    "max_pool_ssrd_lag3",
    "max_pool_stl1_lag0",
    "max_pool_stl1_lag1",
    "max_pool_stl1_lag2",
    "max_pool_stl1_lag3",
    "max_pool_u10_lag0",
    "max_pool_u10_lag1",
    "max_pool_u10_lag2",
    "max_pool_u10_lag3",
    "avg_pool_ro_lag0",
    "avg_pool_ro_lag1",
    "avg_pool_ro_lag2",
    "avg_pool_ro_lag3",
    "max_pool_lai_hv_lag0",
    "max_pool_lai_hv_lag1",
    "max_pool_lai_hv_lag2",
    "max_pool_lai_hv_lag3",
    "avg_pool_e_lag0",
    "avg_pool_e_lag1",
    "avg_pool_e_lag2",
    "avg_pool_e_lag3",
    "avg_pool_skt_lag0",
    "avg_pool_skt_lag1",
    "avg_pool_skt_lag2",
    "avg_pool_skt_lag3",
    "max_pool_sp_lag0",
    "max_pool_sp_lag1",
    "max_pool_sp_lag2",
    "max_pool_sp_lag3",
    "avg_pool_v10_lag0",
    "avg_pool_v10_lag1",
    "avg_pool_v10_lag2",
    "avg_pool_v10_lag3",
    "avg_pool_lai_hv_lag0",
    "avg_pool_lai_hv_lag1",
    "avg_pool_lai_hv_lag2",
    "avg_pool_lai_hv_lag3",
    "max_pool_fal_lag0",
    "max_pool_fal_lag1",
    "max_pool_fal_lag2",
    "max_pool_fal_lag3",
    "max_pool_slhf_lag0",
    "max_pool_slhf_lag1",
    "max_pool_slhf_lag2",
    "max_pool_slhf_lag3",
    "avg_pool_evavt_lag0",
    "avg_pool_evavt_lag1",
    "avg_pool_evavt_lag2",
    "avg_pool_evavt_lag3",
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
    logger.info(f"Start processing")
    logger.info(f"load test")
    test = pd.read_csv(
        os.path.join(PATH_TO_INPUT, "test.csv"),
        index_col="id",
        parse_dates=["dt"],
    )
    logger.info(f"create cities_df")
    cities_df = preprocessing.prepare_cities(
        PATH_TO_INPUT, LAT_MIN, LAT_MAX, LON_MIN, LON_MAX, STEP
    )
    grib_list = [
        el.split(".")[0]
        for el in os.listdir(os.path.join(PATH_TO_INPUT, "ERA5_data"))
        if el.startswith(
            (
                "temp",
                "wind",
                "evaporation1",
                "evaporation2",
                "heat1",
                "heat2",
                "vegetation",
            )
        )
        and el.endswith("2021.grib")
    ]
    for file_name in grib_list:
        logger.info(f"make_pool_features {file_name}")
        preprocessing.make_pool_features(
            os.path.join(PATH_TO_INPUT, "ERA5_data"), file_name, PATH_TO_ADD_DATA
        )
    logger.info(f"add_pooling_features")
    test = features_generation.add_pooling_features(test, PATH_TO_ADD_DATA, count_lag=3)
    logger.info(f"add_cat_date_features")
    test = features_generation.add_cat_date_features(test)
    logger.info(f"add_geo_features")
    test = features_generation.add_geo_features(test, cities_df)

    result_df = pd.DataFrame()
    models = []
    for idx in range(1, 9):
        path_to_model = os.path.join(PATH_TO_MODELS, f"model_{idx}_day.pkl")
        logger.info(f"load model_{idx}_day.pkl")
        with open(path_to_model, "rb") as f:
            logger.info(f"predict for infire_day_{idx}")
            model = pickle.load(f)
        result_df[f"infire_day_{idx}"] = (
            model.predict_proba(test[FEATURES])[:, 1] > 0.51
        ).astype(int)

    logger.info(f"load model_mc.pkl")
    with open(os.path.join(PATH_TO_MODELS, "model_mc.pkl"), "rb") as f:
        meta_model = pickle.load(f)
    logger.info(f"predict for infire_day")
    result_df["infire_day"] = meta_model.predict(test[FEATURES])
    index_to_replace = result_df[
        result_df[[f"infire_day_{day}" for day in range(1, 9)]].sum(axis=1) == 0
    ].index
    logger.info(f"replace by infire_day")
    for i in range(1, 9):
        result_df.loc[
            (result_df.index.isin(index_to_replace) & (result_df["infire_day"] == i)),
            f"infire_day_{i}",
        ] = 1

    logger.info("save output.csv")
    result_df.drop("infire_day", axis=1).to_csv(
        os.path.join(PATH_TO_OUTPUT, "output.csv"), index_label="id"
    )
    t_end = time.time()
    logger.info(f"Processing time: {t_end - t_start}")
