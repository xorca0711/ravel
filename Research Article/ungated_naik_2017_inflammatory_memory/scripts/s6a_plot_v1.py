"""All six panels and observed days; lines connect group summaries, never animals."""
import textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

COLORS = ['#627582', '#1685a2', '#b07c3e', '#8160a1']


def export(fig, output, name):
    fig.savefig(output/(name+'.png'), dpi=230, bbox_inches='tight')
    fig.savefig(output/(name+'.pdf'), bbox_inches='tight', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)


def axes_grid(title):
    fig, axs = plt.subplots(3, 2, figsize=(15, 15), layout='constrained')
    fig.suptitle(title, fontsize=16)
    for ax in axs.flat:
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='y', alpha=.16)
    return fig, list(axs.flat)


def plot(output, mapping, data):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'pdf.fonttype': 42})
    groups = {(x['panel'], x['day'], x['group']): x for x in data['groups']}
    fig, axes = axes_grid('All supplied daily wound-area records\nPoints are spreadsheet observations; lines connect available group means, not animal trajectories')
    for ax, p in zip(axes, mapping['panels']):
        for i, gid in enumerate(p['group_order']):
            color = COLORS[i]
            for day in p['days']:
                vals = [x['value'] for x in data['observations'] if x['panel'] == p['id'] and x['day'] == day and x['group'] == gid and not x['missing']]
                # Fixed horizontal offsets show overlapping records without stochastic jitter.
                offsets = np.linspace(-.065, .065, len(vals)) if len(vals) > 1 else np.array([0.])
                if vals: ax.scatter(day + (i-(len(p['group_order'])-1)/2)*.14 + offsets, vals, color=color, s=15, alpha=.55, linewidths=0)
            vals = [groups[p['id'], d, gid]['mean'] for d in p['days']]
            label = groups[p['id'], p['days'][0], gid]['label']
            ax.plot(p['days'], [np.nan if v is None else v for v in vals], color=color, lw=1.8, marker='o', ms=3,
                label='\n'.join(textwrap.wrap(label, 24)))
        ax.set(title=p['id']+': '+p['label'], xlabel='Days after wounding', ylabel='Remaining wound area (mm²)', xticks=p['days'])
        ax.set_ylim(bottom=0)
        ax.legend(fontsize=8, frameon=False, ncol=2)
    export(fig, output, 'fig01_daily_area_groups')

    for adjusted, name in [(False, 'fig02_raw_area_contrasts'), (True, 'fig03_day0_components')]:
        title = 'Day-0 subtraction of group-area contrasts' if adjusted else 'Raw group-area contrasts across every observed day'
        subtitle = ('Adjusted = raw − day-0 contrast; day-0 zero is structural\n'
            'Solid: mean; dashed: median; ×: all contributing observed areas are 0\n'
            'At ×, adjusted = −baseline, not a persistent repair difference\n'
            'Shared baseline and changing record coverage remain') if adjusted else 'Solid: mean contrast; dashed: median contrast; positive means larger remaining area, not faster closure'
        fig, axes = axes_grid(title+'\n'+subtitle)
        field = 'adjusted_' if adjusted else 'raw_'
        for ax, p in zip(axes, mapping['panels']):
            rows = [r for r in data['contrasts'] if r['panel'] == p['id']]
            labels = []
            for i, c in enumerate(p['contrasts']):
                rs = [r for r in rows if r['contrast'] == p['id']+'__'+c['id']]
                for stat, ls, marker in [('mean', '-', 'o'), ('median', '--', None)]:
                    values = [np.nan if r[field+stat] is None else r[field+stat] for r in rs]
                    ax.plot([r['day'] for r in rs], values, ls, color=COLORS[i], marker=marker, ms=3, lw=1.6,
                        label=c['label'] if stat == 'mean' else None)
                    if adjusted:
                        floor = [r for r in rs if r['adjusted_at_area_floor']]
                        ax.scatter([r['day'] for r in floor], [r[field+stat] for r in floor],
                            color=COLORS[i], marker='x', s=48, linewidths=1.4, zorder=6)
                if adjusted:
                    v = rs[0]['baseline_mean']
                    labels.append(('NA' if v is None else f'{v:.3g}'))
            ax.axhline(0, color='#777777', lw=.7)
            title = p['id']+': '+p['label']
            if adjusted: title += '\nDay-0 mean contrasts, legend order: '+', '.join(labels)+' mm²'
            if p['id'] == 'EDF6f': title += '\nDay 10: WT effect and effect difference are NA'
            ax.set(title=title, xlabel='Days after wounding', ylabel='Adjusted area contrast (mm²)' if adjusted else 'Area contrast (mm²)', xticks=p['days'])
            ax.legend(fontsize=8, frameon=False)
        export(fig, output, name)

    fig, axs = plt.subplots(3, 2, figsize=(15, 10), layout='constrained')
    fig.suptitle('Source-record coverage, not independent animal counts\nNumbers are observed spreadsheet records; 0 = labelled day, all slots blank; — = day not supplied', fontsize=15)
    cmap = ListedColormap(['#ededed', '#edbbbb', '#dcebf0'])
    for ax, p in zip(axs.flat, mapping['panels']):
        display = np.zeros((len(p['group_order']), 11))
        for i, gid in enumerate(p['group_order']):
            for d in range(11):
                n = groups[p['id'], d, gid]['source_n'] if d in p['days'] else None
                display[i, d] = 0 if n is None else (1 if n == 0 else 2)
                ax.text(d, i, '—' if n is None else str(n), ha='center', va='center', fontsize=11)
        ax.imshow(display, vmin=0, vmax=2, cmap=cmap, aspect='auto', interpolation='nearest')
        labels = [groups[p['id'], 0, g]['label'] for g in p['group_order']]
        ax.set(xticks=range(11), yticks=range(len(labels)), yticklabels=['\n'.join(textwrap.wrap(x, 21)) for x in labels],
            xlabel='Days after wounding', title=p['id']+f"; extended caption n={p['extended_caption_n']}; main caption n"+('≥' if p['main_caption_relation']=='at_least' else '=')+str(p['main_caption_n']))
        for spine in ax.spines.values(): spine.set_visible(False)
    export(fig, output, 'fig04_source_coverage')
