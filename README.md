# catdog
Котопёс

generate_input.py - генерация input.json

train_rf.py - тренировка модели для задачи классифкации(есть тренированная модель выгруженная с помощью joblib)

rf_model.joblib - тренированная модель Random Forest Classifier

catdog.py - основной скрипт, принимает input.json, генерит output.json согласно задаче(использует rf_model.joblib)

Датасет должен быть организован в след.формате: PetImages/cat, PetImages/dog

Датасет и input.json генерированный с помощью этого датасета досутпен по ссылке https://drive.google.com/drive/folders/1mmy3QgpxrPi2i8rIU6EbkaV4NWw66v_W?usp=sharing

