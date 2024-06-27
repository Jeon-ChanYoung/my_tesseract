import pytesseract
import pandas as pd
from PIL import Image

# Tesseract 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 이미지 읽기
image = Image.open("test.png")
text = pytesseract.image_to_string(image)

# 텍스트를 행으로 분할 (각 줄이 표의 행이라고 가정)
rows = text.split('\n')

# 데이터 클리닝 및 빈 행 제거
cleaned_rows = []
for row in rows:
    # 불필요한 공백 및 특수 문자 제거
    clean_row = row.strip().replace("[", "").replace("]", "").replace("|", "").replace("_","")
    
    # 공백이 아닌 유효한 행만 추가
    if clean_row:
        cleaned_rows.append(clean_row)

print("Cleaned Rows:")
print(cleaned_rows)

# 각 행을 공백으로 분할하여 데이터프레임 생성
df = pd.DataFrame([row.split() for row in cleaned_rows])
print("DataFrame:")
print(df)
