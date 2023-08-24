import os
import numpy as np
import joblib
import pandas as pd
from skimage.transform import resize
from skimage.io import imread
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report 

Categories = ['cat', 'dog']
Categories_folders = ['PetImages/cat', 'PetImages/dog']
flat_data_arr = []
target_arr = [] 

for category, path in zip(Categories, Categories_folders):
    for img in os.listdir(path):
        if img.endswith(".jpg"):
            img_array = imread(os.path.join(path, img))
            img_resized = resize(img_array, (150, 150, 3))
            flat_data_arr.append(img_resized.flatten())
            target_arr.append(Categories.index(category))
flat_data = np.array(flat_data_arr)
target = np.array(target_arr)

df = pd.DataFrame(flat_data)
df['Target'] = target

x = df.iloc[:, :-1]
y = df.iloc[:, -1]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20,
                                                    random_state=77,
                                                    stratify=y)

rf_classifier = RandomForestClassifier(n_estimators=100, random_state=77, ccp_alpha= 0.01)
rf_classifier.fit(x_train, y_train)

model_filename = "rf_model.joblib"
joblib.dump(rf_classifier, model_filename)
y_pred = rf_classifier.predict(x_test)

print(classification_report(y_test, y_pred, target_names=['cat', 'dog']))
