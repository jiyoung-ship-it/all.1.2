
# 퀴즈 문제 하나를 관리하는 클래스


class Quiz:
    def __init__(self, question, choices, answer, hint=None):
        # 문제와 정답 데이터 검증
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있을 수 없습니다.")

        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 반드시 4개여야 합니다.")

        if any(
            not isinstance(choice, str) or not choice.strip()
            for choice in choices
        ):
            raise ValueError("선택지는 비어 있을 수 없습니다.")

        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답 번호는 1~4여야 합니다.")

        # 힌트가 주어진 경우 문자열인지 확인
        if hint is not None:
            if not isinstance(hint, str) or not hint.strip():
                raise ValueError("힌트는 비어 있지 않은 문자열이어야 합니다.")

        # 퀴즈 정보 저장
        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer

        # 힌트 속성 추가
        # 별도 힌트가 없으면 정답이 아닌 선택지 제거 방식을 사용
        self.hint = hint.strip() if hint is not None else None

    def display(self):
        """문제와 선택지 출력"""
        print(f"\n문제: {self.question}")

        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def check_answer(self, user_answer):
        """사용자가 입력한 정답 확인"""
        return user_answer == self.answer

    def get_hint(self):
        """퀴즈에 등록된 힌트 반환"""
        return self.hint
