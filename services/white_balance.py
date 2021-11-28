from abc import ABC, abstractmethod
from typing import Dict, List, NamedTuple, Optional, Tuple

import math
import numpy as np
from cv2 import cv2

class BaseWhiteBalance(ABC):
    @abstractmethod
    def white_balance(self, image: np.ndarray) -> Optional[np.ndarray]:
        ...

class PerfectReflectiveWhiteBalance(BaseWhiteBalance):
    def __init__(self):
         ...

    def white_balance(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
            Идеальный баланс белого с отражением
            ШАГ 1. Рассчитайте сумму R \ G \ B для каждого пикселя
            ШАГ 2: В соответствии со значением R + G + B рассчитайте значение предыдущего соотношения% как пороговое значение T контрольной точки.
            ШАГ 3: Для каждой точки изображения вычислите среднее значение совокупной суммы компонентов R \ G \ B всех точек, где значение R + G + B больше, чем T.
            ШАГ 4. Определите количество пикселей до [0,255] для каждой точки.
            В зависимости от выбора значения коэффициента изображение не является белым в самой яркой области.
            : param img: данные изображения читаются cv2.imread
            : return: Возвращенные данные изображения результата баланса белого
        """
        img = image.copy()
        b, g, r = cv2.split(img)
        m, n, t = img.shape
        sum_ = np.zeros(b.shape)
        # for i in range(m):
        #     for j in range(n):
        #         sum_[i][j] = int(b[i][j]) + int(g[i][j]) + int(r[i][j])
        sum_ = b.astype(np.int32) + g.astype(np.int32) + r.astype(np.int32)

        hists, bins = np.histogram(sum_.flatten(), 766, [0, 766])
        Y = 765
        num, key = 0, 0
        ratio = 0.01
        while Y >= 0:
            num += hists[Y]
            if num > m * n * ratio / 100:
                key = Y
                break
            Y -= 1

        # sum_b, sum_g, sum_r = 0, 0, 0
        # for i in range(m):
        #     for j in range(n):
        #         if sum_[i][j] >= key:
        #             sum_b += b[i][j]
        #             sum_g += g[i][j]
        #             sum_r += r[i][j]
        #             time = time + 1
        sum_b = b[sum_ >= key].sum()
        sum_g = g[sum_ >= key].sum()
        sum_r = r[sum_ >= key].sum()
        time = (sum_ >= key).sum()

        avg_b = sum_b / time
        avg_g = sum_g / time
        avg_r = sum_r / time

        maxvalue = float(np.max(img))
        # maxvalue = 255
        # for i in range(m):
        #     for j in range(n):
        #         b = int(img[i][j][0]) * maxvalue / int(avg_b)
        #         g = int(img[i][j][1]) * maxvalue / int(avg_g)
        #         r = int(img[i][j][2]) * maxvalue / int(avg_r)
        #         if b > 255:
        #             b = 255
        #         if b < 0:
        #             b = 0
        #         if g > 255:
        #             g = 255
        #         if g < 0:
        #             g = 0
        #         if r > 255:
        #             r = 255
        #         if r < 0:
        #             r = 0
        #         img[i][j][0] = b
        #         img[i][j][1] = g
        #         img[i][j][2] = r

        b = img[:, :, 0].astype(np.int32) * maxvalue / int(avg_b)
        g = img[:, :, 1].astype(np.int32) * maxvalue / int(avg_g)
        r = img[:, :, 2].astype(np.int32) * maxvalue / int(avg_r)
        b[b > 255] = 255
        b[b < 0] = 0
        g[g > 255] = 255
        g[g < 0] = 0
        r[r > 255] = 255
        r[r < 0] = 0
        img[:, :, 0] = b
        img[:, :, 1] = g
        img[:, :, 2] = r

        return img
			 	 
class GammaTrans(BaseWhiteBalance):
    def __init__(self):
         ...

    def white_balance(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
			 гамма-коррекция
			 Использовать адаптивную гамма-коррекцию
			 : param img: данные изображения читаются cv2.imread
			 : return: возвращенные данные изображения после гамма-коррекции
        """
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean = np.mean(img_gray)
        gamma = math.log10 (0.5) / math.log10 (mean / 255) # Формула вычисляет гамму
        gamma_table = [np.power (x / 255.0, gamma) * 255.0 for x in range(256)] # Создать таблицу сопоставления
        gamma_table = np.round (np.array (gamma_table)). astype (np.uint8) # Значение цвета является целым числом
        return cv2.LUT (image, gamma_table) # Найдите таблицу цветов изображения. Кроме того, может быть разработан адаптивный алгоритм по принципу гомогенизации интенсивности (цвета) света.

white_balance_fabric = {
    "perfect": PerfectReflectiveWhiteBalance(),
	"gamma": GammaTrans().
}

class WhiteBalanceCell(CellFromFabric):
    def __init__(self, white_balance: str):
        super().__init__(fabric=white_balance_fabric, item_name=white_balance)

    def __call__(self, context: CVContext):
        context.image = self._item.white_balance(context.image)
        return super().__call__(context=context)