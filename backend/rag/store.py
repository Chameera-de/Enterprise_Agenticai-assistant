import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]/'sample_data'

def load_docs():
    docs=[]
    for p in ROOT.rglob('*.json'):
        d=json.loads(p.read_text()); d['source']=str(p.relative_to(ROOT)); docs.append(d)
    return docs
