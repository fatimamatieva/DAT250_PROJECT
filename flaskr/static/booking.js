
 
window.onload = function() {
    var dateControl = document.querySelector('input[type="date"]');
    var dateFormat = getDateFormat(new Date());
  
    dateControl.value = dateFormat;
    dateControl.min = dateFormat;
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