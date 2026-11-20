"""Plot only measured CSVs; no generation or fabricated server outputs."""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
for scope in ('frozen','original'):
    infile=ROOT/'results'/f'{scope}_transport_comparison.csv'
    if not infile.exists():continue
    with infile.open() as f:rows=list(csv.DictReader(f))
    fig,axes=plt.subplots(1,3,figsize=(15,4.3),sharey=False)
    modes=('none','past_lag','orthogonal','lag_orthogonal','affine_ridge','broken_pair_orthogonal')
    for ax,obs in zip(axes,('material3','raw4','raw6')):
        for rank in (10,20):
            chosen=[q for q in rows if q['observer']==obs and float(q['sigma'])==1e-4 and float(q['anchor'])==4.5 and int(q['rank'])==rank]
            vals=[float(next(q['test_rmse'] for q in chosen if q['method']==name)) for name in modes]
            xx=np.arange(len(modes))+(rank-15)*.032
            ax.plot(xx,np.maximum(vals,1e-14),marker='o',label=f'rank {rank}')
        ax.set_yscale('log');ax.grid(alpha=.25)
        ax.set_xticks(range(len(modes)));ax.set_xticklabels(['raw','lag','ortho','lag+ortho','affine','wrong pair'],rotation=40,ha='right')
        ax.set_title(obs+' | shift +0.5 xi');ax.set_ylabel('Held-out future RMSE')
        ax.legend(fontsize=8)
    fig.suptitle(f'v18.25 {scope} — past-only frame calibration; future test held out')
    fig.tight_layout()
    fig.savefig(ROOT/'results'/f'{scope}_transport_comparison.png',dpi=145,bbox_inches='tight')
    plt.close(fig)
