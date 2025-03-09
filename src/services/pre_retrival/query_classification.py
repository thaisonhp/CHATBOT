from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_query(query):
    labels = ["definition", "comparison", "explanation", "fact"]
    result = classifier(query, labels)
    return result["labels"][0]  # Nhãn có điểm cao nhất

query = "What's the difference between RAG and GPT?"
classify_query(query)  # Output: "comparison"
