def analyze_batches(docs, batch_size=2):
    batches=[]
    for i in range(0,len(docs),batch_size):
        b=docs[i:i+batch_size]
        causes=[]
        for d in b:
            causes += d.get('root_causes',[])
        batches.append({'sources':[d['source'] for d in b], 'root_causes':causes})
    counts={}
    for b in batches:
        for c in b['root_causes']: counts[c]=counts.get(c,0)+1
    return {'batches':batches,'recurring_root_causes':sorted(counts.items(),key=lambda x:x[1],reverse=True)}
