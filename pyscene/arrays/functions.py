import numpy as np

def rgba_to_hsla(rgba):
    color = rgba / 255
    cmin = color[:3].min()
    cmax = color[:3].max()
    L = (cmin + cmax) / 2
    if cmin == cmax:
        S = 0
        H = 0
    else:
        if L > 0.5:
            S = (cmax - cmin)/(2.0 - cmax - cmin)
        else:
            S = (cmax - cmin)/(cmax + cmin)

        arg_loc = color[:3].argmax()
        if arg_loc == 0:
            H = (color[1] - color[2]) / (cmax - cmin)
        elif arg_loc == 1:
            H = 2.0 + (color[2] - color[0]) / (cmax - cmin)
        elif arg_loc == 2:
            H = 4.0 + (color[0] - color[1]) / (cmax - cmin)

    return np.array((H, S, L, color[3])) * np.array((60, 100, 100, 100))

def hsla_to_rgba(hsla):
    color = hsla / np.array((360, 100, 100, 100))
    if color[1] == 0:
        return color * 255
    else:

        def hue2rgb(h, p, q):
            if h < 0: h += 1
            if h > 1: h -= 1

            if h < 1 / 6:
                return p + (q - p) * 6 * h
            if h < 1 / 2:
                return q
            if h < 2 / 3:
                return p + (q - p) * (2 / 3 - h) * 6
            return p

        if color[2] < 0.5:
            q = color[2] * (1.0 + color[1])
        else:
            q = color[2] + color[1] - color[2] * color[1]
        p = 2 * color[2] - q
        H = color[0]
        T = 1 / 3
        R = np.round(hue2rgb(H + T, p, q) * 255)
        G = np.round(hue2rgb(H, p, q) * 255)
        B = np.round(hue2rgb(H - T, p, q) * 255)
        return np.array((R,G,B,color[3] * 255)).astype(int)
