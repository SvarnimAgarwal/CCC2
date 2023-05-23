from ibmcloudant.cloudant_v1 import CloudantV1
from ibmcloudant import CouchDbSessionAuthenticator
from requests.exceptions import HTTPError
from modules.constants import *

class CouchDBClient():

    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url
    
    def connect(self) -> bool:
        try:
            self.authenticator = CouchDbSessionAuthenticator(self.username, self.password)
            self.client = CloudantV1(authenticator=self.authenticator)
            self.client.set_service_url(self.url)
            print("Connected to DB")
            return True
        except:
            print("Failed connection to DB")
            return False

    def get_session(self) -> dict:
        return self.client.get_session_information().get_result()
    
    def get_all_database(self) -> list:
        return self.client.get_all_dbs().get_result()
    
    def get_all_docs_from_database(self, database) -> list:
        return self.client.post_all_docs(db=database).get_result()
    
    def get_document(self, database, id):
        return self.client.get_document(db=database, doc_id=id).get_result()
    
    def update_document(self, database, new_doc):
        print("update called")
        return self.client.post_document(db=database, document=new_doc).get_result()
    
    def get_client(self) -> CloudantV1:
        return self.client
    
    def create_database(self, database) -> bool:
        if (database in self.get_all_database()):
            return True
        return self.client.put_database(database, partitioned=False).get_result()
    
    def add_document(self, database, doc) -> None:
        try:
            response = self.client.post_document(db=database, document=doc).get_result()
            return response
        except HTTPError as err:
            print(f'HTTPError occured on add_document: {err}')
        except Exception as e:
            print(f'Failed add document')
            print(e)

    def add_bulk_document(self, database, docs) -> dict:
        try:
            response = self.client.post_bulk_docs(db=database, bulk_docs=docs).get_result()
            return response
        except HTTPError as err:
            print(f'HTTPError occured on add_bulk_document: {err}')
        except Exception as e:
            print(f'Failed add_bulk_document')
            print(e)

