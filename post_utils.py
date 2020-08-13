import pandas as pd
import numpy as np

def load_csv_daeplotter_many_vars(file_):
    "A DAETOOLs helper function to read exported CSV files from the charting tool daeplotter"
    df = pd.read_csv(file_, skip_blank_lines=True)
    lbl_x, lbl_y0 = df.columns
    vals = df.values
    col1 = vals[:,0]
    col1_f = pd.to_numeric(col1, errors='coerce')
    idx_of_nan_ = np.where(np.isnan(col1_f))[0]
    idx_of_nan = [-1, *idx_of_nan_]

    dfs_variables = [
        df.iloc[i_val+1:idx_of_nan[i+1], :].set_index(lbl_x)
        for i, i_val in enumerate(idx_of_nan) if i < len(idx_of_nan)-1
    ]
    dfs_variables += [df.iloc[idx_of_nan[-1]+1:, :].set_index(lbl_x)]

    labels_orig = [lbl_y0, *df.iloc[idx_of_nan_, 1].values.tolist()]
    labels_new = ['{}-col-{}'.format(lbl, i) for i,lbl in enumerate(labels_orig)]

    dfs_new_lbls = []
    for i, d in enumerate(dfs_variables):
        d.columns = [labels_new[i]]
        dfs_new_lbls += [d]

    df_join = pd.concat(dfs_new_lbls, axis=1).astype('float')
    df_join.index = (df_join.index.astype('float'))
    return df_join
