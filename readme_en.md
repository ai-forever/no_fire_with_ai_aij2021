NoFireWithAI: predicting fire hazard
=================================
[link to github](https://github.com/sberbank-ai/no_fire_with_ai_aij2021/blob/main/readme_en.md)

Competition between algorithms that predict fire hazard in the region for eight days ahead. 

Participants are suggested to predict a fire in a particular region of Russia using various freely accessible data.

## Task setting

Divide the area of Russia into cells of 0.2x0.2 degrees in size and mark each cell with either fire tag or no-fire tag for a particular date. Therefore, we will get a set of rectangles tagged 1 if there was fire on that day, and a set of squares tagged 0 if not.

We need to develop an algorithm that predicts fires (0 or 1) for 1, 2, 3, 4, 5, 6, 7 and 8 days ahead for a particular cell on a particular day. The solution is to be implemented as a program that accepts a CSV table with the following columns as input:  
```
id - id if a line for assessing predictions
dt - date  
lon_min - minimum longitude of a cell  
lat_min - minimum latitude of a cell  
lon_max - maximum longitude of a cell  
lat_max - maximum latitude of a cell 
lon - longitude of a fire in a cell on a particular date (if there was no fire, this is empty)  
lat - latitude of a fire in a cell on a particular date (if there was no fire, this is empty)  
grid_index - cell index
type_id - fire type (if there was no fire, this is empty)  
type_name - fire type description (if there was no fire, this is empty).  
```

The output should be a table specifying, for each cell (lines - id  from an input file), 8 numbers (0 or 1) to denote a fire in 1, 2, 3, 4, 5, 6, 7 and 8 days, respectively. Participants should send the algorithm code in ZIP format to the testing system. Solutions shall be run by Docker in the offline mode.

Additional data accessible to participants during model training and inference in the testing system could be:


- Initial data on the occurred fires - [train_raw.csv](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/train_raw.csv)  
- Example of a table for which it is necessary to generate fires forecasts - [sample_test.csv](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/sample_test.csv)  
- Preprocessed raw data described in the base solution - [train.csv](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/train.csv)  
- Data [openstreetmap](https://www.openstreetmap.org)  - [russia-latest.osm.pbf](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/russia-latest.osm.pbf)
- Data on inhabited locality of the Russian Federation (https://wiki.openstreetmap.org/wiki/RU:Key:place) - [city_town_village.geojson](https://dsworks.s3pd01.sbercloud.ru/aij2021/NoFireWithAI/city_town_village.geojson)  
- Reanalysis data obtained from Copernicus.eu ([ERA5](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land)  — reanalysis data "(2019): ERA5-Land hourly data from 1981 to present. Copernicus Climate Change Service (C3S) Climate Data Store (CDS)". ) The detailed content of the dataset is given in [input/README.md](https://github.com/sberbank-ai/no_fire_with_ai_aij2021/blob/main/input/README.md)  


Participants may also use any open data sources for model training, such as satellite photos or fire hazard indices. However, you should bear in mind that, after the solution is uploaded into the testing system, it will work offline, so all extra data needed for prediction should be packed into a Docker container.


## Solution format

Participants should send the algorithm code in ZIP format to the testing system. Solutions shall be run by Docker in the offline mode. The testing time and resources are limited. Participants do not need to study the Docker technology.

### Container content

The archive root must contain the metadata.json file containing the following:
```json
{
    "image": "cr.msk.sbercloud.ru/aicloud-base-images-test/custom/aij2021/infire:f66e1b5f-1269",
    "entrypoint": "python3 /home/jovyan/solution.py"
}
```

Where `image` is a field with the docker image name, in which the solution will be run, entrypoint is a command that runs the solution. For solution, the archive root will be the current directory. 

To run solutions, existing environments can be used:

- `cr.msk.sbercloud.ru/aicloud-base-images-test/custom/aij2021/infire:f66e1b5f-1269` — [Dockerfile](https://github.com/sberbank-ai/no_fire_with_ai_aij2021/blob/main/Dockerfile) with the description of the image and [requirements](https://github.com/sberbank-ai/no_fire_with_ai_aij2021/blob/main/requirements.txt) with libraries

Any other image which is available in `sbercloud` will be suitable. If necessary, you can prepare your own image, add necessary software and libraries to it (see [the manual on creating Docker images for `sbercloud`](https://github.com/sberbank-ai/no_fire_with_ai_aij2021/blob/main/sbercloud_instruction.md)); to use it, you will need to publish it on `sbercloud`.

### Limitations

During one day, a Participant or a Team of Participants can upload no more than five solutions for evaluation. Only valid attempts that have received a numerical estimate are taken into account.  

The solution container will be run under the following conditions:

- 16 GB RAM;
- 4 vCPU;
- 1 GPU Tesla V100 32 Gb;
- Time for performance: 30m;
- Offline solution;
- Maximal size of your solution archive compressed and decompressed: 10 GB;
- Maximal size of the Docker image used: 15 GB.

## Quality check


The solution shall be evaluated against a lazy fetch.  

The goal of this competition is to find a solution to predict fires. This is not a priority to assess how soon a fire is extinguished, as this depends on many factors. So the metric should use the fire starting tags only. After the first fire starting tag (i.e. first"1" appearing in the forecast), we will consider the cell being ‘on fire’ in the remaining days:  

![Corrected forecast](https://raw.githubusercontent.com/sberbank-ai/no_fire_with_ai_aij2021/main/input/burned_cells.png)



In general, the formula for the metric is as follows:
```
total_error = 1 - sum((C**(penalty_i / 16) - 1) / (C-1)) / N

penalty_i = (-2) * (sum(gt_corr_i) - sum(pred_corr_i)), penalty for the i-th row if the fire happened earlier than predicted
penalty_i = (sum(gt_corr_i) - sum(pred_corr_i)), in another case

where N is the number of rows in the forecast,
С=5 - is the normalization factor, 
pred_corr_i - is adjusted fire forecast for the i-th row,
gt_corr_i - is the corrected actual state of the i-th row.
```

You may choose three solutions to submit for the final assessment. By default, these will be solutions with the best public Leaderboard metric (The best metric value is → 1, the worst is → 0). Higher metric values mean higher results. If two or more participants have the same metric values, the solution uploaded to the system earlier is preferred.

## Prize pool

1st place - RUB 500,000;  
2nd place - RUB 250,000;  
3rd place - RUB 150,000;  

In addition, there is the possibility to be awarded with a special prize of RUB 100,000 given by the panel of experts, which assesses the applicability of solutions to predict dangerous fires. The panel will consider, among others, the following factors:

- transparent reasoning of the model;
- possibility to determine the importance of attributes used;
- total number of attributes and attribute preparation time;
- speed of the model operation and its size.

To be eligible for the special prize, participants should:
- be in Top10 in the leaderboard;
- submit a reproducible solution to train models used in their best attempt.


##
[Terms of use](https://api.dsworks.ru/dsworks-transfer/api/v1/public/file/terms_of_use_en.pdf/download)  
[Rules](https://api.dsworks.ru/dsworks-transfer/api/v1/public/file/rules_en.pdf/download)
