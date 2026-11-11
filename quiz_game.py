
import json
import random
from pathlib import Path

from quiz import Quiz
from quiz_data import get_default_quizzes


# JSON 데이터 저장 파일 위치
STATE_FILE = Path(__file__).resolve().parent / "state.json"


class QuizGame:
    def __init__(self):
        # 기본 퀴즈 목록 생성
        self.quizzes = get_default_quizzes()

        # 최고 점수 초기화
        self.best_score = None

        # 저장된 퀴즈와 최고 점수 불러오기
        self.load_state()

    def show_menu(self):
        # 메인 메뉴 출력
        print("\n===== 나만의 퀴즈 게임 =====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가하기")
        print("3. 퀴즈 목록 보기")
        print("4. 최고 점수 확인")
        print("5. 종료")
        print("==========================")

    def get_menu_choice(self):
        # 메뉴 번호 입력 검증
        while True:
            try:
                choice = input("메뉴 번호를 선택하세요 (1~5): ").strip()

                if not choice:
                    print("입력값이 비어 있습니다.")
                    continue

                if not choice.isdigit():
                    print("숫자만 입력할 수 있습니다.")
                    continue

                number = int(choice)

                if 1 <= number <= 5:
                    return number

                print("1~5 사이의 숫자를 입력하세요.")

            except (KeyboardInterrupt, EOFError):
                print("\n입력이 종료되었습니다.")
                return 5

    def get_answer(self):
        # 정답 번호 입력 검증
        while True:
            try:
                answer = input("정답 번호 (1~4): ").strip()

                if not answer.isdigit():
                    print("1~4 사이의 숫자를 입력하세요.")
                    continue

                number = int(answer)

                if 1 <= number <= 4:
                    return number

                print("1~4 사이의 숫자를 입력하세요.")

            except (KeyboardInterrupt, EOFError):
                print("\n입력이 중단되었습니다.")
                return None

    def get_nonempty_input(self, prompt):
        # 빈 문자열 입력 방지
        while True:
            try:
                value = input(prompt).strip()

                if value:
                    return value

                print("빈 내용은 입력할 수 없습니다.")

            except (KeyboardInterrupt, EOFError):
                print("\n입력이 취소되었습니다.")
                return None

    def get_quiz_count(self):
        # 사용자가 풀 문제 개수 선택
        total = len(self.quizzes)

        print("\n===== 퀴즈 시작 =====")
        print(f"현재 등록된 퀴즈: {total}개")

        while True:
            try:
                value = input(
                    f"몇 문제를 풀겠습니까? (1~{total}): "
                ).strip()

                if not value:
                    print("문제 개수를 입력해야 합니다.")
                    continue

                if not value.isdigit():
                    print("숫자만 입력할 수 있습니다.")
                    continue

                count = int(value)

                if 1 <= count <= total:
                    return count

                print(f"1~{total} 사이의 숫자를 입력하세요.")

            except (KeyboardInterrupt, EOFError):
                print("\n문제 개수 선택이 취소되었습니다.")
                return None

    def play_quiz(self):
        # 퀴즈가 없는 경우 실행 중단
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        # 사용자가 풀 문제 개수 입력
        selected_count = self.get_quiz_count()

        if selected_count is None:
            return

        # 전체 퀴즈 중 선택한 개수만큼 무작위 추출
        # 같은 문제가 중복 출제되지 않음
        selected_quizzes = random.sample(
            self.quizzes,
            selected_count
        )

        score = 0
        total = len(selected_quizzes)

        print(f"\n총 {total}개의 퀴즈를 시작합니다!")
        print("문제는 무작위 순서로 출제됩니다.")

        # 선택한 개수만큼 문제 출제
        for index, quiz in enumerate(selected_quizzes, start=1):
            print(f"\n===== {index}번 문제 / {total} =====")
            quiz.display()

            answer = self.get_answer()

            if answer is None:
                print("퀴즈 풀이를 종료합니다.")
                return

            if quiz.check_answer(answer):
                print("정답입니다!")
                score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        # 선택한 문제 개수를 기준으로 점수 계산
        percentage = round(score / total * 100, 1)

        print("\n===== 퀴즈 결과 =====")
        print(f"정답 개수: {score}/{total}")
        print(f"최종 점수: {percentage}점")

        # 최고 점수 갱신
        if self.best_score is None or percentage > self.best_score:
            self.best_score = percentage
            print("새로운 최고 점수를 달성했습니다!")
            self.save_state()

    def add_quiz(self):
        # 사용자 퀴즈 추가
        print("\n===== 새로운 퀴즈 추가 =====")

        question = self.get_nonempty_input("문제를 입력하세요: ")

        if question is None:
            return

        choices = []

        for number in range(1, 5):
            choice = self.get_nonempty_input(f"{number}번 선택지: ")

            if choice is None:
                return

            choices.append(choice)

        answer = self.get_answer()

        if answer is None:
            return

        try:
            new_quiz = Quiz(question, choices, answer)
            self.quizzes.append(new_quiz)

            print("\n새로운 퀴즈가 등록되었습니다!")
            print(f"현재 등록된 퀴즈: {len(self.quizzes)}개")

            self.save_state()

        except ValueError as error:
            print(f"퀴즈 등록 실패: {error}")

    def show_quiz_list(self):
        # 전체 퀴즈 목록 출력
        print("\n===== 전체 퀴즈 목록 =====")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"총 {len(self.quizzes)}개의 퀴즈가 등록되어 있습니다.")

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n----- {index}번 퀴즈 -----")
            quiz.display()
            print(f"정답: {quiz.answer}번")

        print("\n===== 목록 출력 완료 =====")

    def show_best_score(self):
        # 최고 점수 출력
        print("\n===== 최고 점수 =====")

        if self.best_score is None:
            print("아직 퀴즈를 완료한 기록이 없습니다.")
        else:
            print(f"현재 최고 점수: {self.best_score}점")

    def save_state(self):
        # 기본 퀴즈를 제외하고 추가 퀴즈만 저장
        default_count = len(get_default_quizzes())
        custom_quizzes = self.quizzes[default_count:]

        data = {
            "custom_quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer
                }
                for quiz in custom_quizzes
            ],
            "best_score": self.best_score
        }

        try:
            with open(STATE_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print("게임 데이터가 저장되었습니다.")

        except OSError as error:
            print(f"데이터 저장 실패: {error}")

    def load_state(self):
        # JSON 데이터 불러오기
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

        except FileNotFoundError:
            return

        except (json.JSONDecodeError, UnicodeError) as error:
            print(f"저장 파일이 손상되어 기본 데이터로 시작합니다: {error}")
            return

        except OSError as error:
            print(f"데이터 불러오기 실패: {error}")
            return

        # 저장 데이터 유효성 검사
        try:
            if not isinstance(data, dict):
                raise ValueError("JSON 최상위 데이터는 객체여야 합니다.")

            custom_data = data.get("custom_quizzes", [])

            if not isinstance(custom_data, list):
                raise ValueError("퀴즈 목록 형식이 올바르지 않습니다.")

            loaded_quizzes = []

            for item in custom_data:
                if not isinstance(item, dict):
                    raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.")

                loaded_quizzes.append(
                    Quiz(
                        item["question"],
                        item["choices"],
                        item["answer"]
                    )
                )

            best_score = data.get("best_score")

            if best_score is not None:
                if (
                    type(best_score) not in (int, float)
                    or not 0 <= best_score <= 100
                ):
                    raise ValueError("최고 점수 값이 올바르지 않습니다.")

            self.quizzes.extend(loaded_quizzes)
            self.best_score = best_score

            print("저장된 게임 데이터를 불러왔습니다.")

        except (ValueError, KeyError, TypeError) as error:
            print(f"저장 데이터가 올바르지 않아 기본 데이터로 시작합니다: {error}")

    def run(self):
        # 메인 실행 반복문
        while True:
            self.show_menu()
            choice = self.get_menu_choice()

            if choice == 1:
                self.play_quiz()

            elif choice == 2:
                self.add_quiz()

            elif choice == 3:
                self.show_quiz_list()

            elif choice == 4:
                self.show_best_score()

            elif choice == 5:
                print("\n게임을 종료합니다.")
                break
