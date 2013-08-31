function set_time_cookie() {
    var date = new Date();
    document.time_cookie = "offset=" + (date.getTimezoneOffset()/60).toString() + ";";
}    
