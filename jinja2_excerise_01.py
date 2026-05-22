##############################################
# 0. 준비 단계 (모든 라이브러리 임포트)
##############################################
'''
파일/폴더 설명 ---> 
jinja2_excerse.py: FastAPI 앱을 초기화하고, Jinja2Templates를 output 디렉토리로 경로 작동(라우트) 함수를 정의 파일
output/	: Jinja2와 같은 템플릿 엔진이 찾을 HTML 파일(.html)을 저장하는 폴더로 jinja2_excerse.py에서 이 폴더를 지정
'''
import os
import jinja2
from jinja2 import Environment, FileSystemLoader

# 실습을 위해 output 폴더가 없다면 자동으로 생성해줍니다.
os.makedirs("output", exist_ok=True)

# 실습용 가상 템플릿 파일 만들기 (실행 전 미리 생성)
with open("output/message1.txt", "w", encoding="utf-8") as f:
    f.write("안녕하세요 {{ name }}님, {{ test_name }} 점수는 {{ score }}/{{ max_score }}점입니다.")

with open("output/message2.txt", "w", encoding="utf-8") as f:
    f.write("안녕하세요 {{ name }}님.\n"
            "점수: {{ score }}점\n"
            "{% if score >= 90 %}축하합니다! 합격입니다.{% else %}재시험 대상입니다.{% endif %}")

print("#" * 100)
##############################################
# 1. Render Your First Jinja Template
# 정해진 틀(양식)에 원하는 데이터만 쏙 집어넣어 새로운 문장을 만드는 과정
##############################################
environment = jinja2.Environment()
template = environment.from_string("Hello, {{ name }}!")

print(template.render(name="World"))
print("This is end. -- 1. Render Your First Jinja Template")
print("#" * 100)

###############################################
# 2. Render a Template from a External File
# 여러 학생의 시험 결과 리포트(텍스트 파일)를 자동으로 대량 생성하는 프로그램을 작성
###############################################
max_score = 100
test_name = "Python Challenge"
students = [
    {"name": "Sandrine",  "score": 100},
    {"name": "Gergeley", "score": 87},
    {"name": "Frieda", "score": 92},
]

# 외부에 있는 output 폴더를 로드 경로로 설정
file_environment = Environment(loader=FileSystemLoader("output/"))
template1 = file_environment.get_template("message1.txt")

for student in students:
    print(f"student: {student}, name: {student['name']}, score: {student['score']}")
    
    # 안전하게 파일 경로 생성
    filename = os.path.join("output", f"message1_{student['name'].lower()}.txt") 
   
    content = template1.render(
        student,
        max_score=max_score,
        test_name=test_name
    )
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")
    print("*" * 50)

print("This is end. -- 2. Render a Template from a External File")
print("#" * 100)


##############################################
# 3. Use if Statements
# 특정 점수 이상인 학생에게만 합격 메시지 파일을 생성하거나, 내부 문구를 바꾸는 방식
##############################################
# 3번 목적에 맞는 새로운 템플릿(내부에 if문이 포함된 message2.txt)을 불러오기
template2 = file_environment.get_template("message2.txt")

for student in students:
    # [파이썬 if문] 점수가 90점 이상인 우수 학생만 파일로 저장
    if student['score'] >= 90:
        filename = os.path.join("output", f"message2_{student['name'].lower()}.txt") 
        
        # 템플릿 내부에서도 {% if %} 문에 의해 문구가 변합니다.
        content = template2.render(
            student,
            max_score=max_score,
            test_name=test_name
        )
        with open(filename, mode="w", encoding="utf-8") as message:
            message.write(content)
            print(f"[합격자 파일 생성] ... wrote {filename} (점수: {student['score']})")
    else:
        # 90점 미만인 학생은 파일을 만들지 않고 콘솔에만 출력
        print(f"[보류] {student['name']}님은 파일 생성 대상이 아닙니다. (점수: {student['score']})")
    print("*" * 50)
        
print("This is end. -- 3. Use if Statements")
print("#" * 100)
    
##############################################
# 4. Leverage for Loops
# 여러 학생의 시험 결과 리포트(HTML 파일)를 자동으로 대량 생성하는 프로그램을 작성
# 학생들의 점수에 따라 합격/불합격 여부를 표시하는 HTML 테이블을 생성하는 방식
# 3번 코드와 비교해서 반복문이 어디에 위치하는지, 생성되는 파일 수와 출력 형태가 어떻게 달라지는지 생각하자 !
# - 반복문(for)의 위치 : Jinja2 템플릿(HTML) 내부에 있음 (파이썬은 한 번만 실행)
# - 생성되는 파일 수 : 딱 1개의 HTML 파일 (students_results.html)
# - 출력 형태	: 모든 학생의 점수가 한눈에 보이는 웹 표(Table) 등
##############################################        

max_score = 100
test_name = "Python Challenge"
students = [
    {"name": "Sandrine",  "score": 100},
    {"name": "Gergeley", "score": 87},
    {"name": "Frieda", "score": 92},
    {"name": "Fritz", "score": 40},
    {"name": "Sirius", "score": 75},
]
# 파일 변수명 생성 (실제 파일은 아래 with문에서 만들어짐)
results_filename = "output\students_results.html"
environment = Environment(loader=FileSystemLoader("output/"))

# Jinja2 템플릿 엔진에게 *"output 폴더 안에 있는 results.html 파일을 찾아서 데이터 집어넣을 준비를 해줘"*라고 요청
results_template = environment.get_template("results.html")
print(f"...results_template____loaded {results_template}")

context = {
    "students": students,
    "test_name": test_name,
    "max_score": max_score,
}
# 실제 파일 생성 및 작성 (여기서 파일이 만들어짐)
with open(results_filename, mode="w", encoding="utf-8") as results:
    results.write(results_template.render(context))
    print(f"... wrote {results_filename}")

print("This is end. -- 4. Leverage for Loops")
print("#"*100)    
    
##############################################
# 5. Leverage for Loops with Conditionals
# HTML 템플릿(웹페이지) 내부에서 반복문을 돌리는 동시에, 
# 조건문(if-else)까지 결합하여 학생마다 서로 다른 반응(이모지)을 보여주는 웹페이지를 만드는 코드
'''
This means: If a student's score is greater than 80, the HTML output will include a 😀 emoji.
Otherwise (if the score is 80 or less), the output will include a 😟 emoji.
'''
##############################################        

results_filename = "output\students_results_if.html"
environment = Environment(loader=FileSystemLoader("output/"))

results_template = environment.get_template("results_if.html")

context = {
    "students": students,
    "test_name": test_name,
    "max_score": max_score,
}

with open(results_filename, mode="w", encoding="utf-8") as results:
    results.write(results_template.render(context))
    print(f"... wrote {results_filename}")


print("This is end. -- 5. Leverage for Loops with Conditionals")
print("#"*100)    