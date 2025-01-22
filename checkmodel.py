from huggingface_hub import HfApi
import os

# Load your Hugging Face API token
api_token = os.getenv("HF_TOKEN")  # Replace with your token if not using .env

# Initialize the API client
api = HfApi()

# Get all text-generation models
text_gen_models = api.list_models(
    use_auth_token=api_token, filter="text-generation"  # Task-specific filter
)

# Filter models by size under 10 GB
filtered_models = [
    model
    for model in text_gen_models
    # if model.modelSize and model.modelSize < 10 * 1024**3
]

# Print filtered model names and sizes
print("Text generation models under 10 GB:")
# for model in filtered_models:
# size_in_gb = model.modelSize / (1024**3)  # Convert bytes to GB
# print(f"- {model.modelId} ({size_in_gb:.2f} GB)")

# save to text file list of models

with open("model_list.txt", "a+") as f:
    for model in filtered_models:
        f.write(model.modelId + "\n")
