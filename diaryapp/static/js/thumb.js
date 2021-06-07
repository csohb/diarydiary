 $(function(){
        let mno=$('.bg').attr('mno')
        //console.log('mno='+mno)
        for(i=mno; i>=1; i--){
            let no=$('#mood_'+i).attr('no')
        url=['1.gif','2.gif','3.gif','4.png','5.gif','6.gif','7.gif','8.gif','9.gif','10.gif',
        '11.gif','12.jpg','13.png','14.gif','15.gif','16.gif','17.gif','18.gif','19.gif']
        mood=['쓸쓸','열일','휴식','행복','음악','질주본능','그리움','고독','한잔','우울','혼자','사랑','짜증','고뇌','설렘','여행','평화','비옴','지침']
        let img=url[Number(no)-1]
        let print=mood[Number(no)-1]
        //console.log(print)
        $('#mood_'+i).attr('src','/static/images/mood/'+img);
        $('#print_'+i).text(print)
        }
 })