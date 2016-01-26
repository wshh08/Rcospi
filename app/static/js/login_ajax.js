/**
 * Created by wshh08 on 16-1-25.
 */

var email_str = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/; //Email regular expression

$().ready(function () {
        $('#button-login').click(function () {
            var email = $('#email').val();
            var password = $('#password').val();
            if (email == "" || password == "") {
                alert("用户名或密码不能为空！");
                return false;
            }
            else if (!email_str.test(email)) {
                //alert(email);
                alert("邮件地址格式不正确!");
                return false;
            }
            else {
                //alert(password);
                $.ajax({
                    type: "POST",
                    url: "/auth/ajax/login",
                    dataType: 'json',
                    contentType: 'application/json',
                    //data: "email=" + encodeURIComponent(email) + "&password=" + encodeURIComponent(password),
                    data: JSON.stringify({"email": email,
                           "password": password}),
                    beforeSend: function () {
                        //$("#loading").css("display", "block"); //点击登录后显示loading，隐藏输入框
                        //$("#login").css("display", "none");
                    },
                    success: function (msg) {
                        alert('email: ' + msg.email + '\n' + 'password: ' + msg.password);
                        //$("#loading").hide(); //隐藏loading
                        //if (msg == "success") {
                            //parent.tb_remove();
                            //parent.document.location.href = "admin.htm"; //如果登录成功则跳到管理界面
                            //parent.tb_remove();
                        //}
                        //if (msg == "fail") {
                        //    alert("登录失败！");
                        //}
                    },
                    complete: function (data) {
                        //$("#loading").css("display", "none"); //点击登录后显示loading，隐藏输入框
                        //$("#login").css("display", "block");
                    },
                    error: function (XMLHttpRequest, textStatus, thrownError) {
                    }
                });
            }
        });
    });