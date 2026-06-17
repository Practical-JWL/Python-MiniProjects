import flet
import random

def main(page: flet.Page):
    # 1단계 : 데이터 설계
    # 승리 횟수 변수, 게임 종료 여부, 선택지 리스트를 준비함.
    user_wins = 0
    computer_wins = 0
    options = ["가위", "바위", "보"]

    # 2단계 : 화면 구성(UI) 설계
    # 점수판, 대결상황, 결과 메시지 등을 보여줄 텍스트 요소들을 만듦.
    page.title = "5전 3선승제 가위바위보"
    page.padding = 30
    
    # 추가: 페이지 전체 요소들을 가로/세로 중앙에 고정(버튼 움직임 방지)
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
    page.vertical_alignment = flet.MainAxisAlignment.CENTER
        

    # [점수판]
    score_text = flet.Text("현재 스코어 - 사용자: 0, 컴퓨터: 0", size=20, weight="bold")
    # [대결상황 및 결과 메시지]
    result_text = flet.Text("가위, 바위, 보 중 하나를 선택하세요!", size=18)
    # [최종 우승 축하 메시지]
    final_winner_text = flet.Text("", size=25, color="blue", weight="bold")

    # 3단계 : 핵심 로직 : 버튼 클릭함수(play_game)
    # 버튼을 누를 때마다 컴퓨터와 승부를 겨루고 승점을 계산함.
    def play_game(user_choice):
        nonlocal user_wins, computer_wins # 바깥쪽의 승리 횟수 변수를 수정하기 위해 사용
        
        # 이미 누군가 3승을 했다면 더 이상 게임을 진행하지 않음
        if user_wins >= 3 or computer_wins >= 3:
            return

        computer_choice = random.choice(options)
        
        # 승패 판정 로직 (비김 포함)
        if user_choice == computer_choice:
            outcome = "비겼습니다!"
        elif (user_choice == "가위" and computer_choice == "보") or \
             (user_choice == "바위" and computer_choice == "가위") or \
             (user_choice == "보" and computer_choice == "바위"):
            outcome = "사용자가 이겼습니다!"
            user_wins += 1
        else:
            outcome = "컴퓨터가 이겼습니다!"
            computer_wins += 1

        # 화면에 결과 업데이트
        result_text.value = f"사용자: {user_choice} vs 컴퓨터: {computer_choice}\n결과: {outcome}"
        score_text.value = f"현재 스코어 - 사용자: {user_wins}, 컴퓨터: {computer_wins}"

        # 5전 3선승제 최종 우승 판정
        if user_wins == 3:
            final_winner_text.value = "최종 우승 : 사용자! 축하합니다! 🏆"
            disable_buttons() # 4단계에서 만든 비활성화 함수 호출
        elif computer_wins == 3:
            final_winner_text.value = "최종 우승 : 아쉽게도 컴퓨터가 이겼네요! 🤖"
            disable_buttons()
            
        page.update()

    # 4단계 : 가로 배치와 버튼 비활성화
    # 게임 종료 시 버튼을 못 누르게 막는 함수와 가로 배치를 구현.

    # [버튼 비활성화 함수]
    def disable_buttons():
        scissors_btn.disabled = True
        rock_btn.disabled = True
        paper_btn.disabled = True

    # [선택 버튼 생성]
    # lambda를 사용해 각각의 값을 play_game 함수로 전달함.
    scissors_btn = flet.FilledButton("가위", on_click=lambda _: play_game("가위"))
    rock_btn = flet.FilledButton("바위", on_click=lambda _: play_game("바위"))
    paper_btn = flet.FilledButton("보", on_click=lambda _: play_game("보"))

    # [화면 조립 및 가로 배치]
    # flet.Row를 사용해 버튼 3개를 가로로 정렬함.
    page.add(
        score_text,
        flet.Row(
            [scissors_btn, rock_btn, paper_btn], 
            alignment=flet.MainAxisAlignment.CENTER
        ),
        result_text,
        final_winner_text
    )

# 앱 실행
flet.run(main)