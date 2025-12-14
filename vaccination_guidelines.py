from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Dict

INDIA_UIP_SCHEDULE = [
    {"vaccine": "BCG", "code": "BCG", "age_weeks": 0, "age_label": "At Birth", "description": "Bacillus Calmette-Guerin vaccine for Tuberculosis"},
    {"vaccine": "OPV-0", "code": "OPV0", "age_weeks": 0, "age_label": "At Birth", "description": "Oral Polio Vaccine - Zero dose"},
    {"vaccine": "Hepatitis B-Birth", "code": "HEPB0", "age_weeks": 0, "age_label": "At Birth", "description": "Hepatitis B vaccine - Birth dose"},
    {"vaccine": "OPV-1", "code": "OPV1", "age_weeks": 6, "age_label": "6 Weeks", "description": "Oral Polio Vaccine - First dose"},
    {"vaccine": "Pentavalent-1", "code": "PENTA1", "age_weeks": 6, "age_label": "6 Weeks", "description": "DPT + Hep B + Hib - First dose"},
    {"vaccine": "Rotavirus-1", "code": "ROTA1", "age_weeks": 6, "age_label": "6 Weeks", "description": "Rotavirus vaccine - First dose"},
    {"vaccine": "PCV-1", "code": "PCV1", "age_weeks": 6, "age_label": "6 Weeks", "description": "Pneumococcal Conjugate Vaccine - First dose"},
    {"vaccine": "IPV-1", "code": "IPV1", "age_weeks": 6, "age_label": "6 Weeks", "description": "Inactivated Polio Vaccine - First dose"},
    {"vaccine": "OPV-2", "code": "OPV2", "age_weeks": 10, "age_label": "10 Weeks", "description": "Oral Polio Vaccine - Second dose"},
    {"vaccine": "Pentavalent-2", "code": "PENTA2", "age_weeks": 10, "age_label": "10 Weeks", "description": "DPT + Hep B + Hib - Second dose"},
    {"vaccine": "Rotavirus-2", "code": "ROTA2", "age_weeks": 10, "age_label": "10 Weeks", "description": "Rotavirus vaccine - Second dose"},
    {"vaccine": "OPV-3", "code": "OPV3", "age_weeks": 14, "age_label": "14 Weeks", "description": "Oral Polio Vaccine - Third dose"},
    {"vaccine": "Pentavalent-3", "code": "PENTA3", "age_weeks": 14, "age_label": "14 Weeks", "description": "DPT + Hep B + Hib - Third dose"},
    {"vaccine": "Rotavirus-3", "code": "ROTA3", "age_weeks": 14, "age_label": "14 Weeks", "description": "Rotavirus vaccine - Third dose"},
    {"vaccine": "PCV-2", "code": "PCV2", "age_weeks": 14, "age_label": "14 Weeks", "description": "Pneumococcal Conjugate Vaccine - Second dose"},
    {"vaccine": "IPV-2", "code": "IPV2", "age_weeks": 14, "age_label": "14 Weeks", "description": "Inactivated Polio Vaccine - Second dose"},
    {"vaccine": "Measles-1 / MR-1", "code": "MR1", "age_weeks": 39, "age_label": "9 Months", "description": "Measles-Rubella vaccine - First dose"},
    {"vaccine": "Vitamin A-1", "code": "VITA1", "age_weeks": 39, "age_label": "9 Months", "description": "Vitamin A supplementation - First dose"},
    {"vaccine": "PCV Booster", "code": "PCVB", "age_weeks": 39, "age_label": "9 Months", "description": "Pneumococcal Conjugate Vaccine - Booster"},
    {"vaccine": "JE-1", "code": "JE1", "age_weeks": 39, "age_label": "9 Months", "description": "Japanese Encephalitis - First dose (endemic areas)"},
    {"vaccine": "MR-2", "code": "MR2", "age_weeks": 65, "age_label": "16-24 Months", "description": "Measles-Rubella vaccine - Second dose"},
    {"vaccine": "DPT Booster-1", "code": "DPTB1", "age_weeks": 65, "age_label": "16-24 Months", "description": "DPT Booster - First dose"},
    {"vaccine": "OPV Booster", "code": "OPVB", "age_weeks": 65, "age_label": "16-24 Months", "description": "Oral Polio Vaccine - Booster"},
    {"vaccine": "JE-2", "code": "JE2", "age_weeks": 65, "age_label": "16-24 Months", "description": "Japanese Encephalitis - Second dose"},
    {"vaccine": "Vitamin A-2", "code": "VITA2", "age_weeks": 65, "age_label": "16 Months", "description": "Vitamin A supplementation - Second dose"},
    {"vaccine": "DPT Booster-2", "code": "DPTB2", "age_weeks": 260, "age_label": "5-6 Years", "description": "DPT Booster - Second dose"},
    {"vaccine": "Td/TT", "code": "TD", "age_weeks": 520, "age_label": "10 Years", "description": "Tetanus and Diphtheria vaccine"},
    {"vaccine": "Td/TT", "code": "TD2", "age_weeks": 780, "age_label": "16 Years", "description": "Tetanus and Diphtheria vaccine - Booster"},
]

WHO_SCHEDULE = [
    {"vaccine": "BCG", "code": "BCG", "age_weeks": 0, "age_label": "At Birth", "description": "Bacillus Calmette-Guerin for Tuberculosis"},
    {"vaccine": "Hepatitis B-Birth", "code": "HEPB0", "age_weeks": 0, "age_label": "At Birth", "description": "Hepatitis B vaccine - Birth dose (within 24 hours)"},
    {"vaccine": "OPV-0", "code": "OPV0", "age_weeks": 0, "age_label": "At Birth", "description": "Oral Polio Vaccine - Birth dose"},
    {"vaccine": "DTP-1", "code": "DTP1", "age_weeks": 6, "age_label": "6 Weeks", "description": "Diphtheria-Tetanus-Pertussis - First dose"},
    {"vaccine": "Hepatitis B-1", "code": "HEPB1", "age_weeks": 6, "age_label": "6 Weeks", "description": "Hepatitis B vaccine - First dose"},
    {"vaccine": "Hib-1", "code": "HIB1", "age_weeks": 6, "age_label": "6 Weeks", "description": "Haemophilus influenzae type b - First dose"},
    {"vaccine": "Polio-1", "code": "POLIO1", "age_weeks": 6, "age_label": "6 Weeks", "description": "Polio vaccine - First dose"},
    {"vaccine": "Pneumococcal-1", "code": "PCV1", "age_weeks": 6, "age_label": "6 Weeks", "description": "Pneumococcal Conjugate Vaccine - First dose"},
    {"vaccine": "Rotavirus-1", "code": "ROTA1", "age_weeks": 6, "age_label": "6 Weeks", "description": "Rotavirus vaccine - First dose"},
    {"vaccine": "DTP-2", "code": "DTP2", "age_weeks": 10, "age_label": "10 Weeks", "description": "Diphtheria-Tetanus-Pertussis - Second dose"},
    {"vaccine": "Hepatitis B-2", "code": "HEPB2", "age_weeks": 10, "age_label": "10 Weeks", "description": "Hepatitis B vaccine - Second dose"},
    {"vaccine": "Hib-2", "code": "HIB2", "age_weeks": 10, "age_label": "10 Weeks", "description": "Haemophilus influenzae type b - Second dose"},
    {"vaccine": "Polio-2", "code": "POLIO2", "age_weeks": 10, "age_label": "10 Weeks", "description": "Polio vaccine - Second dose"},
    {"vaccine": "Pneumococcal-2", "code": "PCV2", "age_weeks": 10, "age_label": "10 Weeks", "description": "Pneumococcal Conjugate Vaccine - Second dose"},
    {"vaccine": "Rotavirus-2", "code": "ROTA2", "age_weeks": 10, "age_label": "10 Weeks", "description": "Rotavirus vaccine - Second dose"},
    {"vaccine": "DTP-3", "code": "DTP3", "age_weeks": 14, "age_label": "14 Weeks", "description": "Diphtheria-Tetanus-Pertussis - Third dose"},
    {"vaccine": "Hepatitis B-3", "code": "HEPB3", "age_weeks": 14, "age_label": "14 Weeks", "description": "Hepatitis B vaccine - Third dose"},
    {"vaccine": "Hib-3", "code": "HIB3", "age_weeks": 14, "age_label": "14 Weeks", "description": "Haemophilus influenzae type b - Third dose"},
    {"vaccine": "Polio-3", "code": "POLIO3", "age_weeks": 14, "age_label": "14 Weeks", "description": "Polio vaccine - Third dose"},
    {"vaccine": "Pneumococcal-3", "code": "PCV3", "age_weeks": 14, "age_label": "14 Weeks", "description": "Pneumococcal Conjugate Vaccine - Third dose"},
    {"vaccine": "IPV", "code": "IPV", "age_weeks": 14, "age_label": "14 Weeks", "description": "Inactivated Polio Vaccine"},
    {"vaccine": "Measles-1", "code": "MCV1", "age_weeks": 39, "age_label": "9 Months", "description": "Measles containing vaccine - First dose"},
    {"vaccine": "Rubella", "code": "RCV", "age_weeks": 39, "age_label": "9 Months", "description": "Rubella containing vaccine"},
    {"vaccine": "Yellow Fever", "code": "YF", "age_weeks": 39, "age_label": "9 Months", "description": "Yellow Fever vaccine (endemic areas)"},
    {"vaccine": "Vitamin A", "code": "VITA", "age_weeks": 39, "age_label": "9 Months", "description": "Vitamin A supplementation"},
    {"vaccine": "Measles-2", "code": "MCV2", "age_weeks": 65, "age_label": "15-18 Months", "description": "Measles containing vaccine - Second dose"},
    {"vaccine": "DTP Booster", "code": "DTPB", "age_weeks": 65, "age_label": "15-18 Months", "description": "DTP Booster dose"},
]

CDC_SCHEDULE = [
    {"vaccine": "Hepatitis B-1", "code": "HEPB1", "age_weeks": 0, "age_label": "At Birth", "description": "Hepatitis B vaccine - First dose"},
    {"vaccine": "Hepatitis B-2", "code": "HEPB2", "age_weeks": 4, "age_label": "1-2 Months", "description": "Hepatitis B vaccine - Second dose"},
    {"vaccine": "DTaP-1", "code": "DTAP1", "age_weeks": 8, "age_label": "2 Months", "description": "Diphtheria, Tetanus, Pertussis - First dose"},
    {"vaccine": "Hib-1", "code": "HIB1", "age_weeks": 8, "age_label": "2 Months", "description": "Haemophilus influenzae type b - First dose"},
    {"vaccine": "IPV-1", "code": "IPV1", "age_weeks": 8, "age_label": "2 Months", "description": "Inactivated Polio Vaccine - First dose"},
    {"vaccine": "PCV13-1", "code": "PCV1", "age_weeks": 8, "age_label": "2 Months", "description": "Pneumococcal Conjugate Vaccine - First dose"},
    {"vaccine": "RV-1", "code": "RV1", "age_weeks": 8, "age_label": "2 Months", "description": "Rotavirus vaccine - First dose"},
    {"vaccine": "DTaP-2", "code": "DTAP2", "age_weeks": 16, "age_label": "4 Months", "description": "Diphtheria, Tetanus, Pertussis - Second dose"},
    {"vaccine": "Hib-2", "code": "HIB2", "age_weeks": 16, "age_label": "4 Months", "description": "Haemophilus influenzae type b - Second dose"},
    {"vaccine": "IPV-2", "code": "IPV2", "age_weeks": 16, "age_label": "4 Months", "description": "Inactivated Polio Vaccine - Second dose"},
    {"vaccine": "PCV13-2", "code": "PCV2", "age_weeks": 16, "age_label": "4 Months", "description": "Pneumococcal Conjugate Vaccine - Second dose"},
    {"vaccine": "RV-2", "code": "RV2", "age_weeks": 16, "age_label": "4 Months", "description": "Rotavirus vaccine - Second dose"},
    {"vaccine": "DTaP-3", "code": "DTAP3", "age_weeks": 24, "age_label": "6 Months", "description": "Diphtheria, Tetanus, Pertussis - Third dose"},
    {"vaccine": "Hib-3", "code": "HIB3", "age_weeks": 24, "age_label": "6 Months", "description": "Haemophilus influenzae type b - Third dose"},
    {"vaccine": "IPV-3", "code": "IPV3", "age_weeks": 24, "age_label": "6 Months", "description": "Inactivated Polio Vaccine - Third dose"},
    {"vaccine": "PCV13-3", "code": "PCV3", "age_weeks": 24, "age_label": "6 Months", "description": "Pneumococcal Conjugate Vaccine - Third dose"},
    {"vaccine": "RV-3", "code": "RV3", "age_weeks": 24, "age_label": "6 Months", "description": "Rotavirus vaccine - Third dose"},
    {"vaccine": "Hepatitis B-3", "code": "HEPB3", "age_weeks": 24, "age_label": "6-18 Months", "description": "Hepatitis B vaccine - Third dose"},
    {"vaccine": "Influenza (Yearly)", "code": "FLU1", "age_weeks": 26, "age_label": "6 Months+", "description": "Influenza vaccine - Annual dose"},
    {"vaccine": "MMR-1", "code": "MMR1", "age_weeks": 52, "age_label": "12-15 Months", "description": "Measles, Mumps, Rubella - First dose"},
    {"vaccine": "PCV13-4", "code": "PCV4", "age_weeks": 52, "age_label": "12-15 Months", "description": "Pneumococcal Conjugate Vaccine - Fourth dose"},
    {"vaccine": "Hib-4", "code": "HIB4", "age_weeks": 52, "age_label": "12-15 Months", "description": "Haemophilus influenzae type b - Fourth dose"},
    {"vaccine": "Varicella-1", "code": "VAR1", "age_weeks": 52, "age_label": "12-15 Months", "description": "Chickenpox vaccine - First dose"},
    {"vaccine": "Hepatitis A-1", "code": "HEPA1", "age_weeks": 52, "age_label": "12-23 Months", "description": "Hepatitis A vaccine - First dose"},
    {"vaccine": "DTaP-4", "code": "DTAP4", "age_weeks": 65, "age_label": "15-18 Months", "description": "Diphtheria, Tetanus, Pertussis - Fourth dose"},
    {"vaccine": "Hepatitis A-2", "code": "HEPA2", "age_weeks": 78, "age_label": "18+ Months", "description": "Hepatitis A vaccine - Second dose"},
    {"vaccine": "DTaP-5", "code": "DTAP5", "age_weeks": 208, "age_label": "4-6 Years", "description": "Diphtheria, Tetanus, Pertussis - Fifth dose"},
    {"vaccine": "IPV-4", "code": "IPV4", "age_weeks": 208, "age_label": "4-6 Years", "description": "Inactivated Polio Vaccine - Fourth dose"},
    {"vaccine": "MMR-2", "code": "MMR2", "age_weeks": 208, "age_label": "4-6 Years", "description": "Measles, Mumps, Rubella - Second dose"},
    {"vaccine": "Varicella-2", "code": "VAR2", "age_weeks": 208, "age_label": "4-6 Years", "description": "Chickenpox vaccine - Second dose"},
    {"vaccine": "Tdap", "code": "TDAP", "age_weeks": 572, "age_label": "11-12 Years", "description": "Tetanus, Diphtheria, Pertussis booster"},
    {"vaccine": "HPV-1", "code": "HPV1", "age_weeks": 572, "age_label": "11-12 Years", "description": "Human Papillomavirus - First dose"},
    {"vaccine": "HPV-2", "code": "HPV2", "age_weeks": 598, "age_label": "11-12 Years + 6mo", "description": "Human Papillomavirus - Second dose"},
    {"vaccine": "Meningococcal-1", "code": "MCV1", "age_weeks": 572, "age_label": "11-12 Years", "description": "Meningococcal conjugate vaccine - First dose"},
    {"vaccine": "Meningococcal-2", "code": "MCV2", "age_weeks": 832, "age_label": "16 Years", "description": "Meningococcal conjugate vaccine - Booster"},
]

def get_schedule_for_guideline(guideline: str) -> List[Dict]:
    if guideline == "India (UIP)":
        return INDIA_UIP_SCHEDULE
    elif guideline == "WHO":
        return WHO_SCHEDULE
    elif guideline == "CDC (USA)":
        return CDC_SCHEDULE
    return WHO_SCHEDULE

def calculate_due_date(dob: date, age_weeks: int) -> date:
    return dob + timedelta(weeks=age_weeks)

def generate_vaccination_schedule(dob: date, guideline: str) -> List[Dict]:
    schedule = get_schedule_for_guideline(guideline)
    vaccination_schedule = []
    
    for vaccine in schedule:
        due_date = calculate_due_date(dob, vaccine["age_weeks"])
        vaccination_schedule.append({
            "vaccine_name": vaccine["vaccine"],
            "vaccine_code": vaccine["code"],
            "due_date": due_date,
            "age_label": vaccine["age_label"],
            "description": vaccine["description"]
        })
    
    return vaccination_schedule

def get_vaccine_status(due_date: date, administered_date: date = None) -> str:
    today = date.today()
    
    if administered_date:
        return "completed"
    elif due_date < today:
        return "overdue"
    elif due_date <= today + timedelta(days=30):
        return "upcoming"
    else:
        return "pending"

def categorize_vaccinations(vaccinations: List[Dict]) -> Dict[str, List[Dict]]:
    today = date.today()
    categories = {
        "overdue": [],
        "upcoming": [],
        "completed": [],
        "pending": []
    }
    
    for vacc in vaccinations:
        due_date = vacc.get('due_date')
        if isinstance(due_date, str):
            due_date = date.fromisoformat(due_date)
        
        if vacc.get('status') == 'completed':
            categories["completed"].append(vacc)
        elif due_date < today:
            categories["overdue"].append(vacc)
        elif due_date <= today + timedelta(days=30):
            categories["upcoming"].append(vacc)
        else:
            categories["pending"].append(vacc)
    
    return categories

def get_age_string(dob: date) -> str:
    today = date.today()
    delta = relativedelta(today, dob)
    
    parts = []
    if delta.years > 0:
        parts.append(f"{delta.years} year{'s' if delta.years > 1 else ''}")
    if delta.months > 0:
        parts.append(f"{delta.months} month{'s' if delta.months > 1 else ''}")
    if delta.days > 0 and delta.years == 0:
        parts.append(f"{delta.days} day{'s' if delta.days > 1 else ''}")
    
    return ", ".join(parts) if parts else "Newborn"
