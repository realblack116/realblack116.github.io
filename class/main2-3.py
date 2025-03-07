### 컴퓨터의 외부 및 내부 IP 확인 ###
import requests  # 웹 요청을 보내기 위한 requests 모듈을 불러온다.
import re        # 정규표현식 사용을 위한 re 모듈을 불러온다.

# "http://ipconfig.kr" URL로 GET 요청을 보내고, 그 응답을 req 변수에 저장.
req = requests.get("http://ipconfig.kr")

# 응답받은 텍스트(req.text)에서 정규표현식을 사용하여 IP 주소를 찾는다.
# 정규표현식 설명:
# 'IP Address : ' 문자열 다음에 (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) : 숫자 1~3자리와 점(.)이 반복되어 나오는 형식 (IPv4 주소 형식)을 캡처.
# re.search()는 패턴과 일치하는 첫 번째 결과를 반환하며, [1]은 캡처 그룹에 해당하는 부분 (IP 주소).
out_addr = re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1]

# 추출한 IP 주소를 출력.
print(out_addr)

### 코드 설명 ###
1. 모듈 임포트:
- requests 모듈은 웹 서버에 HTTP 요청을 보내고 응답을 받기 위해 사용.
- re 모듈은 문자열 내에서 정규표현식을 사용하여 원하는 패턴을 찾는데 사용.

2. 웹 요청:
- requests.get("http://ipconfig.kr")을 호출하여 해당 URL의 내용을 가져온다.
- 이 웹페이지는 사용자의 외부 IP 주소 정보를 제공하는 사이트.

3. 정규표현식으로 IP 주소 추출:
- re.search() 함수로 응답 텍스트에서 "IP Address : " 뒤에 나오는 IPv4 형식의 주소를 찾아 캡처.
- [1]을 사용해 캡처 그룹에 해당하는 문자열(실제 IP 주소)만 추출.
- 정규표현식에서 re.search() 함수는 매칭 결과를 담은 "매치 객체(match object)"를 반환.
이 객체는 여러 "그룹(group)"을 포함하는데,
그룹 0: 전체 매칭된 문자열
그룹 1: 첫 번째 괄호로 캡처된 부분
따라서 [1]는 매치 객체에서 첫 번째 캡처 그룹(즉, 괄호 (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})로 감싼 부분)을 가져오는 역할.

즉, 이 경우에는 "IP Address : " 뒤에 나오는 실제 IP 주소 문자열을 추출하는 것이다.

4. 출력:
print(out_addr)를 통해 추출한 외부 IP 주소를 콘솔에 출력.
