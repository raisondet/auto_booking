# auto_booking

셀레니움을 이용하여 테니스 코트 자동 예약 기능 구현을 한 리포입니다.

예약시, captcha 값을 필요해서 2captcah 모듈을 이용하여 captcha 값을 적용하였습니다.

windows, mac 둘 다 동작확인 완료하였습니다.

# 환경셋팅

- 모듈설치

```
pip install selenium
pip install 2captcha-python
```

- config.ini 설정

```
[WEB]
url = 예약하고자 하는 url

[USER]
id = web url에서의 your id
pwd = web url에서의 your pwd

[BROWSER]
type = chrome, firefox 중 선택

[API]
key = 2captcha api key (유료)

[DAY]
day = THU,FRI #예약하고자 하는 요일
```

# 동작

```
python3 main.py
```
