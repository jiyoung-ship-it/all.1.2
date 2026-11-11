
# 퀴즈 문제 하나를 관리하는 클래스


class Quiz:
    def __init__(self, question, choices, answer):
        # 문제와 정답 데이터 검증
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있을 수 없습니다.")

        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 반드시 4개여야 합니다.")

        if any(not isinstance(choice, str) or not choice.strip()
               for choice in choices):
            raise ValueError("선택지는 비어 있을 수 없습니다.")

        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답 번호는 1~4여야 합니다.")

        # 퀴즈 정보 저장
        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer

    def display(self):
        """문제와 선택지 출력"""
        print(f"\n문제: {self.question}")

        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def check_answer(self, user_answer):
        """사용자가 입력한 정답 확인"""
        return user_answer == self.answer
