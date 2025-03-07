# calculator_app_improved.py
import streamlit as st
import math

# 객체지향 계산기 클래스
class Calculator:
    """기본 계산기 클래스"""
    def __init__(self, name="기본 계산기"):
        self.name = name
        self.result = 0
        self.current_input = ""
        self.operation = None
        self.history = []
        self.just_calculated = False
    
    def digit(self, num):
        """숫자 버튼 입력"""
        if self.just_calculated:
            self.current_input = str(num)
            self.just_calculated = False
        else:
            self.current_input += str(num)
        return self.current_input
    
    def decimal(self):
        """소수점 입력"""
        if "." not in self.current_input:
            if self.current_input == "":
                self.current_input = "0."
            else:
                self.current_input += "."
        return self.current_input
    
    def clear_entry(self):
        """현재 입력 지우기"""
        self.current_input = ""
        return self.current_input
    
    def clear_all(self):
        """모두 지우기"""
        self.result = 0
        self.current_input = ""
        self.operation = None
        self._add_to_history("모두 지우기")
        return "0"
    
    def backspace(self):
        """마지막 문자 지우기"""
        if self.current_input:
            self.current_input = self.current_input[:-1]
        return self.current_input or "0"
    
    def set_operation(self, op):
        """연산 설정"""
        if self.current_input:
            if self.operation and not self.just_calculated:
                self.calculate()
            else:
                self.result = float(self.current_input)
            self.operation = op
            self.current_input = ""
            self.just_calculated = False
        elif self.result != 0:
            self.operation = op
        return str(self.result)
    
    def calculate(self):
        """계산 실행"""
        if not self.current_input and not self.just_calculated:
            return str(self.result)
            
        if not self.just_calculated:
            current_value = float(self.current_input)
            if self.operation == "+":
                self.result += current_value
                self._add_to_history(f"{self.result - current_value} + {current_value}")
            elif self.operation == "-":
                self.result -= current_value
                self._add_to_history(f"{self.result + current_value} - {current_value}")
            elif self.operation == "*":
                self.result *= current_value
                self._add_to_history(f"{self.result / current_value} × {current_value}")
            elif self.operation == "/":
                if current_value == 0:
                    self._add_to_history(f"{self.result} ÷ 0 (오류)")
                    return "오류: 0으로 나눌 수 없습니다"
                self.result /= current_value
                self._add_to_history(f"{self.result * current_value} ÷ {current_value}")
            else:
                self.result = float(self.current_input)
                
        self.current_input = ""
        self.just_calculated = True
        return str(self.result)
    
    def _add_to_history(self, operation):
        """계산 기록 추가"""
        self.history.append(f"{operation} = {self.result}")
    
    def get_history(self):
        """계산 기록 조회"""
        return self.history


class ScientificCalculator(Calculator):
    """공학용 계산기 클래스"""
    def __init__(self):
        super().__init__("공학용 계산기")
    
    def square(self):
        """제곱 계산"""
        if self.current_input:
            value = float(self.current_input)
            result = value ** 2
            self._add_to_history(f"{value}²")
            self.result = result
            self.current_input = ""
            self.just_calculated = True
        else:
            self.result = self.result ** 2
            self._add_to_history(f"{self.result}²")
        return str(self.result)
    
    def square_root(self):
        """제곱근 계산"""
        if self.current_input:
            value = float(self.current_input)
            if value < 0:
                self._add_to_history(f"√{value} (오류)")
                return "오류: 음수의 제곱근"
            result = math.sqrt(value)
            self._add_to_history(f"√{value}")
            self.result = result
            self.current_input = ""
            self.just_calculated = True
        else:
            if self.result < 0:
                self._add_to_history(f"√{self.result} (오류)")
                return "오류: 음수의 제곱근"
            self.result = math.sqrt(self.result)
            self._add_to_history(f"√{self.result}")
        return str(self.result)
    
    def sin(self):
        """사인 계산"""
        if self.current_input:
            value = float(self.current_input)
            result = math.sin(math.radians(value))
            self._add_to_history(f"sin({value}°)")
            self.result = result
            self.current_input = ""
            self.just_calculated = True
        else:
            self.result = math.sin(math.radians(self.result))
            self._add_to_history(f"sin({self.result}°)")
        return str(self.result)
    
    def cos(self):
        """코사인 계산"""
        if self.current_input:
            value = float(self.current_input)
            result = math.cos(math.radians(value))
            self._add_to_history(f"cos({value}°)")
            self.result = result
            self.current_input = ""
            self.just_calculated = True
        else:
            self.result = math.cos(math.radians(self.result))
            self._add_to_history(f"cos({self.result}°)")
        return str(self.result)


# 계산기 UI 함수
def create_calculator_ui():
    if 'calculator' not in st.session_state:
        st.session_state.calculator = Calculator()
    if 'display' not in st.session_state:
        st.session_state.display = "0"
    
    calc_type = st.radio(
        "계산기 유형 선택:",
        ("기본 계산기", "공학용 계산기"),
        horizontal=True
    )
    
    if calc_type == "기본 계산기" and not isinstance(st.session_state.calculator, Calculator):
        st.session_state.calculator = Calculator()
        st.session_state.display = "0"
    elif calc_type == "공학용 계산기" and not isinstance(st.session_state.calculator, ScientificCalculator):
        st.session_state.calculator = ScientificCalculator()
        st.session_state.display = "0"
    
    calculator = st.session_state.calculator
    
    # 현재 입력 표시
    st.markdown(
        f"""
        <div style="background-color:#f0f2f6; padding:10px; border-radius:5px; margin-bottom:10px; text-align:right; font-family:monospace;">
            <h2>{st.session_state.display}</h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # 공학용 계산기 추가 버튼
    if isinstance(calculator, ScientificCalculator):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("x²", use_container_width=True):
                st.session_state.display = calculator.square()
        
        with col2:
            if st.button("√x", use_container_width=True):
                st.session_state.display = calculator.square_root()
        
        with col3:
            if st.button("sin", use_container_width=True):
                st.session_state.display = calculator.sin()
        
        with col4:
            if st.button("cos", use_container_width=True):
                st.session_state.display = calculator.cos()
    
    # 기본 기능 버튼 (모든 계산기 공통)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("C", use_container_width=True):
            st.session_state.display = calculator.clear_entry()
    
    with col2:
        if st.button("AC", use_container_width=True):
            st.session_state.display = calculator.clear_all()
    
    with col3:
        if st.button("⌫", use_container_width=True):
            st.session_state.display = calculator.backspace()
    
    with col4:
        if st.button("÷", use_container_width=True):
            st.session_state.display = calculator.set_operation("/")
    
    # 숫자 버튼 및 기본 연산
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("7", use_container_width=True):
            st.session_state.display = calculator.digit(7)
    
    with col2:
        if st.button("8", use_container_width=True):
            st.session_state.display = calculator.digit(8)
    
    with col3:
        if st.button("9", use_container_width=True):
            st.session_state.display = calculator.digit(9)
    
    with col4:
        if st.button("×", use_container_width=True):
            st.session_state.display = calculator.set_operation("*")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("4", use_container_width=True):
            st.session_state.display = calculator.digit(4)
    
    with col2:
        if st.button("5", use_container_width=True):
            st.session_state.display = calculator.digit(5)
    
    with col3:
        if st.button("6", use_container_width=True):
            st.session_state.display = calculator.digit(6)
    
    with col4:
        if st.button("-", use_container_width=True):
            st.session_state.display = calculator.set_operation("-")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("1", use_container_width=True):
            st.session_state.display = calculator.digit(1)
    
    with col2:
        if st.button("2", use_container_width=True):
            st.session_state.display = calculator.digit(2)
    
    with col3:
        if st.button("3", use_container_width=True):
            st.session_state.display = calculator.digit(3)
    
    with col4:
        if st.button("+", use_container_width=True):
            st.session_state.display = calculator.set_operation("+")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("±", use_container_width=True):
            if calculator.current_input and calculator.current_input != "0":
                if calculator.current_input[0] == "-":
                    calculator.current_input = calculator.current_input[1:]
                else:
                    calculator.current_input = "-" + calculator.current_input
                st.session_state.display = calculator.current_input
    
    with col2:
        if st.button("0", use_container_width=True):
            st.session_state.display = calculator.digit(0)
    
    with col3:
        if st.button(".", use_container_width=True):
            st.session_state.display = calculator.decimal()
    
    with col4:
        if st.button("=", use_container_width=True):
            st.session_state.display = calculator.calculate()
    
    # 계산 기록
    with st.expander("계산 기록"):
        history = calculator.get_history()
        if history:
            for entry in history:
                st.write(entry)
        else:
            st.write("아직 계산 기록이 없습니다.")


def main():
    st.set_page_config(page_title="간편 계산기", page_icon="🧮")
    
    st.title("😊 간편 계산기")
    st.write("숫자 버튼을 눌러 계산해보세요!")
    
    create_calculator_ui()


if __name__ == "__main__":
    main()
