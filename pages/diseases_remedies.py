import streamlit as st

def render():
    st.markdown('<h1 class="main-header">Common Child Diseases & Remedies</h1>', unsafe_allow_html=True)
    st.markdown("Learn about common childhood illnesses, their symptoms, and recommended home remedies and treatments.")
    
    diseases_data = [
        {
            "name": "Common Cold",
            "symptoms": ["Runny or stuffy nose", "Sneezing", "Mild fever", "Cough", "Sore throat", "Decreased appetite"],
            "causes": "Viral infection spread through airborne droplets or contact with infected surfaces.",
            "home_remedies": [
                "Ensure plenty of rest and sleep",
                "Keep child well-hydrated with water, warm soups, and juices",
                "Use saline nasal drops to relieve congestion",
                "Honey (for children over 1 year) to soothe cough",
                "Use a cool-mist humidifier in the room",
                "Warm salt water gargle for older children"
            ],
            "when_to_see_doctor": "If fever exceeds 102°F (39°C), symptoms last more than 10 days, or child has difficulty breathing.",
            "prevention": ["Frequent handwashing", "Avoid contact with sick individuals", "Keep toys and surfaces clean"]
        },
        {
            "name": "Ear Infection (Otitis Media)",
            "symptoms": ["Ear pain or tugging at ear", "Fever", "Difficulty sleeping", "Fussiness", "Trouble hearing", "Fluid drainage from ear"],
            "causes": "Bacterial or viral infection in the middle ear, often following a cold.",
            "home_remedies": [
                "Apply warm compress to the affected ear",
                "Keep child's head elevated during sleep",
                "Give age-appropriate pain relievers (acetaminophen or ibuprofen)",
                "Ensure adequate hydration",
                "Encourage swallowing to help drain the ear"
            ],
            "when_to_see_doctor": "If symptoms don't improve within 2-3 days, child has high fever, or there's discharge from the ear.",
            "prevention": ["Keep up with vaccinations", "Avoid secondhand smoke", "Breastfeeding helps build immunity"]
        },
        {
            "name": "Chickenpox (Varicella)",
            "symptoms": ["Itchy rash with fluid-filled blisters", "Fever", "Tiredness", "Loss of appetite", "Headache"],
            "causes": "Varicella-zoster virus, highly contagious through direct contact or airborne transmission.",
            "home_remedies": [
                "Calamine lotion to reduce itching",
                "Cool baths with baking soda or oatmeal",
                "Keep fingernails trimmed to prevent scratching",
                "Dress child in loose, comfortable clothing",
                "Use antihistamines for severe itching (consult doctor first)",
                "Ensure plenty of rest and fluids"
            ],
            "when_to_see_doctor": "If rash spreads to eyes, high fever persists, or blisters become infected.",
            "prevention": ["Varicella vaccine (usually given at 12-15 months)", "Avoid contact with infected individuals"]
        },
        {
            "name": "Hand, Foot, and Mouth Disease",
            "symptoms": ["Fever", "Sore throat", "Painful blisters in mouth", "Rash on hands and feet", "Irritability", "Loss of appetite"],
            "causes": "Coxsackievirus, spread through contact with infected fluids or feces.",
            "home_remedies": [
                "Offer cold foods like ice pops to soothe mouth sores",
                "Avoid acidic or spicy foods",
                "Ensure adequate fluid intake",
                "Use pain relievers for fever and discomfort",
                "Rinse mouth with warm salt water",
                "Apply soothing balm to skin rashes"
            ],
            "when_to_see_doctor": "If child cannot drink fluids, symptoms worsen after a few days, or fever is very high.",
            "prevention": ["Frequent handwashing", "Disinfect shared surfaces", "Teach children not to share utensils"]
        },
        {
            "name": "Gastroenteritis (Stomach Flu)",
            "symptoms": ["Vomiting", "Diarrhea", "Stomach cramps", "Fever", "Nausea", "Muscle aches"],
            "causes": "Viral or bacterial infection affecting the digestive system.",
            "home_remedies": [
                "Oral rehydration solutions (like Pedialyte)",
                "Small, frequent sips of clear fluids",
                "BRAT diet when appetite returns (Bananas, Rice, Applesauce, Toast)",
                "Plenty of rest",
                "Avoid dairy products temporarily",
                "Probiotics may help restore gut balance"
            ],
            "when_to_see_doctor": "Signs of dehydration (dry mouth, no tears, sunken eyes), blood in stool, or symptoms lasting more than 2 days.",
            "prevention": ["Proper hand hygiene", "Safe food preparation", "Keep sick family members isolated"]
        },
        {
            "name": "Croup",
            "symptoms": ["Barking cough", "Hoarse voice", "Stridor (high-pitched breathing)", "Fever", "Difficulty breathing"],
            "causes": "Viral infection causing swelling around the vocal cords and windpipe.",
            "home_remedies": [
                "Calm the child to reduce breathing difficulty",
                "Cool night air or steam from shower can help",
                "Use a cool-mist humidifier",
                "Keep child well-hydrated",
                "Elevate head during sleep",
                "Pain relievers for fever"
            ],
            "when_to_see_doctor": "If child has severe difficulty breathing, blue lips, drooling, or high fever.",
            "prevention": ["Regular handwashing", "Avoid contact with sick individuals", "Keep vaccinations up to date"]
        },
        {
            "name": "Conjunctivitis (Pink Eye)",
            "symptoms": ["Red or pink eye(s)", "Itching or burning", "Discharge from eye", "Watery eyes", "Crusty eyelids in morning", "Sensitivity to light"],
            "causes": "Bacterial or viral infection, or allergies.",
            "home_remedies": [
                "Clean eyes with warm, damp cloth",
                "Apply warm or cool compress for comfort",
                "Use artificial tears to soothe irritation",
                "Wash hands frequently to prevent spread",
                "Change pillowcases daily",
                "Avoid touching or rubbing eyes"
            ],
            "when_to_see_doctor": "If symptoms don't improve in 2-3 days, vision is affected, or there's severe pain.",
            "prevention": ["Teach children not to touch their eyes", "Don't share towels or pillows", "Regular handwashing"]
        },
        {
            "name": "Strep Throat",
            "symptoms": ["Severe sore throat", "Fever", "Red, swollen tonsils", "White patches on throat", "Headache", "Stomach pain"],
            "causes": "Group A Streptococcus bacteria, spread through respiratory droplets.",
            "home_remedies": [
                "Warm salt water gargle for older children",
                "Throat lozenges for children over 4",
                "Warm liquids like soup or tea with honey",
                "Cold treats to soothe throat",
                "Pain relievers for fever and pain",
                "Plenty of rest"
            ],
            "when_to_see_doctor": "Strep requires antibiotics - see doctor if strep is suspected. Also seek care for difficulty breathing or swallowing.",
            "prevention": ["Don't share utensils or cups", "Cover mouth when coughing", "Frequent handwashing"]
        },
        {
            "name": "Asthma",
            "symptoms": ["Wheezing", "Shortness of breath", "Chest tightness", "Coughing (especially at night)", "Difficulty exercising"],
            "causes": "Chronic condition where airways become inflamed and narrow. Triggers include allergens, cold air, exercise, and infections.",
            "home_remedies": [
                "Identify and avoid triggers",
                "Use prescribed inhalers as directed",
                "Keep home clean and dust-free",
                "Use air purifiers",
                "Maintain healthy weight",
                "Practice breathing exercises"
            ],
            "when_to_see_doctor": "If child has severe breathing difficulty, rescue inhaler doesn't help, or symptoms are frequent.",
            "prevention": ["Regular use of controller medications", "Allergy management", "Avoid smoke and strong odors"]
        },
        {
            "name": "Eczema (Atopic Dermatitis)",
            "symptoms": ["Dry, itchy skin", "Red patches", "Thickened skin", "Small bumps that may leak fluid", "Sensitive skin"],
            "causes": "Genetic and environmental factors leading to skin barrier dysfunction.",
            "home_remedies": [
                "Regular moisturizing with fragrance-free products",
                "Lukewarm baths (not hot)",
                "Use gentle, unscented soaps",
                "Dress in soft, breathable fabrics",
                "Keep nails short to prevent scratching",
                "Use wet wrap therapy for severe flares"
            ],
            "when_to_see_doctor": "If skin becomes infected, eczema affects daily life, or over-the-counter treatments don't help.",
            "prevention": ["Daily moisturizing routine", "Identify and avoid triggers", "Manage stress"]
        }
    ]
    
    st.markdown("---")
    
    search_term = st.text_input("Search for a disease", placeholder="Type disease name...")
    
    if search_term:
        filtered_diseases = [d for d in diseases_data if search_term.lower() in d["name"].lower()]
    else:
        filtered_diseases = diseases_data
    
    if not filtered_diseases:
        st.warning("No diseases found matching your search.")
    
    for disease in filtered_diseases:
        with st.expander(f"🏥 {disease['name']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Symptoms")
                for symptom in disease["symptoms"]:
                    st.markdown(f"- {symptom}")
                
                st.markdown("### Causes")
                st.markdown(disease["causes"])
            
            with col2:
                st.markdown("### Home Remedies & Treatments")
                for remedy in disease["home_remedies"]:
                    st.markdown(f"✅ {remedy}")
            
            st.markdown("---")
            
            st.markdown("### ⚠️ When to See a Doctor")
            st.warning(disease["when_to_see_doctor"])
            
            st.markdown("### 🛡️ Prevention Tips")
            prevention_text = " | ".join(disease["prevention"])
            st.info(prevention_text)
    
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #c65d00; padding: 1rem; border-radius: 8px; border-left: 4px solid #8b4000; color: white;">
        <strong>⚠️ Important Disclaimer:</strong><br>
        This information is for educational purposes only and should not replace professional medical advice. 
        Always consult a healthcare provider for proper diagnosis and treatment of your child's health conditions.
    </div>
    """, unsafe_allow_html=True)
