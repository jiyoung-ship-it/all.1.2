
# 코디세이 2주차 Python 퀴즈 게임
# QuizGame 클래스: 게임 전체 기능 관리

from quiz import Quiz
from quiz_data import get_default_quizzes


class QuizGame:
    def __init__(self):
        """게임 데이터 초기화"""
        self.quizzes = get_default_quizzes()
        self.best_score = None

    def show_menu(self):
        """메인 메뉴 출력"""
        print("\n===== 나만의 퀴즈 게임 =====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가하기")
        print("3. 퀴즈 목록 보기")
        print("4. 최고 점수 확인")
        print("5. 종료")
        print("==========================")

    def get_menu_choice(self):
        """메뉴 번호 입력 및 검증"""
        while True:
            try:
                choice = input(
                    "메뉴 번호를 선택하세요 (1~5): "
                ).strip()

                if not choice:
                    print("입력값이 비어 있습니다.")
                    continue

                if not choice.isdigit():
                    print("숫자만 입력할 수 있습니다.")
                    continue

                number = int(choice)

                if not 1 <= number <= 5:
                    print("1~5 사이의 숫자를 입력하세요.")
                    continue

                return number

            except (KeyboardInterrupt, EOFError):
                print("\n입력이 종료되었습니다.")
                return 5

    def get_answer(self):
        """정답 번호 입력 및 검증"""
        while True:
            try:
                answer = input(
                    "정답 번호 (1~4): "
                ).strip()

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
        """빈 문자열을 허용하지 않는 입력"""
        while True:
            try:
                value = input(prompt).strip()

                if value:
                    return value

                print("빈 내용은 입력할 수 없습니다.")

            except (KeyboardInterrupt, EOFError):
                print("\n입력이 취소되었습니다.")
                return None

    def play_quiz(self):
        """퀴즈 플레이 및 최고 점수 갱신"""
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        score = 0
        total = len(self.quizzes)

        print(f"\n총 {total}개의 퀴즈를 시작합니다!")

        for index, quiz in enumerate(
            self.quizzes, start=1
        ):
            print(
                f"\n===== {index}번 문제 / {total} ====="
            )
            quiz.display()

            answer = self.get_answer()

            if answer is None:
                print("퀴즈 풀이를 종료합니다.")
                return

            if quiz.check_answer(answer):
                print("정답입니다!")
                score += 1
            else:
                print(
                    f"오답입니다. "
                    f"정답은 {quiz.answer}번입니다."
                )

        percentage = round(score / total * 100, 1)

        print("\n===== 퀴즈 결과 =====")
        print(f"정답 개수: {score}/{total}")
        print(f"최종 점수: {percentage}점")

        if (
            self.best_score is None
            or percentage > self.best_score
        ):
            self.best_score = percentage
            print("새로운 최고 점수를 달성했습니다!")

    def add_quiz(self):
        """새로운 퀴즈 추가"""
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
            new_quiz = Quiz(
                question, choices, answer
            )

            self.quizzes.append(new_quiz)

            print("\n새로운 퀴즈가 등록되었습니다!")
            print(
                f"현재 등록된 퀴즈: "
                f"{len(self.quizzes)}개"
            )

        except ValueError as error:
            print(f"퀴즈 등록 실패: {error}")

    def show_quiz_list(self):
        """등록된 퀴즈 목록 출력"""
        print("\n===== 전체 퀴즈 목록 =====")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(
            f"총 {len(self.quizzes)}개의 "
            f"퀴즈가 등록되어 있습니다."
        )

        for index, quiz in enumerate(
            self.quizzes, start=1
        ):
            print(f"\n----- {index}번 퀴즈 -----")
            quiz.display()
            print(f"정답: {quiz.answer}번")

        print("\n===== 목록 출력 완료 =====")

    def show_best_score(self):
        """최고 점수 출력"""
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

    def run(self):
        """메인 게임 반복 실행"""
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
