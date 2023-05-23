from ibmcloudant.cloudant_v1 import Document
import json

class Tooth():
    def __init__(self, id, created_date, language, tags, content) -> None:
        self._id = id
        self._created_date = created_date
        self._language = language
        self._hashtags = tags
        self._content = content

    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def get_id(self):
        return self._id
    
    def has_tags(self) -> bool:
        return len(self._tags) > 0
    
    def to_json(self):
        return json.dumps(self.__dict__, indent=2)
    
    def to_document(self):
        return Document(
            tooth_id=self._id,
            created_date=self._created_date,
            language=self._language,
            hashtags=self._hashtags,
            content=self._content
            )