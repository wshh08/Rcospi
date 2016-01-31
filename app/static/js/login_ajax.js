/**
 * Created by wshh08 on 16-1-25.
 */

var email_str = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/; //Email regular expression
var sa = '0';

function pre_login() {
    var email = $('#email-login').val();
    if (email_str.test(email)) {
        alert(email);
        $.ajax({
            type: "POST",
            url: "/ajax/pre_login",
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({"email": email}), //"hash": hash}),
            beforeSend: function () {},
            success: function (data) {
                if (data.result) {
                    sa = data.sa;
                    alert(sa);
                }
                else {
                    alert('Invalid Email!!');
                }
            },
            complete: function () {},
            //success：当请求成功时调用函数，即status==200;
            //complete：当请求完成时调用函数，即status==404、403、302...只要不出错就行。
            error: function () {}
        });
    }
}

function login_clicked() {
    var bcrypt = dcodeIO.bcrypt;
    var email = $('#email-login').val();
    var password = $('#password-login').val();
    //var result = false;
    if (email == "" || password == "") {
        alert("用户名或密码不能为空！");
        return false;
    }
    else if (!email_str.test(email)) {
        alert("邮件地址格式不正确!");
        return false;
    }
    else {
        if (sa=='0') {
            pre_login();
        }
        var ha = bcrypt.hashSync(password, sa);
        $.ajax({
            type: "POST",
            url: "/ajax/login",
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({"email": email,
                "ha": ha}), //"hash": hash}),
            beforeSend: function () {
                //$("#loading").css("display", "block"); //点击登录后显示loading，隐藏输入框
                //$("#login").css("display", "none");
            },
            success: function (data) {
                if (data.result) {
                    window.location.reload();
                }
                //bcrypt.compare(password, data.ha, function (err, res) {
                //    if (res==true) {
                //        result = true;
                //        alert("登录成功");
                //        window.location.reload();
                    //}
                    //else {
                    //    result = false;
                    //    alert("密码或用户名错误,登录失败");
                        //console.log(bcrypt.hashSync(password, data.ha));
                    //}
                    //alert('email: ' + data.email + '\n' + 'hash: ' + hash +
                    //'\n' + 'Check result: ' + bcrypt.compareSync(password, data.hash));
                    //$("#loading").hide(); //隐藏loading
                    //if (data == "success") {
                    //parent.tb_remove();
                    //parent.document.location.href = "admin.htm"; //如果登录成功则跳到管理界面
                    //parent.tb_remove();
                    //}
                    //if (data == "fail") {
                    //    alert("登录失败！");
                    //}
            },

            complete: function () {
                //$("#loading").css("display", "none"); //点击登录后显示loading，隐藏输入框
                //$("#login").css("display", "block");
            },
            error: function (XMLHttpRequest, textStatus, thrownError) {
            }
        });
    }
}

$().ready(function () {
    $('#button-login').click(login_clicked);  //login不能带括号,不然只会在页面载入时执行一次,后续不起作用.
    $('#email-login').blur(pre_login);
    });
