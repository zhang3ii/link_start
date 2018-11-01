/**
 * Created by tarena on 18-10-22.
 */
$(function () {
    //表示手机号是否已经被注册的一个状态值
    // var registerStatus = 1;
    window.registerStatus = 1;
   /***1.为uphone控件绑定blur事件*/
    $("#uu").blur(function () {
        //如果文本框内没有任何东西返回
        if($(this).val().trim().length == 0)
            return;
        //如果文本框内有数据的话则发送ajax请求判断数据是否存在
        $.get(
            '/check_uphone/',
            {'uphone':$(this).val()},
            function (data) {
                $("#err").html(data.msg);
                window.registerStatus = data.status;
            },'json'
        );

     });
    /* 2.为formReg 表单元素绑定submit 事件*/
    $('#formReg').submit(function () {
        // 判断registStatus的值,决定表单是否提交
        if (window.registerStatus == 1)
            return false;
        return true;
    });
});