NoFireWithAI. Инструкция по работе со `sbercloud`
=================================

## 1. Базовые образы
 - В файле [metadata.json](https://github.com/sberbank-ai/no_fire_with_ai_aij2021/blob/main/metadata.json) в качестве значения ключа **"image"** может указываться один из [базовых образов для задач обучения](https://docs.sbercloud.ru/aicloud/mlspace/concepts/environments__basic-images-for-training.html).  
 (или же на платформу `sbercloud` можно запушить свой собственный кастомный образ, во избежание ошибок, **рекомендуем наследоваться от базовых образов**)
 
 ## 2. Загрузка базового образа на локальную машину из `sbercloud`
 - `docker login cr.msk.sbercloud.ru` - выполняем команду, логинимся в `sbercloud`
 ```
        Username: aijcontest
        Password: AIjcontest21

```
- `docker pull cr.msk.sbercloud.ru/aicloud-base-images/horovod-cuda10.2` - команда для загрузки контейнера на локальную машину
- `docker run -it cr.msk.sbercloud.ru/aicloud-base-images/horovod-cuda10.2 pip freeze` - по команде можно посмотреть какие библиотеки в образе

## 3. Создание своего кастомного образа
- `docker build --tag SOURCE_IMAGE[:TAG] .` - команда для создания своего образа (можно наследоваться от базовых образов, см. п.1) из директории где находится ваш **Dockerfile**; **SOURCE_IMAGE[:TAG]** - ваше имя для образа
- `docker tag SOURCE_IMAGE[:TAG] cr.msk.sbercloud.ru/aijcontest2021/{REPOSITORY}[:TAG]` - команда для создания тэга для `sbercloud`'а, который будет ссылаться на ваш образ, созданный в предыдущей команде; **{REPOSITORY}[:TAG]** - нужно указать название, например, своей команды **team1-nofirewithai:f66e1b5f-1269**

## 4. Загрузка вашего кастомного образа на `sbercloud`
- `docker push cr.msk.sbercloud.ru/aijcontest2021/REPOSITORY[:TAG]` - команда для push'а вашего кастомного образа на платформу `sbercloud`. Теперь вы можете указывать этот образ в файле `metadata.json`, под ключом **"image"**.

## Примечание

- В образе `cr.msk.sbercloud.ru/aicloud-base-images/horovod-cuda10.2` не установлена библиотека **tensorflow**, подробности по ссылке на базовые образы п.1
- На данный момент на платформе нет поддержки **cuda >=11.0**
