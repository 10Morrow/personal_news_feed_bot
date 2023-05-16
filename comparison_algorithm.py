from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
# from sklearn.externals import joblib





data = interesting_news + uninteresting_news
labels = ["interesting"] * len(interesting_news) + ["uninteresting"] * len(uninteresting_news)

model = Pipeline([
    ("vectorizer", CountVectorizer()),
    ("classifier", LogisticRegression())
])
model.fit(data, labels)

def predict_preference(post):
    prediction = model.predict([post])
    probability = model.predict_proba([post])[0][1] * 100
    return prediction[0], probability

post = "Новый роботический помощник разработан для помощи в уходе за пожилыми людьми."
preference, probability = predict_preference(post)

if preference == "interesting":
    print(f"Предпочтение: Интересно ({probability:.2f}%)")
else:
    print(f"Предпочтение: Не интересно ({probability:.2f}%)")
