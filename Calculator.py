# 객체지향 계산기 프로그램
class Calculator:
    """기본 계산기 클래스"""
    def __init__(self, name="기본 계산기"):
        self.name = name
        self.result = 0
        self.history = []
    
    def add(self, num):
        """덧셈 연산"""
        self.result += num
        self._add_to_history(f"+ {num}")
        return self.result
    
    def subtract(self, num):
        """뺄셈 연산"""
        self.result -= num
        self._add_to_history(f"- {num}")
        return self.result
    
    def multiply(self, num):
        """곱셈 연산"""
        self.result *= num
        self._add_to_history(f"× {num}")
        return self.result
    
    def divide(self, num):
        """나눗셈 연산"""
        if num == 0:
            self._add_to_history("÷ 0 (오류: 0으로 나눌 수 없음)")
            return "오류: 0으로 나눌 수 없습니다"
        self.result /= num
        self._add_to_history(f"÷ {num}")
        return self.result
    
    def clear(self):
        """결과 초기화"""
        self.result = 0
        self._add_to_history("초기화")
        return self.result
    
    def _add_to_history(self, operation):
        """계산 기록 추가 (내부 메서드)"""
        self.history.append(f"{operation} = {self.result}")
    
    def get_history(self):
        """계산 기록 조회"""
        return self.history
    
    def show_info(self):
        """계산기 정보 출력"""
        print(f"계산기 이름: {self.name}")
        print(f"현재 결과값: {self.result}")


class ScientificCalculator(Calculator):
    """공학용 계산기 클래스"""
    def __init__(self):
        super().__init__("공학용 계산기")
    
    def power(self, num):
        """거듭제곱 연산"""
        self.result **= num
        self._add_to_history(f"^ {num}")
        return self.result
    
    def square_root(self):
        """제곱근 연산"""
        if self.result < 0:
            self._add_to_history("√ (오류: 음수의 제곱근)")
            return "오류: 음수의 제곱근을 계산할 수 없습니다"
        self.result = self.result ** 0.5
        self._add_to_history("√")
        return self.result


# 계산기 사용 예시
def run_calculator():
    print("===== 계산기 프로그램 =====")
    print("1. 기본 계산기")
    print("2. 공학용 계산기")
    choice = input("사용할 계산기를 선택하세요: ")
    
    if choice == "2":
        calc = ScientificCalculator()
    else:
        calc = Calculator()
    
    calc.show_info()
    
    while True:
        print("\n===== 작업 선택 =====")
        print("1: 덧셈   2: 뺄셈   3: 곱셈   4: 나눗셈   5: 초기화")
        
        if isinstance(calc, ScientificCalculator):
            print("6: 거듭제곱   7: 제곱근")
        
        print("0: 종료   h: 계산 기록 보기")
        
        operation = input("원하는 작업을 선택하세요: ")
        
        if operation == "0":
            print("계산기를 종료합니다.")
            break
        
        elif operation == "h":
            print("\n===== 계산 기록 =====")
            for entry in calc.get_history():
                print(entry)
            continue
        
        elif operation in ["1", "2", "3", "4", "6"]:
            try:
                num = float(input("숫자를 입력하세요: "))
                
                if operation == "1":
                    result = calc.add(num)
                elif operation == "2":
                    result = calc.subtract(num)
                elif operation == "3":
                    result = calc.multiply(num)
                elif operation == "4":
                    result = calc.divide(num)
                elif operation == "6" and isinstance(calc, ScientificCalculator):
                    result = calc.power(num)
                
                print(f"결과: {result}")
            
            except ValueError:
                print("유효한 숫자를 입력해주세요.")
        
        elif operation == "5":
            calc.clear()
            print("계산기가 초기화되었습니다.")
        
        elif operation == "7" and isinstance(calc, ScientificCalculator):
            result = calc.square_root()
            print(f"결과: {result}")
        
        else:
            print("잘못된 선택입니다.")


# 프로그램 실행
if __name__ == "__main__":
    run_calculator()