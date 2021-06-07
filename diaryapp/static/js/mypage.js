$(function(){
    $('#heartTable').hide()
    $('#orderTable').hide()
    $('.notyet').hide()
    let mno=$('.th').attr('mno')
    console.log(mno)
    for(i=mno; i>=1; i--){
        let no=$('#mood_'+i).attr('no')
        console.log('no='+no)
        url=['1.gif','2.gif','3.gif','4.png','5.gif','6.gif','7.gif','8.gif','9.gif','10.gif',
        '11.gif','12.jpg','13.png','14.gif','15.gif','16.gif','17.gif','18.gif','19.gif']
        mood=['쓸쓸','열일','휴식','행복','음악','질주본능','그리움','고독','한잔','우울','혼자','사랑','짜증','고뇌','설렘','여행','평화','비옴','지침']
        let img=url[Number(no)-1]
        $('#mood_'+i).attr('src','/static/images/mood/'+img);
    }
})
$(document).on('click','#order',function(){
    $('.notyet').show()
    $('#diaryTable').hide()
    $('#heartTable').hide()
    $('#orderTable').show()
})

$(document).on('click','#mydiary',function(){
    $('.notyet').hide()
    $('#orderTable').hide()
    $('#heartTable').hide()
    $('#diaryTable').show()
})

$(document).on('click','#mypageCancle',function(){
    let id = $('#mypageCancle').attr('cid')
    $.ajax({
        url:'/diary/order_del/',
        type:'get',
        data:{
            'id':id
        },success:function(response){
            console.log('삭제완료')
            $('#orderTable').remove();
            $('.notyet').show()
        }
    })
})

$(document).on('click','#orderGo',function(){
    location.href='/diary/shop/'
})
