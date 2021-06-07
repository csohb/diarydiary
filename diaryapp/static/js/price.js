$(function(){
    sum();
    let box=$('div[id^=cartUpBtn]')
    console.log(box)
    console.log(box.length)

        $('.pro-qty').click(function(){
            let pno=$(this).attr('pno')
            //console.log('pno='+pno)
            let amount=$('#amount_'+pno).val()
            //console.log('amount='+amount)
            let price=$('#price_'+pno).attr('value')
            //console.log('price='+price)
            total=amount*price
            //console.log(total)
            $('#total_'+pno).text(total)
            sum();
            //console.log('아아아아아아')
        })
})

function sum(){
    let box2=$('tr[id^=sum]')
    let final=0
    for(i =1; i<=box2.length; i++)
    {
        let total=Number($('#sum'+i).children('.cart__price').text())
        //console.log('total='+total)
        //console.log('i='+i)
        final+=total
    //console.log('final='+final)
    }

    $('#final').text(final)
}
// 주문번호 매개변수로 받음
function delsum(no){
    let before=$('#final').text();
    console.log("빼기전 가격="+before)
    let del=$('#total_'+no).text();
    console.log("뺄가격="+del)
    let after=before-del;
    console.log("나중가격="+after);
    $('#final').text(after);
}

$(document).on('click','#cancle',function(){
            let dno=$(this).attr('delete')
            console.log('삭제할 주문 번호='+dno)
            let tno=$(this).parents('.cart_tr').attr('id')
            console.log('tno='+tno)
            tno=tno.substring(3,tno.length)
            console.log(tno)
            delsum(dno);
            $('.tr_'+dno).remove()
             $.ajax({
                url:'/diary/cart_del/',
                type:'get',
                async:false,
                data:{
                    "no":dno
                },success:function(response){
                        console.log('삭제완료')
                }
            })
})

// 구매 -> 장바구니 완전 삭제
$(document).on('click','#orderBtn',function(){
    let id=$(this).attr('oid')
    $.ajax({
        url:'/diary/cart_order/',
        type:'get',
        async:false,
        data:{
            "id":id
        },success:function(response){
            console.log('주문완료')
            $('tr').remove();
            //location.href="/diary/"
            sum();
        }
    })
})
