from django.shortcuts import render,redirect
from diaryapp import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
def diary_home(request):
    try:
        id=request.session['id']
        name=request.session['name']
    except:
        id=None
        name=None
    #print(id)
    return render(request,'diary/home.html',{"id":id})

def diary_shop(request):
    try:
        id = request.session['id']
        name = request.session['name']
    except:
        id = None
        name = None
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
            "totalpage":totalpage,"startPage":startPage,"endPage":endPage,"cno":curcno,"curpage":curpage,"range":range(startPage,endPage+1)})

def diary_detail(request):
    try:
        id = request.session['id']
        name = request.session['name']
    except:
        id = None
        name = None
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
    try:
        id = request.session['id']
        name = request.session['name']
    except:
        id = None
        name = None
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
    return render(request,'diary/mydiary.html',{"list":list,"curpage":curpage,"totalpage":totalpage,"startPage":startPage,"endPage":endPage,"range":range(startPage,endPage+1)})

def myDiaryRecord(request):
    try:
        id = request.session['id']
        name = request.session['name']
    except:
        id = None
        name = None
    return render(request,'diary/record.html',{"id":id,"name":name})

def myDiaryRecordOk(request):
    #title,content,pwd,name,regdate,mood
    try:
        id=request.session['id']
    except:
        id=None
    title=request.POST['subject']
    content=request.POST['msg']
    pwd=request.POST['pwd']
    name=request.POST['name']
    mood=request.POST['mood']
    print(title,content,pwd,name,mood)
    insert_value=(title,content,pwd,name,mood,id)
    models.myDiaryInsert(insert_value)
    return redirect('/diary/mydiary/?page=1')

def myDiaryDetatil(request):
    try:
        id = request.session['id']
        name = request.session['name']
    except:
        id = None
        name = None
    no=request.GET['no']
    try:
        page=request.GET['page']
        curpage=int(page)
    except:
        curpage=1
    data=models.myDiaryDetail(int(no))
    #no,title,content,pwd,name,regdate,mood,heart
    detail={"no":data[0],"title":data[1],"content":data[2],"pwd":data[3],"name":data[4],"regdate":data[5],"mood":data[6],"heart":data[7]}
    return render(request,'diary/mydiary_detail.html',{"detail":detail,"curpage":curpage})



# 일기 삭제
def mydiaryDelete(request):
    try:
        id = request.session['id']
        name = request.session['name']
    except:
        id = None
        name = None
    no=request.GET['no']
    return render(request,'diary/mydiary_delete.html',{"no":no,"id":id})

def mydiaryDeleteOK(request):
    try:
        id = request.session['id']
        name = request.session['name']
    except:
        id = None
        name = None
    no=request.POST['no']
    pwd=request.POST['pwd']
    delete_value=(no,pwd)
    result=models.mydiary_delete(delete_value)
    return render(request,'diary/mydiary_delete_ok.html',{"result":result,"id":id})

#일기 수정
def myDiaryUpdate(request):
    try:
        id = request.session['id']
        name = request.session['name']
    except:
        id = None
        name = None
    no=request.GET['no']
    data=models.myDiaryDetail(int(no))
    #no,title,content,pwd,name,regdate,mood,heart
    detail={"title":data[1],"content":data[2],"pwd":data[3],"name":data[4],"mood":data[6],}
    return render(request,'diary/mydiary_update.html',{"no":no,"detail":detail,"id":id})

def myDiaryUpdateOK(request):
    try:
        id = request.session['id']
        name = request.session['name']
    except:
        id = None
        name = None
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
    heart=models.heart_up(int(no))
    result={
        'result':'success',
        'heart':heart
    }
    return JsonResponse(result)

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

def signup_ok(request):
    id=request.POST['id']
    name=request.POST['name']
    email=request.POST['email']
    pwd=request.POST['pwd']
    sex=request.POST['sex']
    tel=request.POST['tel']
    signup_data=(id,name,email,pwd,sex,tel)
    models.signup(signup_data)
    return redirect('/diary/')


def checkid(request):
    id=request.GET['id']
    print(id)
    try:
        check=models.idcheck(id)
    except Exception as e:
        print(e)
    result={
        'result':'success',
        'data':'not exist' if check is "YES" else "NO"
    }
    return JsonResponse(result)
def checkemail(request):
    email=request.GET['email']
    print(email)
    try:
        check=models.emailcheck(email)
    except Exception as e:
        print(e)
    result={
        'result':'success',
        'data':'not exist' if check is "YES" else "NO"
    }
    return JsonResponse(result)

def checktel(request):
    tel=request.GET['tel']
    try:
        check=models.telcheck(tel)
    except Exception as e:
        print(e)
    result={
        'result':'success',
        'data':'not exist' if check is "YES" else "NO"
    }
    return JsonResponse(result)

@csrf_exempt
def cart_ok(request):
    #no,pno,title,amount,price,poster,id
    pno=request.POST['pno']
    title=request.POST['title']
    amount=request.POST['amount']
    price=request.POST['price']
    poster=request.POST['poster']
    try:
        id = request.session['id']
    except:
        id = None
    cart_value = (pno, title, amount, price, poster, id)
    print(cart_value)
    try:
        check=models.cartAdd(cart_value)
        print(check)
    except Exception as e:
        print(e)
    result={
        'result':'success',
        'data':'YES' if check is "YES" else 'NO'
    }
    return JsonResponse(result)

#장바구니 띄우기
def cart(request):
    try:
        id = request.session['id']
    except Exception as e:
        print(e)
    list=[]
    data=models.cartInfo(id)
    #no,pno,title,amount,poster,price
    for row in data:
        price=row[5]
        price=price[:-1]
        price=int(price.replace(',',''))
        print(price)
        amount=row[3]
        total=price*amount
        cd={"no":row[0],"pno":row[1],"title":row[2],"amount":row[3],"poster":row[4],"price":price,"total":total}
        list.append(cd)
    return render(request,'diary/cart.html',{"list":list,"id":id})

#장바구니 삭제
@csrf_exempt
def cartDel(request):
    no=request.GET['no']
    print(no)
    check=models.cartDelete(no)
    print('view='+check)
    result={
        'result': 'success',
        'data': 'YES' if check is 'YES' else 'NO'
    }
    return JsonResponse(result)

#주문하기
def cart_to_order(request):
    id=request.GET['id']
    print(id)
    models.cartToOrder(id)
    result={
        'result':'success',
    }
    return JsonResponse(result)

def mypage(request):
    id = request.session['id']
    oList = models.orderList(id)
    list = []
    # no,pno,title,amount,poster,price
    for row in oList:
        ol = {"no": row[0], "pno": row[1], "title": row[2], "amount": row[3], "poster": row[4], "price": row[5]}
        list.append(ol)
    dList = models.mypageDiaryList(id)
    DList = []
    # no,title,heart,regdate,mood
    for row in dList:
        dl = {"no": row[0], "title": row[1], "heart": row[2], "regdate": row[3], "mood": row[4]}
        DList.append(dl)
    return render(request,'diary/mypage.html',{"id":id,"list":list,"DList":DList})

def mypageOrderList(request):
    id = request.session['id']
    oList = models.orderList(id)
    list = []
    # no,pno,title,amount,poster,price
    for row in oList:
        ol = {"no": row[0], "pno": row[1], "title": row[2], "amount": row[3], "poster": row[4], "price": row[5]}
        list.append(ol)
    json_oList = json.dumps(list)
    data={
        'oList':json_oList
    }
    return JsonResponse(data)

def mypageDList(request):
    id = request.session['id']
    dList=models.mypageDiaryList(id)
    list=[]
    # no,title,heart,regdate,mood
    for row in dList:
        dl={"no":row[0],"title":row[1],"heart":row[2],"regdate":row[3],"mood":row[4]}
        list.append(dl)
    json_dList=json.dumps(list)
    data={
        'dList':json_dList
    }
    return JsonResponse(data)

def orderDelete(request):
    id=request.session['id']
    models.mypageOrderListDelete(id)
    data={
        'result':'success'
    }
    return JsonResponse(data)