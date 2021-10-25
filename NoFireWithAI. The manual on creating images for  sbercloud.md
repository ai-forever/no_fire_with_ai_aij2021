NoFireWithAI. The manual on creating Docker images for `sbercloud`
=================================

## 1. Basic images
 - In the file [metadata.json](https://github.com/sberbank-ai/no_fire_with_ai_aij2021/blob/main/metadata.json) as the value of the key **"image"** can specify one of [basic images for training](https://docs.sbercloud.ru/aicloud/mlspace/concepts/environments__basic-images-for-training.html).  
 (или же на платформу `sbercloud` you can push your own custom image to avoid mistakes, **recommended to inherit from basic images**)
 
 ## 2. Loading the base image on the local machine from `sbercloud`
 - `docker login cr.msk.sbercloud.ru` - execute a command, login to `sbercloud`
 ```
        Username: aijcontest
        Password: AIjcontest21

```
- `docker pull cr.msk.sbercloud.ru/aicloud-base-images/horovod-cuda10.2` - command to load the container on the local machine
- `docker run -it cr.msk.sbercloud.ru/aicloud-base-images/horovod-cuda10.2 pip freeze` - on command you can see which libraries in the image

## 3. Создание своего кастомного образа
- `docker build --tag SOURCE_IMAGE[:TAG] .` - command to build your image (can be inherited from basic images, see p.1) from the directory with your **Dockerfile**; **SOURCE_IMAGE[:TAG]** - your name for the image
- `docker tag SOURCE_IMAGE[:TAG] cr.msk.sbercloud.ru/aijcontest2021/{REPOSITORY}[:TAG]` - command to create a tag for `sbercloud`, which will refer to your image, created in the previous command; **{REPOSITORY}[:TAG]** - you have to specify the name of, for example, your command **team1-nofirewithai:f66e1b5f-1269**

## 4. Загрузка вашего кастомного образа на `sbercloud`
- `docker push cr.msk.sbercloud.ru/aijcontest2021/REPOSITORY[:TAG]` - push command for your custom image on the platform `sbercloud`. Now you can specify this image in the file `metadata.json`, by the key **"image"**.

## Примечание

- In the image `cr.msk.sbercloud.ru/aicloud-base-images/horovod-cuda10.2` library  **tensorflow** not installed, details of the reference to basic images p.1
- Currently no support on the platform **cuda >=11.0**
