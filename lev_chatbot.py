import pandas as pd

# 이전에 작성한 레벤슈타인 거리 계산 함수
def calc_distance(a, b):
    if a == b:
        return 0  # 두 문자열이 완전히 동일한 경우, 편집 거리는 0
    a_len = len(a)
    b_len = len(b)
    if a == "":
        # 문자열 a가 비어있는 경우, 문자열 b를 만들기 위해서는 b의 길이만큼 문자를 삽입해야 하므로 편집 거리는 b_len
        return b_len
    if b == "":
        # 문자열 b가 비어있는 경우, 문자열 a를 b로 만들기 위해서는 a의 길이만큼 문자를 삭제해야 하므로 편집 거리는 a_len
        return a_len

    # 동적 프로그래밍 테이블 생성
    matrix = [[0 for _ in range(b_len + 1)] for _ in range(a_len + 1)]

    # 문자열 a의 첫 i개 문자를 빈 문자열로 만드는 데 필요한 삭제 연산의 수(i)
    for i in range(a_len + 1):
        matrix[i][0] = i
    # 빈 문자열에서 문자열 b의 첫 j개 문자를 만드는 데 필요한 삽입 연산의 수(j)
    for j in range(b_len + 1):
        matrix[0][j] = j

    # 동적 프로그래밍으로 편집 거리를 계산
    for i in range(1, a_len + 1):
        ac = a[i - 1]
        for j in range(1, b_len + 1):
            bc = b[j - 1]
            # 현재 비교하는 두 문자(ac와 bc)가 같으면 cost는 0, 다르면 1
            cost = 0 if ac == bc else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,      # 삭제 연산: a의 현재 문자(ac)를 삭제하는 경우의 총 비용
                matrix[i][j - 1] + 1,      # 삽입 연산: b의 현재 문자(bc)를 a에 삽입하는 경우의 총 비용
                matrix[i - 1][j - 1] + cost # 대체 또는 일치 연산: a의 현재 문자를 b의 현재 문자로 대체하거나 문자들이 일치하는 경우의 총 비용
            )
    return matrix[a_len][b_len] # 최종적으로 계산된 문자열 a와 b 사이의 레벤슈타인 거리


class LevenshteinChatBot:
    def __init__(self, filepath):
        # 지정된 CSV 파일 경로에서 Q, A 데이터를 로드
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # Q 열의 데이터를 추출하여 질문 리스트를 생성
        answers   = data['A'].tolist()  # A 열의 데이터를 추출하여 답변 리스트를 생성
        return questions, answers

    def find_best_answer(self, input_sentence):
        # 입력된 문장과 저장된 모든 질문들 간의 레벤슈타인 거리를 계산하여 리스트에 저장
        distances = [calc_distance(input_sentence, q) for q in self.questions]
        
        # 최소 편집 거리를 가진 질문의 인덱스
        best_match_index = distances.index(min(distances))
        
        # 최소 편집 거리를 가진 질문에 해당하는 답변을 반환
        return self.answers[best_match_index]

# 챗봇이 사용할 데이터가 포함된 CSV 파일 경로
filepath = 'ChatbotData.csv'

# LevenshteinChatBot 클래스의 인스턴스를 생성하여 챗봇을 준비
chatbot = LevenshteinChatBot(filepath)

# 사용자로부터 입력을 받고 '종료'가 입력될 때까지 챗봇과의 상호작용을 반복하는 메인 루프
while True:
    user_input = input("You: ")
    if user_input.lower() == '종료':
        print("Chatbot: 안녕히 가세요! 다음에 또 만나요~") # 사용자가 종료를 입력하면 프로그램 종료
        break
    response = chatbot.find_best_answer(user_input)
    print("Chatbot:", response)