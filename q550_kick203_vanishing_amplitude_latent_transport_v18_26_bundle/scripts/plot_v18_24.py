"""Plot the actual persisted frozen and/or original outputs; no invented data."""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
for scope in ('frozen','original'):
    path=ROOT/'results'/f'{scope}_model_comparison.csv'
    if not path.exists():continue
    rows=list(csv.DictReader(path.open()))
    fig,ax=plt.subplots(figsize=(10,5.7))
    labels=[]
    for obs in ('material3','raw4','raw6'):
        for a in (3.5,4.0,4.5):
            arr=[r for r in rows if r['observer']==obs and float(r['anchor'])==a and float(r['sigma'])==1e-4]
            def val(mode):
                return np.mean([float(r['test_rmse']) for r in arr if r['model']==mode])
            labels.append((obs,a,val('endpoint'),val('chronological'),val('past_random_per_trial')))
    x=np.arange(len(labels));w=.26
    for j,model in enumerate(('Endpoint','Chronological','Past scrambled (endpoint fixed)')):
        ys=[row[j+2] for row in labels]
        ax.bar(x+(j-1)*w,ys,w,label=model)
    ax.set_yscale('log');ax.set_xticks(x)
    ax.set_xticklabels([f'{obs}\nξ={a:g}' for obs,a,*_ in labels],rotation=30,ha='right')
    ax.set_ylabel('Held-out future RMSE (normalized diagnostic output)')
    ax.set_title(f'Q550 v18.24 — {scope}: endpoint-preserved timing test')
    ax.grid(axis='y',alpha=.2);ax.legend(fontsize=8);fig.tight_layout()
    fig.savefig(ROOT/'results'/f'{scope}_endpoint_preserved_history.png',dpi=140);plt.close(fig)
