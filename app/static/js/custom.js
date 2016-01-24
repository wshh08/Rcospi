/**
 * Created by wshh08 on 16-1-18.
 */
$("#login").find(".form").append('<span style="margin-left: 20px">Forget password? <a href="/auth/login">Click here.</a></span>');

function refresh() {
    //var now = moment().locale('zh-cn');
    var now = moment().locale('en');
    var current = now.format('MMM Do YYYY, HH:mm:ss');
    $(".moment_current").replaceWith('<span class="moment_current">'+current+'</span>');
}

setInterval("refresh()", 1000);
