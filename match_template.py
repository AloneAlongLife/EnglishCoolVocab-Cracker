from typing import Optional

import cv2, numpy as np

def ident_image(
    img: np.ndarray,
    template: str,
    thr: float = 0.1,
    x_range: tuple[int, int] = (0, 1440),
    y_range: tuple[int, int] = (0, 3040),
) -> Optional[tuple[tuple[int, int], float]]:
    # 大小過濾
    src = img.copy()[
        y_range[0]:y_range[1]+1,
        x_range[0]:x_range[1]+1,
        :
    ]

    # 讀取模板
    template: np.ndarray = cv2.imread(template)

    # 搜尋位置
    min_val, _, min_pos, _ = cv2.minMaxLoc(
        cv2.matchTemplate(src, template, cv2.TM_SQDIFF_NORMED))

    # 取得座標
    h, w, _ = template.shape
    cen_x, cen_y = min_pos[0] + w // 2, min_pos[1] + h // 2

    # 新增至結果
    return (cen_x+x_range[0], cen_y+y_range[0]) if min_val < thr else None