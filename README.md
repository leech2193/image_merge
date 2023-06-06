# image_merge

1. ## **cut_image.py 사용법**: 
python cut_image.py${original_image_file_name}${column_num}${row_num}${output_file_name}

예) python cut_image.py cat.jpg 2 2 ./untitled/

2. ## **merge_image.py 사용법**: 
python merge_image.py${input_image_file_name}${column_num}${row_num}${output_file_name}${original_image_file_name} 

예) python merge_image.py ./untitled/ 2 2 ./test cat.jpg

## 비고:
cut_image.py의 경우, 완전히 구현 완료

merge_image.py의 경우, 2*2 경우 구현 완료. 3*3의 경우 완전하지 않음(속도문제)
