import streamlit as st

def render():
    st.markdown("""
    <style>
        /* Fix expander header background when expanded */
        [data-testid="stExpander"] details[open] > summary {
            background-color: transparent !important;
            color: #ffffff !important;
        }

        /* Ensure text stays visible on hover */
        [data-testid="stExpander"] details[open] > summary:hover {
            background-color: rgba(255, 255, 255, 0.08) !important;
            color: #ffffff !important;
        }

        [data-testid="stExpander"] {
            color: #fff !important;
        }
        [data-testid="stExpander"] button {
            color: #fff !important;
            background-color: transparent !important;
            border: none !important;
            font-weight: 600 !important;
        }
        [data-testid="stExpander"] button:hover {
            background-color: transparent !important;
            color: #fff !important;
            border: none !important;
            font-weight: 600 !important;
        }
        [data-testid="stExpander"] button:active {
            color: #fff !important;
            background-color: transparent !important;
        }
        [data-testid="stExpander"] details {
            color: #fff !important;
        }
        [data-testid="stExpander"] details[open] {
            color: #fff !important;
        }
        [data-testid="stExpander"] details:hover {
            background-color: transparent !important;
        }
        [data-testid="stExpander"] summary {
            color: #fff !important;
            font-weight: 800 !important;
            font-size: 1.05em !important;
            cursor: pointer !important;
        }
        [data-testid="stExpander"] summary:hover {
            background-color: transparent !important;
            color: #fff !important;
            font-weight: 800 !important;
            font-size: 1.05em !important;
        }
        [data-testid="stExpander"] summary:focus {
            color: #fff !important;
            outline: none !important;
            font-weight: 800 !important;
        }
        [data-testid="stExpander"] p, [data-testid="stExpander"] span {
            color: #000 !important;
        }
        /* Fix expander header background when expanded */
        [data-testid="stExpander"] details[open] > summary {
            background-color: transparent !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            font-size: 1.05em !important;
        }
        /* Ensure text stays visible on hover */
        [data-testid="stExpander"] details[open] > summary:hover {
            background-color: rgba(255, 255, 255, 0.08) !important;
            color: #ffffff !important;
            font-weight: 800 !important;
            font-size: 1.05em !important;
        }
        button, [data-testid="baseButton-primary"], [data-testid="baseButton-secondary"] {
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 style="color: #667eea; margin-top: 0;">🏥 Common Child Diseases & Remedies</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #000; margin-bottom: 1rem;">Learn about common childhood illnesses, their symptoms, and recommended treatments</p>', unsafe_allow_html=True)
    
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
        },
        {
            "name": "Measles",
            "emoji": "🔴",
            "symptoms": ["Fever", "Cough", "Runny nose", "Red watery eyes", "Rash starting on face and spreading down body"],
            "causes": "Highly contagious viral infection spread through airborne droplets.",
            "home_remedies": [
                "Ensure complete bed rest",
                "High-dose vitamin A supplementation (consult doctor)",
                "Maintain adequate hydration",
                "Use cool-mist humidifier to ease cough",
                "Keep room darkened to ease eye irritation",
                "Dress in comfortable, breathable clothing"
            ],
            "when_to_see_doctor": "Seek immediate medical attention if suspected, as measles requires professional monitoring.",
            "prevention": ["MMR vaccine", "Avoid contact with infected individuals"]
        },
        {
            "name": "Strep Throat",
            "emoji": "😖",
            "symptoms": ["Severe sore throat", "Fever over 101°F", "Swollen red tonsils", "White/yellow spots on tonsils", "Headache", "Nausea"],
            "causes": "Group A Streptococcus bacteria spread through droplets from coughing or sneezing.",
            "home_remedies": [
                "Warm salt water gargles several times daily",
                "Cold throat lozenges or popsicles for pain relief",
                "Honey to soothe throat irritation",
                "Anti-inflammatory medications like ibuprofen",
                "Adequate hydration with warm drinks",
                "Complete rest until fever subsides"
            ],
            "when_to_see_doctor": "Consult doctor for antibiotics, which are essential to prevent complications like rheumatic fever.",
            "prevention": ["Frequent handwashing", "Teach child not to share utensils or drinks", "Keep infected child away from others"]
        },
        {
            "name": "Pink Eye (Conjunctivitis)",
            "emoji": "👁️",
            "symptoms": ["Red or pink conjunctiva", "Itching and burning", "Watery or discharge from eyes", "Swollen eyelids", "Light sensitivity", "Crusting of eyelids"],
            "causes": "Bacterial, viral, or allergic infection/irritation of the eye membrane.",
            "home_remedies": [
                "Wash hands frequently before touching eyes",
                "Use warm compresses on closed eyes",
                "Gently clean away discharge with warm water",
                "Apply artificial tears if irritated",
                "Avoid touching or rubbing eyes",
                "Use clean towels and pillowcases frequently"
            ],
            "when_to_see_doctor": "If discharge is thick/yellowish (bacterial), eyes become painful, or vision is affected.",
            "prevention": ["Regular handwashing", "Don't share eye makeup or contacts", "Avoid rubbing eyes with dirty hands"]
        },
        {
            "name": "Croup",
            "emoji": "🎺",
            "symptoms": ["Barking, seal-like cough", "Hoarse voice", "Stridor (high-pitched breathing)", "Fever", "Runny nose", "Mild symptoms during day, worse at night"],
            "causes": "Viral infection, usually parainfluenza virus, causing inflammation in the airways.",
            "home_remedies": [
                "Cool mist or steam inhalation for 15-20 minutes",
                "Keep child calm and relaxed",
                "Elevate head with extra pillows",
                "Use humidifier in bedroom overnight",
                "Offer honey and warm drinks (for children over 1 year)",
                "Avoid smoke and irritants"
            ],
            "when_to_see_doctor": "If stridor is present during rest, severe difficulty breathing, drooling, or symptoms worsen.",
            "prevention": ["Avoid second-hand smoke", "Regular handwashing", "Up-to-date vaccinations"]
        },
        {
            "name": "Whooping Cough (Pertussis)",
            "emoji": "💨",
            "symptoms": ["Severe coughing fits followed by 'whooping' sound", "Nasal congestion", "Low-grade fever", "Sneezing", "Coughing may last 6+ weeks"],
            "causes": "Bordetella pertussis bacteria, highly contagious respiratory infection.",
            "home_remedies": [
                "Ensure child gets complete rest",
                "Maintain high fluid intake",
                "Use humidifier to ease congestion",
                "Smaller, frequent meals to prevent vomiting",
                "Keep environment calm and quiet",
                "Monitor for complications like pneumonia"
            ],
            "when_to_see_doctor": "Medical attention essential; antibiotics may be prescribed. Hospitalization may be needed for severe cases.",
            "prevention": ["DTaP vaccine", "Booster shots for older children and adults", "Avoid contact with infected individuals"]
        },
        {
            "name": "Atopic Dermatitis (Eczema)",
            "emoji": "🔴",
            "symptoms": ["Intense itching, especially at night", "Red or brownish patches", "Small raised bumps that leak fluid when scratched", "Swollen, cracked skin", "Raw, sensitive skin from scratching"],
            "causes": "Genetic predisposition combined with environmental triggers and impaired skin barrier function.",
            "home_remedies": [
                "Use fragrance-free, gentle moisturizers immediately after bathing",
                "Lukewarm (not hot) baths with mild cleansers",
                "Apply hydrocortisone cream for itching (under medical guidance)",
                "Use humidifier to maintain skin moisture",
                "Avoid harsh detergents and fabrics",
                "Keep fingernails trimmed to prevent damage from scratching"
            ],
            "when_to_see_doctor": "If rash spreads, signs of infection appear, or over-the-counter treatments don't help.",
            "prevention": ["Use mild, hypoallergenic products", "Avoid known triggers", "Keep skin well-moisturized", "Avoid excessive sweating"]
        },
        {
            "name": "Mumps",
            "emoji": "🐭",
            "symptoms": ["Swollen salivary glands (cheeks puff out)", "Fever", "Headache", "Muscle aches", "Loss of appetite", "Difficulty eating or drinking"],
            "causes": "Mumps virus spread through droplets from coughing or sneezing; highly contagious.",
            "home_remedies": [
                "Complete bed rest during acute phase",
                "Soft foods like mashed potatoes, yogurt, pudding",
                "Pain relievers for aches and fever",
                "Warm compresses on swollen glands",
                "Encourage fluid intake",
                "Avoid acidic foods and drinks that irritate glands"
            ],
            "when_to_see_doctor": "For confirmation, monitoring, and watching for complications like meningitis or hearing loss.",
            "prevention": ["MMR vaccine (highly effective)", "Avoid contact with infected individuals"]
        }
    ]
    
    st.divider()
    
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
    
    st.divider()
    st.markdown("""
    <div class="info-box" style="background: #f0f7ff; border-left: 4px solid #667eea; padding: 1.5rem; border-radius: 8px;">
        <h3 style="color: #667eea; margin: 0 0 0.5rem 0;">⚕️ Important Disclaimer</h3>
        <p style="color: #333; margin: 0;">This information is for educational purposes only and should not replace professional medical advice. Always consult with your child's pediatrician if you're concerned about your child's health. In case of emergency, contact emergency services immediately.</p>
    </div>
    """, unsafe_allow_html=True)
