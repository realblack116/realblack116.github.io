### class1 숫자 맞추기 게임 만들기 ###
main1-1.py
import random  # random 모듈을 불러와서 난수 생성 기능을 사용할 수 있게 한다.

# 1부터 100 사이의 정수를 무작위로 선택하여 random_number 변수에 저장한다.
random_number = random.randint(1, 100)

# 생성된 무작위 정수를 출력한다.
print(random_number)

### 코드 설명 ###
1. import random
- 파이썬의 내장 모듈인 random을 가져와서 난수 생성 관련 함수를 사용할 수 있게 한다.

2. random_number = random.randint(1, 100)
- random.randint(1, 100) 함수는 1부터 100 사이의 정수(양 끝 포함)를 무작위로 생성한다.
- 생성된 정수는 random_number 변수에 할당된다.

3. print(random_number)
-변수 random_number에 저장된 무작위 정수를 콘솔에 출력한다.

이 코드는 간단하게 1부터 100 사이의 임의의 숫자를 생성해서 출력하는 역할을 한다.
