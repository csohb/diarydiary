from django.shortcuts import render,redirect
from diaryapp import models
# Create your views here.
def diary_home(request):
    id=request.session['id']
    name=request.session['name']
    print(id)
    return render(request,'diary/home.html',{"id":id,"name":name})

def diary_shop(request):
    # get에 없을경우 default 처리해주기
    id = request.session['id']
    name = request.session['name']
    try:
        cno = request.GET['cno']
        curcno=int(cno)
        page = request.GET['page']
        curpage=int(page)
    except:
        curcno=1
        curpage=1


    d_list=[]
    s_list=[]
    cd=models.shopCategoryList()
    for row in cd:
        if row[0] < 8:
            d_data={"cno":row[0],"title":row[1],"type":row[2]}
            d_list.append(d_data)
        else:
            s_data={"cno":row[0],"title":row[1],"type":row[2]}
            s_list.append(s_data)

    list=[] #메인리스트
    ss=models.shopListData(int(curcno),int(curpage))
    #no,cno,thumb,title,brand,price
    for row in ss:
        data={"no":row[0],"cno":row[1],"thumb":row[2],"title":row[3],"brand":row[4],"price":row[5]}
        list.append(data)

    #페이지넘기기
    totalpage=models.shopTotalPage(curcno)
    print(totalpage)
    block=10
    startPage=((curpage-1)//block*block)+1
    endPage=((curpage-1)//block*block)+block
    if endPage > totalpage:
        endPage=totalpage


    return render(request,'diary/shop.html',{"d_list":d_list,"s_list":s_list,"list":list,
            "totalpage":totalpage,"startPage":startPage,"endPage":endPage,"cno":curcno,"curpage":curpage,"range":range(startPage,endPage+1),"id":id})

def diary_detail(request):
    id = request.session['id']
    name = request.session['name']
    no=request.GET['no']
    data=models.shopDetail(int(no))
    #no,cno,thumb,brand,price,mileage,made,material,big,detail,title
    if data[1] < 8:
        category="Diary"
    else:
        category="Sticker"
    dd={"no":data[0],"cno":data[1],"thumb":data[2],"brand":data[3],"price":data[4],"mileage":data[5],"made":data[6],"material":data[7],"big":data[8],"detail":data[9],"title":data[10],"category":category}
    cno=data[1]
    re_data=models.shopRecommend(int(cno))
    #print(re_data)
    list=[]
    #no, cno, thumb,price,title,num
    for row in re_data:
        if row[1] < 8:
            category = "Diary"
        else:
            category = "Sticker"
        data={"no":row[0],"category":category,"thumb":row[2],"price":row[3],"title":row[4]}
        list.append(data)

    return render(request,'diary/detail.html',{"dd":dd,"list":list,"id":id})

def myDiary(request):
    id = request.session['id']
    name = request.session['name']
    try:
        page=request.GET['page']
        curpage=int(page)
    except:
        curpage=1

    # 페이지넘기기
    totalpage = models.myDailyTotalPage()
    print(totalpage)
    block = 5
    startPage = ((curpage - 1) // block * block) + 1
    endPage = ((curpage - 1) // block * block) + block
    if endPage > totalpage:
        endPage = totalpage
    list=[]
    #no,title,thumb,heart,mood,regdate,name,num
    data=models.myDailyList(curpage)
    for row in data:
        d_data={"no":row[0],"title":row[1],"thumb":row[2],"heart":row[3],"mood":row[4],"regdate":row[5],"name":row[6]}
        list.append(d_data)
    #print(startPage)
    #print(endPage)
    return render(request,'diary/mydiary.html',{"list":list,"curpage":curpage,"totalpage":totalpage,"startPage":startPage,"endPage":endPage,"range":range(startPage,endPage+1),"id":id})

def myDiaryRecord(request):
    id = request.session['id']
    name = request.session['name']
    return render(request,'diary/record.html',{"id":id,"name":name})

def myDiaryRecordOk(request):
    #title,content,pwd,name,regdate,mood
    title=request.POST['subject']
    content=request.POST['msg']
    pwd=request.POST['pwd']
    name=request.POST['name']
    mood=request.POST['mood']
    print(title,content,pwd,name,mood)
    insert_value=(title,content,pwd,name,mood)
    models.myDiaryInsert(insert_value)
    return redirect('/diary/mydiary/?page=1')

def myDiaryDetatil(request):
    id = request.session['id']
    name = request.session['name']
    no=request.GET['no']
    try:
        page=request.GET['page']
        curpage=int(page)
    except:
        curpage=1
    data=models.myDiaryDetail(int(no))
    #no,title,content,pwd,name,regdate,mood,heart
    detail={"no":data[0],"title":data[1],"content":data[2],"pwd":data[3],"name":data[4],"regdate":data[5],"mood":data[6],"heart":data[7]}
    return render(request,'diary/mydiary_detail.html',{"detail":detail,"curpage":curpage,"id":id})



# 일기 삭제
def mydiaryDelete(request):
    id = request.session['id']
    name = request.session['name']
    no=request.GET['no']
    return render(request,'diary/mydiary_delete.html',{"no":no,"id":id})

def mydiaryDeleteOK(request):
    id = request.session['id']
    name = request.session['name']
    no=request.POST['no']
    pwd=request.POST['pwd']
    delete_value=(no,pwd)
    result=models.mydiary_delete(delete_value)
    return render(request,'diary/mydiary_delete_ok.html',{"result":result,"id":id})

#일기 수정
def myDiaryUpdate(request):
    id = request.session['id']
    name = request.session['name']
    no=request.GET['no']
    data=models.myDiaryDetail(int(no))
    #no,title,content,pwd,name,regdate,mood,heart
    detail={"title":data[1],"content":data[2],"pwd":data[3],"name":data[4],"mood":data[6],}
    return render(request,'diary/mydiary_update.html',{"no":no,"detail":detail,"id":id})

def myDiaryUpdateOK(request):
    id = request.session['id']
    name = request.session['name']
    no = request.POST['no']
    print(no)
    title = request.POST['subject']
    content = request.POST['msg']
    pwd = request.POST['pwd']
    name = request.POST['name']
    mood = request.POST['mood']
    update_value=(no,title,content,pwd,name,mood)
    check=models.mydiary_update(update_value)
    return render(request,'diary/mydiary_update_ok.html',{"no":no,"check":check,"id":id})

# 일기 하트 증가
def myDiaryHeart(request):
    no=request.GET['no']
    curpage=request.GET['page']
    models.heart_up(int(no))
    return redirect('/diary/mydiary_detail/?no='+no+'&page='+curpage)

#로그인
def login(request):
    return render(request,'diary/login.html')

def login_ok(request):
    id = request.POST['id']
    pwd = request.POST['pwd']
    login_value = (id, pwd)
    data = models.login(login_value)
    print(data['result'])
    result=""
    if data['result'] == "OK":
        request.session['id'] = id
        request.session['name'] = data['name']
        result="OK"
    elif data['result'] == "NOID":
        result="NOID"
    elif data['result'] == "NOPWD":
        result="NOPWD"
    return render(request,'diary/login_ok_ok.html',{"result":result})

def logout(request):
    request.session['id'] = None
    return redirect('/diary/')

#회원가입
def signup(request):
    return render(request,'diary/signup.html')