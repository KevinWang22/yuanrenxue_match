// main文件，做一个简易后台，接收request，调用dm_decrypt解析，并返回解析后的数据

// 导入依赖包，express用于创建应用；body-parser用于处理请求
var express = require('express')
var bodyParser = require('body-parser')

// 导入抠出来的js文件
// require写的是文件路径
var encrypt = require('./match4')

// 创建应用实例
var app = express()


// 使用 body-parser 中间件
// urlencoded和json，分别处理表单提交和json格式的请求体，只支持utf-8编码
// 当Content-Type 为 x-www-form-urlencoded 的时候，POST 的请求数据是表单
// Content-Type 为 application/json 的时候，HTTP POST请求数据是JSON的
/* 当urlencoded中extended为false时，会使用querystring库解析URL编码的数据,键值对中的值就为'String'或'Array'类型
   当urlencoded中extended为true时，会使用qs库解析URL编码的数据，键值对中的值是任意类型
   默认是True
 */

// for parsing application/x-www-form-urlencoded
// 判断请求体格式是不是表单格式，如果是的话会调用qs库把请求体字符串转成对象
app.use(bodyParser.urlencoded({extended: true, limit: "200mb", parameterLimit:500000}))

// for parsing application/json
// 判断请求体格式是不是json格式，是的话调用JSON.parse把请求体字符串解析成对象
// app.use(bodyParser.json({limit: "200mb", parameterLimit: 500000}))

// 以上两个只会有一个生效


// 创建路由
// app.post(path, callback)
// app.post('python调用的url', function(req, res) {回调函数的具体逻辑，在这里调用抠出来的js代码})
app.post('/encrypt', function (req, res){
    // req.body  request请求的内容，这里传的就是加密的数据
    var item = req.body;
    var key = item.encrypt_key,
        value = item.encrypt_value

    // 调用解析函数
    var encryptData = encrypt.hex_md5(Buffer.from(key + value).toString('base64').replace(/=/g, ''))

    // 返回解析结果
    res.send(encryptData)
})


// 启动服务，指定监听的端口，在python请求时要记得加端口
// app.listen([port[, host[, backlog]]][, callback])
app.listen(2229,() => {
    console.log('服务开启，端口2229')
})

/* 启动方法:
   1.控制台进到这个文件目录
   2.运行这个main.js    node main.js
 */


