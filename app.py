from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

# Playwright 
p = sync_playwright().start()

# Chromium 브라우저 실행
browser = p.chromium.launch(headless=False)
page = browser.new_page()

# 페이지 열기
page.goto("https://www.wanted.co.kr/search?query=flutter&tab=position")

# time.sleep(5)

# 특정 요소 클릭
# Element : Button
# Class Name : Aside_searchButton_rajGo
# page.click("button.Aside_searchButton__rajGo")

# time.sleep(5)

# # 입력 필드의 placeholder 속성 값을 받아 온 다음 "flutter" 입력
# page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")

# time.sleep(5)

# # Enter 키 누르는 동작
# page.keyboard.down("Enter")

# time.sleep(10)

# # 특정 요소 클릭
# # Element : Anchor
# # Id : search_tab_position
# page.click("a#search_tab_position")

# 페이지 스크롤 내리기
for x in range(3):
    time.sleep(5)
    page.keyboard.down("End")

# 현재 페이지의 HTML 콘텐츠를 가져오는 메서드
content = page.content()

# Playwright 인스턴스 종료 - 초기화하기 위함
p.stop()

# BeautifulSoup(args1, args2) : HTMl 혹은 XML 문서를 파싱하는 라이브러리
# args1 : 파싱할 HTML 혹은 XML 문서
# args2 : 파서 종류 (e.g. html.parser, lxml, html5lib...)
soup = BeautifulSoup(content, "html.parser")

# 포지션 탭의 모든 Job Card 불러오기
jobs = soup.find_all("div", class_="JobCard_container__REty8")

# job database
jobs_db = []

# job : 각각의 div를 의미 (soup의 Element)
# a Element를 찾은 다음 href attribute 찾기
for job in jobs:
    link = f"https://www.wanted.co.kr/{job.find('a')['href']}"
    title = job.find("strong", class_="JobCard_title__HBpZf").text
    company_name = job.find("span", class_="JobCard_companyName__N1YrF").text
    reward = job.find("span", class_="JobCard_reward__cNlG5").text

    job = {
        "title": title,
        "company_name": company_name,
        "reward": reward,
        "link": link
    }

    # job을 jobs_db list 안에 넣기
    jobs_db.append(job)

print(jobs_db)
print(len(jobs_db))

# CSV : Comma Separated Values
# open() : 파일 열어주는 함수. 만약 파일이 존재하지 않으면 파일을 생성해준다.
# "w" : write
file = open("jobs.csv", "w")
writer = csv.writer(file)
writer.writerow(
    [
        "Title", 
        "Company", 
        "Reward", 
        ㅌ"Link"
    ]
)

for job in jobs_db:
    writer.writerow(job.values())