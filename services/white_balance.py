import math
from abc import ABC
from abc import abstractmethod
from typing import Optional

import numpy as np
from cv2 import cv2
from cv2 import xphoto_GrayworldWB
from cv2 import xphoto_LearningBasedWB
from cv2 import xphoto_SimpleWB
from cv2.xphoto import createGrayworldWB
from cv2.xphoto import createLearningBasedWB
from cv2.xphoto import createSimpleWB

from services.chain.cell import CellFromFabric
from services.cv_context import CVContext


class BaseWB(ABC):
    @abstractmethod
    def white_balance(self, image: np.ndarray) -> Optional[np.ndarray]:
        ...


class PerfectReflectiveWB(BaseWB):
    def white_balance(self, image: np.ndarray) -> Optional[np.ndarray]:
        wb: xphoto_SimpleWB = createSimpleWB()
        return wb.balanceWhite(image)


class LearningBasedWB(BaseWB):
    def white_balance(self, image: np.ndarray) -> Optional[np.ndarray]:
        wb: xphoto_LearningBasedWB = createLearningBasedWB()
        return wb.balanceWhite(image)


class GrayWorldWB(BaseWB):
    def white_balance(self, image: np.ndarray) -> Optional[np.ndarray]:
        wb: xphoto_GrayworldWB = createGrayworldWB()
        return wb.balanceWhite(image)


class GammaTransWB(BaseWB):
    def white_balance(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        гамма-коррекция
        Использовать адаптивную гамма-коррекцию
        : param img: данные изображения читаются cv2.imread
        : return: возвращенные данные изображения после гамма-коррекции
        """
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean = np.mean(img_gray)
        # Формула вычисляет гамму
        gamma = math.log10(0.5) / math.log10(mean / 255)
        gamma_table = [np.power(x / 255.0, gamma) * 255.0
                       for x in range(256)]  # Создать таблицу сопоставления
        gamma_table = np.round(np.array(gamma_table)).astype(
            np.uint8)  # Значение цвета является целым числом
        return cv2.LUT(image, gamma_table)


white_balance_fabric = {
    "perfect": PerfectReflectiveWB(),
    "learning": LearningBasedWB(),
    "gray": GrayWorldWB(),
    "gamma": GammaTransWB(),
}


class WhiteBalanceCell(CellFromFabric):
    def __init__(self, white_balance: str):
        super().__init__(fabric=white_balance_fabric, item_name=white_balance)

    def __call__(self, context: CVContext):
        context.image = self._item.white_balance(context.image)
        return super().__call__(context=context)
