from flask import Flask, request, render_template
import os

app = Flask(__name__)
IMAGE_DIR = "static/images"
STATIC_PATH = "D:/Swinburne/Sem 4/Internship Project/ProjectCancerData/5. final_output&Presentation/static/images"
os.makedirs(STATIC_PATH, exist_ok=True)

# Mapping of keywords to image filenames (relative to the static/images directory)
IMAGE_MAPPING = {
    "treatment transaction": "treatment transaction.png",
    "age distribution": "age distribution.png",
    "bottom treatment success rate": "bottom_treatment success rate.png",
    "colorectal cancer": "COLORECTAL CANCER.png",
    "counts of modifications": "counts of modifications.png",
    "dose distribution": "dose distribution.png",
    "hormonal therapy treatment": "HORMONAL THERAPY TREATMENT.png",
    "image": "image.png",
    "lymphoma regimens": "Lymphoma Regimens.png",
    "middle treatment success rate": "middle treatment success rate.png",
    "regimen frequency": "regimen_frequency.png",
    "success fail for modified": "success fail for modified and modified regimens.png",
    "survival curves by age": "survival curves by age group.png",
    "top 10 common treatment": "TOP 10 MOST COMMON TREATMENT REGIMENS.png",
    "top 30 fluoropyrimidine": "Top 30 Fluoropyrimidine-based Treatment Regimens.png",
    "top 30 immunotherapy": "Top 30 Immunotherapy.png",
    "top 30 targeted therapy": "TOP 30 TARGETED THERAPY.png",
    "top 30 colorectal cancer": "TOP 30 TREATMENT REGIMENS - COLORECTAL CANCER.png",
    "top 30 lung cancer": "TOP 30 TREATMENT REGIMENS - LUNG CANCER.png",
    "top treatment regiments by cancer type": "top 30 treatment regiments by cancer type.png",
    "top treatment success rate": "top treatment success rate.png",
    # Add more keywords as needed
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    print(f"User asked: {question}")
    image_filename = None

    for keyword, filename in IMAGE_MAPPING.items():
        if keyword in question.lower():
            image_filename = filename
            break  # Stop after finding the first match

    if image_filename and os.path.exists(os.path.join(STATIC_PATH, image_filename)):
        image_path = os.path.join(IMAGE_DIR, image_filename)
        return render_template('result.html', image_path=image_path)
    else:
        return render_template('result.html', message="No matching visualization found for your question.")

if __name__ == '__main__':
    app.run(debug=True)