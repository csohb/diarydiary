$(function(){
    $('#cartBtn').click(function(){
        let pno=$('#no').attr('no')
        let title=$('#title').attr('no')
        let price=$('#price').attr('no')
        let poster=$('#poster').attr('src')
        let amount=$('#amount').val()
        console.log('pno='+pno)
        console.log('title='+title)
        console.log('price='+price)
        console.log('poster='+poster)
        console.log('amount='+amount)
        $.ajax({
            url:'/diary/cart_ok/',
            type:'post',
            dataType:'json',
            data: {
                pno:pno,
                title:title,
                price:price,
                poster:poster,
                amount:amount
            },
            success:function(response){
                if(response.data == 'YES'){
                    alert('장바구니에 담기 완료!')
                    return
                }else{
                    alert('로그인이 필요합니다!')
                    return
                }
            }
        })
    })
})