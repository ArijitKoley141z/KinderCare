import streamlit as st

def render():
    st.markdown("""
    <style>
        [data-testid="stExpander"] {
            color: #000 !important;
        }
        [data-testid="stExpander"] button {
            color: #000 !important;
            background-color: transparent !important;
        }
        [data-testid="stExpander"] button:hover {
            background-color: transparent !important;
            color: #000 !important;
        }
        [data-testid="stExpander"] summary {
            color: #000 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 style="color: #667eea; margin-top: 0;">🏥 Common Child Diseases & Remedies</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #000;">Learn about common childhood illnesses, their symptoms, and recommended treatments</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    diseases_data = [
        {
            "name": "Common Cold",
            "emoji": "🤧",
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
            "name": "Ear Infection",
            "emoji": "👂",
            "symptoms": ["Ear pain or tugging at ear", "Fever", "Difficulty sleeping", "Fussiness", "Trouble hearing"],
            "causes": "Bacterial or viral infection in the middle ear, often following a cold.",
            "home_remedies": [
                "Apply warm compress to the affected ear",
                "Keep child's head elevated during sleep",
                "Give age-appropriate pain relievers",
                "Ensure adequate hydration",
                "Encourage swallowing to help drain the ear"
            ],
            "when_to_see_doctor": "If symptoms don't improve within 2-3 days, child has high fever, or there's discharge from the ear.",
            "prevention": ["Keep up with vaccinations", "Avoid secondhand smoke", "Breastfeeding builds immunity"]
        },
        {
            "name": "Chickenpox (Varicella)",
            "emoji": "🦠",
            "symptoms": ["Itchy rash with fluid-filled blisters", "Fever", "Tiredness", "Loss of appetite", "Headache"],
            "causes": "Varicella-zoster virus, highly contagious through direct contact or airborne transmission.",
            "home_remedies": [
                "Calamine lotion to reduce itching",
                "Cool baths with baking soda or oatmeal",
                "Keep fingernails trimmed to prevent scratching",
                "Dress child in loose, comfortable clothing",
                "Use antihistamines for severe itching",
                "Ensure plenty of rest and fluids"
            ],
            "when_to_see_doctor": "If rash spreads to eyes, high fever persists, or blisters become infected.",
            "prevention": ["Varicella vaccine", "Avoid contact with infected individuals"]
        },
        {
            "name": "Hand, Foot & Mouth Disease",
            "emoji": "🦶",
            "symptoms": ["Fever", "Sore throat", "Painful blisters in mouth", "Rash on hands and feet", "Irritability"],
            "causes": "Coxsackievirus, spread through contact with infected fluids or feces.",
            "home_remedies": [
                "Offer cold foods like ice pops to soothe mouth sores",
                "Avoid acidic or spicy foods",
                "Ensure adequate fluid intake",
                "Use pain relievers for fever",
                "Rinse mouth with warm salt water",
                "Apply soothing balm to skin rashes"
            ],
            "when_to_see_doctor": "If child cannot drink fluids, symptoms worsen, or fever is very high.",
            "prevention": ["Frequent handwashing", "Disinfect shared surfaces", "Teach children not to share utensils"]
        },
        {
            "name": "Gastroenteritis (Stomach Flu)",
            "emoji": "🤢",
            "symptoms": ["Vomiting", "Diarrhea", "Stomach cramps", "Fever", "Nausea"],
            "causes": "Viral or bacterial infection affecting the digestive system.",
            "home_remedies": [
                "Oral rehydration solutions (like Pedialyte)",
                "Small, frequent sips of clear fluids",
                "BRAT diet (Bananas, Rice, Applesauce, Toast)",
                "Plenty of rest",
                "Avoid dairy and fatty foods temporarily",
                "Keep child away from others to prevent spread"
            ],
            "when_to_see_doctor": "If signs of dehydration appear, vomiting persists beyond 24 hours, or bloody stools are present.",
            "prevention": ["Rotavirus vaccine", "Proper food handling", "Regular handwashing"]
        }
    ]
    
    st.markdown("---")
    
    for disease in diseases_data:
        with st.expander(f"{disease['emoji']} {disease['name']}", expanded=False):
            symptoms_text = " • ".join(disease['symptoms'])
            symptoms_formatted = symptoms_text.replace(' • ', '<br>• ')
            
            remedies_text = " • ".join(disease['home_remedies'])
            remedies_formatted = remedies_text.replace(' • ', '<br>• ')
            
            prevention_text = " • ".join(disease['prevention'])
            prevention_formatted = prevention_text.replace(' • ', '<br>• ')
            
            st.markdown(f"""
            <div style="color: #000;">
                <p><strong>What causes it?</strong><br>{disease['causes']}</p>
                <p><strong>Symptoms:</strong><br>• {symptoms_formatted}</p>
                <p><strong>Home Remedies:</strong><br>• {remedies_formatted}</p>
                <p><strong>When to See a Doctor:</strong><br>{disease['when_to_see_doctor']}</p>
                <p><strong>Prevention:</strong><br>• {prevention_formatted}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div class="info-box" style="background: #f0f7ff; border-left: 4px solid #667eea; padding: 1.5rem; border-radius: 8px;">
        <h3 style="color: #667eea; margin: 0 0 0.5rem 0;">⚕️ Important Disclaimer</h3>
        <p style="color: #333; margin: 0;">This information is for educational purposes only and should not replace professional medical advice. Always consult with your child's pediatrician if you're concerned about your child's health. In case of emergency, contact emergency services immediately.</p>
    </div>
    """, unsafe_allow_html=True)
