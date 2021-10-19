function Confirm(room){
    //CSRF protection - https://flask-wtf.readthedocs.io/en/0.15.x/csrf/
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", $('input[name=csrf_token]').val())
            }
        }
    });
    var reservation = {
      date: $("#selectedDate").val(),
      time: $("#selectedTime").val(),
      room_number: room,
    }

    $.ajax({
      type: "POST",
      url: "/booking/confirm",
      data: JSON.stringify(reservation),
      contentType: "application/json",
      dataType: 'json',
      success: function(){
        //redirect to homepage if booking is success
        location.href = '/';
      },
      error: function(){
        //display message: something went wrong
      }   
    });
}