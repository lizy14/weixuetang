
// followings are for calendar

window.get_day = function(date) {
    day = date.getDay();
    if (day === 0) return 6;
    else return day - 1;
};

window.is_same_week = function(a, b) {
    day = get_day(b);
    if (a >= b) {
        if ((a - b)/1000/86400 < 7 - day) return true;
        else return false;
    }
    else if (a < b) {
        if ((b - a)/1000/86400 < day + 1) return true;
        else return false;
    }
    else return true;
};


window.schedule = function (items, num_dates, focus_day) {
    new_items = new Array(num_dates);
    for (var i = 0; i < num_dates; i++) {
        new_items[i] = [];
    }
    if (!items) return new_items;

    if (num_dates == 7) { // Schedule for week view
        items.forEach(function(i) {
            if (i.begin) { // curriculum
                d = parseDate(i.begin);
                if (!is_same_week(d, focus_day)) return;
                index = 0;
                i['start_time'] = {hour: d.getHours(), min: d.getMinutes(), day: get_day(d)};
                e = parseDate(i.end);
                i['end_time'] = {hour: e.getHours(), min: e.getMinutes(), day: get_day(e)};
            }
            else if (i.date) { // global events
                d = parseDate(i.date);
                if (!is_same_week(d, focus_day)) return;
                index = get_day(d);
            }
            else if (i.end_time) {  // homework
                d = i.end_time;
                if (!is_same_week(d, focus_day)) return;
                index = get_day(d);
            }
            else return;

            new_items[index].push(i);
        });
    }
    else {  // Schedule for month view
        month = focus_day.getMonth();
        items.forEach(function(i) {
            if (i.begin) { // curriculum
                d = parseDate(i.begin);
                if (d.getMonth() != month) return;
                index = d.getDate() - 1;

                i['start_time'] = {hour: d.getHours(), min: d.getMinutes()};
                e = parseDate(i.end);
                i['end_time'] = {hour: e.getHours(), min: e.getMinutes()};
            }
            else if (i.date) { // global events
                d = parseDate(i.date);
                if (d.getMonth() != month) return;
                index = d.getDate() - 1;
            }
            else if (i.end_time) {  // homework
                d = i.end_time;
                if (d.getMonth() != month) return;
                index = d.getDate() - 1;
            }
            else return;

            new_items[index].push(i);
        });
    }
    return new_items;
};

window.calculate_margin = function(day) {
    fst_day = get_day(new Date(day.getFullYear(), day.getMonth(), 1));
    lst_day = get_day(new Date(day.getFullYear(), day.getMonth()+1, 0));
    return {
        before:  fst_day,
        after: 6 - lst_day
    };
};

window.produce_course_block = function (data) {
    if (!data) return [];
    data.forEach(function(i){
        start = i.start_time;
        //alert(start[0] + ' ' + start[1]);
        i['top'] = (start.hour - 8)* 60 + start.min + 3;
        end = i.end_time;
        i['height'] = (end.hour - 8) * 60 + end.min - i['top'] - 17;
    });
};

window.produce_course_block_for_week = function (data) {
    if (!data) return [];
    data.forEach(function(i){
        start = i.start_time;
        //alert(start[0] + ' ' + start[1]);
        i['top'] = (start.hour - 8)* 60 + start.min + 18;
        end = i.end_time;
        i['height'] = (end.hour - 8) * 60 + end.min - i['top'] + 10;
    });
};

window.month_range = function(data) {
    year = data.getFullYear();
    month = data.getMonth();
    s = new Date(year, month, 1, 8).toISOString().substring(0,10);
    e = new Date(year, month+1, 0, 8).toISOString().substring(0,10);
    return {'start': s, 'end': e};
};

window.week_range = function(data) {
    year = data.getFullYear();
    month = data.getMonth();
    date = data.getDate();
    day = get_day(data);

    s = new Date(year, month, date-day, 8).toISOString().substring(0,10);
    e = new Date(year, month, date-day+7, 8).toISOString().substring(0,10);
    return {'start': s, 'end': e};
};
