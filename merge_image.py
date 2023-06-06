import cv2
import numpy as np
import imutils
from PIL import Image, ImageChops
import random
import itertools
import sys
import glob
import math

file_path = sys.argv[1]
col_num = int(sys.argv[2])
row_num = int(sys.argv[3])
output_filename = sys.argv[4] + ".jpg"

list_images = glob.glob(file_path + '*.jpg')

img_lst = []

for image in list_images:
    jpeg_image = Image.open(image)
    image_copy = Image.new(jpeg_image.mode, jpeg_image.size)
    image_copy.paste(jpeg_image)

    img_lst.append([image_copy])


def rmsdiff(image1, image2):
    # 이미지 차이 계산. 이미지 간 차이 반환
    diff = ImageChops.difference(image1, image2)
    # 차이 이미지의 히스토그램
    h = diff.histogram()
    # h 각 요소에 대해 제곱 값 계산
    sq = (value * ((idx % 256) ** 2) for idx, value in enumerate(h))
    # sq 총합
    sum_of_squares = sum(sq)
    # rms 값 계산 작을수록 두 이미지 유사
    rms = math.sqrt(sum_of_squares / float(image1.size[0] * image1.size[1]))
    return rms


for i, img in enumerate(img_lst):
    # 이미지가 세로로 돌려져있다면
    if img[0].size[0]<img[0].size[1]:
        # 다시 가로로 돌려놓기
        img = img[0].rotate(90, expand=True)
        img_lst[i] = [img]
    else:
        img = img[0]


# 원본 이미지 6번째 매개변수로 받는다
compare_img = Image.open(sys.argv[5])

# 사진 순서 리스트
img_order = list(np.arange(0, (col_num * row_num) ))


# 좌우 반전과 상하 반전의 모든 조합 생성
flip_combinations = list(itertools.product([False, True], repeat=col_num*row_num*2))

# 가능한 모든 사진 순서 및 조합 생성
all_permutations = list(itertools.permutations(img_order))
## 3*3의 경우 해당 코드에서 많은 시간 소요
all_combinations = list(itertools.product(all_permutations, flip_combinations))

# 각 순열 및 조합에 대해 사진 이어 붙이기 수행
# left right flip 여부, top bottom flip 여부 사진의 위치를 경우의 수로 두고 사진을 이어붙임
# 이를 원본 사진과 비교 후 rmse 값이 10 미만일 경우 원본과 같다고 판정

# 속도를 빠르게 하기 위해 [0,0]위치의 사진과, 원본의 [0,0] 위치를 crop해 비교하는 방식을 변경 필요할 듯
for combination in all_combinations:
    permutation, flips = combination

    # 원래 사진 사이즈로 캔버스 만들기. 이 위에서 이어 붙여 나갈 것
    new_img = Image.new('RGB', (img_lst[0][0].size[0] * col_num, img_lst[0][0].size[1] * row_num))

    for i, img_index in enumerate(permutation):

        img = img_lst[img_index][0]


        if col_num == 2:
            flip_lr = flips[i] # left 뒤집을지 여부
            flip_tb = flips[i + 4] # top bottom 뒤집을지 여부

            if flip_lr:
                img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if flip_tb:
                img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

            # 사진을 어디에 이어 붙일 것인지
            if i % 2 == 0:
                x = 0
            else:
                x = img_lst[0][0].size[0]

            if i < 2:
                y = 0
            else:
                y = img_lst[0][0].size[1]

        elif col_num==3:
            flip_lr = flips[i % 9]
            flip_tb = flips[(i + 4) % 9]

            if flip_lr:
                img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if flip_tb:
                img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

            if i % 3 == 0:
                x = 0
            elif i % 3 == 1:
                x = img_lst[0][0].size[0]
            else:
                x = 2 * img_lst[0][0].size[0]

            if i < 3:
                y = 0
            elif i < 6:
                y = img_lst[0][0].size[1]
            else:
                y = 2 * img_lst[0][0].size[1]

        new_img.paste(img, box=(x, y))

    rms_diff = rmsdiff(new_img, compare_img)
    # 이미지 두장 간의 rms 값이 10 미만이면 같다고 가정
    if rms_diff<10:
        new_img.save(output_filename)
        break

