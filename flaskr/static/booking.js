
 
window.onload = function() {
    var dateControl = document.querySelector('input[type="date"]');
    var dateFormat = getDateFormat(new Date());
  
    dateControl.value = dateFormat;
    dateControl.min = dateFormat;
  
  
  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];
  
  var modal = document.getElementById("mdlBooking");
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
  };
  
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
  
  function setModalContent(obj){
    document.getElementById("mdlBooking").style.display = "block";
    var date = document.getElementById("selectedDate").value
    var timeSelect = document.getElementById("selectedTime")
  
    var room = obj.id
    document.getElementById("mdlDate").value = date
    document.getElementById("mdlTime").value = timeSelect.value
    document.getElementById("room").value = room
  }