from pydantic import BaseModel


class File(BaseModel):
    name: str
    download_url: str


class Record(BaseModel):
    id: int
    doi: str
    title: str
    created: str
    updated: str
    links: dict
    files: list


class Template(BaseModel):
    id: str
    doi: str
    title: str
    created: str
    updated: str
    links: dict
