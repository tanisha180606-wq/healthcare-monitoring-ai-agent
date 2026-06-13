from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SPECIALIST_DATABASE = {
    "fever": ["Internal Medicine Physician", "CBC blood test, temperature check"],
    "dengue": ["Infectious Disease Specialist", "Dengue NS1, IgM/IgG, CBC platelet count"],
    "malaria": ["Infectious Disease Specialist", "Malaria parasite smear, rapid malaria test, CBC"],
    "typhoid": ["Internal Medicine Physician", "Widal test, blood culture, CBC"],
    "diabetes": ["Endocrinologist / Diabetologist", "Fasting sugar, PP sugar, HbA1c"],
    "thyroid": ["Endocrinologist", "TSH, T3, T4 blood test"],
    "chest pain": ["Cardiologist / Emergency Physician", "ECG, cardiac enzymes, chest X-ray"],
    "heart attack": ["Cardiologist / Emergency Physician", "ECG, troponin test, echocardiogram"],
    "high bp": ["Cardiologist", "BP monitoring, ECG, kidney function test"],
    "headache": ["Neurologist", "BP check, eye checkup, MRI if severe"],
    "migraine": ["Neurologist", "Clinical exam, MRI if doctor suggests"],
    "stroke": ["Neurologist / Emergency Physician", "CT brain, MRI brain"],
    "seizure": ["Neurologist", "EEG, MRI brain"],
    "kidney stone": ["Urologist", "Urine test, ultrasound, CT KUB"],
    "urine pain": ["Urologist", "Urine routine test, urine culture, ultrasound"],
    "fracture": ["Orthopedic Surgeon", "X-ray, CT scan"],
    "bone pain": ["Orthopedic Specialist", "X-ray, vitamin D/calcium blood test"],
    "back pain": ["Orthopedic Specialist", "X-ray, MRI if severe"],
    "joint pain": ["Rheumatologist / Orthopedic Specialist", "X-ray, blood tests"],
    "cough": ["Pulmonologist / ENT Specialist", "Throat exam, chest X-ray if severe"],
    "cold": ["ENT Specialist", "Clinical checkup, throat exam if needed"],
    "asthma": ["Pulmonologist", "Spirometry, peak flow test, chest X-ray"],
    "pneumonia": ["Pulmonologist", "Chest X-ray, CBC, oxygen level check"],
    "tuberculosis": ["Pulmonologist", "Sputum test, chest X-ray, CT chest"],
    "stomach pain": ["Gastroenterologist", "Ultrasound abdomen, stool test if needed"],
    "vomiting": ["Gastroenterologist", "Blood test, urine test, ultrasound if needed"],
    "diarrhea": ["Gastroenterologist", "Stool test, urine test, electrolytes"],
    "acidity": ["Gastroenterologist", "Upper endoscopy if frequent"],
    "jaundice": ["Hepatologist / Gastroenterologist", "Liver function test, bilirubin, ultrasound"],
    "skin rash": ["Dermatologist", "Skin examination, allergy test if needed"],
    "allergy": ["Allergist / Dermatologist", "Allergy test, blood test"],
    "eye pain": ["Ophthalmologist", "Vision test, eye pressure test"],
    "ear pain": ["ENT Specialist", "Ear examination"],
    "cancer": ["Oncologist", "Biopsy, CT scan, PET scan"],
    "tumor": ["Oncologist / Surgeon", "MRI/CT scan, biopsy"],
    "breast lump": ["Oncologist / Breast Surgeon", "Mammogram, ultrasound, biopsy"],
    "anemia": ["Hematologist", "CBC, iron studies, vitamin B12 test"],
    "depression": ["Psychiatrist / Psychologist", "Mental health assessment"],
    "anxiety": ["Psychiatrist / Psychologist", "Mental health assessment"],
}

EMERGENCY_WORDS = [
    "chest pain",
    "heart attack",
    "stroke",
    "breathing difficulty",
    "fainting",
    "seizure",
    "severe bleeding",
]

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").lower()
    agent = data.get("agent", "Diagnostics AI")

    specialist = "General Physician / Family Medicine Specialist"
    tests = "Basic vitals check. Doctor will decide if tests are needed."
    risk = "🟢 Low Risk"
    warning = "Monitor symptoms. Visit doctor if symptoms continue or increase."
    duration = "Observe for 1-2 days if mild."

    for problem, info in SPECIALIST_DATABASE.items():
        if problem in message:
            specialist = info[0]
            tests = info[1]
            risk = "🟡 Needs Specialist Guidance"
            warning = "Consult the suggested specialist for proper diagnosis."
            duration = "Visit specialist within 1-3 days if symptoms continue."
            break

    for word in EMERGENCY_WORDS:
        if word in message:
            risk = "🔴 Emergency"
            warning = "Go to hospital or emergency care immediately."
            duration = "Immediate medical care required."
            break

    reply = f"""
🏥 HEALTHMIND AI REPORT

Selected Agent:
{agent}

Risk Level:
{risk}

Recommended Specialist:
Meet {specialist}

Suggested Tests / Scans:
{tests}

Food Guidance:
Eat fruits, vegetables, warm food, soup, and drink enough water.
Avoid junk food, oily food, cold drinks, and self-medication.

Follow-up Duration:
{duration}

Warning:
{warning}

Safety Note:
This AI gives educational guidance only.
It does not replace a doctor.
For serious symptoms, visit hospital immediately.
"""

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)