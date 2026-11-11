
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

        # 저장된 데이터 불러오기
        self.load_state()

    def show_menu(self):
        # 메인 메뉴 출력
        print("\n===== 나만의 퀴즈 게임 =====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가하기")
        print("3. 퀴즈 목록 보기")
        print("4. 최고 점수 확인")
        print("5. 퀴즈 삭제하기")
        print("6. 종료")
        print("==========================")

    def get_menu_choice(self):
        # 메뉴 번호 입력 검증
        while True:
            try:
                value = input(
                    "메뉴 번호를 선택하세요 (1~6): "
                ).strip()

                if not value:
                    print("입력값이 비어 있습니다.")
                    continue

                if not value.isdigit():
                    print("숫자만 입력할 수 있습니다.")
                    continue

                number = int(value)

                if 1 <= number <= 6:
                    return number

                print("1~6 사이의 숫자를 입력하세요.")

            except (KeyboardInterrupt, EOFError):
                print("\n입력이 종료되었습니다.")
                return 6

    def get_answer(self):
        # 퀴즈 추가 시 정답 번호 입력
        while True:
            try:
                value = input("정답 번호 (1~4): ").strip()

                if not value.isdigit():
                    print("1~4 사이의 숫자를 입력하세요.")
                    continue

                number = int(value)

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

    def get_answer_with_hint(self, quiz):
        # 문제 풀이 중 힌트 제공
        hint_used = False

        while True:
            try:
                value = input(
                    "정답 번호 (1~4, 힌트 h): "
                ).strip().lower()

                if value == "h":
                    # 문제당 힌트 한 번만 허용
                    if hint_used:
                        print(
                            "이 문제에서는 이미 힌트를 사용했습니다."
                        )
                        continue

                    hint_used = True

                    # 오답 3개 중 2개를 무작위로 제거
                    wrong_choices = [
                        number
                        for number in range(1, 5)
                        if number != quiz.answer
                    ]

                    removed_choices = random.sample(
                        wrong_choices, 2
                    )

                    remaining_choices = [
                        number
                        for number in range(1, 5)
                        if number not in removed_choices
                    ]

                    print(
                        "\n[힌트] 정답이 아닌 선택지 "
                        "2개를 제외합니다."
                    )

                    print(
                        "남은 선택지: "
                        + ", ".join(
                            f"{number}번"
                            for number in remaining_choices
                        )
                    )

                    print(
                        "힌트를 사용했으므로 이 문제는 "
                        "정답을 맞혀도 50점만 인정됩니다."
                    )
                    continue

                if not value.isdigit():
                    print(
                        "1~4 사이의 숫자 또는 h를 입력하세요."
                    )
                    continue

                answer = int(value)

                if not 1 <= answer <= 4:
                    print("1~4 사이의 숫자를 입력하세요.")
                    continue

                return answer, hint_used

            except (KeyboardInterrupt, EOFError):
                print("\n퀴즈 풀이가 중단되었습니다.")
                return None, hint_used

    def play_quiz(self):
        # 등록된 퀴즈가 없는 경우 실행 중단
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        # 문제 개수 선택
        selected_count = self.get_quiz_count()

        if selected_count is None:
            return

        # 중복 없이 무작위로 문제 선택
        selected_quizzes = random.sample(
            self.quizzes, selected_count
        )

        total = len(selected_quizzes)
        correct_count = 0
        total_points = 0

        print(f"\n총 {total}개의 퀴즈를 시작합니다!")
        print("문제는 무작위 순서로 출제됩니다.")
        print("힌트가 필요하면 h를 입력하세요.")

        for index, quiz in enumerate(
            selected_quizzes, start=1
        ):
            print(f"\n===== {index}번 문제 / {total} =====")
            quiz.display()

            answer, hint_used = self.get_answer_with_hint(quiz)

            if answer is None:
                print("퀴즈 풀이를 종료합니다.")
                return

            if quiz.check_answer(answer):
                correct_count += 1

                # 힌트 사용 시 50점, 미사용 시 100점
                points = 50 if hint_used else 100
                total_points += points

                print(f"정답입니다! (+{points}점)")

            else:
                print(
                    f"오답입니다. 정답은 {quiz.answer}번입니다."
                )

        # 최종 점수 계산
        percentage = round(total_points / total, 1)

        print("\n===== 퀴즈 결과 =====")
        print(f"정답 개수: {correct_count}/{total}")
        print(f"획득 점수 합계: {total_points}점")
        print(f"최종 점수: {percentage}점")

        # 최고 점수 갱신
        if (
            self.best_score is None
            or percentage > self.best_score
        ):
            self.best_score = percentage
            print("새로운 최고 점수를 달성했습니다!")
            self.save_state()

    def add_quiz(self):
        # 새로운 퀴즈 추가
        print("\n===== 새로운 퀴즈 추가 =====")

        question = self.get_nonempty_input(
            "문제를 입력하세요: "
        )

        if question is None:
            return

        choices = []

        for number in range(1, 5):
            choice = self.get_nonempty_input(
                f"{number}번 선택지: "
            )

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
            print(
                f"현재 등록된 퀴즈: {len(self.quizzes)}개"
            )

            # 변경된 전체 퀴즈 목록 저장
            self.save_state()

        except ValueError as error:
            print(f"퀴즈 등록 실패: {error}")

    def show_quiz_list(self):
        # 전체 퀴즈 목록 출력
        print("\n===== 전체 퀴즈 목록 =====")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(
            f"총 {len(self.quizzes)}개의 "
            "퀴즈가 등록되어 있습니다."
        )

        for index, quiz in enumerate(
            self.quizzes, start=1
        ):
            print(f"\n----- {index}번 퀴즈 -----")
            quiz.display()
            print(f"정답: {quiz.answer}번")

        print("\n===== 목록 출력 완료 =====")

    def delete_quiz(self):
        # 퀴즈 삭제 기능
        print("\n===== 퀴즈 삭제 =====")

        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        # 삭제 가능한 퀴즈 목록 출력
        for index, quiz in enumerate(
            self.quizzes, start=1
        ):
            print(f"{index}. {quiz.question}")

        total = len(self.quizzes)

        # 삭제할 퀴즈 번호 입력
        while True:
            try:
                value = input(
                    "\n삭제할 퀴즈 번호 (0: 취소): "
                ).strip()

                if not value.isdigit():
                    print("숫자만 입력할 수 있습니다.")
                    continue

                number = int(value)

                if number == 0:
                    print("퀴즈 삭제를 취소했습니다.")
                    return

                if 1 <= number <= total:
                    break

                print(
                    f"1~{total} 사이의 번호를 입력하세요."
                )

            except (KeyboardInterrupt, EOFError):
                print("\n퀴즈 삭제가 취소되었습니다.")
                return

        # 삭제 전 확인
        while True:
            try:
                confirm = input(
                    "정말 삭제하시겠습니까? (y/n): "
                ).strip().lower()

                if confirm == "y":
                    # 선택한 퀴즈 삭제
                    deleted_quiz = self.quizzes.pop(
                        number - 1
                    )

                    print(
                        f"\n삭제된 퀴즈: "
                        f"{deleted_quiz.question}"
                    )
                    print("퀴즈가 삭제되었습니다.")

                    # 삭제 후 전체 퀴즈 목록 저장
                    self.save_state()
                    return

                if confirm == "n":
                    print("퀴즈 삭제를 취소했습니다.")
                    return

                print("y 또는 n을 입력하세요.")

            except (KeyboardInterrupt, EOFError):
                print("\n퀴즈 삭제가 취소되었습니다.")
                return

    def show_best_score(self):
        # 최고 점수 출력
        print("\n===== 최고 점수 =====")

        if self.best_score is None:
            print(
                "아직 퀴즈를 완료한 기록이 없습니다."
            )
        else:
            print(
                f"현재 최고 점수: "
                f"{self.best_score}점"
            )

    def save_state(self):
        # 전체 퀴즈 목록과 최고 점수 저장
        # 기본 퀴즈 삭제 내역까지 보존하기 위해
        # 기존 custom_quizzes 방식 대신 quizzes 사용
        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer
                }
                for quiz in self.quizzes
            ],
            "best_score": self.best_score
        }

        try:
            with open(
                STATE_FILE, "w", encoding="utf-8"
            ) as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            print("게임 데이터가 저장되었습니다.")

        except OSError as error:
            print(f"데이터 저장 실패: {error}")

    def load_state(self):
        # JSON 데이터 불러오기
        try:
            with open(
                STATE_FILE, "r", encoding="utf-8"
            ) as file:
                data = json.load(file)

        except FileNotFoundError:
            return

        except (
            json.JSONDecodeError,
            UnicodeError
        ) as error:
            print(
                "저장 파일이 손상되어 "
                f"기본 데이터로 시작합니다: {error}"
            )
            return

        except OSError as error:
            print(f"데이터 불러오기 실패: {error}")
            return

        try:
            if not isinstance(data, dict):
                raise ValueError(
                    "JSON 최상위 데이터는 객체여야 합니다."
                )

            # 새로운 저장 형식: 전체 퀴즈 목록
            if "quizzes" in data:
                quiz_data = data["quizzes"]

                if not isinstance(quiz_data, list):
                    raise ValueError(
                        "퀴즈 목록 형식이 올바르지 않습니다."
                    )

                loaded_quizzes = []

                for item in quiz_data:
                    if not isinstance(item, dict):
                        raise ValueError(
                            "퀴즈 데이터 형식이 올바르지 않습니다."
                        )

                    loaded_quizzes.append(
                        Quiz(
                            item["question"],
                            item["choices"],
                            item["answer"]
                        )
                    )

            # 기존 저장 형식: 추가 퀴즈 목록
            else:
                custom_data = data.get(
                    "custom_quizzes", []
                )

                if not isinstance(custom_data, list):
                    raise ValueError(
                        "퀴즈 목록 형식이 올바르지 않습니다."
                    )

                loaded_quizzes = get_default_quizzes()

                for item in custom_data:
                    if not isinstance(item, dict):
                        raise ValueError(
                            "퀴즈 데이터 형식이 올바르지 않습니다."
                        )

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
                    raise ValueError(
                        "최고 점수 값이 올바르지 않습니다."
                    )

            # 유효한 데이터를 확인한 뒤 반영
            self.quizzes = loaded_quizzes
            self.best_score = best_score

            print("저장된 게임 데이터를 불러왔습니다.")

        except (
            ValueError,
            KeyError,
            TypeError
        ) as error:
            print(
                "저장 데이터가 올바르지 않아 "
                f"기본 데이터로 시작합니다: {error}"
            )

    def run(self):
        # 게임 메인 반복문
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
                self.delete_quiz()

            elif choice == 6:
                print("\n게임을 종료합니다.")
                break
