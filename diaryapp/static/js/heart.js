$(document).on('click','#heartBtn',function(){
    let hno=$(this).attr('hno')
    $.ajax({
        url:'/diary/heart/',
        type:'get',
        data:{
            'no':hno
        },success:function(response){
            let heart=response.heart
            console.log('heart='+heart)
            console.log('하트증가 완료')
            $('#heartArea').text(heart+' hearts')
        }
    })
})