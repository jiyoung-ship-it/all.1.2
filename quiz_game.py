
import json
import random
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

from quiz import Quiz
from quiz_data import get_default_quizzes


# 프로젝트 루트에 저장되는 JSON 파일
STATE_FILE = Path(__file__).resolve().parent / "state.json"
BACKUP_FILE = STATE_FILE.with_name("state.json.bak")


class QuizGame:
    def __init__(self):
        # 기본 퀴즈와 최고 점수, 풀이 기록 초기화
        self.quizzes = get_default_quizzes()
        self.best_score = None
        self.history = []
        self.storage_safe = True  # 손상된 파일을 덮어쓰지 않도록 보호

        # 기존 저장 데이터 불러오기
        self.load_state()

    def show_menu(self):
        # 게임의 메인 메뉴 출력
        print("\n===== 나만의 퀴즈 게임 =====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가하기")
        print("3. 퀴즈 목록 보기")
        print("4. 최고 점수 확인")
        print("5. 퀴즈 삭제하기")
        print("6. 풀이 기록 보기")
        print("7. 종료")
        print("==========================")

    def get_menu_choice(self):
        # 메뉴 번호 입력 및 예외 처리
        while True:
            try:
                value = input("메뉴 번호를 선택하세요 (1~7): ").strip()

                if not value:
                    print("입력값이 비어 있습니다.")
                    continue

                if not value.isdigit():
                    print("숫자만 입력할 수 있습니다.")
                    continue

                number = int(value)

                if 1 <= number <= 7:
                    return number

                print("1~7 사이의 숫자를 입력하세요.")

            except (KeyboardInterrupt, EOFError):
                print("\n입력이 종료되었습니다.")
                return 7

    def get_answer(self):
        # 퀴즈 등록 시 정답 번호 입력
        while True:
            try:
                value = input("정답 번호 (1~4): ").strip()

                if not value:
                    print("정답 번호를 입력하세요.")
                    continue

                if not value.isdigit():
                    print("숫자만 입력할 수 있습니다.")
                    continue

                number = int(value)

                if 1 <= number <= 4:
                    return number

                print("1~4 사이의 숫자를 입력하세요.")

            except (KeyboardInterrupt, EOFError):
                print("\n입력이 중단되었습니다.")
                return None

    def get_nonempty_input(self, prompt):
        # 빈 입력 방지
        while True:
            try:
                value = input(prompt).strip()

                if value:
                    return value

                print("빈 내용은 입력할 수 없습니다.")

            except (KeyboardInterrupt, EOFError):
                print("\n입력이 취소되었습니다.")
                return None

    def get_optional_hint(self):
        # 퀴즈 추가 시 힌트는 선택적으로 입력
        try:
            hint = input(
                "힌트를 입력하세요 (생략하려면 Enter): "
            ).strip()

            return hint if hint else None

        except (KeyboardInterrupt, EOFError):
            print("\n힌트 입력이 취소되었습니다.")
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
        # 문제 풀이 중 힌트 사용 여부 관리
        hint_used = False

        while True:
            try:
                value = input(
                    "정답 번호 (1~4, 힌트 h): "
                ).strip().lower()

                if value == "h":
                    if hint_used:
                        print("이미 힌트를 사용했습니다.")
                        continue

                    hint_used = True

                    # Quiz 클래스에 등록된 힌트 확인
                    registered_hint = quiz.get_hint()

                    if registered_hint:
                        # 직접 작성한 힌트 출력
                        print(f"\n[힌트] {registered_hint}")

                    else:
                        # 등록된 힌트가 없으면 오답 2개 제거
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
                            "\n[힌트] 오답 선택지 2개를 제외합니다."
                        )
                        print(
                            "남은 선택지: "
                            + ", ".join(
                                f"{number}번"
                                for number in remaining_choices
                            )
                        )

                    print(
                        "힌트 사용 시 정답 점수는 50점입니다."
                    )
                    continue

                if not value:
                    print("정답 번호 또는 h를 입력하세요.")
                    continue

                if not value.isdigit():
                    print("1~4 사이의 숫자 또는 h를 입력하세요.")
                    continue

                answer = int(value)

                if 1 <= answer <= 4:
                    return answer, hint_used

                print("1~4 사이의 숫자를 입력하세요.")

            except (KeyboardInterrupt, EOFError):
                print("\n퀴즈 풀이가 중단되었습니다.")
                return None, hint_used

    def play_quiz(self):
        # 등록된 퀴즈가 없는 경우
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        selected_count = self.get_quiz_count()

        if selected_count is None:
            return

        # 문제 순서를 무작위로 선택
        selected_quizzes = random.sample(
            self.quizzes, selected_count
        )

        total = len(selected_quizzes)
        correct_count = 0
        total_points = 0
        hint_count = 0

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

            if hint_used:
                hint_count += 1

            if quiz.check_answer(answer):
                correct_count += 1

                points = 50 if hint_used else 100
                total_points += points

                print(f"정답입니다! (+{points}점)")

            else:
                print(
                    f"오답입니다. 정답은 {quiz.answer}번입니다."
                )

        # 선택한 문제 개수를 기준으로 점수 계산
        percentage = round(total_points / total, 1)

        print("\n===== 퀴즈 결과 =====")
        print(f"정답 개수: {correct_count}/{total}")
        print(f"획득 점수 합계: {total_points}점")
        print(f"힌트 사용 횟수: {hint_count}회")
        print(f"최종 점수: {percentage}점")

        # 최고 점수 갱신
        if (
            self.best_score is None
            or percentage > self.best_score
        ):
            self.best_score = percentage
            print("새로운 최고 점수를 달성했습니다!")

        # 날짜와 시간을 포함한 풀이 기록 생성
        record = {
            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "total": total,
            "correct": correct_count,
            "hints_used": hint_count,
            "score": percentage
        }

        self.history.append(record)
        self.save_state()

        print("이번 퀴즈 풀이 기록이 저장되었습니다.")

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

        # Quiz 클래스의 hint 속성에 저장할 내용
        hint = self.get_optional_hint()

        try:
            new_quiz = Quiz(
                question, choices, answer, hint
            )

            self.quizzes.append(new_quiz)

            print("\n새로운 퀴즈가 등록되었습니다!")
            print(
                f"현재 등록된 퀴즈: {len(self.quizzes)}개"
            )

            self.save_state()

        except ValueError as error:
            print(f"퀴즈 등록 실패: {error}")

    def show_quiz_list(self):
        # 등록된 퀴즈 목록 확인
        print("\n===== 전체 퀴즈 목록 =====")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(
            f"총 {len(self.quizzes)}개의 퀴즈가 등록되어 있습니다."
        )

        for index, quiz in enumerate(
            self.quizzes, start=1
        ):
            print(f"\n----- {index}번 퀴즈 -----")
            quiz.display()
            print(f"정답: {quiz.answer}번")

            if quiz.get_hint():
                print(f"등록된 힌트: {quiz.get_hint()}")

        print("\n===== 목록 출력 완료 =====")

    def delete_quiz(self):
        # 퀴즈 삭제
        print("\n===== 퀴즈 삭제 =====")

        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        for index, quiz in enumerate(
            self.quizzes, start=1
        ):
            print(f"{index}. {quiz.question}")

        total = len(self.quizzes)

        while True:
            try:
                value = input(
                    "\n삭제할 퀴즈 번호 (0: 취소): "
                ).strip()

                if not value:
                    print("삭제할 퀴즈 번호를 입력하세요.")
                    continue

                if not value.isdigit():
                    print("숫자만 입력할 수 있습니다.")
                    continue

                number = int(value)

                if number == 0:
                    print("퀴즈 삭제를 취소했습니다.")
                    return

                if 1 <= number <= total:
                    break

                print(f"1~{total} 사이의 번호를 입력하세요.")

            except (KeyboardInterrupt, EOFError):
                print("\n퀴즈 삭제가 취소되었습니다.")
                return

        while True:
            try:
                confirm = input(
                    "정말 삭제하시겠습니까? (y/n): "
                ).strip().lower()

                if confirm == "y":
                    deleted_quiz = self.quizzes.pop(
                        number - 1
                    )

                    print(
                        f"\n삭제된 퀴즈: {deleted_quiz.question}"
                    )
                    print("퀴즈가 삭제되었습니다.")

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
            print("아직 퀴즈를 완료한 기록이 없습니다.")
        else:
            print(f"현재 최고 점수: {self.best_score}점")

    def show_history(self):
        # 전체 퀴즈 풀이 기록 출력
        print("\n===== 퀴즈 풀이 기록 =====")

        if not self.history:
            print("아직 저장된 풀이 기록이 없습니다.")
            return

        for index, record in enumerate(
            self.history, start=1
        ):
            print(f"\n{index}회차 | {record['date']}")
            print(f"문제 수: {record['total']}개")
            print(
                f"정답: {record['correct']}/{record['total']}"
            )
            print(
                f"힌트 사용: {record['hints_used']}회"
            )
            print(f"최종 점수: {record['score']}점")

        print("\n===== 기록 출력 완료 =====")

    def _validate_state(self, data):
        # 원본과 백업 모두 같은 검증을 거친다.
        if not isinstance(data, dict):
            raise ValueError(
                "JSON 최상위 데이터는 객체여야 합니다."
            )

        # 최신 JSON 형식
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
                        item["answer"],
                        item.get("hint")
                    )
                )

        # 이전 버전의 JSON 형식도 지원
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
                        item["answer"],
                        item.get("hint")
                    )
                )

        # 최고 점수 검증
        best_score = data.get("best_score")

        if best_score is not None:
            if (
                type(best_score) not in (int, float)
                or not 0 <= best_score <= 100
            ):
                raise ValueError(
                    "최고 점수 값이 올바르지 않습니다."
                )

        # 풀이 기록 검증
        history = data.get("history", [])

        if not isinstance(history, list):
            raise ValueError(
                "풀이 기록 형식이 올바르지 않습니다."
            )

        for record in history:
            if not isinstance(record, dict):
                raise ValueError(
                    "풀이 기록 데이터가 올바르지 않습니다."
                )

            required_keys = (
                "date",
                "total",
                "correct",
                "hints_used",
                "score"
            )

            if not all(
                key in record
                for key in required_keys
            ):
                raise ValueError(
                    "풀이 기록에 필요한 정보가 없습니다."
                )

            if (
                not isinstance(record["date"], str)
                or type(record["total"]) is not int
                or record["total"] < 1
                or type(record["correct"]) is not int
                or not 0 <= record["correct"] <= record["total"]
                or type(record["hints_used"]) is not int
                or not 0 <= record["hints_used"] <= record["total"]
                or type(record["score"]) not in (int, float)
                or not 0 <= record["score"] <= 100
            ):
                raise ValueError(
                    "풀이 기록 값이 올바르지 않습니다."
                )
        return loaded_quizzes, best_score, history

    def _read_valid_state(self, path):
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return self._validate_state(data)

    def _atomic_write(self, destination, data):
        # 같은 폴더에 임시 파일을 쓰고 성공한 경우에만 교체한다.
        temp_name = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=destination.parent,
                prefix=".quiz_", suffix=".tmp", delete=False
            ) as file:
                temp_name = file.name
                json.dump(data, file, ensure_ascii=False, indent=4)
                file.flush()
                os.fsync(file.fileno())
            os.replace(temp_name, destination)
        finally:
            if temp_name is not None and os.path.exists(temp_name):
                os.unlink(temp_name)

    def save_state(self):
        # 손상된 원본을 기본 데이터로 덮어쓰지 않는다.
        if not self.storage_safe:
            print("저장 중단: 기존 데이터 손상 또는 읽기 오류가 해결되지 않았습니다.")
            return False

        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer,
                    "hint": quiz.get_hint()
                }
                for quiz in self.quizzes
            ],
            "best_score": self.best_score,
            "history": self.history
        }

        try:
            # 기존 원본이 유효할 때만 백업한다.
            if STATE_FILE.exists():
                self._read_valid_state(STATE_FILE)
                # 기존 백업을 덮기 전에 원본을 임시 파일에 복사한다.
                backup_temp = BACKUP_FILE.with_name(BACKUP_FILE.name + ".tmp")
                try:
                    shutil.copy2(STATE_FILE, backup_temp)
                    os.replace(backup_temp, BACKUP_FILE)
                finally:
                    if backup_temp.exists():
                        backup_temp.unlink()

            self._atomic_write(STATE_FILE, data)
            # 첫 저장이라면 복구 가능한 백업도 만든다.
            if not BACKUP_FILE.exists():
                shutil.copy2(STATE_FILE, BACKUP_FILE)
            print("게임 데이터가 저장되었습니다.")
            return True

        except (OSError, UnicodeError, ValueError, KeyError,
                TypeError, json.JSONDecodeError) as error:
            print(f"데이터 저장 실패: {error}")
            print("기존 저장 파일과 백업을 확인한 후 다시 시도하세요.")
            return False

    def load_state(self):
        # 원본이 없거나 손상되면 백업에서 복구한다.
        try:
            if STATE_FILE.exists():
                loaded = self._read_valid_state(STATE_FILE)
                print("저장된 게임 데이터를 불러왔습니다.")
            elif BACKUP_FILE.exists():
                print("원본 파일이 없어 백업 복원을 시도합니다.")
                loaded = self._read_valid_state(BACKUP_FILE)
                shutil.copy2(BACKUP_FILE, STATE_FILE)
                print("백업에서 게임 데이터를 복원했습니다.")
            else:
                return

        except (OSError, UnicodeError, ValueError, KeyError,
                TypeError, json.JSONDecodeError) as error:
            print(f"원본 데이터를 읽을 수 없습니다: {error}")
            try:
                loaded = self._read_valid_state(BACKUP_FILE)
                # 손상된 원본은 보존하고 복원본을 원본에 기록한다.
                if STATE_FILE.exists():
                    damaged = STATE_FILE.with_name("state.json.damaged")
                    if damaged.exists():
                        print("기존 손상 파일 보관본이 있어 자동 복원을 중단합니다.")
                        self.storage_safe = False
                        return
                    os.replace(STATE_FILE, damaged)
                shutil.copy2(BACKUP_FILE, STATE_FILE)
                print("백업에서 게임 데이터를 복원했습니다.")
            except (OSError, UnicodeError, ValueError, KeyError,
                    TypeError, json.JSONDecodeError) as backup_error:
                print(f"백업 복원 실패: {backup_error}")
                print("데이터 보호를 위해 자동 저장을 중단합니다.")
                self.storage_safe = False
                return

        self.quizzes, self.best_score, self.history = loaded

    def run(self):
        # 게임 전체 실행
        try:
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
                    self.show_history()

                elif choice == 7:
                    break

        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 안전하게 종료합니다.")

        finally:
            # 정상 종료와 예외 종료 모두 저장 시도
            self.save_state()
            print("\n게임을 종료합니다.")
