NoFireWithAI. Описание данных
=================================

В качестве данных, доступных участникам как на момент обучения моделей, так и в момент инференса в проверяющей системе, могут быть использованы: 

- Исходные данные по произошедшим [пожарам](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/train_raw.csv);
- Данные [openstreetmap](https://www.openstreetmap.org)  - [russia-latest.osm.pbf](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/russia-latest.osm.pbf)
- Данные по населённым пунктам РФ (https://wiki.openstreetmap.org/wiki/RU:Key:place) - [city_town_village.geojson](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/city_town_village.geojson)
 - Данные реанализа, полученные от Copernicus.eu ([ERA5](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land)  — данные реанализа "(2019): ERA5-Land hourly data from 1981 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS)". ) 



## Данные реанализа:

Датасет содержит климатические данные в формате .grib за 2018 - 2021 гг. Пример работы с этим форматом приведён в базовом решении к данному соревнованию.
Перечисленные ниже файлы будут доступны при запуске решений в проверяющей системе по адресу:  
**input/ERA5_data/** :

| Файл | климатические данные ([описание переменных](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land)) | год |
|--|--|--|
| [temp_2018](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/temp_2018.grib) |2m dewpoint temperature, 2m temperature, Skin temperature, Soil temperature level 1| 2018|
| [temp_2019](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/temp_2019.grib) |2m dewpoint temperature, 2m temperature, Skin temperature, Soil temperature level 1| 2019|
| [temp_2020](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/temp_2020.grib) |2m dewpoint temperature, 2m temperature, Skin temperature, Soil temperature level 1| 2020|
| [temp_2021](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/temp_2021.grib) |2m dewpoint temperature, 2m temperature, Skin temperature, Soil temperature level 1| 2021|
| [wind_2018](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/wind_2018.grib) |10m u-component of wind, 10m v-component of wind, Surface pressure, Total precipitation| 2018|
| [wind_2019](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/wind_2019.grib) |10m u-component of wind, 10m v-component of wind, Surface pressure, Total precipitation| 2019|
| [wind_2020](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/wind_2020.grib) |10m u-component of wind, 10m v-component of wind, Surface pressure, Total precipitation| 2020|
| [wind_2021](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/wind_2021.grib) |10m u-component of wind, 10m v-component of wind, Surface pressure, Total precipitation| 2021|
| [vegetation_2018](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/vegetation_2018.grib) |Leaf area index, high vegetation, Leaf area index, low vegetation| 2018|
| [vegetation_2019](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/vegetation_2019.grib) |Leaf area index, high vegetation, Leaf area index, low vegetation| 2019|
| [vegetation_2020](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/vegetation_2020.grib) |Leaf area index, high vegetation, Leaf area index, low vegetation| 2020|
| [vegetation_2021](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/vegetation_2021.grib) |Leaf area index, high vegetation, Leaf area index, low vegetation| 2021|
| [heat1_2018](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/heat1_2018.grib) |Forecast albedo, Surface latent heat flux, Surface net solar radiation, Surface net thermal radiation| 2018|
| [heat1_2019](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/heat1_2019.grib) |Forecast albedo, Surface latent heat flux, Surface net solar radiation, Surface net thermal radiation| 2019|
| [heat1_2020](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/heat1_2020.grib) |Forecast albedo, Surface latent heat flux, Surface net solar radiation, Surface net thermal radiation| 2020|
| [heat1_2021](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/heat1_2021.grib) |Forecast albedo, Surface latent heat flux, Surface net solar radiation, Surface net thermal radiation| 2021|
| [heat2_2018](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/heat2_2018.grib) |Surface sensible heat flux, Surface solar radiation downwards, Surface thermal radiation downwards| 2018|
| [heat2_2019](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/heat2_2019.grib) |Surface sensible heat flux, Surface solar radiation downwards, Surface thermal radiation downwards| 2019|
| [heat2_2020](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/heat2_2020.grib) |Surface sensible heat flux, Surface solar radiation downwards, Surface thermal radiation downwards| 2020|
| [heat2_2021](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/heat2_2021.grib) |Surface sensible heat flux, Surface solar radiation downwards, Surface thermal radiation downwards| 2021|
| [evaporation1_2018](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/evaporation1_2018.grib) |Evaporation from bare soil, Evaporation from the top of canopy, Evaporation from vegetation transpiration, Potential evaporation, Total evaporation| 2018|
| [evaporation1_2019](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/evaporation1_2019.grib) |Evaporation from bare soil, Evaporation from the top of canopy, Evaporation from vegetation transpiration, Potential evaporation, Total evaporation| 2019|
| [evaporation1_2020](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/evaporation1_2020.grib) |Evaporation from bare soil, Evaporation from the top of canopy, Evaporation from vegetation transpiration, Potential evaporation, Total evaporation| 2020|
| [evaporation1_2021](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/evaporation1_2021.grib) |Evaporation from bare soil, Evaporation from the top of canopy, Evaporation from vegetation transpiration, Potential evaporation, Total evaporation| 2021|
| [evaporation2_2018](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/evaporation2_2018.grib) |Runoff, Sub-surface runoff, Surface runoff| 2018|
| [evaporation2_2019](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/evaporation2_2019.grib) |Runoff, Sub-surface runoff, Surface runoff| 2019|
| [evaporation2_2020](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/evaporation2_2020.grib) |Runoff, Sub-surface runoff, Surface runoff| 2020|
| [evaporation2_2021](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/evaporation2_2021.grib) |Runoff, Sub-surface runoff, Surface runoff| 2021|
