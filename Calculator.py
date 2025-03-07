import streamlit as st
import math

class Calculator:
    """기본 계산기 클래스"""
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.current_input = ""
        self.result = 0
        self.operation = None
        self.previous_operation = None
        self.history = []
        self.just_calculated = False
    
    def process_digit(self, digit):
        if self.just_calculated:
            self.current_input = str(digit)
            self.just_calculated = False
        else:
            self.current_input += str(digit)
        return self.current_input if self.current_input else "0"
    
    def process_decimal(self):
        if "." not in self.current_input:
            if not self.current_input:
                self.current_input = "0."
            else:
                self.current_input += "."
        return self.current_input
    
    def clear_entry(self):
        self.current_input = ""
        return "0"
    
    def clear_all(self):
        self.reset()
        return "0"
    
    def backspace(self):
        if self.current_input:
            self.current_input = self.current_input[:-1]
        return self.current_input if self.current_input else "0"
    
    def negate(self):
        if self.current_input:
            if self.current_input[0] == "-":
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            return self.current_input
        elif self.result != 0:
            self.result = -self.result
            return str(self.result)
        return "0"
    
    def set_operation(self, op):
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
        if not self.current_input and not self.just_calculated:
            return str(self.result)
        
        if not self.just_calculated:
            current_value = float(self.current_input)
            if self.operation == "+":
                self.result += current_value
                self.history.append(f"{self.result - current_value} + {current_value} = {self.result}")
            elif self.operation == "-":
                self.result -= current_value
                self.history.append(f"{self.result + current_value} - {current_value} = {self.result}")
            elif self.operation == "*":
                self.result *= current_value
                self.history.append(f"{self.result / current_value} × {current_value} = {self.result}")
            elif self.operation == "/":
                if current_value == 0:
                    self.history.append(f"{self.result} ÷ 0 = Error")
                    return "Error: Division by zero"
                self.result /= current_value
                self.history.append(f"{self.result * current_value} ÷ {current_value} = {self.result}")
            else:
                self.result = float(self.current_input)
        
        self.previous_operation = self.operation
        self.operation = None
        self.current_input = ""
        self.just_calculated = True
        
        # 소수점 아래가 0인 경우 정수로 표시
        if self.result == int(self.result):
            return str(int(self.result))
        return str(self.result)

class ScientificCalculator(Calculator):
    """공학용 계산기 클래스"""
    def square(self):
        if self.current_input:
            value = float(self.current_input)
            result = value ** 2
            self.history.append(f"{value}² = {result}")
            self.result = result
        else:
            self.result = self.result ** 2
            self.history.append(f"{self.result / self.result ** 0.5}² = {self.result}")
        
        self.current_input = ""
        self.just_calculated = True
        
        if self.result == int(self.result):
            return str(int(self.result))
        return str(self.result)
    
    def square_root(self):
        if self.current_input:
            value = float(self.current_input)
            if value < 0:
                self.history.append(f"√{value} = Error")
                return "Error: Invalid input"
            result = math.sqrt(value)
            self.history.append(f"√{value} = {result}")
            self.result = result
        else:
            if self.result < 0:
                self.history.append(f"√{self.result} = Error")
                return "Error: Invalid input"
            self.result = math.sqrt(self.result)
            self.history.append(f"√{self.result * self.result} = {self.result}")
        
        self.current_input = ""
        self.just_calculated = True
        
        if self.result == int(self.result):
            return str(int(self.result))
        return str(self.result)
    
    def sin(self):
        if self.current_input:
            value = float(self.current_input)
            result = math.sin(math.radians(value))
            self.history.append(f"sin({value}°) = {result}")
            self.result = result
        else:
            self.result = math.sin(math.radians(self.result))
            self.history.append(f"sin({value}°) = {self.result}")
        
        self.current_input = ""
        self.just_calculated = True
        return str(self.result)
    
    def cos(self):
        if self.current_input:
            value = float(self.current_input)
            result = math.cos(math.radians(value))
            self.history.append(f"cos({value}°) = {result}")
            self.result = result
        else:
            self.result = math.cos(math.radians(self.result))
            self.history.append(f"cos({value}°) = {self.result}")
        
        self.current_input = ""
        self.just_calculated = True
        return str(self.result)

# 계산기 상태 초기화
if 'calc' not in st.session_state:
    st.session_state.calc = Calculator()
if 'display' not in st.session_state:
    st.session_state.display = "0"
if 'calc_type' not in st.session_state:
    st.session_state.calc_type = "basic"

# 액션 처리 함수들
def digit_click(num):
    st.session_state.display = st.session_state.calc.process_digit(num)

def operation_click(op):
    st.session_state.display = st.session_state.calc.set_operation(op)

def calculate_click():
    st.session_state.display = st.session_state.calc.calculate()

def decimal_click():
    st.session_state.display = st.session_state.calc.process_decimal()

def clear_entry_click():
    st.session_state.display = st.session_state.calc.clear_entry()

def clear_all_click():
    st.session_state.display = st.session_state.calc.clear_all()

def backspace_click():
    st.session_state.display = st.session_state.calc.backspace()

def negate_click():
    st.session_state.display = st.session_state.calc.negate()

def square_click():
    st.session_state.display = st.session_state.calc.square()

def sqrt_click():
    st.session_state.display = st.session_state.calc.square_root()

def sin_click():
    st.session_state.display = st.session_state.calc.sin()

def cos_click():
    st.session_state.display = st.session_state.calc.cos()

def change_calc_type():
    if st.session_state.calc_type == "basic":
        st.session_state.calc = Calculator()
    else:
        st.session_state.calc = ScientificCalculator()
    st.session_state.display = "0"

# UI 구성
st.set_page_config(page_title="간편 계산기", page_icon="🧮")
st.title("😊 간편 계산기")
st.write("숫자 버튼을 눌러 계산해보세요!")

# 계산기 유형 선택
calc_type = st.radio(
    "계산기 유형 선택:",
    ("기본 계산기", "공학용 계산기"),
    horizontal=True,
    key="calc_type_radio",
    on_change=change_calc_type
)

if calc_type == "기본 계산기":
    st.session_state.calc_type = "basic"
    if not isinstance(st.session_state.calc, Calculator) or isinstance(st.session_state.calc, ScientificCalculator):
        st.session_state.calc = Calculator()
else:
    st.session_state.calc_type = "scientific"
    if not isinstance(st.session_state.calc, ScientificCalculator):
        st.session_state.calc = ScientificCalculator()

# 디스플레이
st.markdown(
    f"""
    <div style="background-color:#f0f2f6; padding:10px; border-radius:5px; margin-bottom:10px; text-align:right; font-family:monospace;">
        <h2>{st.session_state.display}</h2>
    </div>
    """, 
    unsafe_allow_html=True
)

# 공학용 계산기 추가 버튼
if isinstance(st.session_state.calc, ScientificCalculator):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("x²", use_container_width=True, on_click=square_click)
    with col2:
        st.button("√x", use_container_width=True, on_click=sqrt_click)
    with col3:
        st.button("sin", use_container_width=True, on_click=sin_click)
    with col4:
        st.button("cos", use_container_width=True, on_click=cos_click)

# 기본 기능 버튼
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("C", use_container_width=True, on_click=clear_entry_click)
with col2:
    st.button("AC", use_container_width=True, on_click=clear_all_click)
with col3:
    st.button("⌫", use_container_width=True, on_click=backspace_click)
with col4:
    st.button("÷", use_container_width=True, on_click=operation_click, args=("/",))

# 숫자 버튼 7, 8, 9 및 곱하기
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("7", use_container_width=True, on_click=digit_click, args=(7,))
with col2:
    st.button("8", use_container_width=True, on_click=digit_click, args=(8,))
with col3:
    st.button("9", use_container_width=True, on_click=digit_click, args=(9,))
with col4:
    st.button("×", use_container_width=True, on_click=operation_click, args=("*",))

# 숫자 버튼 4, 5, 6 및 빼기
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("4", use_container_width=True, on_click=digit_click, args=(4,))
with col2:
    st.button("5", use_container_width=True, on_click=digit_click, args=(5,))
with col3:
    st.button("6", use_container_width=True, on_click=digit_click, args=(6,))
with col4:
    st.button("-", use_container_width=True, on_click=operation_click, args=("-",))

# 숫자 버튼 1, 2, 3 및 더하기
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("1", use_container_width=True, on_click=digit_click, args=(1,))
with col2:
    st.button("2", use_container_width=True, on_click=digit_click, args=(2,))
with col3:
    st.button("3", use_container_width=True, on_click=digit_click, args=(3,))
with col4:
    st.button("+", use_container_width=True, on_click=operation_click, args=("+",))

# 부호 변경, 0, 소수점, 계산
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("±", use_container_width=True, on_click=negate_click)
with col2:
    st.button("0", use_container_width=True, on_click=digit_click, args=(0,))
with col3:
    st.button(".", use_container_width=True, on_click=decimal_click)
with col4:
    st.button("=", use_container_width=True, on_click=calculate_click)

# 계산 기록
with st.expander("계산 기록"):
    if hasattr(st.session_state.calc, 'history'):
        history = st.session_state.calc.history
        if history:
            for entry in history:
                st.write(entry)
        else:
            st.write("아직 계산 기록이 없습니다.")
