### class1 숫자 맞추기 게임 만들기 ###
main1-2.py
import random  # 난수 생성을 위한 random 모듈을 불러온다.

# 1부터 100 사이의 정수를 무작위로 선택하여 random_number 변수에 저장한다.
random_number = random.randint(1, 100)

# print(random_number)  # 디버깅용으로 선택된 숫자를 출력할 수 있지만, 현재는 주석 처리되어 있다.

game_count = 1  # 사용자의 추측 횟수를 기록하기 위한 변수이다.

# 무한 루프를 시작한다.
while True:
    # 사용자로부터 1~100 사이의 숫자를 입력받아 정수형으로 변환한다.
    my_number = int(input("1~100 사이의 숫자를 입력하세요:"))
    
    # 사용자가 입력한 숫자가 random_number보다 클 경우 '다운' 메시지를 출력한다.
    if my_number > random_number:
        print("다운")
    # 입력한 숫자가 random_number보다 작을 경우 '업' 메시지를 출력한다.
    elif my_number < random_number:
        print("업")
    # 입력한 숫자가 random_number와 같으면 축하 메시지를 출력하고 루프를 종료한다.
    elif my_number == random_number:
        print(f"축하합니다. {game_count}회 만에 맞췄습니다")
        break  # 정답을 맞췄으므로 반복문을 종료.
    
    # 한 번의 시도가 끝날 때마다 시도 횟수를 1 증가한다.
    game_count = game_count + 1

### 코드 설명 ###
1. 난수 생성:
- random.randint(1, 100)를 사용해 1부터 100 사이의 임의의 정수를 생성한다.

2. 게임 루프:
- while True 무한 루프를 통해 사용자가 올바른 숫자를 입력할 때까지 계속해서 입력을 받고,
  입력 값이 정답보다 크면 "다운" (즉, 숫자를 낮추세요)
  입력 값이 정답보다 작으면 "업" (즉, 숫자를 높이세요)
  정답을 맞추면 축하 메시지를 출력하고 루프를 종료한다.

3. 시도 횟수:
- game_count 변수를 통해 사용자가 몇 번의 시도로 정답에 도달했는지를 기록된다.
