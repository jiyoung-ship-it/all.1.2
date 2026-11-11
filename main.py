
# 코디세이 2주차 Python 퀴즈 게임

from quiz import Quiz
from quiz_data import get_default_quizzes


def show_menu():
    """메인 메뉴 출력"""
    print("\n===== 나만의 퀴즈 게임 =====")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가하기")
    print("3. 퀴즈 목록 보기")
    print("4. 최고 점수 확인")
    print("5. 종료")
    print("==========================")


def get_menu_choice():
    """메뉴 번호 입력 및 검증"""
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

            if not 1 <= number <= 5:
                print("1~5 사이의 숫자를 입력하세요.")
                continue

            return number

        except (KeyboardInterrupt, EOFError):
            print("\n입력이 종료되었습니다.")
            return 5


def get_answer():
    """퀴즈 정답 번호 입력 및 검증"""
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
            print("\n퀴즈 풀이가 중단되었습니다.")
            return None


def play_quiz(quizzes):
    """퀴즈 진행 및 점수 계산"""
    if not quizzes:
        print("\n등록된 퀴즈가 없습니다.")
        return

    score = 0
    total = len(quizzes)

    print(f"\n총 {total}개의 퀴즈를 시작합니다!")

    for index, quiz in enumerate(quizzes, start=1):
        print(f"\n===== {index}번 문제 / {total} =====")
        quiz.display()

        answer = get_answer()

        if answer is None:
            return

        if quiz.check_answer(answer):
            print("정답입니다!")
            score += 1
        else:
            print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

    percentage = round(score / total * 100, 1)

    print("\n===== 퀴즈 결과 =====")
    print(f"정답 개수: {score}/{total}")
    print(f"최종 점수: {percentage}점")


def get_nonempty_input(prompt):
    """빈 문자열을 허용하지 않는 입력 함수"""
    while True:
        try:
            value = input(prompt).strip()

            if value:
                return value

            print("빈 내용은 입력할 수 없습니다.")

        except (KeyboardInterrupt, EOFError):
            print("\n퀴즈 추가를 취소합니다.")
            return None


def add_quiz(quizzes):
    """새로운 퀴즈 추가"""
    print("\n===== 새로운 퀴즈 추가 =====")

    question = get_nonempty_input("문제를 입력하세요: ")

    if question is None:
        return

    choices = []

    for number in range(1, 5):
        choice = get_nonempty_input(f"{number}번 선택지: ")

        if choice is None:
            return

        choices.append(choice)

    answer = get_answer()

    if answer is None:
        return

    try:
        new_quiz = Quiz(question, choices, answer)
        quizzes.append(new_quiz)

        print("\n새로운 퀴즈가 등록되었습니다!")
        print(f"현재 등록된 퀴즈: {len(quizzes)}개")

    except ValueError as error:
        print(f"퀴즈 등록 실패: {error}")


def main():
    """게임 실행"""
    quizzes = get_default_quizzes()

    while True:
        show_menu()
        choice = get_menu_choice()

        if choice == 1:
            play_quiz(quizzes)

        elif choice == 2:
            add_quiz(quizzes)

        elif choice == 3:
            print("\n[퀴즈 목록 보기] 기능 준비 중입니다.")

        elif choice == 4:
            print("\n[최고 점수 확인] 기능 준비 중입니다.")

        elif choice == 5:
            print("\n게임을 종료합니다.")
            break


if __name__ == "__main__":
    main()
