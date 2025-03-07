import streamlit as st
import math

# OOP 방식의 계산기 클래스
class SimpleCalculator:
    def __init__(self):
        self.expression = ""
        self.result = "0"
        self.history = []
        self.replace_next = False
    
    def append_value(self, value):
        """숫자나 연산자를 표현식에 추가"""
        if self.replace_next:
            self.expression = str(value)
            self.replace_next = False
        else:
            self.expression += str(value)
    
    def calculate(self):
        """현재 표현식 계산"""
        try:
            # 안전한 계산을 위해 eval 대신 사용할 수 있지만 간결성을 위해 eval 사용
            result = eval(self.expression)
            # 정수 결과는 소수점 없이 표시
            if result == int(result):
                result = int(result)
            self.result = str(result)
            self.history.append(f"{self.expression} = {self.result}")
            self.expression = self.result
            self.replace_next = True
            return self.result
        except Exception as e:
            self.result = "오류"
            self.expression = ""
            self.replace_next = True
            return "오류"
    
    def clear(self):
        """계산기 초기화"""
        self.expression = ""
        self.result = "0"
        self.replace_next = False
    
    def backspace(self):
        """마지막 문자 삭제"""
        self.expression = self.expression[:-1]
    
    def square_root(self):
        """제곱근 계산"""
        try:
            value = eval(self.expression) if self.expression else 0
            if value < 0:
                self.result = "오류"
                self.replace_next = True
                return "오류"
            result = math.sqrt(value)
            if result == int(result):
                result = int(result)
            self.result = str(result)
            self.history.append(f"√({self.expression}) = {self.result}")
            self.expression = self.result
            self.replace_next = True
            return self.result
        except:
            self.result = "오류"
            self.replace_next = True
            return "오류"
    
    def square(self):
        """제곱 계산"""
        try:
            value = eval(self.expression) if self.expression else 0
            result = value ** 2
            if result == int(result):
                result = int(result)
            self.result = str(result)
            self.history.append(f"({self.expression})² = {self.result}")
            self.expression = self.result
            self.replace_next = True
            return self.result
        except:
            self.result = "오류"
            self.replace_next = True
            return "오류"
    
    def toggle_sign(self):
        """부호 변경"""
        try:
            value = eval(self.expression) if self.expression else 0
            result = -value
            if result == int(result):
                result = int(result)
            self.result = str(result)
            self.history.append(f"-({self.expression}) = {self.result}")
            self.expression = self.result
            self.replace_next = True
            return self.result
        except:
            self.result = "오류"
            self.replace_next = True
            return "오류"
    
    def get_history(self):
        """계산 기록 반환"""
        return self.history

# 계산기 상태 초기화
if 'calculator' not in st.session_state:
    st.session_state.calculator = SimpleCalculator()

# 액션 처리 함수들
def append_value(value):
    st.session_state.calculator.append_value(value)

def calculate():
    st.session_state.calculator.calculate()

def clear():
    st.session_state.calculator.clear()

def backspace():
    st.session_state.calculator.backspace()

def square_root():
    st.session_state.calculator.square_root()

def square():
    st.session_state.calculator.square()

def toggle_sign():
    st.session_state.calculator.toggle_sign()

# Streamlit UI 구성
st.set_page_config(page_title="간단한 계산기", page_icon="🧮")
st.title("🧮 간단한 계산기")
st.write("객체지향 프로그래밍(OOP)으로 구현된 계산기입니다.")

# 표현식과 결과 표시
st.text_input("계산식:", value=st.session_state.calculator.expression, key="expr_display", disabled=True)
st.markdown(f"<h2 style='text-align: right;'>{st.session_state.calculator.result}</h2>", unsafe_allow_html=True)

# 계산기 버튼 배열
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("C", key="clear", on_click=clear, use_container_width=True)
with col2:
    st.button("x²", key="square", on_click=square, use_container_width=True)
with col3:
    st.button("√", key="sqrt", on_click=square_root, use_container_width=True)
with col4:
    st.button("÷", key="divide", on_click=lambda: append_value("/"), use_container_width=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("7", key="7", on_click=lambda: append_value(7), use_container_width=True)
with col2:
    st.button("8", key="8", on_click=lambda: append_value(8), use_container_width=True)
with col3:
    st.button("9", key="9", on_click=lambda: append_value(9), use_container_width=True)
with col4:
    st.button("×", key="multiply", on_click=lambda: append_value("*"), use_container_width=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("4", key="4", on_click=lambda: append_value(4), use_container_width=True)
with col2:
    st.button("5", key="5", on_click=lambda: append_value(5), use_container_width=True)
with col3:
    st.button("6", key="6", on_click=lambda: append_value(6), use_container_width=True)
with col4:
    st.button("-", key="minus", on_click=lambda: append_value("-"), use_container_width=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("1", key="1", on_click=lambda: append_value(1), use_container_width=True)
with col2:
    st.button("2", key="2", on_click=lambda: append_value(2), use_container_width=True)
with col3:
    st.button("3", key="3", on_click=lambda: append_value(3), use_container_width=True)
with col4:
    st.button("+", key="plus", on_click=lambda: append_value("+"), use_container_width=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("±", key="negate", on_click=toggle_sign, use_container_width=True)
with col2:
    st.button("0", key="0", on_click=lambda: append_value(0), use_container_width=True)
with col3:
    st.button(".", key="decimal", on_click=lambda: append_value("."), use_container_width=True)
with col4:
    st.button("=", key="equals", on_click=calculate, use_container_width=True)

# 계산 기록 표시
with st.expander("계산 기록"):
    history = st.session_state.calculator.get_history()
    if history:
        for entry in history:
            st.write(entry)
    else:
        st.write("아직 계산 기록이 없습니다.")
