/**
 * Created by tarena on 18-10-22.
 */
window.onload = function () {
	$('#bj').click(function(){
		$('#dz').html($('#bj').html())
	});
	$('#gz').click(function(){
		$('#dz').html($('#gz').html())
	});
	$('#hz').click(function(){
		$('#dz').html($('#hz').html())
	});
	$('#banner2').hide();

	var banner = document.getElementsByClassName('wrapper')[0];
	var imgs = banner.children;
	var imgNav = document.getElementsByClassName('imgNav')[0];
	var indInfo = imgNav.children;
	var imgIndex = 0; //初始下标
	var timer;
	timer = setInterval(autoPlay,2000);

	function autoPlay(){
		//设置元素隐藏与显示
		imgs[imgIndex].style.display = 'none';
		imgIndex = ++ imgIndex == imgs.length ? 0 : imgIndex;
		imgs[imgIndex].style.display = 'block';
		for (var i=0;i <indInfo.length;i++){
			indInfo[i].style.background = "gray";
		}

		//切换索引  切换背景色
		indInfo[imgIndex].style.background = 'gold';
	}
	banner.onmouseover = function(){
		clearInterval(timer);

	};
	banner.onmouseout = function(){
		timer = setInterval(autoPlay,2000);
	};
};


function check_login() {
    //向  /check_login/ 发送异步请求
    $.get('/check_login/',function (data) {
        var html = "";
        if (data.loginStatus == 0){
            html += '<a href="/login">[登录]</a>';
            html += "<a href='/register'>[注册,有惊喜]</a>";
            html += "  ";
            html += '<a href="/login">[登录后即可查看购物车]</a>'
        }else{
            html += "欢迎:"+data.uname;
            html += "<a href='/logout'>退出</a>";
            html += "  ";
            html += "<a href='/cart_views'>[购物车]</a>"
        }
        $('#login').html(html);
    },'json');
}

/* 加载所有的商品信息以及商品信息(每个分类取前10个)*/
function loadGoods() {
	$.get('/load_type_goods/',function (data) {
		//data 响应回来的JSON对象
		var show = '';
		$.each(data,function(i,obj){
			var jsonType = JSON.parse(obj.type);
			show += '<div class="item" style="overflow: hidden;">';
			show += '<p class="goodsClass">';
			show += "<img src='/"+jsonType.picture+"'>";
			show += "<a href='#'>更多</a>";
			show += '</p>';
			show += "<ul>";
            	var jsonGoods = JSON.parse(obj.goods);
            	$.each(jsonGoods,function (i,good) {
					//创建li
					show += '<li ';
					if ((i+1) % 5 == 0){
						show+="class='no-margin'";
					}
					show += '>';
						//拼 P 标记 表示商品的图片
						show += "<p>";
                    		show += "<img src='/"+good.fields.picture+"'>";
							show += "<div class='content'>";
                    		show += "<a href='javascript:add_cart("+good.pk+");'>";
                    		show += "<img src='/static/img/cart.png'>";
                    		show += "</a>";
                    		show += "<p>"+good.fields.title+"</p>";
                    		show += "<span>";
                    		show += "&yen;"+good.fields.price+"/"+good.fields.spec;
							show += "</span>";
							show += "</div>";
						//拼div标记 表示商品详细描述
					show += '</li>';

                });
            show += "</ul>";
			show += "</div>";
		});
		$('#main').html(show);
    },'json');
}


function add_cart(gid) {

    //1.验证登录账户,如果没有用户登录的话给出相应的提示

    $.get('/check_login/',function (data) {
        if (data.loginStatus == 0){
            alert('请登录');
        }else{
            //增加到购物车
            $.get('/add_cart',
                {'gid':gid},
                function (data) {
                if(data.status == 1){
                    alert(data.statusText);
                }else{
                    alert(data.statusText);
                }
            },'json');
        }
    },'json')
    //2...... ....

}

/**加载商品购物车*/
function del_g() {
    $('#del').on('click', function () {
        if (window.confirm('确定要删除该项吗?')) {
            $(this).parent().parent().remove();
        }
    });
}


$(function () {
    /*调用check_login 检查登录状态*/
    check_login();
	loadGoods();
	del_g()

});