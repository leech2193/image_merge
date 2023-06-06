import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt
from PIL import Image, ImageChops
import random
import itertools
import sys

# cropped images folder
route = sys.argv[1]

# set image size
col_num = int(sys.argv[2])
row_num = int(sys.argv[3])

# output file location
output_file = sys.argv[4]

img = Image.open(route)

# real image size
img_col_size = img.size[0]
img_row_size = img.size[1]


# column 나누어지게끔 사이즈 정하기
def cut_col(c_num, img_c_size):
    if img_c_size % c_num != 0:
        img_c_size -= 1
        return cut_col(c_num, img_c_size)
    else:
        return img_c_size

# row 나누어지게끔 사이즈 정하기
def cut_row(r_num, img_r_size):
    if img_r_size % r_num != 0:
        img_r_size -= 1
        return cut_row(r_num, img_r_size)
    else:
        return img_r_size


img_col_size = cut_col(col_num, img_col_size)
img_row_size = cut_row(row_num, img_row_size)

col_per_size = (img_col_size) / col_num
row_per_size = (img_row_size) / row_num

# 사진 사이즈 정하기
def cut_size(img_size, per_size):
    lst = []
    per_size = int(per_size)
    for i in range(0, img_size, per_size):

        lst2 = []

        p = 0
        if i == 0:
            lst2.append(p)
            lst2.append(p+per_size)
        if i != 0:
            p = i
            lst2.append(p)
            lst2.append(p+per_size)

        lst.append(lst2)

    return lst

# column, row 자를 사이즈
col_cutted = cut_size(img_col_size, col_per_size)
row_cutted = cut_size(img_row_size, row_per_size)

# 이미지 자르기
img_lst = []
for a in col_cutted:
    for b in row_cutted:
        # 크롭될 사이즈
        img_cropped = img.crop((a[0], b[0], a[1], b[1]))

        # 0,1 사이의 숫자 정하기. 각 50%의 확률로 rotate, flip, mirror 가 정해진다
        ri = random.randint(0, 1)
        if ri == 0:
            img_cropped = img_cropped.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        ri = random.randint(0, 1)
        if ri == 0:
            img_cropped = img_cropped.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

        ri = random.randint(0, 1)
        if ri == 0:
            img_cropped = img_cropped.rotate(270, expand=True)

        img_lst.append([img_cropped])
        # 이름 랜덤으로 정하기
        rn = str(random.randint(0, 100000))

        img_cropped.save(output_file + rn + '.jpg')
