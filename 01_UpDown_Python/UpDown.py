# 사용할 도구를 준비!
import flet
import random

# 화면에 나타날 요소들을 정의하기!
def main(page: flet.Page):
    info_text = flet.Text(value="1~100 사이의 숫자를 맞춰보세요!")    
    answer = random.randint(1, 100) 
    input_box = flet.TextField(label="숫자 입력", width=200)
    result_message = flet.Text(value="결과가 여기 나옵니다.")

    # '정답 확인' 함수 설계!
    def btn_click(e):
        user_guess = input_box.value
        guess_number = int(user_guess)
        if guess_number == answer:
            result_message.value = "정답입니다!"
        elif guess_number < answer:
            result_message.value = "UP!!"
        else:
            result_message.value = "DOWN!!"
        page.update() # 화면 업데이트(Flet에서 쓰는 업데이트 명령어)

# 조립 및 실행  
    check_button = flet.FilledButton("정답 확인", on_click=btn_click)    
    page.add(info_text, input_box, result_message, check_button)

flet.app(target=main)



