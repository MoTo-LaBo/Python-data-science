import numpy as np
import pandas as pd
import nibabel as nib
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


# ------------------ NiFTI Data 変換関数 -------------------

def load_nifti(path):
    nifti = nib.load(path)
    data = nifti.get_fdata()
    return np.rollaxis(data, 1)


# ------------------ Mask Data RGB 変換関数 -------------------

def label_color(mask_volume,
               ggo_color = [255, 0 , 0],
               consolidation_color = [0, 255 , 0],
               effusion_color = [0, 0 , 255]):
    
    shp = mask_volume.shape
    # 箱作成
    mask_color = np.zeros((shp[0], shp[1], shp[2], 3), dtype=np.float32)
    # 色付け
    mask_color[np.equal(mask_volume, 1)] = ggo_color
    mask_color[np.equal(mask_volume, 2)] = consolidation_color
    mask_color[np.equal(mask_volume, 3)] = effusion_color
    
    return mask_color



# ------------------ HU to gray 変換関数 -------------------

def hu_to_gray(volume):
    maxhu = np.max(volume)
    minhu = np.min(volume)
    volume_rerange = (volume - minhu) / max((maxhu-minhu), 1e-3)
    volume_rerange = volume_rerange * 255
    volume_rerange = np.stack([volume_rerange, volume_rerange, volume_rerange], axis=-1)
    
    # astype(np.uint8) にすることで　0 ~ 255 の　int　で返してくれる
    return volume_rerange.astype(np.uint8)



# ------------------ Overlay 重ね合わせ関数 -------------------

def overlay(gray_volume, mask_volume, mask_color, alpha):
    mask_filter = np.greater(mask_volume, 0)
    mask_filter = np.stack([mask_filter, mask_filter, mask_filter], axis=-1)
    overlayed = np.where(mask_filter,
                       ((1-alpha)*gray_volume + alpha*mask_color).astype(np.uint8), gray_volume)
    
    return overlayed