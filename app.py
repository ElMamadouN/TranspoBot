from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = FastAPI(title="TranspoBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

SYSTEM_PROMPT = """Tu es un assistant IA pour une societe de transport urbain au Senegal.
Tu dois repondre aux questions en langage naturel en generant des requetes SQL SELECT uniquement.

Schema de la base de donnees:
- vehicules(id, immatriculation, marque, modele, annee, kilometrage, statut)
- chauffeurs(id, nom, prenom, telephone, licence, date_embauche, statut)
- lignes(id, numero, nom, debut_terminal, fin_terminal, distance_km)
- tarifs(id, ligne_id, type_tarif, montant)
- trajets(id, vehicule_id, chauffeur_id, ligne_id, date_heure_depart, date_heure_arrivee, nb_passagers, statut)
- incidents(id, trajet_id, description, date_incident, gravite)

Regles importantes:
1. Reponds TOUJOURS par un SQL SELECT (jamais INSERT, UPDATE, DELETE)
2. Utilise les jointures quand necessaire (trajets.chauffeur_id = chauffeurs.id, etc.)
3. Pour les dates, utilise NOW() et DATE_SUB(NOW(), INTERVAL X DAY/MONTH)
4. Formate ta reponse en francais de maniere claire
5. Si la question n'est pas SQL-able (ex: "qui est le patron?"), reponds directement

Reponds avec ce format:
SQL: <requete SQL>
REPONSE: <reponse en francais>"""

def get_db():
    import sqlite3
    db_path = os.path.join(os.path.dirname(__file__), "transport.db")
    return sqlite3.connect(db_path)

class Question(BaseModel):
    question: str

def extract_sql(text: str) -> str:
    for line in text.split('\n'):
        if line.startswith('SQL:'):
            return line.replace('SQL:', '').strip()
    return text

@app.get("/")
def root():
    return {"message": "TranspoBot API - Gestion de Transport Urbain"}

@app.get("/vehicules")
def get_vehicules():
    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicules")
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chauffeurs")
def get_chauffeurs():
    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chauffeurs")
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trajets")
def get_trajets():
    try:
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trajets ORDER BY date_heure_depart DESC LIMIT 20")
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard")
def get_dashboard():
    try:
        from datetime import datetime, timedelta
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM vehicules WHERE statut='actif'")
        vehicules_actifs = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM chauffeurs WHERE statut='actif'")
        chauffeurs_actifs = cursor.fetchone()['total']
        
        semaine_derniere = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        cursor.execute("SELECT COUNT(*) as total FROM trajets WHERE statut='termine' AND date_heure_depart >= ?", (semaine_derniere,))
        try:
            trajets_semaine = cursor.fetchone()['total']
        except:
            trajets_semaine = 0
        
        mois_dernier = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        cursor.execute("SELECT COUNT(*) as total FROM incidents WHERE date_incident >= ?", (mois_dernier,))
        try:
            incidents_mois = cursor.fetchone()['total']
        except:
            incidents_mois = 0
        
        cursor.close()
        conn.close()
        
        return {
            "vehicules_actifs": vehicules_actifs,
            "chauffeurs_actifs": chauffeurs_actifs,
            "trajets_semaine": trajets_semaine,
            "incidents_mois": incidents_mois
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def call_llm(prompt: str) -> str:
    if USE_OLLAMA:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": "llama3",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
        )
        return response.json()["message"]["content"]
    else:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content

@app.post("/chat")
def chat(question: Question):
    try:
        llm_response = call_llm(question.question)
        
        sql_query = extract_sql(llm_response)
        
        if sql_query and "SELECT" in sql_query.upper():
            conn = get_db()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            sql_results = [dict(row) for row in rows]
            cursor.close()
            conn.close()
            
            return {
                "sql": sql_query,
                "results": sql_results,
                "response": llm_response
            }
        
        return {
            "sql": None,
            "results": None,
            "response": llm_response
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)