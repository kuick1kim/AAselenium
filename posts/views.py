from django.http import (
    HttpResponseBadRequest,
    HttpResponseRedirect,
    HttpResponseForbidden,HttpResponse
)
from django.shortcuts import render, redirect
from django.urls import reverse

from posts.forms import *
from posts.models import Post, Comment, PostImage, HashTag

from .commona import *
import time, json



driver = ""

try:
    with open('static/basic/new.json', 'r') as json_file:
        saved_excel_path = json.load(json_file)["saved_excel_path"]
except:
    saved_excel_path = "static/basic/origin.xlsx"



def feeds(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("users:login")

    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        "posts": posts,
        "comment_form": comment_form,
    }
    return render(request, "posts/feeds.html", context)




def button_view(request): 
    if os.path.exists('static/mougi/result.csv'):
        os.remove('static/mougi/result.csv')   ### 있으면 삭제한다
    global driver ### 드라이버를 글로벌로 만들어준다
    
    button_number = request.POST.get('button_number')

    basic_image='/static/basic/ready.png'
    image_url ='/static/hohoho.png'  

    driver = open_selenium()#### '셀레니움 이 안돌아가요.ERROR'    

    df_input = pd.read_excel(saved_excel_path , sheet_name='Sheet1')### 여기서 뉴파일을 읽어온다
    if button_number == '1': #### 1을 누르면 이미지를 모두 새로만듦
        
        remove_folder('static/mougi/')
        try :
            process_a(driver, df_input,button_number)      
        except:
            with open(basic_image, 'rb') as source_file, open(image_url, 'wb') as destination_file:
                destination_file.write(source_file.read())          
       
    elif button_number == '2': ##### 여기는 이미지 저장안하고 돌아간다. 
        process_a(driver, df_input,button_number)
    data1 = roll_a()##### 여기서 롤링계산을 해서 재저장
      
    # data1 = {'data1': pass_fail, 'image1': f'../..{image_url}'}
    
    if driver:
        driver.quit() ### 드라이버는 항상 꺼준다. 계속돌아가면 잡아먹으니
    
    return render(request, 'posts/selenium_example.html', {'data1': data1})  











def upload_excel(request):
    def error_df():
        df = pd.DataFrame()
        df[0] = ["오류가 발생했습니다.올린 파일이 형식이 맞지 않습니다. 다시다운받아 정리후 확인해 주세요  "]
        return df

    if request.method == 'POST':
        form = ExcelFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['file']
            # 업로드된 엑셀 파일을 읽어서 DataFrame으로 변환
             # 서버 내에 업로드된 엑셀 파일 저장
            aaa = str(excel_file.name).split(".")[-1]
            saved_excel_path = os.path.join('static', 'basic', f'new.{aaa}')
           
            with open('static/basic/new.json', 'w') as json_file:
                json.dump({"saved_excel_path": saved_excel_path }, json_file, ensure_ascii=False, indent=4)
            # 파일이 있으면 삭제
            if os.path.exists(saved_excel_path):
                os.remove(saved_excel_path)
            with open(saved_excel_path, 'wb') as destination:
                for chunk in excel_file.chunks():
                    destination.write(chunk)
            try:
                df = pd.read_excel(excel_file, sheet_name='Sheet1')
                if len(df['스크립트a'])<= 1:
                    df = error_df()
                elif len(df['스크립트b'])<= 1:
                    df = error_df()                     
            except:
               df = error_df()

            # DataFrame을 HTML 테이블로 변환하여 전달
            table_html = df.to_html()
            form = ExcelFileForm(request.POST, request.FILES)
            return render(request, 'posts/upload_excel.html', {'table_html': table_html, 'form': form})
    else:
        form = ExcelFileForm()
    return render(request, 'posts/upload_excel.html', {'form': form})





##### 여기는 원본 작성방법을 다운 받는곳
def download_file(request):
    # 다운로드할 파일의 경로를 설정
    file_path = 'static/basic/origin.xlsx'

    # 파일이 존재하는지 확인   # 파일을 읽어서 HttpResponse에 담아 전송
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=origin.xlsx'
            return response
    else:        
        return HttpResponse(f"{file_path}----경로가 잘못 되었나 봐요File not found.", status=404)





##### 여기는 원본 작성방법을 다운 받는곳
def download_result(request):
    # 다운로드할 파일의 경로를 설정
    file_path = 'static/mougi/result.csv'

    # 파일이 존재하는지 확인   # 파일을 읽어서 HttpResponse에 담아 전송
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=result.csv'
            return response
    else:        
        return HttpResponse(f"{file_path}----경로가 잘못 되었나 봐요File not found.", status=404)


