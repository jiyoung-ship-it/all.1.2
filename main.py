
# 코디세이 2주차 Python 퀴즈 게임


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
    """메뉴 입력값 검사 및 예외 처리"""
    while True:
        try:
            choice = input("메뉴 번호를 선택하세요 (1~5): ").strip()

            if not choice:
                print("입력값이 비어 있습니다. 다시 입력하세요.")
                continue

            if not choice.isdigit():
                print("숫자만 입력할 수 있습니다.")
                continue

            number = int(choice)

            if number < 1 or number > 5:
                print("1~5 사이의 숫자를 입력하세요.")
                continue

            return number

        except (KeyboardInterrupt, EOFError):
            print("\n입력이 종료되어 게임을 종료합니다.")
            return 5


def main():
    """프로그램 실행"""
    while True:
        show_menu()
        choice = get_menu_choice()

        if choice == 1:
            print("\n[퀴즈 풀기] 기능 준비 중입니다.")

        elif choice == 2:
            print("\n[퀴즈 추가하기] 기능 준비 중입니다.")

        elif choice == 3:
            print("\n[퀴즈 목록 보기] 기능 준비 중입니다.")

        elif choice == 4:
            print("\n[최고 점수 확인] 기능 준비 중입니다.")

        elif choice == 5:
            print("\n게임을 종료합니다.")
            break


if __name__ == "__main__":
    main()
