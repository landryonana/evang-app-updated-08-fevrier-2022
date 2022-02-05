$(function() {

    $('#btn-search').click(function() {
        $('.search-form').toggleClass('active');
    })

    
    $('#btn-load-user-form').click(function(){
        $.ajax({
            url: $(this).attr("data-url"),
            type:'get',
            dataType:'json',
            beforeSend:function(){
                $("#modal-form .modal-content").html("");
                $('#modal-form').modal('show');
            },
            success:function(data){
                $("#modal-form .modal-content").html(data.html_form);
            }
        })
    });
//==========================rechercher bar================
    $('#empty-result').html('');
    $('#query').keyup(function(){
        var input = $(this).val();
        query = {
            name:$(this).attr('name'),
            value:$(this).val()
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
                    $('#result_list tbody').html(data.users);
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
                    $('#result_list tbody').html(data.users);
                    $('#result-search').html("");
                }
            })
        }
        
    })
    
})