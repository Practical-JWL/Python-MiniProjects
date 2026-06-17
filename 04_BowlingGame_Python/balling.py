import flet as ft
import random
import threading

class BowlingGame(ft.Column):
    def __init__(self):
        super().__init__()
        self.spacing = 20
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self.human_dropdown = ft.Dropdown(
            label="플레이어 (사람) 수",
            options=[ft.dropdown.Option(str(i)) for i in range(1, 5)],
            value="1", width=200
        )
        self.bot_dropdown = ft.Dropdown(
            label="컴퓨터 (봇) 수",
            options=[ft.dropdown.Option(str(i)) for i in range(0, 4)],
            value="0", width=200
        )
        self.setup_error_text = ft.Text("", color="red", weight="bold")
        self.bot_timer = None 
        self.is_paused = False 
        self.last_status_msg = "게임을 시작합니다!" # 상태 메시지 보존용
        
        self.show_setup_screen(is_init=True)

    # ==========================================
    # [화면 구성: 설정 화면]
    # ==========================================
    def show_setup_screen(self, is_init=False):
        self.controls = [
            ft.Container(height=50),
            ft.Text("🎳 볼링 300 챌린지 - 멀티플레이", size=30, weight="bold", color="blue"),
            ft.Text("총 인원은 1명에서 최대 4명까지 가능합니다.", size=16),
            ft.Container(height=20),
            self.human_dropdown,
            self.bot_dropdown,
            self.setup_error_text,
            ft.Container(height=20),
            ft.ElevatedButton(
                content=ft.Text("게임 시작하기", size=18, weight="bold"),
                style=ft.ButtonStyle(bgcolor="blue", color="white", padding=20),
                on_click=self.start_game
            )
        ]
        if not is_init:
            if self.page: self.update()

    def start_game(self, e):
        h_count = int(self.human_dropdown.value)
        b_count = int(self.bot_dropdown.value)
        total = h_count + b_count
        
        if total > 4:
            self.setup_error_text.value = "총 인원은 4명을 초과할 수 없습니다!"
            self.update()
            return
        elif total < 1:
            self.setup_error_text.value = "최소 1명 이상의 플레이어가 필요합니다!"
            self.update()
            return
            
        self.last_status_msg = "게임을 시작합니다!"
        self.init_game_state(h_count, b_count)
        self.show_game_screen()

    def init_game_state(self, h_count, b_count):
        self.players = []
        for i in range(h_count):
            self.players.append(self.create_player_dict(f"Player {i+1}", is_bot=False))
        for i in range(b_count):
            self.players.append(self.create_player_dict(f"CPU {i+1}", is_bot=True))
            
        self.active_idx = 0
        self.game_is_finished = False
        self.is_paused = False
        
        if self.bot_timer:
            self.bot_timer.cancel()

    def create_player_dict(self, name, is_bot):
        return {
            "name": name,
            "is_bot": is_bot,
            "rolls": [],
            "current_frame": 1,
            "current_roll": 1,
            "pins": list(range(1, 11)),
            "game_over": False
        }

    # ==========================================
    # [화면 구성: 일시정지 및 확인 화면 (모달 팝업 원천 배제)]
    # 팝업 대신 화면 자체를 교체하여 프리징(먹통) 현상을 영구적으로 막습니다.
    # ==========================================
    def show_pause_menu(self, e):
        self.is_paused = True
        if self.bot_timer:
            self.bot_timer.cancel()

        self.controls = [
            ft.Container(height=100),
            ft.Text("⏸️ 게임 일시정지", size=35, weight="bold", color="black"),
            ft.Container(height=30),
            ft.ElevatedButton(
                content=ft.Text("▶️ 이어서 하기", size=20, weight="bold"),
                style=ft.ButtonStyle(bgcolor="green", color="white", padding=20),
                width=300,
                on_click=self.resume_game
            ),
            ft.Container(height=10),
            ft.ElevatedButton(
                content=ft.Text("🔄 처음부터 다시", size=20, weight="bold"),
                style=ft.ButtonStyle(bgcolor="orange", color="white", padding=20),
                width=300,
                on_click=lambda e: self.confirm_action("restart", from_pause=True)
            ),
            ft.Container(height=10),
            ft.ElevatedButton(
                content=ft.Text("❌ 메인 화면으로", size=20, weight="bold"),
                style=ft.ButtonStyle(bgcolor="red", color="white", padding=20),
                width=300,
                on_click=lambda e: self.confirm_action("exit", from_pause=True)
            )
        ]
        if self.page: self.update()

    def confirm_action(self, action_type, from_pause=False):
        self.is_paused = True
        if self.bot_timer:
            self.bot_timer.cancel()

        if action_type == "restart":
            msg = "게임을 처음부터 다시 시작하시겠습니까?"
            yes_action = self.execute_restart
        else:
            msg = "게임을 종료하고 메인 화면으로 돌아가시겠습니까?"
            yes_action = self.execute_exit

        def no_action(e):
            if from_pause:
                self.show_pause_menu(e)
            else:
                self.resume_game(e)

        self.controls = [
            ft.Container(height=150),
            ft.Text("⚠️ 확인", size=35, weight="bold", color="red"),
            ft.Container(height=10),
            ft.Text(msg, size=20, color="black", weight="bold"),
            ft.Container(height=40),
            ft.Row([
                ft.ElevatedButton(
                    content=ft.Text("예 (Yes)", size=18, weight="bold"),
                    style=ft.ButtonStyle(bgcolor="red", color="white", padding=20),
                    width=150,
                    on_click=yes_action
                ),
                ft.ElevatedButton(
                    content=ft.Text("아니오 (No)", size=18, weight="bold"),
                    style=ft.ButtonStyle(bgcolor="grey", color="white", padding=20),
                    width=150,
                    on_click=no_action
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
        ]
        if self.page: self.update()

    def execute_restart(self, e):
        self.is_paused = False
        self.last_status_msg = "게임을 시작합니다!"
        h_count = sum(1 for p in self.players if not p["is_bot"])
        b_count = sum(1 for p in self.players if p["is_bot"])
        self.init_game_state(h_count, b_count)
        self.show_game_screen()

    def execute_exit(self, e):
        self.is_paused = False
        self.show_setup_screen(is_init=False)

    def resume_game(self, e):
        self.is_paused = False
        # 기존 게임 상태를 그대로 보존한 채로 게임 화면만 다시 그려줍니다.
        self.show_game_screen() 

    # ==========================================
    # [게임 메인 화면 및 실행 로직]
    # ==========================================
    def show_game_screen(self):
        top_bar = ft.Row([
            ft.Container(expand=True), 
            ft.ElevatedButton(
                content=ft.Text("⏸️ PAUSE", weight="bold"), 
                style=ft.ButtonStyle(bgcolor="red", color="white", padding=15),
                on_click=self.show_pause_menu
            )
        ], alignment=ft.MainAxisAlignment.END)

        self.status_text = ft.Text(self.last_status_msg, size=20, weight="bold", color="blue")
        self.pin_visual_text = ft.Text("", size=24, font_family="monospace", color="black")
        self.scoreboards_column = ft.Column(spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.roll_button = ft.ElevatedButton(
            content=ft.Text("🎳 무작위 공 굴리기 (Random Roll)", size=16),
            on_click=self.handle_human_roll,
            style=ft.ButtonStyle(bgcolor="green", color="white", padding=20),
            width=300
        )
        
        self.restart_button = ft.ElevatedButton(
            content=ft.Text("🏠 메인 화면으로 나가기", size=16),
            on_click=lambda e: self.confirm_action("exit", from_pause=False),
            style=ft.ButtonStyle(bgcolor="orange", color="white", padding=15),
            width=300
        )

        self.controls = [
            top_bar,
            ft.Row([self.status_text], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=10),
            ft.Row([self.pin_visual_text], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=20),
            self.scoreboards_column,
            ft.Container(height=20),
            ft.Row([self.roll_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=10),
            ft.Row([self.restart_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=40),
        ]
        self.update_game_ui()
        self.check_and_run_bot_turn()
        if self.page: self.update()

    def handle_human_roll(self, e):
        if self.game_is_finished or self.is_paused: return
        p = self.players[self.active_idx]
        if p["is_bot"] or p["game_over"]: return
        self.execute_roll()

    def execute_bot_roll(self):
        if self.is_paused or self.game_is_finished: return
        self.execute_roll()

    def execute_roll(self):
        if self.game_is_finished or self.is_paused: return
        if not hasattr(self, 'players') or len(self.players) == 0: return
        
        p = self.players[self.active_idx]
        
        num_to_fall = random.randint(0, len(p["pins"]))
        fallen_pins = random.sample(p["pins"], num_to_fall)
        for pin in fallen_pins:
            p["pins"].remove(pin)
            
        pins_count = len(fallen_pins)
        turn_msg = f"[{p['name']}] "
        
        if pins_count == 10 and p["current_roll"] == 1:
            self.last_status_msg = turn_msg + "💥 스트라이크!!"
        elif len(p["pins"]) == 0 and p["current_roll"] > 1:
            self.last_status_msg = turn_msg + "🎯 스페어 메이드!"
        else:
            self.last_status_msg = turn_msg + f"{pins_count}핀 쓰러짐!"
            
        self.status_text.value = self.last_status_msg
            
        turn_ended = self.process_roll_logic(p, pins_count)
        self.update_game_ui()
        
        if turn_ended:
            self.advance_turn()
        else:
            if p["is_bot"]:
                self.check_and_run_bot_turn()

    def process_roll_logic(self, p, pins):
        p["rolls"].append(pins)
        turn_ended = False
        
        if p["current_frame"] < 10:
            if p["current_roll"] == 1:
                if pins == 10:
                    p["current_frame"] += 1
                    p["pins"] = list(range(1, 11))
                    turn_ended = True
                else:
                    p["current_roll"] = 2
            else:
                p["current_frame"] += 1
                p["current_roll"] = 1
                p["pins"] = list(range(1, 11))
                turn_ended = True
        else:
            if p["current_roll"] == 1:
                if pins == 10: p["pins"] = list(range(1, 11))
                p["current_roll"] = 2
            elif p["current_roll"] == 2:
                is_spare = (p["rolls"][-2] != 10 and p["rolls"][-2] + pins == 10)
                if pins == 10 or is_spare:
                    p["pins"] = list(range(1, 11))
                    p["current_roll"] = 3
                else:
                    p["game_over"] = True
                    turn_ended = True
            elif p["current_roll"] == 3:
                p["game_over"] = True
                turn_ended = True
                
        return turn_ended

    def advance_turn(self):
        if all(p["game_over"] for p in self.players):
            self.game_is_finished = True
            self.last_status_msg = "🎉 모든 게임이 종료되었습니다!"
            self.status_text.value = self.last_status_msg
            self.roll_button.disabled = True
            if self.page: self.update()
            return

        while True:
            self.active_idx = (self.active_idx + 1) % len(self.players)
            if not self.players[self.active_idx]["game_over"]:
                break
                
        self.update_game_ui()
        self.check_and_run_bot_turn()

    def check_and_run_bot_turn(self):
        if self.game_is_finished or self.is_paused: return
        if not hasattr(self, 'players') or len(self.players) == 0: return
        p = self.players[self.active_idx]
        
        if p["is_bot"]:
            self.roll_button.disabled = True
            self.last_status_msg = f"🤖 {p['name']}가 공을 굴릴 준비를 합니다..."
            self.status_text.value = self.last_status_msg
            if self.page: self.update()
            
            self.bot_timer = threading.Timer(1.0, self.execute_bot_roll)
            self.bot_timer.start()
        else:
            self.roll_button.disabled = False
            if self.page: self.update()

    def update_game_ui(self):
        if not hasattr(self, 'players') or not self.players:
            return
            
        p = self.players[self.active_idx]
        display = ""
        rows = [[7, 8, 9, 10], [4, 5, 6], [2, 3], [1]]
        for row in rows:
            line = " ".join(["🔴" if pin in p["pins"] else "⚪" for pin in row])
            display += line.center(15) + "\n"
        self.pin_visual_text.value = display

        board_controls = []
        for i, player in enumerate(self.players):
            is_active = (i == self.active_idx and not self.game_is_finished)
            bg_color = "#E8F5E9" if is_active else "#F5F5DC"
            border_color = "green" if is_active else "black"
            border_width = 3 if is_active else 2
            
            player_label = ft.Text(
                f"{'👉 ' if is_active else ''}{player['name']} {'(종료)' if player['game_over'] else ''}", 
                weight="bold", size=16, color="black"
            )
            
            row_data = self.get_scoreboard_data(player["rolls"])
            row_ui = self.create_scoreboard_row_ui(row_data, bg_color, border_color, border_width)
            board_controls.append(ft.Column([player_label, row_ui], spacing=5, alignment=ft.MainAxisAlignment.CENTER))
            
        self.scoreboards_column.controls = board_controls
        
        if self.page: 
            self.update()

    def get_scoreboard_data(self, rolls):
        frames = [{"rolls": [], "score": ""} for _ in range(10)]
        roll_idx = 0
        cumulative_score = 0

        for frame_idx in range(10):
            if roll_idx >= len(rolls): break

            if frame_idx < 9:
                r1 = rolls[roll_idx]
                if r1 == 10:
                    frames[frame_idx]["rolls"] = ["", "X"]
                    if roll_idx + 2 < len(rolls):
                        cumulative_score += 10 + rolls[roll_idx+1] + rolls[roll_idx+2]
                        frames[frame_idx]["score"] = cumulative_score
                    roll_idx += 1
                else:
                    if roll_idx + 1 < len(rolls):
                        r2 = rolls[roll_idx+1]
                        r1_str = "-" if r1 == 0 else str(r1)
                        if r1 + r2 == 10:
                            frames[frame_idx]["rolls"] = [r1_str, "/"]
                            if roll_idx + 2 < len(rolls):
                                cumulative_score += 10 + rolls[roll_idx+2]
                                frames[frame_idx]["score"] = cumulative_score
                        else:
                            r2_str = "-" if r2 == 0 else str(r2)
                            frames[frame_idx]["rolls"] = [r1_str, r2_str]
                            cumulative_score += r1 + r2
                            frames[frame_idx]["score"] = cumulative_score
                        roll_idx += 2
                    else:
                        r1_str = "-" if r1 == 0 else str(r1)
                        frames[frame_idx]["rolls"] = [r1_str, ""]
                        roll_idx += 1
            else:
                r_strs = []
                for i in range(3):
                    if roll_idx + i < len(rolls):
                        val = rolls[roll_idx + i]
                        if val == 10: r_strs.append("X")
                        elif i == 1 and rolls[roll_idx] + val == 10 and rolls[roll_idx] != 10: r_strs.append("/")
                        elif i == 2 and rolls[roll_idx+1] + val == 10 and rolls[roll_idx+1] != 10 and r_strs[1] != "/": r_strs.append("/")
                        else: r_strs.append("-" if val == 0 else str(val))
                frames[frame_idx]["rolls"] = r_strs
                if len(r_strs) == 3 or (len(r_strs) == 2 and rolls[roll_idx] + rolls[roll_idx+1] < 10):
                    frames[frame_idx]["score"] = self.calculate_total_score(rolls)
        return frames

    def calculate_total_score(self, rolls):
        score, idx = 0, 0
        for _ in range(10):
            if idx >= len(rolls): break
            if rolls[idx] == 10: 
                if idx + 2 < len(rolls): score += 10 + rolls[idx+1] + rolls[idx+2]
                idx += 1
            elif idx + 1 < len(rolls) and rolls[idx] + rolls[idx+1] == 10: 
                if idx + 2 < len(rolls): score += 10 + rolls[idx+2]
                idx += 2
            elif idx + 1 < len(rolls):
                score += rolls[idx] + rolls[idx+1]
                idx += 2
            else: break
        return score

    def create_scoreboard_row_ui(self, data_list, bg_color, border_color, border_width):
        frame_controls = []
        for i in range(10):
            data = data_list[i]
            is_last = (i == 9)
            width = 90 if is_last else 60
            rolls = data["rolls"]
            
            def make_slot(text, is_right, is_bottom):
                b_right = ft.BorderSide(1, "black") if is_right else ft.BorderSide(0, "transparent")
                b_bottom = ft.BorderSide(1, "black") if is_bottom else ft.BorderSide(0, "transparent")
                return ft.Container(
                    content=ft.Text(text, size=14, weight="bold", color="black"), 
                    width=30, height=30, alignment=ft.Alignment.CENTER, 
                    border=ft.Border(right=b_right, bottom=b_bottom)
                )

            if not is_last:
                s1 = rolls[0] if len(rolls) > 0 else ""
                s2 = rolls[1] if len(rolls) > 1 else ""
                slots = [make_slot(s1, True, True), make_slot(s2, False, True)]
            else:
                s1 = rolls[0] if len(rolls) > 0 else ""
                s2 = rolls[1] if len(rolls) > 1 else ""
                s3 = rolls[2] if len(rolls) > 2 else ""
                slots = [make_slot(s1, True, True), make_slot(s2, True, True), make_slot(s3, False, True)]

            score_val = str(data["score"]) if data["score"] != "" else " "
            frame_container = ft.Container(
                content=ft.Column([
                    ft.Container(content=ft.Text(str(i+1), weight="bold", color="black"), alignment=ft.Alignment.CENTER, height=25, bgcolor="#E0E0E0", border=ft.Border(bottom=ft.BorderSide(1, "black"))),
                    ft.Row(slots, spacing=0),
                    ft.Container(content=ft.Text(score_val, size=16, weight="bold", color="black"), alignment=ft.Alignment.CENTER, height=45)
                ], spacing=0),
                width=width, border=ft.border.all(border_width, border_color), bgcolor=bg_color
            )
            frame_controls.append(frame_container)
        return ft.Row(frame_controls, spacing=0, alignment=ft.MainAxisAlignment.CENTER)

def main(page: ft.Page):
    page.title = "볼링 300 시뮬레이터 (멀티플레이 & Pause)"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.add(BowlingGame())

if __name__ == "__main__":
    ft.run(main)