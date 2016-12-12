



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
    debugger;
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
            callback(data);
        }
    )
}


// function krEncodeEntities(s){
// 		return $("<div/>").text(s).html();
// }
// function krDencodeEntities(s){
// 		return $("<div/>").html(s).text();
// }
