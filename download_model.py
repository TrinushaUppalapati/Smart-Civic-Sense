from huggingface_hub import hf_hub_download
import shutil
import os

print("Downloading Civic AI model...")

model_path = hf_hub_download(
    repo_id="Vansh180/PotholeNet-V1",
    filename="Vision Classification.pt"
)

destination = "civic_model.pt"

shutil.copy(model_path, destination)

print("Model downloaded successfully!")
print("Saved as:", os.path.abspath(destination))