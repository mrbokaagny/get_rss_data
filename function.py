import os
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_rss_flux(rss_flux): 
    articles = []
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try: 
        response = requests.get(rss_flux, headers=headers)

        if response.status_code == 200: 
            soup = BeautifulSoup(response.text, 'lxml-xml')

            for item in soup.find_all('item'): 
                article = {
                    "id": item.guid.text if item.guid else None,
                    "title": item.title.text if item.title else None,
                    "description": item.description.text if item.description else None,
                    "published": item.pubDate.text if item.pubDate else None,
                    "creator": item.find('dc:creator').text if item.find('dc:creator') else None,
                    "link": item.link.text if item.link else None,
                    "category": item.category.text if item.category else None
                }
                articles.append(article)
            
            return articles
        else: 
            print("fail to load data ..., status code : ", response.status_code)
            return []

    except requests.exceptions.RequestException as e:
        print("Erreur lors de la requête :", e)
        return []

def store_data_in_volume(data, chemin_destination) : 

    
    if data:
        articles_dataframe = pd.DataFrame(data)
        
        os.makedirs('/data', exist_ok=True) 
        
        articles_dataframe.to_csv(chemin_destination, index=False)
        print(f"Données stockées avec succès dans {chemin_destination}")
    else:
        print("Aucune donnée à enregistrer.")

def load_data_from_volume(file_path):

    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier {file_path} est introuvable dans le volume data.")
        return None
    
    try:
        df = pd.read_csv(file_path)
        print("Données chargées avec succès depuis le fichier CSV.")
        return df
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV : {e}")


def store_in_database(df, db_connection, table_name): 
    if df is not None and not df.empty:
        try:
            df.to_sql(table_name, db_connection, if_exists='append', index=False)
            print(f"Données stockées avec succès dans la table précise : '{table_name}'.")
        except Exception as e:
            print("Erreur lors de l'enregistrement dans la base de données :", e)
    else:
        print("Aucune donnée à enregistrer dans la base de données.")


