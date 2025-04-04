### class1 숫자 맞추기 게임 만들기 ###
main1-3.py
import random  # 난수 생성 기능을 제공하는 random 모듈을 가져온다.

# 1부터 100 사이의 임의의 정수를 생성하여 random_number 변수에 저장한다.
random_number = random.randint(1, 100)

# print(random_number)  # 디버깅 용도로 생성된 난수를 확인할 수 있으나, 현재는 주석 처리되어 있다.

game_count = 1  # 사용자가 시도한 횟수를 기록하기 위한 변수이다.

# 사용자에게 계속해서 숫자 입력을 받기 위해 무한 루프를 시작한다.
while True:
    try:
        # 사용자로부터 1~100 사이의 숫자를 입력받고, 정수형으로 변환한다.
        my_number = int(input("1~100 사이의 숫자를 입력하세요:"))
        
        # 사용자가 입력한 숫자가 생성된 난수보다 큰 경우, "다운"을 출력한다.
        if my_number > random_number:
            print("다운")
        # 입력한 숫자가 난수보다 작으면 "업"을 출력한다.
        elif my_number < random_number:
            print("업")
        # 입력한 숫자가 난수와 같으면, 축하 메시지를 출력하고 반복문을 종료한다.
        elif my_number == random_number:
            print(f"축하합니다. {game_count}회 만에 맞췄습니다")
            break  # 정답을 찾았으므로 루프를 종료한다.
        
        # 한 번의 시도 후, 시도 횟수를 1 증가한다.
        game_count = game_count + 1
        
    except:
        # 숫자가 아닌 값 등을 입력하여 변환 오류가 발생하면 예외 처리하여 에러 메시지를 출력한다.
        print("에러가 발생하였습니다. 숫자를 입력하세요")

### 코드 설명 ###
1. 난수 생성 및 변수 초기화:
- random.randint(1, 100) 함수를 사용해 1부터 100 사이의 임의의 정수를 생성하고,
  이를 random_number에 저장한다. 또한, game_count 변수를 1로 초기화하여 사용자의 시도 횟수를 추적한다.

2. 무한 루프와 예외 처리:
- while True 무한 루프 안에서 사용자에게 숫자 입력을 요청한다.
  입력값을 정수로 변환할 때, 만약 올바르지 않은 입력(예: 문자열, 공백 등)이 들어오면 예외가 발생하여 except 블록이 실행되고,
  사용자에게 에러 메시지가 출력된다.

3. 입력값 비교:
- 입력한 숫자(my_number)가 random_number보다 크면 "다운", 작으면 "업"을 출력하여 사용자가 정답에 더 가까워지도록 힌트를 제공한다.
  정답을 맞출 경우 축하 메시지를 출력하고 반복문을 종료한다.
