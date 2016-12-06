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

window.api = {
    get: function (url, data, success, fail, complete) {
        success = success || $.noop;
        fail = fail || $.noop;
        complete = complete || $.noop;
        return $.get(url, data).done(function (response, status, xhr) {
            if (response.code !== 0) {
                return fail(response.code, response.msg);
            } else {
                return success(response.data);
            }
        }).fail(function (xhr, errmsg, e) {
            return fail(-2, errmsg, e);
        }).always(complete);
    },
    post: function (url, data, success, fail, complete) {
        success = success || $.noop;
        fail = fail || $.noop;
        complete = complete || $.noop;
        return $.ajax({
            type: 'POST',
            url: url,
            data: JSON.stringify(data),
            contentType: 'application/json'
        }).done(function (response, status, xhr) {
            if (response.code !== 0) {
                return fail(response.code, response.msg);
            } else {
                return success(response.data);
            }
        }).fail(function (xhr, errmsg, e) {
            return fail(-2, errmsg, e);
        }).always(complete);
    }
};

window.expand = function (items){
    items.forEach(function(i){
        i.days_left = Math.floor((parseDate(i.end_time) - today) / 86400 / 1000)
    })
}

window.prune = function (items) {
    console.log(items[0].detail);
    items.forEach(function(i){
        i.detail.replace('&nbsp;', '');
    })
    console.log(items[0].detail);
}

window.parseDate = function (str){
    return new Date(str);
}

window.today =  new Date()
