### 컴퓨터의 외부 및 내부 IP 확인 ###
main2-1.py
import socket  # 네트워크 관련 기능을 제공하는 socket 모듈을 불러온다.

# 현재 시스템의 호스트 이름을 가져와서 해당 이름에 연결된 IP 주소를 얻는다.
# socket.gethostname()은 현재 컴퓨터의 호스트 이름을 반환하고, socket.gethostbyname()은 그 호스트 이름을 IP 주소로 변환한다.
in_addr = socket.gethostbyname(socket.gethostname())

print(in_addr)  # 얻은 IP 주소를 콘솔에 출력한다.

### 코드 설명 ###
1. import socket
- 네트워크 소켓 통신을 위한 기능을 제공하는 파이썬 내장 모듈인 socket을 가져온다.

2. socket.gethostname()
- 현재 컴퓨터의 호스트 이름(네트워크 상에서의 이름)을 반환한다.

3. socket.gethostbyname(socket.gethostname())
- 위에서 얻은 호스트 이름을 이용해, 해당 호스트 이름에 매핑된 IP 주소를 반환한다.
- 보통 로컬 네트워크 내의 IP 주소(예: 192.168.x.x 또는 127.0.0.1)를 반환하게 된다.

4. print(in_addr)
- 최종적으로 얻은 IP 주소를 출력한다.
