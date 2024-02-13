import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time,re, os , shutil
import requests
import pandas as pd


##### 사용법
##### http://127.0.0.1:8000/sel/?url=https://www.naver.com
github_raw_url = "https://raw.githubusercontent.com/kuick1kim/cmmn/main/kms_git.json"
response = requests.get(github_raw_url)

  
def open_selenium():
    # Chrome 웹 드라이버 생성
    s = Service("chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('--no-sandbox')
    options.add_argument("disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
    driver = webdriver.Chrome(service=s, options=options)
    return driver

# 폴더를 삭제후 다시 생성
def remove_folder(path):  # 폴더가 이미 존재하는 경우 삭제
    if os.path.exists(path):
        shutil.rmtree(path)        
    os.makedirs(path)# 폴더 생성
    



#### 사진촬영


### 클린 텍스트 파일이름 저장하려면
def clean_text(filename):
    # 특수 문자 제거 및 공백을 언더스코어로 대체
    cleaned_filename = re.sub(r'[^\w\s.-]', '', filename).strip().replace(' ', '_')
    return cleaned_filename

### 사진찍기
def screenshot_a(driver,save_filename):
    driver.save_screenshot(f'static/mougi/{save_filename}.png')
    print(f'static/mougi/{save_filename}.png')

def save_df(return_df,return_df2) :
    return_df = pd.concat([return_df,return_df2], axis=0)    
    return_df.to_csv('static/mougi/result.csv' ,index=False, mode='w', encoding='utf-8-sig')                                      
    return return_df

def open_return_df():
    try:
        return_df = pd.read_csv('static/mougi/result.csv', low_memory=False)   
    except:
        return_df = pd.DataFrame()
    return return_df


def check_element(driver,texta, textb):
    texta = texta.lower()
    if 'xpath' in texta:
        element_a = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,textb)))  
    elif 'id' in texta:
        element_a = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,textb)))  
    elif 'class' in texta:
        element_a = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,textb)))  
    elif 'tag' in texta:
        element_a = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME,textb)))  
    elif 'name' in texta:
        element_a = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME,textb)))  
    elif 'partial' in texta:
        element_a = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,textb)))  
    elif 'link' in texta:
        element_a = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT,textb)))  
    elif 'css' in texta:
        element_a = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,textb)))  
    return element_a
    


### 로그인 할때
def login(driver, row, number_p):
    driver.get(row['스크립트b'])### 0.5초후에 사진촬영      

    if number_p == '1':       
        save_filename = clean_text(row['행동'])   
        screenshot_a(driver, row['번호']+"-"+save_filename)                    
        ### 여기서 사진찍기          

### 로그인 할때
    
def assert_a(driver,row,number_p):
    element_a = check_element(driver,row['스크립트a'],row['스크립트b'])
    driver.execute_script("arguments[0].style.border = '4px solid rgba(255, 0, 0, 0.6)';", element_a) 
    if number_p == '1':    
        save_filename = clean_text(row['행동'])   
        screenshot_a(driver, row['번호']+"-"+save_filename)    
        ### 여기를 사진찍음
    driver.execute_script("arguments[0].style.border = '';", element_a)
    
def click_a(driver,row,number_p):
    element_a = check_element(driver,row['스크립트a'],row['스크립트b'])
    driver.execute_script("arguments[0].style.border = '4px solid rgba(255, 0, 0, 0.6)';", element_a) 
    if number_p == '1':    
        save_filename = clean_text(row['행동'])   
        screenshot_a(driver, row['번호']+"-"+save_filename)    
        ### 여기를 사진찍음
    element_a.click()

    
def change_window(driver,row,number_p):
    textaa = row['스크립트a'].lower()
    if "change_window" in textaa:
        driver.switch_to.window(driver.window_handles[-1]) ###마지막 창으로 변경해 준다   
    elif "close_window" in textaa:
        driver.close() 
        driver.switch_to.window(driver.window_handles[-1]) ###마지막 창으로 변경해 준다   
    if number_p == '1':    
        time.sleep(0.3)
        save_filename = clean_text(row['행동'])   
        screenshot_a(driver, row['번호']+"-"+save_filename)    

    
def input(driver,row,number_p):           
    input_text = row['스크립트b'].split("--")
    elem = input_text[1] 
    input_text = input_text[0] 
    element_a = check_element(driver,row['스크립트a'], elem)
    element_a.send_keys(input_text)
   
    driver.execute_script("arguments[0].style.border = '4px solid rgba(255, 0, 0, 0.6)';", element_a) 
    if number_p == '1':    
        save_filename = clean_text(row['행동'])   
        screenshot_a(driver, row['번호']+"-"+save_filename)    ### 여기를 사진찍음
        driver.execute_script("arguments[0].style.border = '';", element_a) ### 여기는 지워줌
        

def iframe_a(driver,row,number_p):
    if 'in' in row['스크립트a']:
        element_a = check_element(driver,row['스크립트a'],row['스크립트b'])
        driver.execute_script("arguments[0].style.border = '4px solid rgba(255, 0, 0, 0.6)';", element_a) 
        if number_p == '1':    
            save_filename = clean_text(row['행동'])   
            screenshot_a(driver, row['번호']+"-"+save_filename)    
            ### 여기를 사진찍음
        driver.execute_script("arguments[0].style.border = '';", element_a) ### 여기는 지워줌
        driver.switch_to.frame(element_a)
    elif 'out' in row['스크립트a']:
        driver.switch_to.default_content()        
        if number_p == '1':    
            save_filename = clean_text(row['행동'])   
            screenshot_a(driver, row['번호']+"-"+save_filename)    
            ### 여기를 사진찍음

    

def dropbox_a(driver,row,number_p):
    input_text = row['스크립트b'].split("--")
    elem = input_text[1] 
    input_text = input_text[0] 
    element_a = check_element(driver,row['스크립트a'],elem)
    driver.execute_script("arguments[0].style.border = '4px solid rgba(255, 0, 0, 0.6)';", element_a) 
    element_a.click()

    select_a = check_element(driver,row['스크립트a'],f"//option[text()='{input_text}']")
    driver.execute_script("arguments[0].style.border = '4px solid rgba(255, 0, 0, 0.6)';", select_a) 
    if number_p == '1':    
        save_filename = clean_text(row['행동'])   
        screenshot_a(driver, row['번호']+"-"+save_filename)    
        ### 여기를 사진찍음
    driver.execute_script("arguments[0].style.border = '';", element_a)
    driver.execute_script("arguments[0].style.border = '';", select_a)
    select_a.click()
  
    






# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,  '//*[@id="id_web_app_link"]'))).click()
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,  '//*[@id="id_web_app_link"]'))).click()
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,  '//*[@id="id_web_app_link"]'))).click()
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,  '//*[@id="id_web_app_link"]'))).click()

# dic = {"prediction" :1, "김민상":2}
##### 여기에 df가 있어야 한다. 

def process_b(driver,df_a,number_p):
    #### 여기서 오픈df를 불러온다. 
    return_df = open_return_df()
    #### 수행시간

    time_A = time.time()
    time_B = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    email2 = df_a.at[0, "담당자이메일"]#담당자 이메일
    damdang = df_a.at[0, "담당자"]#담당자 이메일
    testcase_a = df_a.at[0, "테스트케이스"]#담당자 이메일
    message_b = "잘했어요 "

    for index, row in df_a.iterrows():
        print(index)    #### 나중에 지우세요
        print(row['번호'],row['행동'],row['스크립트a'],row['스크립트b'])      #### 나중에 지우세요

        #### 로그인이 있을때.    
        texta = str(row['스크립트a']).lower()         
        save_filename = clean_text(row['행동'])   
        num_a = row['번호']

        if 'open' in texta:
            try: 
                login(driver, row ,number_p) 
                return_df2 = pd.DataFrame([{"수행시간" :time_B,"테스트번호" :num_a,"테스트케이스" :testcase_a,
                       "행동":save_filename, "진행시간":"{:.3f}".format(time.time()- time_A),
                       "성공여부":"PASS", "담당자":damdang, "이메일":email2 , "추가":"" }])
                return_df= save_df(return_df,return_df2)          

            except Exception as e:
                return_df2 = pd.DataFrame([{"수행시간" :time_B,"테스트번호" :num_a,"테스트케이스" :testcase_a,
                       "행동":save_filename, "진행시간":"{:.3f}".format(time.time()- time_A),
                       "성공여부":"FAIL", "담당자":damdang, "이메일":email2 , "추가":e}])
                return_df= save_df(return_df,return_df2)


        #### assert가 있을때.                
        elif 'assert' in texta:
            try: 
                assert_a(driver,row,number_p)                                     
                return_df2 = pd.DataFrame([{"수행시간" :time_B,"테스트번호" :num_a,"테스트케이스" :testcase_a,
                       "행동":save_filename, "진행시간":"{:.3f}".format(time.time()- time_A),
                       "성공여부":"PASS", "담당자":damdang, "이메일":email2 , "추가":"" }])
                return_df= save_df(return_df,return_df2)

            except Exception as e:
                return_df2 = pd.DataFrame([{"수행시간" :time_B,"테스트번호" :num_a,"테스트케이스" :testcase_a,
                       "행동":save_filename, "진행시간":"{:.3f}".format(time.time()- time_A),
                       "성공여부":"FAIL", "담당자":damdang, "이메일":email2 , "추가":e}])
                return_df= save_df(return_df,return_df2)
                

        #### click이 있을때.                
        elif 'click' in texta:
            try: 
                click_a(driver,row,number_p)               
               
                return_df2 = pd.DataFrame([{"수행시간" :time_B,"테스트번호" :num_a,"테스트케이스" :testcase_a,
                       "행동":save_filename, "진행시간":"{:.3f}".format(time.time()- time_A),
                       "성공여부":"PASS", "담당자":damdang, "이메일":email2 , "추가":"" }])
                return_df= save_df(return_df,return_df2)

            except Exception as e:
                return_df2 = pd.DataFrame([{"수행시간" :time_B,"테스트번호" :num_a,"테스트케이스" :testcase_a,
                       "행동":save_filename, "진행시간":"{:.3f}".format(time.time()- time_A),
                       "성공여부":"FAIL", "담당자":damdang, "이메일":email2 , "추가":e}])
                return_df= save_df(return_df,return_df2)
        
        #### click이 있을때.                
        elif 'time_sleep' in texta:            
            time.sleep(int(row['스크립트b']))### 여기서 시간을 넣으세요           
               
            return_df2 = pd.DataFrame([{"수행시간" :time_B,"테스트번호" :num_a,"테스트케이스" :testcase_a,
                    "행동":save_filename, "진행시간":"{:.3f}".format(time.time()- time_A),
                    "성공여부":"PASS", "담당자":damdang, "이메일":email2 , "추가":"" }])
            return_df= save_df(return_df,return_df2)
            if number_p == '1':    
                save_filename = clean_text(row['행동'])   
                screenshot_a(driver, row['번호']+"-"+save_filename)    


        #### 창 변환.                
        elif 'window' in texta:            
            change_window(driver,row,number_p)            
            try:
                return_df2 = pd.DataFrame([{"수행시간" :time_B,"테스트번호" :num_a,"테스트케이스" :testcase_a,
                       "행동":save_filename, "진행시간":"{:.3f}".format(time.time()- time_A),
                       "성공여부":"PASS", "담당자":damdang, "이메일":email2 , "추가":"" }])
                return_df= save_df(return_df,return_df2)

            except Exception as e:
                return_df2 = pd.DataFrame([{"수행시간" :time_B,"테스트번호" :num_a,"테스트케이스" :testcase_a,
                       "행동":save_filename, "진행시간":"{:.3f}".format(time.time()- time_A),
                       "성공여부":"FAIL", "담당자":damdang, "이메일":email2 , "추가":e}])
                return_df= save_df(return_df,return_df2)             
             
        #### input text              
        elif 'input' in texta:
            try: 
                input(driver,row,number_p)               
               
                return_df2 = pd.DataFrame([{"수행시간" :time_B,"테스트번호" :num_a,"테스트케이스" :testcase_a,
                       "행동":save_filename, "진행시간":"{:.3f}".format(time.time()- time_A),
                       "성공여부":"PASS", "담당자":damdang, "이메일":email2 , "추가":"" }])
                return_df= save_df(return_df,return_df2)

            except Exception as e:
                return_df2 = pd.DataFrame([{"수행시간" :time_B,"테스트번호" :num_a,"테스트케이스" :testcase_a,
                       "행동":save_filename, "진행시간":"{:.3f}".format(time.time()- time_A),
                       "성공여부":"FAIL", "담당자":damdang, "이메일":email2 , "추가":e}])
                return_df= save_df(return_df,return_df2)

        #### 아이프레임.                
        elif 'iframe' in texta:            
            iframe_a(driver,row,number_p)
            try:
                return_df2 = pd.DataFrame([{"수행시간" :time_B,"테스트번호" :num_a,"테스트케이스" :testcase_a,
                       "행동":save_filename, "진행시간":"{:.3f}".format(time.time()- time_A),
                       "성공여부":"PASS", "담당자":damdang, "이메일":email2 , "추가":"" }])
                return_df= save_df(return_df,return_df2)

            except Exception as e:
                return_df2 = pd.DataFrame([{"수행시간" :time_B,"테스트번호" :num_a,"테스트케이스" :testcase_a,
                       "행동":save_filename, "진행시간":"{:.3f}".format(time.time()- time_A),
                       "성공여부":"FAIL", "담당자":damdang, "이메일":email2 , "추가":e}])
                return_df= save_df(return_df,return_df2)             
            

        #### dropbox.                
        elif 'dropbox' in texta:            
            dropbox_a(driver,row,number_p)
            try:
                return_df2 = pd.DataFrame([{"수행시간" :time_B,"테스트번호" :num_a,"테스트케이스" :testcase_a,
                       "행동":save_filename, "진행시간":"{:.3f}".format(time.time()- time_A),
                       "성공여부":"PASS", "담당자":damdang, "이메일":email2 , "추가":"" }])
                return_df= save_df(return_df,return_df2)

            except Exception as e:
                return_df2 = pd.DataFrame([{"수행시간" :time_B,"테스트번호" :num_a,"테스트케이스" :testcase_a,
                       "행동":save_filename, "진행시간":"{:.3f}".format(time.time()- time_A),
                       "성공여부":"FAIL", "담당자":damdang, "이메일":email2 , "추가":e}])
                return_df= save_df(return_df,return_df2)             
            

            
        

d= response.json()['사용자']

def process_a(driver,df,number):### 여기서 엑셀과 1번 또는 2번을 잡고 들어간다. 
    df = df.dropna(subset=['테스트케이스'])
    #전체 담당자 이메일 
    email1 = df.at[0, "전체담당자이메일"]   #### 이메일을 가져온다
    list_k = df['테스트케이스'].unique()    #### 리스트를 만들어준다. 
    message_a= "-" #### 공메세지를 넣어준다 
    for i in list_k:
        df_a = df[df['테스트케이스']== i]
        df_a = df_a.reset_index(drop=True)
        email2 = df_a.at[0, "담당자이메일"]#담당자 이메일
        
        try: 
            process_b(driver,df_a,number) #### 이것을 들고 저쪽으로 들어간다
            # message_b 는 한개씩 지나간 과정이다. 
    
            

        except Exception as e:            
            pass_fail = send_email("[확인해주세요] 어디서 오류가 발생 했어요 : ", e, email1,email2 )
            print(e)

    
    return message_a



# JSON 파일 가져오기



def send_email(subject, body,s, r):    
 
    message = MIMEMultipart()
    message["From"] = s
    message["To"] = r
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # SMTP 서버 설정
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    # SMTP 서버 연결 및 이메일 전송
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(s, d['bun4']+d['bun3']+d['bun2']+d['bun1'])
        server.sendmail(s, r, message.as_string())
        server.quit()        
        pass_fail = "이메일 전송 성공"
    except Exception as e:
        print("이메일 전송 중 오류가 발생했습니다:");        print(e);        print(traceback.format_exc())
        pass_fail = "이메일 주소에 문제가 있는것 같아요 : " +  e
    return pass_fail






###### 여기서 롤링계산을해서 다시 재저장한다. 
def roll_a():
    time_B = time.strftime("%Y%m%d_%H%M", time.localtime())
    if not os.path.exists('static/mougi2/'):
        os.makedirs('static/mougi2/')
    #### 여기서 저장된것을 연다. 
    df = pd.read_csv('static/mougi/result.csv', low_memory=False)         
    df['시간차'] = df['진행시간'].diff()  # 롤링 차이 계산    
    df['시간차'] = df['시간차'].fillna(0)   # NaN 값을 0으로 채우기
    df['시간차'] = df['시간차'].round(2)   # 
    df['시간차'] = df['시간차'].clip(lower=0)   # 0 미만의 값을 0으로 클리핑
    df = df[['수행시간','테스트번호','테스트케이스','행동','성공여부',
             '시간차','진행시간','담당자','이메일','추가']]
    df.to_csv('static/mougi/result.csv' ,index=False, mode='w', encoding='utf-8-sig') 
    ##### 여기서 재저장한다. 
    df.to_csv(f'static/mougi2/result-{time_B}.csv' ,index=False, mode='w', encoding='utf-8-sig') 
    #### 여기서 데이터를 만들어 줄꺼다.    

        
    data1 = []
    for index, row in df.iterrows():
        list_a =[row.수행시간, row.테스트번호, row.테스트케이스, row.행동, row.성공여부,
                 row.시간차, row.진행시간, row.담당자, row.이메일, 
                '../../static/mougi/' + row.테스트번호+"-"+row.행동+".png"]        
        data1.append(list_a)
 
    
    return data1




# 이메일 서버에 연결
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.starttls()
    # server.login('your-email@gmail.com', 'your-password')

    # # 이메일 보내기
    # server.sendmail(sender, receiver, msg.as_string())
    # server.quit()

# 이메일 보내기
# send_email('your-email@gmail.com', 'receiver-email@gmail.com', '파이썬에서 이메일 보내기', '안녕하세요! 파이썬에서 이메일을 보내는 예제입니다.')




# 가져온 JSON 데이터를 딕셔너리로 파싱


### 몇분마다 자동으로 돌아가게 할 것인가?
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Auto Refresh Page</title>
# </head>
# <body>

# <button onclick="startAutoRefresh()">Start Auto Refresh</button>
# <button onclick="stopAutoRefresh()">Stop Auto Refresh</button>
# <label>Refresh Interval (seconds):</label>
# <input type="number" id="refreshInterval" value="10">

# <script src="auto-refresh.js"></script>
# </body>
# </html>


# let refreshIntervalId;

# function refreshPage() {
#     console.log("페이지 리프레시");
#     location.reload(true);  // 페이지 리프레시
# }

# function startAutoRefresh() {
#     const intervalSeconds = document.getElementById("refreshInterval").value;
    
#     // 유효한 간격인지 확인
#     if (!isNaN(intervalSeconds) && intervalSeconds > 0) {
#         console.log(`자동 리프레시 시작 (간격: ${intervalSeconds}초)`);
#         refreshIntervalId = setInterval(refreshPage, intervalSeconds * 1000);
#     } else {
#         alert("유효한 간격을 입력하세요.");
#     }
# }

# function stopAutoRefresh() {
#     console.log("자동 리프레시 중지");
#     clearInterval(refreshIntervalId);
# }



##### 크롬업데이트시 다운로드
# import requests

# url = "https://github.com/kuick1kim/kimstargram/raw/main/chromedriver.exe"
# response = requests.get(url)

# if response.status_code == 200:
#     with open("chromedriver.exe", "wb") as file:
#         file.write(response.content)
#     print("다운로드가 완료되었습니다.")
# else:
#     print(f"다운로드에 실패했습니다. 상태 코드: {response.status_code}")



#### 사진촬영


#### DB입력/// db가 넘치면 db 삭제


#### 시간체크



#### 오류시 이메일 발송




#### 분석사이트 만들어줌



#### 엑셀틀 다운로드


#### 엑셀틀 올리기 그리고 내틀 다운로드




#### 엘레멘트 찾기


#### 어써트 확인


#### 클릭



#### 글씨 입력 input text
    #### 두가지 입력방법 한가지는 일반
    #### 두번째는 특수한 입력방법 pyautogui


#### 프레임 이동
#### 프레임 닫기
# 원래 프레임으로 가기


#### 아이프레임 으로 전환하기 
#### 아이프레임에서 원래 프레임으로 나오기


# 경고창 클릭



#### 그래프 그리기


#### 오류 저장







# def selenium_01(request):
#     start_time = time.time()
#     sympathy = 0 ;  comment = 0
#     return_obj = {}

#     current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
#     return_obj["date"] = current_time



#     try:
#         aaa = request.GET.get('url', None)
#         print('aaa = ', str(aaa))
#         blog_url = request.GET.get('url', None)      
#         screenshot_filename = f"image/hohoho.png"
#         # screenshot_filename = f"image/{blog_url.split('.')[-2]}.png"

#         return_obj["url"] = blog_url    

#     except:
#         blog_url = 'unknown'
#         print(blog_url)
#         print()
        
        
#     # Load Page
#     driver.get(url=blog_url)
#     time.sleep(0.5)

#     # Capture screenshot    
#     driver.save_screenshot(screenshot_filename)
#     #### 사진찍고 문 닫음
#     driver.quit()


#     return_obj["sympathy"] = sympathy
#     return_obj["comment"] = comment
#     return_obj["process_time"] = round(time.time() - start_time, 2)

#     # show_image(screenshot_filename)
#     image_url =f'http://127.0.0.1:8000/{screenshot_filename}'


#     return render(request, 'selenium_example.html', {'image': image_url,'home1': blog_url, 'data': json.dumps(return_obj, indent=2)})
    