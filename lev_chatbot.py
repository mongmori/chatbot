import pandas as pd

# 이전에 작성한 레벤슈타인 거리 계산 함수
def calc_distance(a, b):
    if a == b:
        return 0  # 두 문자열이 같으면 편집 거리는 0
    a_len = len(a)
    b_len = len(b)
    if a == "":
        return b_len  # a가 빈 문자열이면 b_len 만큼 삽입 필요
    if b == "":
        return a_len  # b가 빈 문자열이면 a_len 만큼 삭제 필요

    # (a_len+1) x (b_len+1) 크기의 2차원 행렬 생성 및 초기화
    matrix = [[0 for _ in range(b_len + 1)] for _ in range(a_len + 1)]
    # 첫 번째 행과 첫 번째 열에 초기값 설정
    for i in range(a_len + 1):
        matrix[i][0] = i
    for j in range(b_len + 1):
        matrix[0][j] = j

    # 동적 계획법으로 편집 거리 계산
    for i in range(1, a_len + 1):
        ac = a[i - 1]
        for j in range(1, b_len + 1):
            bc = b[j - 1]
            cost = 0 if ac == bc else 1  # 문자가 같으면 비용 0, 다르면 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,      # 삭제
                matrix[i][j - 1] + 1,      # 삽입
                matrix[i - 1][j - 1] + cost  # 대체 또는 일치
            )
    return matrix[a_len][b_len]

class LevenshteinChatBot:
    def __init__(self, filepath):
        # CSV 파일에서 질문(Q)과 답변(A) 데이터를 로드
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문 열을 리스트로 변환
        answers   = data['A'].tolist()  # 답변 열을 리스트로 변환
        return questions, answers

    def find_best_answer(self, input_sentence):
        # 입력 문장과 모든 질문 간의 레벤슈타인 거리를 계산
        distances = [calc_distance(input_sentence, q) for q in self.questions]
        # 거리가 가장 작은 질문의 인덱스를 찾음
        best_match_index = distances.index(min(distances))
        # 해당 질문의 답변을 반환
        return self.answers[best_match_index]

# CSV 파일 경로 지정
filepath = 'ChatbotData.csv'

# 챗봇 인스턴스를 생성
chatbot = LevenshteinChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복
while True:
    user_input = input("You: ")
    if user_input.lower() == '종료':
        break
    response = chatbot.find_best_answer(user_input)
    print("Chatbot:", response)