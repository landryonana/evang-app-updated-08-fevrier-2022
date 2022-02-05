$(document).ready(function(){
    $(window).scroll(function () {
        if (this.scrollY > 60) {
          $("#nav-id").addClass("nav_sticky");
        } else if(this.scrollY < 60) {
          $("#nav-id").removeClass("nav_sticky");
        }
    });

    $('.sub-btn').click(function(){
      $(this).next('.sub-menu').slideToggle();
      $(this).find('.dropdown').toggleClass('rotate');
    });

    $('.menu-btn').click(function(){
        $('.side-bar').toggleClass('active');
        $('.logo').toggleClass('logo-visibility');
        $('.menu-btn').toggleClass('ico');
    });

    $('.block-empty').click(function(){
        $('.side-bar').removeClass('active');
        $('.menu-btn').removeClass('ico');
    })

  //================================MULTI SELECTE============================
//I needed the count of all checkboxes which are checked. Instead of writing a loop i did this
//$(".myCheckBoxClass:checked").length;
//$('#checkbox').is(':checked'); 
//var active = $('#modal-check-visible').prop("checked") ? 1 : 0 ;
    function getAllInputChecked() {
        var arr = [];
        $('input:checkbox:checked').not(this).each(function () {
            if ($(this).val() != 'on') {
              arr.push($(this).val());
            }
            
        });
        if (arr.length>1) {
          $('#selection').html(`${arr.length} selectionnés`);
        } else if (arr.length === 1) {
          $('#selection').html(`${arr.length} selectionné`);
        }else if (arr.length === 0) {
          $('#selection').html("");
        }
        return arr;
    }

    function getAllRadioInput() {
      var arr = [];
      $('input:checkbox').each(function () {
          if ($(this).val() != 'on') {
            arr.push($(this).val());
          }
          
      });
      return arr;
    }

    $('#action-toggle').click(function(){
      //on coche tous les input checkbox
      $('input:checkbox').not(this).prop('checked', this.checked);
      var arr = getAllInputChecked();
      if (arr.length>0) {
        $('#result_list tbody tr').css('background', '#e9c18b');
      } else {
        $('#result_list tbody tr').css('background', '#fff');
        $('#selection').html("");
      }
      
    });

    $('.action-select').click(function(){
      console.log($(this).is(":checked"));
      if ($(this).is(":checked")) {
        //on le décoche
        $('input#action-toggle:checked').prop("checked", 0);
        $(this).parent().parent().css('background', '#e9c18b'); 
      }else{
        $(this).parent().parent().css('background', '#fff'); 
      }
      //on récupère tous les inputs checkbox cocher
      var arr = getAllInputChecked();
      //on récupère tous les inputs checkbox
      var arrRadio = getAllRadioInput();
      //on vérifie s'il y'a pas de input cocher
      if (arr.length == 0) {
        //on vérifie si input#action-toggle est cocher
        if ($('input#action-toggle:checked').is(":checked")) {
          //on le décoche
          $('input#action-toggle:checked').prop("checked", 0);
          $('#result_list tbody tr').css('background', '#fff');
        }
      //on vérifie s'il le tableau des inputs checkbox cocher est égal au tableau de
      //tous les inputs checkbox sauf input#action-toggle
      }else if(arr.length == arrRadio.length){
        //on coche input#action-toggle
        $('input#action-toggle:checkbox').prop("checked", this.checked);
        $('#result_list tbody tr').css('background', '#e9c18b');
      }
    });
});