import requests

def validId(topic):
    # categories = [{"id":9, "name":"General Knowledge"},
    #             {"id":10, "name":"Entertainment: Books"},
    #             {"id":11, "name":"Entertainment: Film"},
    #             {"id":12, "name":"Entertainment: Music"},
    #             {"id":13, "name":"Entertainment: Musicals & Theatres"},
    #             {"id":14, "name":"Entertainment: Television"},
    #             {"id":15, "name":"Entertainment: Video Games"},
    #             {"id":16, "name":"Entertainment: Board Games"},
    #             {"id":17, "name":"Science & Nature"},
    #             {"id":18, "name":"Science: Computers"},
    #             {"id":19, "name":"Science: Mathematics"},
    #             {"id":20, "name":"Mythology"},
    #             {"id":21, "name":"Sports"},
    #             {"id":22, "name":"Geography"},
    #             {"id":23, "name":"History"},
    #             {"id":24, "name":"Politics"},
    #             {"id":25, "name":"Art"},
    #             {"id":26, "name":"Celebrities"},
    #             {"id":27, "name":"Animals"},
    #             {"id":28, "name":"Vehicles"},
    #             {"id":29, "name":"Entertainment: Comics"},
    #             {"id":30, "name":"Science: Gadgets"},
    #             {"id":31, "name":"Entertainment: Japanese Anime & Manga"},
    #             {"id":32, "name":"Entertainment: Cartoon & Animations"}]

    if (topic >= 9) and (topic <= 32):
        return True
    return False

def quiz(topic, amount, difficulty):
    if validId(topic):
        maxQue = requests.get(f"https://opentdb.com/api_count.php?category={topic}").json()
        maxQue = maxQue.get('category_question_count')
        # totalQue = maxQue.get('total_question_count')
        easyQue = maxQue.get('total_easy_question_count')
        mediumQue = maxQue.get('total_medium_question_count')
        hardQue = maxQue.get('total_hard_question_count')
        difficulties = ['easy', 'medium', 'hard']
        if difficulty == 0:
            amount = easyQue if amount > easyQue else amount
        if difficulty == 1:
            amount = mediumQue if amount > mediumQue else amount
        if difficulty == 2:
            amount = hardQue if amount > hardQue else amount
        res = requests.get(f"https://opentdb.com/api.php?amount={amount}&category={topic}&difficulty={difficulties[difficulty]}").json()
        if res.get('response_code') == 0:
            return res
    return None

def getQuiz(topic, amount=10, difficulty=1):
    if difficulty > 3 or difficulty < 1:
        difficulty = 3 if difficulty > 3 else 1
    amount = 1 if amount < 1 else amount
    amount = 50 if amount > 50 else amount
    if topic:
        return quiz(topic, amount, difficulty)