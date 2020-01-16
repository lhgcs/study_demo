jsonObject = JSON.parse(jsonData);
// 遍历
for (var key in jsonObject) {
    console.log(key, jsonObject[key]);
    data =  jsonObject[key];

    // 所有字段转字符串
    if ( null == data || underfined == data) {
        jsonObject[key] = "";
    } else if ("number" == typeof(data)) {
        // float转为int型数据
        let temp = parseInt(data);
        // 转为字符串
        jsonObject[key] = temp.toString();
    } else if ("string" == typeof(data) || "object" == typeof(data)) {
    }
}

let str = JSON.stringify(jsonObject); 
console.log(str); 