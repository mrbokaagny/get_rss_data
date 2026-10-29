import sys
import os
from db import get_db_conn
from function import get_rss_flux, load_data_from_volume, store_data_in_volume, store_in_database

NOM_TABLE_PRECISE = "articles"

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else None
    rss_url = sys.argv[2] if len(sys.argv) > 2 else None

    if not action:
        print("Erreur : Aucune action spécifiée (scrape ou insert).")
        sys.exit(1)

    flux_name = rss_url.split('/')[-2] if rss_url else "generic"
    chemin_csv = f"/data/{flux_name}_articles.csv"

    if action == "scrape":
        if not rss_url:
            print("Erreur : URL manquante pour le scraping.")
            sys.exit(1)
            
        print(f"Extraction du flux RSS : {rss_url}")
        datas = get_rss_flux(rss_url)
        store_data_in_volume(datas, chemin_csv)
        print(f"Flux sauvegardé dans le volume : {chemin_csv}")

    elif action == "insert":
        print(f"Lecture du fichier depuis le volume : {chemin_csv}")
        datas = load_data_from_volume(chemin_csv)

        if datas is not None and len(datas) > 0:
            conn = get_db_conn()
            store_in_database(datas, conn, NOM_TABLE_PRECISE)
            conn.dispose()
            print(f"Données de {flux_name} insérées en BDD avec succès.")
        else:
            print(f"Aucune donnée trouvée ou fichier vide pour {chemin_csv}")
