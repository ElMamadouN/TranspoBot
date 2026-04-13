from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="TranspoBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

USE_OLLAMA = os.environ.get("USE_OLLAMA", "false").lower() == "true"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

SYSTEM_PROMPT = """Tu es un assistant IA pour une societe de transport urbain au Senegal.
Tu generes des requetes SQL SELECT pour repondre aux questions.

Tables: vehicules, chauffeurs, lignes, trajets, incidents

Reponds avec format:
SQL: <requete SQL>
REPONSE: <reponse>"""

VEHICULES = [
    {"id":1,"immatriculation":"DK-9012-EF","marque":"Mercedes","modele":"Citaro","annee":2020,"kilometrage":78000,"statut":"maintenance"},
    {"id":2,"immatriculation":"DK-1234-AB","marque":"Volvo","modele":"7900","annee":2019,"kilometrage":120000,"statut":"actif"},
    {"id":3,"immatriculation":"DK-5678-CD","marque":"Iveco","modele":"Urbanway","annee":2021,"kilometrage":45000,"statut":"actif"},
    {"id":4,"immatriculation":"DK-9012-GH","marque":"Mercedes","modele":"Citaro","annee":2018,"kilometrage":180000,"statut":"hors_service"},
    {"id":5,"immatriculation":"DK-3456-IJ","marque":"Scania","modele":"N230","annee":2022,"kilometrage":25000,"statut":"actif"}
]

CHAUFFEURS = [
    {"id":1,"nom":"FALL","prenom":"Ibrahima","telephone":"771234567","licence":"B","date_embauche":"2019-03-15","statut":"actif"},
    {"id":2,"nom":"DIOP","prenom":"Moussa","telephone":"772345678","licence":"D","date_embauche":"2020-06-01","statut":"actif"},
    {"id":3,"nom":"SOW","prenom":"Fatou","telephone":"773456789","licence":"B","date_embauche":"2018-01-10","statut":"actif"},
    {"id":4,"nom":"NDIAYE","prenom":"Ousmane","telephone":"774567890","licence":"D","date_embauche":"2021-09-05","statut":"conge"},
    {"id":5,"nom":"SYLLA","prenom":"Mamadou","telephone":"775678901","licence":"B","date_embauche":"2022-02-20","statut":"actif"}
]

LIGNES = [
    {"id":1,"numero":"L1","nom":"Gare Routiere - Point E","debut_terminal":"Gare Routiere","fin_terminal":"Point E","distance_km":15.5},
    {"id":2,"numero":"L2","nom":"Pikine - Almadies","debut_terminal":"Pikine","fin_terminal":"Almadies","distance_km":22.0},
    {"id":3,"numero":"L3","nom":"Dakar Plateau - AIBD","debut_terminal":"Dakar Plateau","fin_terminal":"AIBD","distance_km":35.0}
]

TRAJETS = [
    {"id":1,"vehicule_id":1,"chauffeur_id":1,"ligne_id":1,"date_heure_depart":"2026-04-07 08:00:00","date_heure_arrivee":"2026-04-07 08:45:00","nb_passagers":45,"statut":"termine"},
    {"id":2,"vehicule_id":2,"chauffeur_id":2,"ligne_id":2,"date_heure_depart":"2026-04-07 09:00:00","date_heure_arrivee":"2026-04-07 09:50:00","nb_passagers":38,"statut":"termine"},
    {"id":3,"vehicule_id":3,"chauffeur_id":3,"ligne_id":1,"date_heure_depart":"2026-04-07 10:00:00","date_heure_arrivee":"2026-04-07 10:45:00","nb_passagers":52,"statut":"termine"},
    {"id":4,"vehicule_id":1,"chauffeur_id":1,"ligne_id":3,"date_heure_depart":"2026-04-08 08:00:00","date_heure_arrivee":"2026-04-08 09:00:00","nb_passagers":28,"statut":"termine"},
    {"id":5,"vehicule_id":2,"chauffeur_id":2,"ligne_id":2,"date_heure_depart":"2026-04-08 09:00:00","date_heure_arrivee":"2026-04-08 09:50:00","nb_passagers":41,"statut":"termine"}
]

INCIDENTS = [
    {"id":1,"trajet_id":1,"description":"Retard de 10 min","date_incident":"2026-04-07 08:30:00","gravite":"legel"},
    {"id":2,"trajet_id":2,"description":"Panne technique","date_incident":"2026-04-07 09:30:00","gravite":"moyen"},
    {"id":3,"trajet_id":4,"description":"Accident","date_incident":"2026-04-08 08:15:00","gravite":"grave"}
]

@app.get("/")
def root():
    return {"message": "TranspoBot API"}

@app.get("/vehicules")
def get_vehicules():
    return VEHICULES

@app.get("/chauffeurs")
def get_chauffeurs():
    return CHAUFFEURS

@app.get("/trajets")
def get_trajets():
    return TRAJETS

@app.get("/dashboard")
def get_dashboard():
    return {
        "vehicules_actifs": len([v for v in VEHICULES if v["statut"]=="actif"]),
        "chauffeurs_actifs": len([c for c in CHAUFFEURS if c["statut"]=="actif"]),
        "trajets_semaine": len([t for t in TRAJETS if t["statut"]=="termine"]),
        "incidents_mois": len(INCIDENTS)
    }

class Question(BaseModel):
    question: str

def extract_sql(text: str) -> str:
    for line in text.split('\n'):
        if line.startswith('SQL:'):
            return line.replace('SQL:', '').strip()
    return text

def search_data(sql: str):
    sql = sql.upper()
    results = []
    
    if "VEHICULES" in sql or ("SELECT" in sql and "VEHICULE" in sql):
        results = VEHICULES
        if "STATUT" in sql and "ACTIF" in sql:
            results = [v for v in VEHICULES if v["statut"]=="actif"]
        elif "MAINTENANCE" in sql:
            results = [v for v in VEHICULES if v["statut"]=="maintenance"]
    
    elif "CHAUFFEURS" in sql or "CHAUFFEUR" in sql:
        results = CHAUFFEURS
        if "STATUT" in sql and "ACTIF" in sql:
            results = [c for c in CHAUFFEURS if c["statut"]=="actif"]
    
    elif "TRAJETS" in sql or "TRAJET" in sql:
        results = TRAJETS
        if "COUNT" in sql:
            return [{"COUNT(*)": len(TRAJETS)}]
        if "TERMINE" in sql:
            results = [t for t in TRAJETS if t["statut"]=="termine"]
    
    elif "INCIDENTS" in sql or "INCIDENT" in sql:
        results = INCIDENTS
        if "COUNT" in sql:
            return [{"COUNT(*)": len(INCIDENTS)}]
    
    elif "COUNT(*)" in sql or "COUNT(" in sql:
        if "VEHICULE" in sql:
            return [{"COUNT(*)": len(VEHICULES)}]
        elif "CHAUFFEUR" in sql:
            return [{"COUNT(*)": len(CHAUFFEURS)}]
        elif "TRAJET" in sql:
            return [{"COUNT(*)": len(TRAJETS)}]
        elif "INCIDENT" in sql:
            return [{"COUNT(*)": len(INCIDENTS)}]
    
    return results

@app.post("/chat")
def chat(question: Question):
    if not OPENAI_API_KEY:
        return {"response": "API key non configuree. Utilisez USE_OLLAMA=true en local."}
    
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question.question}
        ],
        max_tokens=500
    )
    
    llm_response = response.choices[0].message.content
    sql_query = extract_sql(llm_response)
    
    if sql_query and "SELECT" in sql_query.upper():
        results = search_data(sql_query)
        return {"sql": sql_query, "results": results, "response": llm_response}
    
    return {"response": llm_response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)