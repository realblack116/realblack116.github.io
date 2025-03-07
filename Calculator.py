import streamlit as st
import math

class Calculator:
    """객체지향 계산기 클래스"""
    def __init__(self):
        self.reset()
        
    def reset(self):
        """계산기 상태 초기화"""
        self.expression = ""
        self.result = "0"
        self.history = []
        self.replace_next = False
        
    def process_input(self, value):
        """사용자 입력 처리"""
        if isinstance(value, (int, float)) or value in "+-*/().":
            self._append_value(value)
        elif value == "=":
            self._calculate()
        elif value == "C":
            self.reset()
        elif value == "√":
            self._square_root()
        elif value == "x²":
            self._square()
        elif value == "±":
            self._toggle_sign()
        
        # 가독성을 위해 결과 포맷팅
        if self.result and self.result != "오류":
            try:
                num = float(self.result)
                if num.is_integer():
                    self.result = str(int(num))
            except:
                pass
                
        return self.get_display(), self.result
    
    def _append_value(self, value):
        """숫자나 연산자를 표현식에 추가"""
        if self.replace_next:
            self.expression = str(value)
            self.replace_next = False
        else:
            self.expression += str(value)
    
    def _calculate(self):
        """표현식 계산"""
        if not self.expression:
            return
            
        try:
            # 계산 시도
            result = eval(self.expression)
            self.result = str(result)
            self.history.append(f"{self.expression} = {self.result}")
            self.expression = self.result
            self.replace_next = True
        except Exception as e:
            self.result = "오류"
            self.history.append(f"{self.expression} = 오류")
            self.replace_next = True
    
    def _square_root(self):
        """제곱근 계산"""
        try:
            if not self.expression:
                return
                
            value = eval(self.expression)
            if value < 0:
                self.result = "오류"
                self.history.append(f"√({value}) = 오류 (음수)")
            else:
                result = math.sqrt(value)
                self.result = str(result)
                self.history.append(f"√({value}) = {result}")
                
            self.expression = self.result
            self.replace_next = True
        except:
            self.result = "오류"
            self.replace_next = True
    
    def _square(self):
        """제곱 계산"""
        try:
            if not self.expression:
                return
                
            value = eval(self.expression)
            result = value ** 2
            self.result = str(result)
            self.history.append(f"({value})² = {result}")
            self.expression = self.result
            self.replace_next = True
        except:
            self.result = "오류"
            self.replace_next = True
    
    def _toggle_sign(self):
        """부호 전환"""
        try:
            if not self.expression:
                return
                
            value = eval(self.expression)
            self.result = str(-value)
            self.history.append(f"-({value}) = {self.result}")
            self.expression = self.result
            self.replace_next = True
        except:
            self.result = "오류"
            self.replace_next = True
    
    def get_display(self):
        """현재 표시할 표현식 반환"""
        return self.expression if self.expression else "0"
    
    def get_history(self):
        """계산 기록 반환"""
        return self.history

# 스타일 관련 함수
def get_button_style(key):
    """버튼 스타일 반환"""
    styles = {
        'number': {
            'background-color': '#ffffff',
            'color': '#333333',
            'font-weight': 'normal',
            'border': '1px solid #dddddd'
        },
        'operator': {
            'background-color': '#f8f9fa',
            'color': '#0366d6',
            'font-weight': 'bold',
            'border': '1px solid #dddddd'
        },
        'equals': {
            'background-color': '#0366d6',
            'color': 'white',
            'font-weight': 'bold',
            'border': '1px solid #0366d6'
        },
        'clear': {
            'background-color': '#ff4b4b',
            'color': 'white',
            'font-weight': 'bold',
            'border': '1px solid #ff4b4b'
        },
        'function': {
            'background-color': '#f1f8ff',
            'color': '#0366d6',
            'font-weight': 'bold',
            'border': '1px solid #dddddd'
        }
    }
    
    if key in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
        return styles['number']
    elif key in ['+', '-', '×', '÷']:
        return styles['operator']
    elif key == '=':
        return styles['equals']
    elif key in ['C']:
        return styles['clear']
    else:
        return styles['function']

def create_styled_button(label, key, on_click_handler=None, args=None):
    """스타일이 적용된 버튼 생성"""
    style = get_button_style(key)
    
    html_button = f"""
    <button 
        style="
            background-color: {style['background-color']};
            color: {style['color']};
            font-weight: {style['font-weight']};
            border: {style['border']};
            border-radius: 5px;
            padding: 10px 0;
            width: 100%;
            font-size: 16px;
            cursor: pointer;
        "
        class="calculator-button"
        data-key="{key}"
    >
        {label}
    </button>
    """
    
    st.markdown(html_button, unsafe_allow_html=True)
    
    # JavaScript를 통한 클릭 이벤트 처리
    st.markdown("""
    <script>
    const buttons = document.querySelectorAll('.calculator-button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const key = this.getAttribute('data-key');
            // Streamlit에 메시지 전송
            window.parent.postMessage({
                type: 'calculator_input',
                key: key
            }, '*');
        });
    });
    </script>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="객체지향 계산기",
        page_icon="🧮",
        layout="centered"
    )
    
    # CSS 스타일
    st.markdown("""
    <style>
    .calculator-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .calculator-display {
        background-color: white;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 5px;
        text-align: right;
        font-family: 'Courier New', monospace;
        border: 1px solid #dddddd;
    }
    
    .display-result {
        font-size: 24px;
        font-weight: bold;
    }
    
    .display-expression {
        font-size: 14px;
        color: #666;
        min-height: 20px;
    }
    
    .footer {
        margin-top: 20px;
        text-align: center;
        font-size: 12px;
        color: #666;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🧮 객체지향 계산기")
    
    # 계산기 객체 초기화
    if 'calculator' not in st.session_state:
        st.session_state.calculator = Calculator()
    
    # 계산기 화면
    st.markdown('<div class="calculator-container">', unsafe_allow_html=True)
    
    # 디스플레이
    st.markdown(f"""
    <div class="calculator-display">
        <div class="display-expression">{st.session_state.calculator.expression}</div>
        <div class="display-result">{st.session_state.calculator.result}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 버튼 행 1
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("C", use_container_width=True, key="clear"):
            st.session_state.calculator.process_input("C")
            st.experimental_rerun()
    with col2:
        if st.button("x²", use_container_width=True, key="square"):
            st.session_state.calculator.process_input("x²")
            st.experimental_rerun()
    with col3:
        if st.button("√", use_container_width=True, key="sqrt"):
            st.session_state.calculator.process_input("√")
            st.experimental_rerun()
    with col4:
        if st.button("÷", use_container_width=True, key="divide"):
            st.session_state.calculator.process_input("/")
            st.experimental_rerun()
    
    # 버튼 행 2
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("7", use_container_width=True, key="7"):
            st.session_state.calculator.process_input(7)
            st.experimental_rerun()
    with col2:
        if st.button("8", use_container_width=True, key="8"):
            st.session_state.calculator.process_input(8)
            st.experimental_rerun()
    with col3:
        if st.button("9", use_container_width=True, key="9"):
            st.session_state.calculator.process_input(9)
            st.experimental_rerun()
    with col4:
        if st.button("×", use_container_width=True, key="multiply"):
            st.session_state.calculator.process_input("*")
            st.experimental_rerun()
    
    # 버튼 행 3
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("4", use_container_width=True, key="4"):
            st.session_state.calculator.process_input(4)
            st.experimental_rerun()
    with col2:
        if st.button("5", use_container_width=True, key="5"):
            st.session_state.calculator.process_input(5)
            st.experimental_rerun()
    with col3:
        if st.button("6", use_container_width=True, key="6"):
            st.session_state.calculator.process_input(6)
            st.experimental_rerun()
    with col4:
        if st.button("-", use_container_width=True, key="minus"):
            st.session_state.calculator.process_input("-")
            st.experimental_rerun()
    
    # 버튼 행 4
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("1", use_container_width=True, key="1"):
            st.session_state.calculator.process_input(1)
            st.experimental_rerun()
    with col2:
        if st.button("2", use_container_width=True, key="2"):
            st.session_state.calculator.process_input(2)
            st.experimental_rerun()
    with col3:
        if st.button("3", use_container_width=True, key="3"):
            st.session_state.calculator.process_input(3)
            st.experimental_rerun()
    with col4:
        if st.button("+", use_container_width=True, key="plus"):
            st.session_state.calculator.process_input("+")
            st.experimental_rerun()
    
    # 버튼 행 5
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("±", use_container_width=True, key="negate"):
            st.session_state.calculator.process_input("±")
            st.experimental_rerun()
    with col2:
        if st.button("0", use_container_width=True, key="0"):
            st.session_state.calculator.process_input(0)
            st.experimental_rerun()
    with col3:
        if st.button(".", use_container_width=True, key="decimal"):
            st.session_state.calculator.process_input(".")
            st.experimental_rerun()
    with col4:
        if st.button("=", use_container_width=True, key="equals"):
            st.session_state.calculator.process_input("=")
            st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 계산 기록
    with st.expander("계산 기록"):
        history = st.session_state.calculator.get_history()
        if history:
            for entry in history[::-1]:  # 최신 기록이 위에 오도록 역순으로 표시
                st.write(entry)
        else:
            st.write("아직 계산 기록이 없습니다.")
    
    # 푸터
    st.markdown(
        '<div class="footer">객체지향 프로그래밍으로 만든 계산기 © 2025</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
