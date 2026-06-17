import flet
import random

def main(page: flet.Page):
    page.title = "숫자 맞추기 게임 (보안관 버전)"
    page.window_width = 400
    page.window_height = 500
    
    info_text = flet.Text(value="1~100 사이의 숫자를 맞춰보세요!", size=18)    
    answer = random.randint(1, 100) 
    input_box = flet.TextField(label="숫자 입력", width=200, hint_text="숫자를 적어주세요")
    result_message = flet.Text(value="결과가 여기 나옵니다.", color="blue", size=16)

    def btn_click(e):
        user_guess = input_box.value
        
        # --- 핵심: 예외 처리 구간 ---
        try:
            # 사용자의 입력을 정수로 변환 시도
            guess_number = int(user_guess)
        except ValueError:
            # 만약 숫자가 아니어서 에러가 발생하면 이쪽이 실행됨
            result_message.value = "⚠️ 오류: 숫자만 입력 가능합니다!"
            result_message.color = "red"
            page.update()
            return # 함수를 여기서 종료하여 아래 비교 로직을 실행하지 않음
        # --------------------------

        # 숫자 비교 로직
        result_message.color = "blue" # 다시 파란색으로 복구
        if guess_number == answer:
            result_message.value = "🎉 정답입니다! 축하해요!"
            result_message.color = "green"
        elif guess_number < answer:
            result_message.value = "UP ↑ (더 큰 숫자를 입력하세요)"
        else:
            result_message.value = "DOWN ↓ (더 작은 숫자를 입력하세요)"
        
        page.update()

    check_button = flet.FilledButton("정답 확인", on_click=btn_click)    
    
    # 화면 레이아웃 구성
    page.add(
        flet.Column(
            controls=[
                info_text, 
                input_box, 
                check_button, 
                result_message
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=20
        )
    )

flet.app(target=main)