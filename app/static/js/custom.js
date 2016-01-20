/**
 * Created by wshh08 on 16-1-18.
 */
function refresh() {
    //var now = moment().locale('zh-cn');
    var now = moment().locale('en');
    var current = now.format('MMM Do YYYY, HH:mm:ss');
    $(".moment_current").replaceWith('<span class="moment_current">'+current+'</span>');
}

setInterval("refresh()", 1000);
