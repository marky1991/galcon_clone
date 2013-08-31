function poll() {
    return $.ajax({
        type: "POST",
        url: "/chat/poll/",
        async: true,
        cache: false,
        timeout: 100000,
        success: function(data) {
            if (!$.isEmptyObject(data)) {
                var was_at_bottom = is_at_bottom($("#messages"));
                for (var i=0; i < data.length; i = i + 1) {
                    var color = name_to_color(data[i].author_name);
                    var text = "<div class='message'>" + "<span class='time'>" + data[i].post_date + "</span> ";
                    if (data[i].author_name !== "server") {
                        text = text + "<span>&lt;<a href='/users/" + data[i].author_name + "/' style='color: " + color + "'>" + data[i].author_name + "</a>&gt;: " + data[i].text + "</span>";
                    }
                    else {
                        if (data[i].text.indexOf("has joined") !== -1) {
                            var username = data[i].text.split(" ")[0];
                            $("<div><img style='padding-right: 5px; vertical-align: middle' src='/users/" + username + "/highest_flag/'/><a href='/users/" + username + "/" + "'>" + username + "</a></div>").appendTo($("#player_list"));
                        }
                        else if (data[i].text.indexOf("has left") !== -1) {
                            var username = data[i].text.split(" ")[0];
                            var to_remove = $("#player_list *:contains('" + username + "')");
                            to_remove.remove();
                        }
                        text = text + "<span style='color: #AAAAAA'>" + data[i].text + "</span>";
                    }
                    text = text + "</div>";                               

                    $("#messages").append($(text));
                }
                if (was_at_bottom) {
                    $("#messages").scrollTop($("#messages").prop("scrollHeight"));
                }
            }
            setTimeout(poll, 1000);
            return;
        },
        dataType: 'json'
    });
}


/*function sum_chars(chars) {
    var sum = 0;
    for (var index = 0; index < chars.length; index = index + 1) {
        sum = sum + chars.charCodeAt(index);
    }
    return (sum % 255).toString();
}

function name_to_color(name) {
    var char_count = name.length / 3;
    var r_chars = name.slice(0, Math.floor(char_count));
    var g_chars = name.slice(Math.floor(char_count), 2*Math.floor(char_count));
    var b_chars = name.slice(2*Math.floor(char_count), name.length);
    var color = "rgb(" + sum_chars(r_chars) + "," + sum_chars(g_chars) + "," + sum_chars(b_chars)+ ")";
    return color;
}*/
function HSV_to_RGB(h, s, v) {
    //Copied from http://www.cs.rit.edu/~ncs/color/t_convert.html
    //Because the version phil had was awful to read (It was so bad that I didn't know
    //how to fix it!)
    if (s == 0) {
        r = g = b = v;
    }
    else {
        var i = Math.floor(h * 6);
        var f = h * 6 - i;
        var p = v * (1 - s);
        var q = v * (1 - f * s);
        var t = v * (1 - (1 - f) * s);

        if (i === 0) {
            r = v;
            g = t;
            b = p;
        }
        else if (i === 1) {
            r = q;
            g = v;
            b = p;
        }
        else if (i === 2) {
            r = p;
            g = v;
            b = t;
        }
        else if (i === 3) {
            r = p;
            g = q;
            b = v;
        }
        else if (i === 4) {
            r = t;
            g = p;
            b = v;
        }
        else {
            r = v;
            g = p;
            b = q;
        }
    }
    console.log("RGB: ", r*255, g*255, b*255);
    return "#"+RGBtoHex(Math.floor(r*255),Math.floor(g*255),Math.floor(b*255));
}
function RGBtoHex(R,G,B) {
    return toHex(R)+toHex(G)+toHex(B);
}
function toHex(N) {
    if (N==null) {
        return "00";
    }
    N=parseInt(N);
    if (N==0 || isNaN(N)) {
        return "00";
    }
    N=Math.max(0,N);
    N=Math.min(N,255);
    N=Math.round(N);
    
    return "0123456789ABCDEF".charAt((N-N%16)/16) + "0123456789ABCDEF".charAt(N%16);
}
function name_to_color(name) {
    var i;
    name = name.toLowerCase();
    var val = 120;
    for (i=0; i < name.length; i = i + 1) {
        //Was originally 43
        val = val + name.charCodeAt(i)*20;
    }
    //Originally .65
    console.log(val, "val", name)
    return HSV_to_RGB((val%360)/360, 1.0, 0.85);
}

function is_at_bottom(object) {
    console.log($(object).scrollTop(), ($(object).prop("scrollHeight")) - $(object).height() - 2*parseInt($(object).css("padding")));
    console.log($(object).scrollTop() == ($(object).prop("scrollHeight") - $(object).height()  - 2*parseInt($(object).css("padding"))));
    return $(object).scrollTop() == ($(object).prop("scrollHeight") - $(object).height()  - 2*parseInt($(object).css("padding")));
}

function format_time(date) {
    var hour = date.getHours();
    if (hour >= 12) {
        var thingy = "p.m.";
    }
    else {
        var thingy = "a.m.";
    }
    hour = hour % 12;
    if (hour == 0) {
        hour = 12;
    }
    var minutes = date.getMinutes();
    return hour.toString() + ":" + ("00" + minutes.toString()).slice(-2) + " " + thingy;
}
