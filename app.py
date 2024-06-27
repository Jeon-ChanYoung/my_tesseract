import cv2
import numpy as np
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# 이미지 파일 경로
image_path = 'test.png'

# 이미지 읽기 (OpenCV 사용)
image = cv2.imread(image_path)

# 그레이스케일 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 이진화 (adaptive thresholding)
binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
# 경계 검출을 위해 이미지 반전

binary = cv2.bitwise_not(binary)
cv2.imshow("a", binary)

# 수평과 수직 경계 검출
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))

horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

# 수평과 수직 경계를 합침
table_structure = cv2.addWeighted(horizontal_lines, 0.5, vertical_lines, 0.5, 0.0)

# 경계 검출
contours, _ = cv2.findContours(table_structure, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 결과 이미지를 위해 복사본 생성
result_image = image.copy()

# 셀 인식 및 OCR 수행
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cell = result_image[y:y+h, x:x+w]
    cell_pil = Image.fromarray(cell)
    
    # OCR 수행
    cell_text = pytesseract.image_to_string(cell_pil, lang="kor", config='--psm 6')
    
    # 인식된 텍스트 출력
    print(f'Cell at ({x}, {y}) with size ({w}, {h}):')
    print(cell_text)
    
    # 셀 경계 표시 (선택 사항)
    cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# 결과 이미지 보여주기 (선택 사항)
cv2.imshow('Detected Table', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
