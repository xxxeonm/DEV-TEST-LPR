lp_detection.py

- detection 전처리
1) 회색조로 색변환
2) 블러필터 적용
3) 가장자리 추출: canny
4) 객체 추출: findContours

- detection
1) 객체 boxing: rectange
2) box 필터링 by 사이즈, 가로세로 비율
3) 버블 정렬
4) box 리스트 필터링 by box간 간격과 높이

- recognition 전처리
1) 수평 보정
2) resize
3) 필터적용: morph_close, threshold

- recognition
1) kor_lp_gen.traineddata: 
    - 도로명주소에 사용되는 `한길체`&`한길체장체` bold, regular, italic 사용
    - jTessBoxEditor로 생성
2) 한글+숫자만 필터링


<<OVERFITTED
: 수정필요,

<<Training Korean
- '주'를 '루'로 인식함^^
- '주'를 '조'로 인식함^^???
- '3'을 '5'로 인식함...
