



function getQueryParams(qs) {
    qs = qs.split('+').join(' ');

    var params = {},
        tokens,
        re = /[?&]?([^=]+)=([^&]*)/g;

    while ((tokens = re.exec(qs))) {
        params[decodeURIComponent(tokens[1])] = decodeURIComponent(tokens[2]);
    }

    return params;
}

window.urlParam = getQueryParams(document.location.search);

window.dftFail = function (errno, errmsg, e) {
    alert("加载失败: [" + errno + "] " + errmsg + " " + e + "\n请重试");
};

window.expand = function (items){
    items.forEach(function(i){
        i.days_left = Math.floor((parseDate(i.end_time) - today) / 86400 / 1000);
    });
};

window.prune = function (items) {
    items.forEach(function(i){
        i.detail.replace('&nbsp;', '');
    });
};

window.parseDate = function (str){
    d = new Date(str);
    d.setHours(23);
    d.setMinutes(59);
    return d;
};

window.today =  new Date();

window.getJSON = function(url, payload, callback){
    payload = $.extend(payload, window.urlParam);
    $.getJSON(
        url,
        payload,
        function(data){
            if(data.code == 10){ // UnbindError
                var BIND_LANDING = "/u/bind";
                if (location.pathname != BIND_LANDING) {
                    alert('先绑定 info 账号才可以哦 :(');
                    location.href = BIND_LANDING + location.search;
                }
            }
            if(callback){
                callback(data);
            }
        }
    )
}

window.schedule = function (items, num_dates, month) {
    new_items = new Array(num_dates);
    items.forEach(function(i) {
        if (i.begin) {
            d = parseDate(i.begin);
            if (d.getMonth() != month) return;
            index = d.getDate() - 1;
        }
        else if (i.date) {
            d = parseDate(i.date);
            if (d.getMonth() != month) return;
            index = d.getDate() - 1;
        }
        else if (i.end_time) {
            d = parseDate(i.end_time);
            if (d.getMonth() != month) return;
            index = d.getDate() - 1;
        }
        else return;

        if (new_items[index]) {
            new_items[index].push(i);
        }
        else {
            new_items[index] = new Array();
            new_items[index].push(i);
        }
    });
    return new_items;
}

window.calculate_margin = function(day) {
    return {
        before: new Date(day.getYear()+1900, day.getMonth(), 1).getDay() - 1,
        after: 7 - new Date(day.getYear()+1900, day.getMonth()+1, 0).getDay()
    }
}

window.postForm = function(url, payload, callback){
    payload = $.extend(payload, window.urlParam);
    $.post(
        url,
        payload,
        function(data){
            if(data.code == 10){ // UnbindError
                var BIND_LANDING = "/u/bind";
                if (location.pathname != BIND_LANDING) {
                    alert('先绑定 info 账号才可以哦 :(');
                    location.href = BIND_LANDING + location.search;
                }
            }
            if(callback){
                callback(data);
            }
        }
    )
}

window.produce_course_block = function (data) {
    data.forEach(function(i){
        start = i.start_time.split(':');
        //alert(start[0] + ' ' + start[1]);
        i['top'] = parseInt(start[0]-8) * 60 + parseInt(start[1]) + 3;
        end = i.end_time.split(':');
        i['height'] = parseInt(end[0]-8) * 60 + parseInt(end[1]) - i['top'] - 17;

    });
}

window.month_range = function(date) {
    year = today.getYear() + 1900;
    month = today.getMonth();
    s = new Date(year, month, 1, 8).toISOString().substring(0,10);
    e = new Date(year, month+1, 0, 8).toISOString().substring(0,10);
    return {'start': s, 'end': e}
}

window.week_range = function(data) {
    // TODO
    year = today.getYear() + 1900;
    day = today.getMonth();
    s = new Date(year, month, 1, 8).toISOString().substring(0,10);
    e = new Date(year, month+1, 0, 8).toISOString().substring(0,10);
    return {'start': s, 'end': e}
}

// function krEncodeEntities(s){
// 		return $("<div/>").text(s).html();
// }
// function krDencodeEntities(s){
// 		return $("<div/>").html(s).text();
// }
