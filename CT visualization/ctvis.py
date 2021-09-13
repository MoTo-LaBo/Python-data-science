import pandas as pd
from glob import glob


# ------------------ DataFrame 作成関数 -------------------
def _get_df(base_path='public-covid-data', folder='ra_im'):
    data_dict = pd.DataFrame({'FilePath': glob('{}/{}/*'.format(base_path, folder)),
                            'FileName': [p.split('/')[-1] for p in glob('{}/{}/*'.format(base_path, folder))]})
    return data_dict



def get_df_all(base_path='public-covid-data'):
    rp_im_df = _get_df(base_path, folder='rp_im')
    rp_msk_df = _get_df(base_path, folder='rp_msk')
    return rp_im_df.merge(rp_msk_df, on='FileName', suffixes=('Image', 'Mask'))
# ------------------ DataFrame 作成関数 -------------------