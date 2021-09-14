import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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


# ------------------ Mask Data RGB 変換(algorithm) -------------------

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



# ------------------ slice annotation　表示(algorithm) -------------------

def vis_overlay(overlayed, cols=5, display_num=45, figsize=(15, 15)):
    
    rows = (display_num - 1) // cols + 1  # 行 = (25枚表示　-1)//5 + 1 / -1 をする事により割きれて行が増える事を防止
    total_num = overlayed.shape[-2]       # トータルの枚数 : (630, 630, 45, 3)
    interval = total_num / display_num    # 等間隔にする : 100 / 10 = 10　飛ばし飛ばし
    if interval < 1:                      # もしトータルより表示枚数が多くても、１が入るので必ず次の枚数を取得できる
        interval = 1

    fig, ax = plt.subplots(rows, cols, figsize=figsize)
    for i in range(display_num):          # トータルの枚数

        # 変数にしてしまう
        row_i = i//cols                   # 商
        col_i = i%cols                    # 余り  
        idx = int((i * interval))         # interval を計算した後に　intに変換
        if idx >= total_num:              # index は 0 から始まるので　＞＝　にする
            break                         # error ハンドリング　トータル枚数になったら　for文を抜ける

    #     ax[i//cols, i%cols].imshow(overlayed[:, :, 10])　変数に置き換える
        ax[row_i, col_i].imshow(overlayed[:, :, idx])