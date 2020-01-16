let fs = require('fs');

// 创建目录
let createFolder = function(folder){
    try{
        fs.accessSync(folder); 
    }catch(e){
        fs.mkdirSync(folder);
    }  
};



/**
 * 读取路径信息
 * @param {string} path 路径
 */
function getStat(path){
    return new Promise((resolve, reject) => {
        fs.stat(path, (err, stats) => {
            if(err){
                resolve(false);
            }else{
                resolve(stats);
            }
        })
    })
}
 
/**
 * 创建路径
 * @param {string} dir 路径
 */
function mkdir(dir){
    return new Promise((resolve, reject) => {
        fs.mkdir(dir, err => {
            if(err){
                resolve(false);
            }else{
                resolve(true);
            }
        })
    })
}
 
/**
 * 路径是否存在，不存在则创建
 * @param {string} dir 路径
 */
async function dirExists(dir){
    let isExists = await getStat(dir);
    //如果该路径且不是文件，返回true
    if(isExists && isExists.isDirectory()){
        return true;
    }else if(isExists){     //如果该路径存在但是文件，返回false
        return false;
    }
    //如果该路径不存在
    let tempDir = path.parse(dir).dir;      //拿到上级路径
    //递归判断，如果上级目录也不存在，则会代码会在此处继续循环执行，直到目录存在
    let status = await dirExists(tempDir);
    let mkdirStatus;
    if(status){
        mkdirStatus = await mkdir(dir);
    }
    return mkdirStatus;
}




// 移动文件需要使用fs模块
var fs = require('fs');
app.post('/file-upload', function(req, res) {
  // 获得文件的临时路径
  var tmp_path = req.files.thumbnail.path;
 // 指定文件上传后的目录 - 示例为"images"目录。 
 var target_path = './public/images/' + req.files.thumbnail.name;
 // 移动文件
 fs.rename(tmp_path, target_path, function(err) {
   if (err) throw err;
   // 删除临时文件夹文件, 
   fs.unlink(tmp_path, function() {
      if (err) throw err;
      res.send('File uploaded to: ' + target_path + ' - ' + req.files.thumbnail.size + ' bytes');
   });
 });
};






