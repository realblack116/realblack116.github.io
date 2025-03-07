### 컴퓨터의 외부 및 내부 IP 확인 ###
import socket  # 네트워크 소켓 통신을 위한 내장 socket 모듈을 불러온다.

# IPv4(AF_INET)와 TCP(SOCK_STREAM)를 사용하는 소켓 객체를 생성.
in_addr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# "www.google.co.kr"의 443 포트(HTTPS 기본 포트)로 연결을 시도.
in_addr.connect(("www.google.co.kr", 443))

# 소켓의 로컬 주소 정보를 가져온다.
# getsockname()은 (로컬 IP 주소, 로컬 포트) 형태의 튜플을 반환.
# 여기서는 로컬 IP 주소를 출력하기 위해 인덱스 0의 값을 출력.
print(in_addr.getsockname()[0])

### 코드 설명 ###
1. 소켓 생성
- socket.socket(socket.AF_INET, socket.SOCK_STREAM)을 사용하여 IPv4와 TCP 프로토콜을 기반으로 하는 소켓을 만듬.
  이는 네트워크 통신에서 많이 사용되는 기본 소켓 설정.

2. 원격 서버에 연결
in_addr.connect(("www.google.co.kr", 443)) 명령으로 구글의 한국 도메인(www.google.co.kr)에서 HTTPS 통신에 사용되는 443 포트로 연결을 시도.
이 과정에서 운영체제는 로컬 네트워크 인터페이스를 통해 연결할 수 있는 IP 주소를 할당.

3. 로컬 IP 주소 확인
in_addr.getsockname() 함수는 소켓이 사용 중인 로컬 IP 주소와 포트 번호를 반환.
여기서 [0] 인덱스를 사용해 로컬 IP 주소만 추출하고 출력.
