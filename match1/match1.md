# 猿人学第一题
```
获取五页机票的价格，计算平均值
```
## 抓包分析
1. 打开浏览器的调试器，会自动调用setInterval方法无限的执行debugger命令，阻止调试，在浏览器里可以右键那一行选择"never pause here"，也可以用hook的方法，把setInterval方法设置为空
```javascript
(function () {
    
    _setInterval = setInterval;
    setInterval = function () { };
})();
```
2. 点击第二页，可以看到api/match/1这个请求里获取了需要的数据，检查请求的cookie会发现没有什么特别的内容，在请求的参数里，除了有一个page参数外，还有一个m参数，这个参数看起来像是加密过的一个值再拼接上一个“|”和时间戳。
3. 再点击其他页面，发现这个参数是不断变化的，看起来这个就是关键参数了，基本上就能确定这个请求就只需要构造一个参数就可以了
---
## 参数构造方法
查看这个请求的调用栈，会找到它调用了一个request方法，点击进去，就能看到这样一段代码
```javascript
request = function () {
    var timestamp = Date.parse(new Date()) + 100000000;
    var m = oo0O0(timestamp.toString()) + window.f;
    var list = {
        "page": window.page,
        "m": m + '丨' + timestamp / 1000
    }
```
上面这段里面直接就写明了m是`oo0O0()`这个方法对一个时间戳进行操作之后加上`window.f`得到的值再和“|"和时间戳/1000拼接得到的
在`oo0O0()`这个方法上下个断点，再重新请求一下，就能找到这个方法的定义，接下来就是扣代码的环节啦。

把`oo0O0()`这个方法抠下来后，会发现这个函数返回的是一个空字符串，也就是说m其实就是`window.f`，但是搜一下这个参数，会发现代码里没有直接写出来是在哪里生成的，这时候就要用到hook大法了，在最开始执行js代码的地方下个断点，然后在控制台执行一下下面的代码
```javascript
(function () {
    'use strict';
    Object.defineProperty(window, 'f', {
        set: function (data) {   
            debugger;
            return data;
        }
    });
})()
```
再执行代码，当`window.f`被赋值的时候，就会自动断点下来，然后就会看到，生成`window.f`的代码是在一个VM开头的js虚拟机文件里的，这一段代码就没有什么混淆了，很清楚就是把时间戳做了一次md5加密，而且加密的方法也在里面了，直接扣！
把抠出来的代码修改一下，把全局变量替换掉，然后把`window.f`改成一个方法生成并返回值，以便调用
```javascript
function get_f(timestamp){
	f = hex_md5(timestamp);
	return f;
}
```
剩下就是写代码了，可以用execjs这个包调用js代码或者用node.js的后端框架来调用，因为这里没有速度要求，所以直接就用execjs调用就完事了
这里还有个坑就是拼接`m`的“|”是中文的，在请求里可以看到这个“|”是被转码过的，直接把转码后的内容复制出来拼接就好了。


