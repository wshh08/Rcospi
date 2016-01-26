/**
 * Created by wshh08 on 16-1-18.
 */

$("#form-login").find(".form").append('<span style="margin-left: 20px">Forget password? <a href="/auth/login">Click here.</a></span>');

 /* center modal */
//function centerModals() {
//    $('#modal-login').each(function () {
//        var $clone = $(this).clone().css('display', 'block').appendTo('body');
//        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
//        //var top = ($(document).height() -$('#modal-login').height()) / 2;
//        top = top > 0 ? top : 0;
//        $clone.remove();
//        $(this).find('.modal-content').css("margin-top", top);
//    });
//}
//$('#modal-login').on('show.bs.modal', centerModals);
//$(window).on('resize', centerModals);

$('#nav-login').click(function() {
    $('#modaltabs').find('li:eq(0)').find('a').tab('show');
});
$('#nav-register').click(function() {
    $('#modaltabs').find('li:eq(1)').find('a').tab('show');
});

function refresh() {
    //var now = moment().locale('zh-cn');
    var now = moment().locale('en');
    var current = now.format('MMM Do YYYY, HH:mm:ss');
    $(".moment_current").replaceWith('<span class="moment_current">'+current+'</span>');
}
setInterval("refresh()", 1000);
