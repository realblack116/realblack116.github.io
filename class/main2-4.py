import socket    # 네트워크 소켓 통신을 위한 socket 모듈을 가져온다.
import requests  # HTTP 요청을 보내기 위한 requests 모듈을 가져온.
import re        # 정규표현식을 사용하기 위한 re 모듈을 가져온.

# 내부 IP 확인을 위한 소켓 생성 (IPv4, TCP 사용)
in_addr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# www.google.co.kr의 443 포트(HTTPS)를 대상으로 연결을 시도.
in_addr.connect(("www.google.co.kr", 443))
# 소켓의 로컬 주소 정보를 가져오고, 인덱스 0을 통해 IP 주소만 추출하여 출력.
print("내부IP: ", in_addr.getsockname()[0])

# 외부 IP를 확인하기 위해, ipconfig.kr 사이트에 GET 요청을 보낸다.
req = requests.get("http://ipconfig.kr")
# 사이트의 응답 텍스트에서 "IP Address : " 뒤에 나오는 IPv4 형식의 주소를 추출.
# re.search() 함수는 매치 객체를 반환하며, [1]을 사용해 첫 번째 캡처 그룹(실제 IP 주소)을 가져온다.
out_addr = re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1]
# 추출한 외부 IP 주소를 출력.
print("외부IP: ", out_addr)

### 코드 설명 ###
1. 모듈 임포트:
- socket 모듈은 네트워크 연결을 위해 사용되고, requests 모듈은 웹 서버와의 HTTP 통신을 위해, re 모듈은 정규표현식을 이용해 문자열 패턴을 찾기 위해 사용.

2. 내부 IP 확인:
- 소켓을 생성하고 구글의 HTTPS 포트(443)에 연결합니다.
- 연결 후 getsockname() 함수를 통해 로컬에서 사용된 IP 주소(내부 IP)를 추출하여 출력.

3. 외부 IP 확인:
ipconfig.kr에 GET 요청을 보내 외부 IP 주소가 포함된 응답을 받아온다.
정규표현식을 이용해 "IP Address : " 뒤에 나오는 IPv4 주소 패턴을 찾고, 매치 객체의 첫 번째 캡처 그룹([1])에서 실제 IP 주소를 추출하여 출력.
