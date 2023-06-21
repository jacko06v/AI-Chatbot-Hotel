import spacy
from spacy.matcher import Matcher
from helper import elaborate_info
from api import trova_prezzo

# carica il modello italiano di spaCy
nlp = spacy.load("it_core_news_sm")

# definisce un pattern per estrarre delle date 
date_pattern = [
    [{"LOWER": {"REGEX": "dal|da"}}, {"TEXT": {"REGEX": "\d{1,2}"}}, {"TEXT": {"REGEX": "\w+"}}, {"LOWER": {"REGEX": "al|a"}}, {"TEXT": {"REGEX": "\d{1,2}"}}, {"TEXT": {"REGEX": "\w+"}}],
    [{"LOWER": {"REGEX": "al|a"}}, {"TEXT": {"REGEX": "\d{1,2}"}}, {"TEXT": "/"}, {"TEXT": {"REGEX": "\d{1,2}"}}, {"LOWER": {"REGEX": "al|a"}}, {"TEXT": {"REGEX": "\d{1,2}"}}, {"TEXT": "/"}, {"TEXT": {"REGEX": "\d{1,2}"}}],
    [{"TEXT": {"REGEX": "\\d{2}/\\d{2}"}, "OP": "?"}, {"LOWER": "dal"}, {"TEXT": {"REGEX": "\\d{2}/\\d{2}"}, "OP": "?"}, {"LOWER": "al"}, {"TEXT": {"REGEX": "\\d{2}/\\d{2}"}, "OP": "?"}],
    [{"TEXT": {"REGEX": "\\d{2}/\\d{2}"}, "OP": "?"}, {"LOWER": "da"}, {"TEXT": {"REGEX": "\\d{2}/\\d{2}"}, "OP": "?"}, {"LOWER": "a"}, {"TEXT": {"REGEX": "\\d{2}/\\d{2}"}, "OP": "?"}],
     [{"TEXT": {"REGEX": "\\d{2}/\\d{2}/\\d{4}"}, "OP": "?"}, {"LOWER": "dal"}, {"TEXT": {"REGEX": "\\d{2}/\\d{2}"}, "OP": "?"}, {"LOWER": "al"}, {"TEXT": {"REGEX": "\\d{2}/\\d{2}"}, "OP": "?"}],
    [{"TEXT": {"REGEX": "\\d{2}/\\d{2}/\\d{4}"}, "OP": "?"}, {"LOWER": "da"}, {"TEXT": {"REGEX": "\\d{2}/\\d{2}"}, "OP": "?"}, {"LOWER": "a"}, {"TEXT": {"REGEX": "\\d{2}/\\d{2}"}, "OP": "?"}],
    [{"LOWER": "dal"},  {"TEXT": {"REGEX": "\d{1,2}"}}, {"LOWER": {"REGEX": "(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)"}, "OP": "?"}, {"TEXT": {"REGEX": "\d{4}"}, "OP": "?"}, {"LOWER": "al"},  {"TEXT": {"REGEX": "\d{1,2}"}},  {"LOWER": {"REGEX": "(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)"}},  {"TEXT": {"REGEX": "\d{4}"}, "OP": "?"}],
]

# definisce un pattern per estrarre la tipologia di camera (es. camera doppia, stanza doppia, camera matrimoniale, stanza matrimoniale, camera singola, stanza singola, una matrimoniale, una singola)
room_pattern = [
    [{"TEXT": {"REGEX": "camera"}}, {"TEXT": {"REGEX": "doppia|matrimoniale|singola|tripla|quadrupla"}}],
    [{"TEXT": {"REGEX": "stanza"}}, {"TEXT": {"REGEX": "doppia|matrimoniale|singola|tripla|quadrupla"}}],
    [{"TEXT": {"REGEX": "una"}}, {"TEXT": {"REGEX": "doppia|matrimoniale|singola|tripla|quadrupla"}}],
]

# crea un matcher e aggiunge i pattern definiti
matcher = Matcher(nlp.vocab)
matcher.add("DATE", date_pattern)
matcher.add("ROOM", room_pattern)

# definisce una funzione per estrarre le informazioni dal testo
def extract_info(text):
    # analizza il testo
    doc = nlp(text)
    # cerca i pattern
    matches = matcher(doc)
    # se non trova nessun pattern ritorna None
    if not matches:
        return None
    # altrimenti crea un dizionario per le informazioni
    info = {}
    # scorre i match
    for match_id, start, end in matches:
        # recupera il nome del pattern
        name = nlp.vocab.strings[match_id]
        # recupera il testo del pattern
        value = doc[start:end].text
        # aggiunge il testo al dizionario
        info[name] = value
    # ritorna il dizionario
    return info

# definisce una funzione per estrarre le informazioni dal testo e stamparle
def print_info(text):
        info = extract_info(text)
        if info is None:
           return "Non ho capito bene, per avere un preventivo ti consiglio di chiedere: 'qual è il prezzo di una camera doppia dal 10 al 12 maggio?'", False
        elif "DATE" in info and "ROOM" in info:
            obj, frase = elaborate_info(info)
            return frase, trova_prezzo(obj)
        else:
            return "Non ho capito bene, per avere un preventivo ti consiglio di chiedere: 'qual è il prezzo di una camera doppia dal 10 al 12 maggio?'", False
