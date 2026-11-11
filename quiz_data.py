
# Python 프로그래밍 기초 퀴즈 데이터

from quiz import Quiz


def get_default_quizzes():
    """기본 퀴즈 5개 생성"""

    return [
        Quiz(
            "Python에서 화면에 문자를 출력하는 함수는?",
            ["input()", "print()", "return", "len()"],
            2
        ),
        Quiz(
            "Python에서 정수를 나타내는 자료형은?",
            ["str", "float", "int", "bool"],
            3
        ),
        Quiz(
            "Python에서 조건문을 시작할 때 사용하는 키워드는?",
            ["for", "while", "if", "def"],
            3
        ),
        Quiz(
            "Python에서 함수를 정의할 때 사용하는 키워드는?",
            ["class", "def", "import", "return"],
            2
        ),
        Quiz(
            "Python에서 여러 값을 순서대로 저장하는 자료형은?",
            ["dict", "bool", "int", "list"],
            4
        )
    ]
