
import numpy as np

def apply_flip_image(img, how):
    if how == "vertical":
        return np.flipud(img)
    elif how == "horizontal":
        return np.fliplr(img)
    elif how == "both":
        return np.flipud(np.fliplr(img))
    return img
