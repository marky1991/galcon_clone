function localize_time(time_string) {
    var date = new Date(time_string);
    var dummy_date = new Date();
    date = date + dummy_date.getTimezoneOffset()/60;
    return date.toString();
}
