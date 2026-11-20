"""Diagnostic plots from actual CSV files; original and frozen never conflated."""
from pathlib import Path
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];RES=ROOT/'results'

def read(path):
    with path.open() as f:return list(csv.DictReader(f))

def main():
    source='original' if (RES/'original_amplitude_prediction.csv').exists() else 'frozen'
    rows=read(RES/f'{source}_rank20_vs_10.csv')
    amps=np.array(sorted({float(r['amplitude']) for r in rows}))
    # An explicit paired ratio: ratio>1 means rank20 better.
    fig,ax=plt.subplots(figsize=(10,6))
    for mode in ('none','affine_ridge'):
      for anchor in (3.5,4.5):
        yy=[]
        for eps in amps:
          r=next(r for r in rows if r['observer']=='material3' and
                 r['noise_mode']=='none' and float(r['anchor'])==anchor and
                 r['method']==mode and float(r['amplitude'])==eps)
          yy.append(float(r['rank10_over_rank20']))
        ax.plot(amps,yy,marker='o',label=f'{mode} ξ={anchor}')
    ax.axhline(1.,linestyle='--',linewidth=1,label='equal rank-10 / rank-20 errors')
    ax.set(xscale='log',xlabel='Perturbation amplitude ε',ylabel='Test RMSE(rank10) / RMSE(rank20)',
           title=f'v18.26 {source.upper()} — Cross-posture latent rank (zero sensor noise)')
    ax.legend(fontsize=8);ax.grid(alpha=.25)
    fig.tight_layout();fig.savefig(RES/f'{source}_rank_survival_vs_amplitude.png',dpi=145);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,6))
    for noise in ('fixed_normalized','fixed_absolute'):
        yy=[]
        for eps in amps:
            r=next(r for r in rows if r['observer']=='material3' and r['method']=='none'
                and float(r['anchor'])==4. and r['noise_mode']==noise and
                float(r['amplitude'])==eps)
            yy.append(float(r['rank10_rmse']))
        ax.plot(amps,yy,marker='o',label=noise)
    ax.set(xscale='log',yscale='log',xlabel='Perturbation amplitude ε',ylabel='Held-out test RMSE (rank 10)',
           title=f'v18.26 {source.upper()} — Distinct normalized and absolute noise protocols')
    ax.legend();ax.grid(alpha=.25)
    fig.tight_layout();fig.savefig(RES/f'{source}_noise_floor_vs_amplitude.png',dpi=145);plt.close(fig)
    if source=='original':
        rows=read(RES/'original_even_odd_probe.csv')
        fig,ax=plt.subplots(figsize=(10,6))
        for obs in ('material3','raw4','raw6'):
            subset=sorted((r for r in rows if r['observer']==obs and float(r['anchor'])==4.),
                          key=lambda r:float(r['amplitude']))
            ax.loglog([float(r['amplitude']) for r in subset],
                      [float(r['even_response_rms']) for r in subset],'-o',label=f'{obs}: even signal')
            ax.loglog([float(r['amplitude']) for r in subset],
                      [float(r['odd_vs_tangent_rms']) for r in subset],'--o',label=f'{obs}: odd-tangent residual')
        ax.set(xlabel='Perturbation amplitude ε',ylabel='Normalized response RMS',
          title='Original ODE ±ε: even response versus odd residual / tangent')
        ax.grid(alpha=.25);ax.legend(fontsize=8)
        fig.tight_layout();fig.savefig(RES/'original_even_odd_scaling.png',dpi=145);plt.close(fig)
    print('PLOTS_COMPLETE',source)
if __name__=='__main__':main()
