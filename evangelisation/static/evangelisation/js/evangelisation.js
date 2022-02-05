$(function() {
    

    //==========================rechercher bar================
    $('#empty-result').html('');
    $('#query').keyup(function(){
        var input = $(this).val();
        query = {
            name: $(this).attr('name'),
            value: $(this).val()
        }
        if(input.length>0){
            $.ajax({
                url: $(this).attr("data-url"),
                type:'get',
                dataType:'json',
                data: query,
                beforeSend:function(){
                    $('#spinner').addClass('active');
                },
                success:function(data){
                    $('#spinner').removeClass('active');
                    $('#person-evang tbody').html(data.models);
                    console.log(data.models)
                    $('#result-search').html(data.counter_str);
                    if (data.counter == 0) {
                        $('#empty-result').html(data.empty_result);
                    } else {
                        $('#empty-result').html('');
                    }
                }
            });
        }else{
            $.ajax({
                url: $(this).attr("data-url"),
                type:'get',
                dataType:'json',
                beforeSend:function(){
                    $('#spinner').addClass('active');
                },
                success:function(data){
                    $('#spinner').removeClass('active');
                    $('#person-evang tbody').html(data.models);
                    $('#result-search').html("");
                }
            })
        }
        
    });


    $(".btn-ajax-operations").click(()=>{
        $('#modal-form').modal('show');
        console.log("======= : ",$(this).attr('data-url'));
    });


});