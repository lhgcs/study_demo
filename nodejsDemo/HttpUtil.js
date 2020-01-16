let http = require("http");  

/**
 * @description: 回调处理数据
 * @param {type} 
 * @return: 
 */
function callback_fun(res){
    let body = ''; 
    console.log("response: " + res.statusCode + JSON.stringify(res.headers));
    if (res.statusCode == 200){ //响应正常
        res.setEncoding('utf8'); 
        res.on('data',function(data){  
            body += data;  
        }).on('end', function(){ 
            // 数据接收完成 
            console.log(body)  
        });  
    }
}

/**
 * @description: 是否能连接上服务器
 * @param {type} 
 * @return: 
 */
function test_server() {
    try {
        let opt = {
            host:'www.utdimensions.com', // 不能加http
            port:'5005',  
            method:'GET',  
            path:'/index/',  
            headers:{  
                "Content-Type": 'application/json',  
                "Content-Length": data.length  
            }
        };

        let data = {
            username: "hello",
            password: "123456"
        };
        data = JSON.stringify(data); 

        let req = http.request(opt, callback_fun).on('error', function(e) {  
            console.log("error: " + e.message);  
        });
        //req.write(data);  
        req.end(); 
    }catch(e) {
        console.log(e)
    }
}
