# catdog
Котопёс

generate_input.py - генерация input.json

train_rf.py - тренировка модели для задачи классифкации(есть тренированная модель выгруженная с помощью joblib)

rf_model.joblib - тренированная модель Random Forest Classifier

catdog.py - основной скрипт, принимает input.json, генерит output.json согласно задаче(использует rf_model.joblib)
