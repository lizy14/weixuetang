window.BIND_LANDING = "/u/bind";



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



window.prune = function (items) {
    items.forEach(function(i){
        i.detail.replace('&nbsp;', '');
    });
};


window.parseDate = function (stamp){
    return new Date(stamp * 1000);
};

window.datify = function (obj){
    function datify_obj(obj){
        for(var key in obj) {
            if(key.endsWith('_time') && !key.startsWith('s_')){
                obj[key] = parseDate(obj[key]);
            }
        }
        return obj;
    }
    if (obj instanceof Array){
        return obj.map(datify_obj);
    }else if(typeof obj == 'object'){
        return datify_obj(obj);
    }
};
Date.prototype.readable = function(time) {
    var mm = this.getMonth() + 1;
    var dd = this.getDate();
    var yy = this.getFullYear();
    var h = this.getHours();
    h = h >= 10 ? h : "0" + h;
    var m = this.getMinutes();
    m = m >= 10 ? m : "0" + m;

    if (time) {
        return yy + '-' + mm + '-' + dd + ' ' + h + ':' + m;
    } else {
        return yy + '-' + mm + '-' + dd;
    }
};

Date.prototype.days_left = function(){
    var ddl = this;
    // 北京时间当天零点 -> 北京时间当天 23:59
    ddl = new Date(ddl.getTime() + 86400 * 1000);
    return Math.floor((ddl - today) / 86400 / 1000);
};

window.today =  new Date();

window.getJSON = function(url, payload, callback, err_callback){
    payload = $.extend(payload, window.urlParam);
    var wrapped_err = function(err){
        if(err_callback){
            err_callback(err);
        }else{
            alert("加载失败 " + (err.statusText || err.status || err.msg || err.code || ""));
        }
    };
    $.getJSON(
        url,
        payload,
        function(data){
            if(data.code !== 0){
                wrapped_err(data);
            }
            if(data.code === 0){
                data.data = datify(data.data);
            }
            if(callback){
                callback(data);
            }
        }
    ).fail(wrapped_err);
};
window.postForm = function(url, payload, callback){
    payload = $.extend(payload, window.urlParam);
    $.post(
        url,
        payload,
        function(data){
            if(data.code === 0){
                data.data = datify(data.data);
            }
            if(callback){
                callback(data);
            }
        }
    );
};
