

$(function() {
    //setting default value, and minimum date. 
    var dateControl = $('input[type="date"]');
    var dateFormat = getDateFormat(new Date());
    dateControl.val(dateFormat);
    dateControl.attr('min',dateFormat);
});
  
function getDateFormat(date){
  var day = date.getDate(),
      month = date.getMonth() + 1;
  if (day.toFixed().length == 1){
    day = '0' + day;
  }
  if (month.toFixed().length == 1){
    month = '0' + month;
  }
  return date.getFullYear() + '-' + month + '-' + day
}

function Confirm(room){

  var confirmbox = $("#confirmBox");
  var span = $(".close")[0];

// when the user clicks anywhere outside of the modal or clicks on the close btn, close it
  span.onclick = function() {
    closeConfirmBox(confirmbox);
  }
  window.onclick = function(event) {
    if (event.target == confirmbox[0]) {
      closeConfirmBox(confirmbox[0]);
    }
  }

  confirmbox.show();
  $(".confirm-text>span").html(room)

  $("#btnConfirm").on("click", function(ev){
    ev.preventDefault();
    var reservation = {
      date: new Date($("#selectedDate").val()),
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
        closeConfirmBox(confirmbox[0]);
      }
    });
  });
}

function closeConfirmBox(elem){
  //hide confirmbox and turn off event-listner
  $(elem).hide();
  $(elem).find("#btnConfirm").off("click");
}