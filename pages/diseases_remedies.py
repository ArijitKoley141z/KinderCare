import streamlit as st
import json
import os

def load_diseases_data():
    """Load diseases information from JSON file."""
    json_path = "data/disease_information_database.json"
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            return data.get('diseases', [])
    except FileNotFoundError:
        st.error(f"Disease database file not found at {json_path}")
        return []

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
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 style="color: #667eea; margin-top: 0;">🏥 Common Child Diseases & Remedies</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #000; margin-bottom: 1rem;">Learn about common childhood illnesses, their symptoms, and recommended treatments</p>', unsafe_allow_html=True)
    
    # Load diseases data from JSON file
    diseases_data = load_diseases_data()
    
    if not diseases_data:
        st.error("Unable to load disease information. Please try again later.")
        return
    
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
