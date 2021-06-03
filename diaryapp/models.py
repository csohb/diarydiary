from django.db import models
import cx_Oracle
# Create your models here.
def getConnection():
    try:
        conn=cx_Oracle.connect("hr/happy@localhost:1521/xe")
    except Exception as e:
        print(e)
    return conn

def shopCategoryList():
    conn=getConnection()
    cursor=conn.cursor()
    sql="""
        SELECT cno, title, type
        FROM diary_category
        """
    cursor.execute(sql)
    list=cursor.fetchall()
    cursor.close()
    conn.close()
    return list

def shopListData(cno,page):
    conn=getConnection()
    cursor=conn.cursor()
    rowSize=12
    start=(page*rowSize)-(rowSize-1)
    end=(page*rowSize)
    sql=f"""
        SELECT no,cno,thumb,title,brand,price,num
        FROM (SELECT no,cno,thumb,title,brand,price,rownum as num
        FROM (SELECT /*+ INDEX_ASC(diary, di_no_pk) */ no,cno,thumb,title,brand,price
        FROM diary WHERE cno={cno}))
        WHERE num BETWEEN {start} AND {end}
        """
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    conn.close()
    return data
def shopTotalPage(cno):
    conn = getConnection()
    cursor = conn.cursor()
    sql=f"SELECT CEIL(COUNT(*)/12.0) FROM diary WHERE cno={cno}"
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    conn.close()
    return data[0]

def shopDetail(no):
    conn=getConnection()
    cursor=conn.cursor()
    sql=f"""
        SELECT no,cno,thumb,brand,price,NVL(mileage, '포인트 적립 없음'),made,NVL(material, ' '),NVL(big, ' '),detail,title
        FROM diary
        WHERE no={no}
    """
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    conn.close()
    return data

#관련상품 추천하기 (랜덤)
def shopRecommend(cno):
    conn=getConnection()
    cursor=conn.cursor()
    sql=f"""
        SELECT no, cno, thumb,price,title,num
        FROM (SELECT no, cno, thumb,price,title,rownum as num
        FROM (SELECT no, cno, thumb,price,title
        FROM diary WHERE cno={cno}
        order by dbms_random.value))
        WHERE num BETWEEN 1 AND 6
    """
    cursor.execute(sql)
    data=cursor.fetchall()
    #print(data)
    cursor.close()
    conn.close()
    return data

#다이어리 리스트 불러오기
def myDailyList(page):
    conn=getConnection()
    cursor=conn.cursor()
    rowSize = 6
    start = (page * rowSize) - (rowSize - 1)
    end = (page * rowSize)
    sql=f"""
        SELECT no,title,thumb,NVL(heart, '0'),mood,regdate,name,num
        FROM (SELECT no,title,thumb,heart,mood,regdate,name,rownum as num
        FROM (SELECT no,title,thumb,heart,mood,regdate,name
        FROM daily ORDER BY no DESC))
        WHERE num BETWEEN {start} AND {end}
    """
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    conn.close()
    return data

#다이어리 총페이지
def myDailyTotalPage():
    conn = getConnection()
    cursor = conn.cursor()
    sql="SELECT CEIL(COUNT(*)/6.0) FROM daily"
    cursor.execute(sql)
    page=cursor.fetchone()
    cursor.close()
    conn.close()
    return page[0]

#다이어리 insert
def myDiaryInsert(insert_value):
    conn = getConnection()
    cursor = conn.cursor()
    sql="""
        INSERT INTO daily(no,title,content,pwd,name,regdate,mood)
        VALUES(
             (SELECT NVL(MAX(no)+1,1) FROM daily),:1,:2,:3,:4,SYSDATE,:6
        )
    """
    cursor.execute(sql,insert_value)
    #print("일기 입력 완료!")
    conn.commit()
    cursor.close()
    conn.close()

#다이어리 detail
def myDiaryDetail(no):
    conn = getConnection()
    cursor = conn.cursor()
    sql=f"""
        SELECT no,title,content,pwd,name,regdate,mood,NVL(heart, 0)
        FROM daily
        WHERE no={no}
    """
    cursor.execute(sql)
    md=cursor.fetchone()
    data=(md[0],md[1],md[2].read(),md[3],md[4],md[5],md[6],md[7])
    cursor.close
    conn.close()
    return data

# 다이어리 삭제
def mydiary_delete(delete_value):
    conn = getConnection()
    cursor = conn.cursor()
    no=delete_value[0]
    pwd=delete_value[1]
    sql=f"""
        SELECT pwd FROM daily
        WHERE no={no}
    """
    cursor.execute(sql)
    db_pwd=cursor.fetchone()
    print(db_pwd)
    cursor.close()
    result= False
    if db_pwd[0] == pwd:
        result = True
        cursor=conn.cursor()
        sql=f"""
            DELETE FROM daily
            WHERE no={no}
        """
        cursor.execute(sql)
        conn.commit()
        cursor.close()
    else:
        cursor=conn.cursor()
        result=False
        cursor.close()
        conn.close()
    return result

# 다이어리 수정
def mydiary_update(update_value):
    conn = getConnection()
    cursor = conn.cursor()
    #update_value=(no,title,content,pwd,name,mood)
    no=update_value[0]
    title=update_value[1]
    content=update_value[2]
    pwd=update_value[3]
    name=update_value[4]
    mood=update_value[5]
    ud=(name,title,content,mood,no)
    sql=f"""
        SELECT pwd FROM daily
        WHERE no={no}
    """
    cursor.execute(sql)
    db_pwd=cursor.fetchone()
    cursor.close()

    check = False
    if pwd == db_pwd[0]:
        check = True
        cursor=conn.cursor()
        sql="""
            UPDATE daily SET 
            name=:1,
            title=:2,
            content=:3,
            mood=:4
            WHERE no=:5
        """
        cursor.execute(sql,ud)
        conn.commit()
        cursor.close()
    else:
        check = False
    conn.close()
    return check

#로그인
def login(login_value):
    conn = getConnection()
    cursor = conn.cursor()
    id=login_value[0]
    pwd=login_value[1]
    result=""
    name=""
    sql=f"""
        SELECT COUNT(*) FROM D_MEMBER
        WHERE id='{id}'
    """
    cursor.execute(sql)
    idc=cursor.fetchone()
    cursor.close()
    if idc[0] == 0:
        result="NOID"
    else:
        cursor = conn.cursor()
        sql=f"""
            SELECT pwd,name FROM D_MEMBER
            WHERE id='{id}'
        """
        cursor.execute(sql)
        db_pwd=cursor.fetchone()
        if db_pwd[0] == pwd:
            result="OK"
            name=db_pwd[1]
            cursor.close()
        else:
            result="NOPWD"
            cursor.close()
    conn.close()
    data={"result":result,"name":name}
    return data

# 다이어리 하트 증기
def heart_up(no):
    conn = getConnection()
    cursor = conn.cursor()
    print(no)
    sql=f"""
        UPDATE daily SET
        heart=heart+1
        WHERE no={no}
    """
    cursor.execute(sql)
    conn.commit()
    print("하트 증가 완료")
    cursor.close()
    conn.close