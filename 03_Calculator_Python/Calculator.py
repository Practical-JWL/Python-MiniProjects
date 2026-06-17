import flet as ft

# ==========================================
# 1. 백엔드: 계산기 로직
# ==========================================
class 숫자만추출():
    def __init__(self): pass
    def _숫자_추출(self, 입력숫자): pass

class 계산기(숫자만추출):
    def __init__(self, *입력숫자):
        super().__init__()
        self.숫자 = []
        self.숫자아님 = []
        self._숫자_추출(입력숫자)

    def _숫자_가져오기(self, 숫자모음, 반환):
        for 숫자 in 숫자모음:
            if isinstance(숫자, (int, float)): 반환.append(숫자)
            else: self.숫자아님.append(숫자)
        return 반환

    def _숫자_추출(self, 입력숫자):
        for 숫자 in 입력숫자:
            if isinstance(숫자, (int, float)): self.숫자.append(숫자)
            elif type(숫자) in (list, tuple):
                self._숫자_가져오기(숫자, self.숫자)
            else: self.숫자아님.append(숫자)

    def 숫자_재입력(self, *입력숫자):
        self.숫자 = []
        self.숫자아님 = []
        self._숫자_추출(입력숫자)

    def 더하기(self): return sum(self.숫자) if self.숫자 else 0

    def 빼기(self):
        if len(self.숫자) >= 2:
            반환 = self.숫자[0]
            for 숫자 in self.숫자[1:]: 반환 -= 숫자
            return 반환
        return self.숫자[0] if self.숫자 else 0

    def 곱하기(self):
        if len(self.숫자) >= 2:
            반환 = self.숫자[0]
            for 숫자 in self.숫자[1:]: 반환 *= 숫자
            return 반환
        return self.숫자[0] if self.숫자 else 0

    def 나누기(self):
        if len(self.숫자) >= 2:
            반환 = self.숫자[0]
            for 숫자 in self.숫자[1:]:
                if 숫자 == 0: return "Error (0 나눔)"
                반환 /= 숫자
            return 반환
        return self.숫자[0] if self.숫자 else 0


# ==========================================
# 2. 프론트엔드: 버그 없는 UI
# ==========================================
def main(page: ft.Page):
    page.title = "계산기" # 제목이 이걸로 떠야 최신 코드가 적용된 것입니다!
    page.padding = 30
    page.theme_mode = "light" 
    page.window_width = 600
    page.window_height = 800

    calc_obj = 계산기()

    # --- UI 컴포넌트 ---
    num1_input = ft.TextField(label="첫 번째 숫자 입력", border_radius=10)
    num2_input = ft.TextField(label="두 번째 숫자 입력", border_radius=10)
    
    operator_dropdown = ft.Dropdown(
        label="연산 기호 선택",
        options=[
            ft.dropdown.Option("+"),
            ft.dropdown.Option("-"),
            ft.dropdown.Option("*"),
            ft.dropdown.Option("/"),
        ],
        border_radius=10
    )

    result_display = ft.Text(
        value="결과가 여기에 표시됩니다.", 
        size=22, 
        weight="bold",  
        color="blue"
    )

    # --- 계산 실행 함수 ---
    def run_calculation(e):
        try:
            val1 = float(num1_input.value) if num1_input.value else 0
            val2 = float(num2_input.value) if num2_input.value else 0
        except ValueError:
            result_display.value = "오류: 숫자만 입력해주세요."
            page.update()
            return

        calc_obj.숫자_재입력(val1, val2)

        op = operator_dropdown.value
        if not op:
            result_display.value = "연산자를 선택해주세요."
        else:
            if op == "+": res = calc_obj.더하기()
            elif op == "-": res = calc_obj.빼기()
            elif op == "*": res = calc_obj.곱하기()
            elif op == "/": res = calc_obj.나누기()
            
            if isinstance(res, (int, float)):
                if isinstance(res, float) and res.is_integer():
                    res = int(res)
                result_display.value = f"결과: {res:,}"
            else:
                result_display.value = res 
        
        page.update()

    # --- 중앙 레이아웃 ---
    main_panel = ft.Container(
        width=500, 
        content=ft.Column(
            controls=[
                ft.Text("🔢 단계별 사칙연산 프로세스", size=25, weight="bold"),
                ft.Divider(height=20),
                
                ft.Text("Step 1. 첫 번째 숫자를 입력하세요.", size=16),
                num1_input,
                
                ft.Text("Step 2. 수행할 연산을 선택하세요.", size=16),
                operator_dropdown,
                
                ft.Text("Step 3. 두 번째 숫자를 입력하세요.", size=16),
                num2_input,
                
                ft.Divider(height=30),
                
                ft.ElevatedButton(
                    content=ft.Text("계산 결과 보기 (=)", color="white", weight="bold"),
                    on_click=run_calculation,
                    bgcolor="blue",
                    height=55,
                    width=500 
                ),
                
                # 💡 핵심 해결: height와 alignment를 모두 지우고, 패딩(padding)과 Row로 글씨를 가운데 정렬합니다.
                # 이렇게 하면 화면을 늘려도 회색 버그가 생기지 않습니다!
                ft.Container(
                    content=ft.Row(
                        controls=[result_display],
                        alignment="center" # Row를 이용한 안전한 가로 중앙 정렬
                    ),
                    padding=30, # 상하좌우 여백을 주어 자연스럽게 높이를 확보
                    margin=ft.margin.only(top=20),
                    bgcolor="#e3f2fd", 
                    border_radius=10,
                    width=500
                )
            ],
            spacing=15
        )
    )

    page.add(
        ft.Row(
            controls=[main_panel],
            alignment="center" 
        )
    )

if __name__ == "__main__":
    ft.app(target=main)