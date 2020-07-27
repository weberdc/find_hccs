import networkx as nx
import os.path
import utils


def open_log_file(out_dir):
    log_file = os.path.join(out_dir, 'lcn_log.csv')
    columns = ['timestamp,tweets,nodes,edges,components,biggest_component']
    with open(log_file, 'w', encoding='utf-8') as out_f:
        out_f.write('%s\n' % ','.join(columns))
    return log_file


def log_g(ts_s, g, t_count, log_file, dry_run):
    if dry_run:
        return

    ts_str = utils.ts_to_str(ts_s)
    with open(log_file, 'a', encoding='utf-8') as out_f:
        if not g:
            out_f.write('%s,0,0,0,0,0\n' % ts_str)
        else:
            components = sorted(nx.connected_components(g), key=len, reverse=True)
            out_f.write('%s,%d,%d,%d,%d,%d\n' % (
                ts_str, t_count, g.number_of_nodes(), g.number_of_edges(),
                len(components), len(components[0])
            ))
