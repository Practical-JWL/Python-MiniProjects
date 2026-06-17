# 🎮 Flet 기반 숫자 맞추기 (Up-Down) 게임
Python Flet 라이브러리를 사용하여 제작한 GUI 기반의 숫자 맞추기 게임.
난수 생성과 조건문을 활용한 실시간 상태 업데이트를 학습하기 위해 만듦.

---  
📂 프로젝트 구성
프로젝트의 발전 과정을 확인하기 위해 두 가지 버전의 소스 코드를 포함함.
 #### UpDown.py(초기버전) : 기본 기능 구현, 예외처리 미적
 #### UpDown_Repair.py(수정버전) : try-except문을 적용한 안정화 버전
---

## 1. 🎯 주요 기능
난수 생성: random.randint를 활용하여 매 게임마다 새로운 정답(1~100) 생성.

실시간 피드백: 사용자가 입력한 숫자와 정답을 비교하여 UP / DOWN / 정답 메시지 출력.

반응형 UI: 버튼 클릭 시 page.update()를 통해 화면의 텍스트가 즉각적으로 변경됨.

---

## 2. 🧠 논리 전개 과정 (Flowchart)
이 프로그램은 사용자의 동작에 반응하는 이벤트 기반(Event-driven) 방식으로 작동하며, 데이터의 흐름은 다음과 같음.

- 초기화(Initialization): 프로그램 실행 시 random 라이브러리가 정답을 생성하고 메모리에 저장함.
- 사용자 입력(User Input): 사용자가 TextField UI를 통해 데이터를 입력함.
- 이벤트 발생(Event Trigger): '정답 확인' 버튼 클릭 시 바인딩된 btn_click 핸들러가 호출됨.
- 데이터 처리(Data Processing): 입력된 문자열을 정수형으로 **형변환(Casting)**하며, 이 과정에서 try-except를 통한 유효성 검사를 수행함.
- 조건 판별(Logical Comparison): 연산자를 통해 정답 여부를 판별하고 출력 메시지를 결정함.
- 결과 반영(UI Rendering): page.update()를 호출하여 변경된 상태를 화면에 다시 그려줌.

<img width="540" height="884" alt="image" src="https://github.com/user-attachments/assets/e1624e33-6263-458a-ab53-bb91e54b64b4" />

---

## 3. 🏗️ 코드 핵심 개념 구조
🔹 데이터 흐름과 형변환
문제점: input_box.value로 들어오는 데이터는 기본적으로 문자열(String) 타입임.

해결: int(user_guess)를 통해 정수형으로 변환해 주어야 크기 비교(>, <) 연산이 가능해짐.

---

## 4. ⭐ 중요 구현 포인트
가독성 높은 UI: FilledButton과 TextField를 적절히 배치하여 직관적인 인터페이스를 구성함.

직관적인 조건문: **if-elif-else** 구조를 사용하여 세 가지 케이스(정답, 작음, 큼)를 명확하게 분기 처리함.

---

## 5. 오류발생
문자로 입력했을때 오류발생(예외처리 미구현)
<img width="549" height="217" alt="image" src="https://github.com/user-attachments/assets/e44bf712-3e1b-4ed4-84f4-cc078801af28" />

---

## 6. 문제해결
- try-except문을 사용해 에러를 미리 방지하도록함.
<img width="390" height="233" alt="image" src="https://github.com/user-attachments/assets/37327262-6dca-43c0-96d9-880b877dd5ae" />

- 문제: int() 함수를 사용할 때 사용자가 문자를 입력하면 ValueError가 발생하며 프로그램이 **강제 종료**되는 현상 발견.
- 해결: try-except 블록을 도입하여 예외 상황을 포착함.
- try: 정수 변환을 시도하고 성공하면 정상 게임 진행.
- except ValueError: 숫자가 아닌 값이 들어올 경우 사용자에게 에러 메시지를 시각적으로 표시하고 함수를 안전하게 종료(return).
- 결과: 사용자의 실수에도 프로그램이 멈추지 않고 계속 작동하는 **코드의 견고성**(**Robustness**)을 확보함.







