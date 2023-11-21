import pandas as pd

import sklearn
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
data = pd.read_csv("insurance.csv")
data = data.dropna()
label_encoder = LabelEncoder()
# print(data.columns)
# for i in data.columns:
#     print(data[i].unique())
data["sex"] = label_encoder.fit_transform(data["sex"])
data["smoker"] = label_encoder.fit_transform(data["smoker"])
data["region"] = label_encoder.fit_transform(data["region"])
print(data)
# print(f"max is {max(data['bmi'])}")
# print(f"min is {min(data['bmi'])}")
# print(data)


