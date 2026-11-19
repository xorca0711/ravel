"""Complete finite-gene displays; no patient-population inference or gene selection."""
import string
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot(frames, output, constructed=False):
    plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False,
                         'pdf.fonttype': 42, 'font.family': 'DejaVu Sans'})
    fig, axes = plt.subplots(3, 2, figsize=(11, 12), layout='constrained')
    rows = [('P: post-challenge I - NI', 'A: response interaction'),
            ('R_NI: stimulation response', 'R_I: stimulation response'),
            ('A: primary MOR', 'A: total-count sensitivity')]
    for r in range(3):
        values = []
        for patient in ['4', '83']:
            primary, secondary = frames[patient]['MOR'], frames[patient]['total']
            mask = primary.eligible
            x, y = [(primary.P, primary.A), (primary.R_NI, primary.R_I), (primary.A, secondary.A)][r]
            values.append((x[mask].to_numpy(), y[mask].to_numpy()))
        arrays = [a for pair in values for a in pair if len(a)]
        bound = max(1., max((float(np.max(np.abs(a))) for a in arrays), default=1.))*1.05
        for c, patient in enumerate(['4', '83']):
            ax = axes[r, c]; x, y = values[c]
            if len(x):
                artist = ax.hexbin(x, y, gridsize=55, bins='log', mincnt=1, cmap='viridis',
                                   extent=(-bound, bound, -bound, bound), linewidths=0)
                artist.set_clim(1, max(2, float(artist.get_array().max())))
                fig.colorbar(artist, ax=ax, label='Genes per bin', shrink=.75)
            else:
                ax.text(.5, .5, 'No eligible genes', transform=ax.transAxes, ha='center')
            ax.axhline(0, color='.65', lw=.6); ax.axvline(0, color='.65', lw=.6)
            ax.plot([-bound, bound], [-bound, bound], '--', color='.35', lw=.7)
            ax.set(xlim=(-bound, bound), ylim=(-bound, bound), aspect='equal',
                   xlabel=rows[r][0]+' (log2 scale)', ylabel=rows[r][1]+' (log2 scale)',
                   title=f'{string.ascii_uppercase[2*r+c]}  Patient {patient}; {len(x):,} eligible genes')
    label = 'CONSTRUCTED DATA — no Hamdan outcomes\n' if constructed else ''
    fig.suptitle(label+'Concurrent-control response decomposition\nTwo donors reported separately; gene density is not biological replication', fontsize=12)
    for extension in ['png', 'pdf']:
        fig.savefig(output/('fig01_response_decomposition.'+extension), dpi=220, metadata={'Creator': 'Ravel S7 descriptive analysis'})
    plt.close(fig)
