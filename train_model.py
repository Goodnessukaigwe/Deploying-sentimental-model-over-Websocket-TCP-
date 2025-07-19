from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

# Sample training data
X = [
    "I love this!",
    "This is amazing",
    "I hate this",
    "This is awful",
    "Not bad",
    "I feel great",
    "I'm very disappointed",
    "Absolutely horrible"
]
y = ["positive", "positive", "negative", "negative", "neutral", "positive", "negative", "negative"]

# Create pipeline: text vectorization + classifier
model = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])

model.fit(X, y)

# Save the model
joblib.dump(model, "sentiment_model.joblib")
print("Model trained and saved.")
