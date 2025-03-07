# calculator_app.py
import streamlit as st
import math

# 객체지향 계산기 클래스
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
    
    def sin(self):
        """사인 연산"""
        self.result = math.sin(math.radians(self.result))
        self._add_to_history("sin")
        return self.result
    
    def cos(self):
        """코사인 연산"""
        self.result = math.cos(math.radians(self.result))
        self._add_to_history("cos")
        return self.result
    
    def tan(self):
        """탄젠트 연산"""
        self.result = math.tan(math.radians(self.result))
        self._add_to_history("tan")
        return self.result
    
    def log10(self):
        """로그(밑수 10) 연산"""
        if self.result <= 0:
            self._add_to_history("log (오류: 0이하의 수의 로그)")
            return "오류: 0 이하의 수의 로그를 계산할 수 없습니다"
        self.result = math.log10(self.result)
        self._add_to_history("log")
        return self.result


# Streamlit 앱 인터페이스
def main():
    st.set_page_config(page_title="객체지향 계산기 앱", page_icon="🧮")
    
    st.title("객체지향 계산기 애플리케이션")
    
    # 세션 상태 초기화
    if 'calculator' not in st.session_state:
        st.session_state.calculator = None
    if 'display' not in st.session_state:
        st.session_state.display = "0"
    if 'need_clear' not in st.session_state:
        st.session_state.need_clear = False
    
    # 계산기 유형 선택
    calc_type = st.radio(
        "계산기 유형 선택:",
        ("기본 계산기", "공학용 계산기")
    )
    
    if calc_type == "기본 계산기" and not isinstance(st.session_state.calculator, Calculator):
        st.session_state.calculator = Calculator()
        st.session_state.display = "0"
    elif calc_type == "공학용 계산기" and not isinstance(st.session_state.calculator, ScientificCalculator):
        st.session_state.calculator = ScientificCalculator()
        st.session_state.display = "0"
    
    calculator = st.session_state.calculator
    
    # 현재 결과 표시
    st.subheader(f"현재 결과:")
    result_display = st.empty()
    result_display.markdown(f"## {st.session_state.display}")
    
    # 숫자 입력
    num_input = st.number_input("숫자 입력:", value=0.0, key="num_input")
    
    # 기본 연산 버튼들
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("더하기 (+)"):
            calculator.add(num_input)
            st.session_state.display = str(calculator.result)
    
    with col2:
        if st.button("빼기 (-)"):
            calculator.subtract(num_input)
            st.session_state.display = str(calculator.result)
    
    with col3:
        if st.button("곱하기 (×)"):
            calculator.multiply(num_input)
            st.session_state.display = str(calculator.result)
    
    with col4:
        if st.button("나누기 (÷)"):
            result = calculator.divide(num_input)
            st.session_state.display = str(result)
    
    # 초기화 버튼
    if st.button("초기화 (C)"):
        calculator.clear()
        st.session_state.display = "0"
    
    # 공학용 계산기 기능
    if isinstance(calculator, ScientificCalculator):
        st.subheader("공학용 계산기 기능")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("거듭제곱 (^)"):
                calculator.power(num_input)
                st.session_state.display = str(calculator.result)
        
        with col2:
            if st.button("제곱근 (√)"):
                result = calculator.square_root()
                st.session_state.display = str(result)
        
        with col3:
            if st.button("사인 (sin)"):
                calculator.sin()
                st.session_state.display = str(calculator.result)
        
        with col4:
            if st.button("코사인 (cos)"):
                calculator.cos()
                st.session_state.display = str(calculator.result)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("탄젠트 (tan)"):
                calculator.tan()
                st.session_state.display = str(calculator.result)
        
        with col2:
            if st.button("로그 (log10)"):
                result = calculator.log10()
                st.session_state.display = str(result)
    
    # 계산 기록 표시
    st.subheader("계산 기록")
    history = calculator.get_history()
    
    if history:
        for entry in history:
            st.text(entry)
    else:
        st.text("아직 계산 기록이 없습니다.")


if __name__ == "__main__":
    main()
