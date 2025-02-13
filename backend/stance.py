import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Map labels
label_map = {"agree": 0, "disagree": 1, "discuss": 2, "unrelated": 3}
inv_label_map = {v: k for k, v in label_map.items()}

# Use model name from training
MODEL_NAME = "distilroberta-base"

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Load the model architecture
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=4)

# Load saved weights from saved file
saved_model_path = os.path.join("model", "TruthScope.pth")
if os.path.exists(saved_model_path):
    state_dict = torch.load(saved_model_path, map_location=torch.device("cpu"))
    model.load_state_dict(state_dict)
else:
    print(f"Warning: Saved model not found at {saved_model_path}. Using untrained weights.")

# Set model to eval mode
model.eval()

def predict_stance(query: str, article: str) -> str:
    """
    Given the user query (used as headline) and the article content (used as body),
    predict stance
    Returns agree, disagree, discuss, or unrelated
    """
    # Concatenate query and article using the separator <s/> for RoBERTa
    text = query + " </s> " + article
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding="max_length")
    with torch.no_grad():
        outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()
    return inv_label_map.get(prediction, "unknown")