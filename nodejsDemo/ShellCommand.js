/*
 * @Description: 执行shell命令
 * @Version: 1.0
 * @Autor: lhgcs
 * @Date: 2019-06-13 11:03:07
 * @LastEditors  : lhgcs
 * @LastEditTime : 2020-01-06 16:35:24
 */

let exec = require('child_process').exec;
const execSync = require('child_process').execSync;


/**
 * @description: 同步执行
 * @param {type} 
 * @return: 
 */
function commandSync(command, callback) {
    let res = execSync(command);
    console.log('receive: ' + res);
    try {
        callback(res);
        return true;
    } catch(e) {
        console.log(e);
        return false;
    }
}

/**
 * @description: 异步执行
 * @param {type} 
 * @return: 
 */
function commandRsync(command, callback) {
    let res = exec(command, function (error, stdout, stderr) {
        if(error) {
            console.log(error.stack);
            console.log('Error code: '+error.code);
            console.log('Signal received: '+error.signal);
            console.log(stderr.toString());
        } else {
            callback(stdout.toString());
        }
    });
    return res;
}

module.exports = {
    commandSync,
    commandRsync
};
