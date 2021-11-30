import numpy as np

from services.white_balance import (
    GammaTransWB,
    GrayWorldWB,
    LearningBasedWB,
    PerfectReflectiveWB,
)


def test_perfect_reflection_wb_works(
    perfect_reflective_wb_image, white_balance_test_image
):
    img = PerfectReflectiveWB().white_balance(white_balance_test_image)
    assert np.allclose(img, perfect_reflective_wb_image)


def test_gray_world_wb_works(gray_world_wb_image, white_balance_test_image):
    img = GrayWorldWB().white_balance(white_balance_test_image)
    assert np.allclose(img, gray_world_wb_image)


def test_learning_based_wb_works(learning_based_wb_image, white_balance_test_image):
    img = LearningBasedWB().white_balance(white_balance_test_image)
    assert np.allclose(img, learning_based_wb_image)


def test_gamma_trans_wb_works(gamma_trans_wb_image, white_balance_test_image):
    img = GammaTransWB().white_balance(white_balance_test_image)
    assert np.allclose(img, gamma_trans_wb_image)
