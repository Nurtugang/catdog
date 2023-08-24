import json
import base64
import numpy as np
from io import BytesIO
import joblib
from PIL import Image
from skimage.transform import resize
from sklearn.metrics import confusion_matrix, precision_score, accuracy_score, f1_score, recall_score

import pandas as pd

from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

rf = joblib.load("rf_model.joblib") #модель классификатора Random Forest

def predict_photo(photo): #перевод с BASE_64 в матричный формат, предсказание и генерация словаря
    img_id = photo["ID"]
    img_base64 = photo["img_code"]
    img_bytes = base64.b64decode(img_base64)
    img = Image.open(BytesIO(img_bytes))
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_resized = resize(img_array, (150, 150, 3))
    l = [img_resized.flatten()]
    probability = rf.predict_proba(l)

    result = {
        "ID": img_id,
        "cat_prob": round(probability[0][0], 1),
        "dog_prob": round(probability[0][1], 1)
    }

    return result

class JSONManipulationResource(Resource):
    def post(self):
        try:
            input_json = request.get_json() 
            
            true_labels = [ 0 if 'cat' in photo["ID"] else 1 for photo in input_json["photos"]]
            df_true_labels = pd.DataFrame(true_labels)
            df_true_labels.to_csv("df_true_labels.csv", index=False)
            

            results = []

            for photo in input_json["photos"]:
                result = predict_photo(photo)
                results.append(result)

            final_json = {"results": results}

            predicted_labels = [1 if result["dog_prob"] > result["cat_prob"] else 0 for result in results]
            df_predicted_labels = pd.DataFrame(predicted_labels)
            df_predicted_labels.to_csv("df_predicted_labels.csv", index=False)

            confusion = confusion_matrix(predicted_labels, true_labels)
            df_confusion = pd.DataFrame(confusion)
            df_confusion.to_csv("df_confusion.csv", index=False)

            accuracy = accuracy_score(predicted_labels, true_labels)
            confusion = confusion_matrix(true_labels, predicted_labels)
            precision = precision_score(true_labels, predicted_labels)
            recall = recall_score(true_labels, predicted_labels)
            f1 = f1_score(true_labels, predicted_labels)
            metrics = {
                'Accuracy': [accuracy],
                'Precision': [precision],
                'Recall': [recall],
                'F1 Score': [f1]
            }
            df_metrics = pd.DataFrame(metrics)
            df_metrics.to_csv("df_metrics.csv", index=False)

            return final_json, 200
        except Exception as e:
            return {"error": str(e)}, 500

api.add_resource(JSONManipulationResource, '/process_photos')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7000)
