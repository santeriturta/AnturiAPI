# AnturiAPI
 
## HUOM!
### Jotta virtuaaliympäristö toimii on oltava ./lopputyö/AnturiAPI kansiossa!


## Tarvittavat resurssit
### Työn suorittamiseksi täytyy ajaa seuraavat komennot (asentaa tarvittavat resurssit):

pip install fastapi
pip install pydantic
pip install sqlalchemy
pip install uvicorn
pip install venv


## Projektin käynnistäminen (bash terminaalissa)

python -m venv env

source ./env/Scripts/activate
uvicorn main:app --reload
