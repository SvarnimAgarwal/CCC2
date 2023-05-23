from ibmcloudant.cloudant_v1 import Document
from modules.mastodon_client import MastodonClient
from modules.db_client import CouchDBClient
from modules.constants import *
import os

def get_couchDB_client() -> CouchDBClient:
    db_client = CouchDBClient(DB_USERNAME, DB_PASSWORD, DB_URL)
    return db_client

def connect_to_couchDB(db_client: CouchDBClient) -> bool:
    return db_client.connect()

def get_available_site(db_client: CouchDBClient) -> dict:
    tokens = db_client.get_all_docs_from_database(TOKEN_DATABASE)
    if (tokens["total_rows"] == 0):
        for site in MASTODON_SITES:
            db_client.add_document(TOKEN_DATABASE, Document(URL=site['URL'], TOKEN= site['TOKEN'], IN_USE=False))
            tokens = db_client.get_all_docs_from_database(TOKEN_DATABASE) 
    for doc in tokens['rows']:
        site_doc = db_client.get_document(TOKEN_DATABASE, doc['id'])
        if site_doc['IN_USE']:
            continue
        db_client.update_document(TOKEN_DATABASE, Document(id=site_doc['_id'], rev=site_doc['_rev'], URL=site_doc['URL'], TOKEN=site_doc['TOKEN'], IN_USE=True))
        return site_doc
    return None

def release_token(db_client: CouchDBClient, site: dict) -> None:
    if (site != None) and (db_client != None):
        site_doc = db_client.get_document(TOKEN_DATABASE, site['_id'])
        db_client.update_document(TOKEN_DATABASE, Document(id=site_doc['_id'], rev=site_doc['_rev'], URL=site_doc['URL'], TOKEN=site_doc['TOKEN'], IN_USE=False))

def get_mastodon_client(db_client: CouchDBClient, site: dict) -> MastodonClient:
    url = site['URL']
    token = os.environ[site['TOKEN']]
    mastodon_client = MastodonClient(url, token, db_client)
    return mastodon_client

def main() -> None:
    trial = 0
    site = None
    
    while trial < MAX_ATTEMPT:
        try:
            mastodon_clinet = None
            db_client = get_couchDB_client()
            connected = connect_to_couchDB(db_client)
            
            if (not connected):
                print("Failed to connect to db")
                return
            
            if (not db_client.create_database(TOOTH_DATABASE)) or (not db_client.create_database(TOKEN_DATABASE)):
                print("Failed to create database")
                return
            
            print("fetching available site")
            site = get_available_site(db_client)
            
            if (site == None):
                print("All Mastodon API Token in use...")
                return
            
            print("initialising mastodon client")
            mastodon_client = get_mastodon_client(db_client, site)

            print("public streaming started")
            mastodon_client.start_public_streaming()
            
        except Exception as e:
            print(f"Accounted Error {trial} times: {e}")
            if mastodon_clinet != None:
                mastodon_client.close_stream()
            release_token(db_client, site)
            trial += 1

    release_token(db_client, site)

if __name__ == '__main__':
    main()