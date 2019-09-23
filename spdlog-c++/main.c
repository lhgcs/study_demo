#include <stdio.h>
#include "iostream"
#include "spdlog/spdlog.h"
#include "spdlog/sinks/basic_file_sink.h"
#include "spdlog/sinks/stdout_color_sinks.h"
#include "spdlog/sinks/rotating_file_sink.h"
#include "spdlog/sinks/daily_file_sink.h"

int main(int argc, char *argv[])
{
    // 格式化
    spdlog::set_pattern("[%Y-%m-%d %H:%M:%S %z] [%n] [%^---%L---%$] [thread %t] %v");
    // 输出等级（默认是info）
    spdlog::set_level(spdlog::level::debug);


    // 输出到标准输出
    spdlog::debug("This message should be displayed..");   
    spdlog::info("Welcome to spdlog!");
    spdlog::warn("Easy padding in numbers like {:08d}", 12);
    spdlog::error("Some error message with arg: {}", 1);
    spdlog::critical("Support for int: {0:d};  hex: {0:x};  oct: {0:o}; bin: {0:b}", 42);


    // 输出日志到文件（目录logs必须存在，basic.txt不存在则自动创建）
    try {
        auto file_logger = spdlog::basic_logger_mt("basic_logger", "logs/basic.txt");
        spdlog::set_default_logger(file_logger); 
    } catch (const spdlog::spdlog_ex &ex) {
        std::cout << "Log init failed: " << ex.what() << std::endl;
    }

    spdlog::debug("This message should be displayed..");   

    // 循环覆盖（每个文件最大5M，3个文件）
    auto rotating_logger = spdlog::rotating_logger_mt("rotating", "logs/rotating.txt", 1048576 * 5, 3);
    spdlog::get("rotating")->info("send to logs/rotating.txt");

    // 创建日志文件（每天2:30am）
    auto daily_logger = spdlog::daily_logger_mt("daily_logger", "logs/daily.txt", 2, 30);
 
    return 0;
}


// Compile time log levels
// define SPDLOG_ACTIVE_LEVEL to desired level
// SPDLOG_TRACE("Some trace message with param {}", {});
// SPDLOG_DEBUG("Some debug message");

// auto console = spdlog::stdout_color_mt("console");    
// auto err_logger = spdlog::stderr_color_mt("stderr");    
// spdlog::get("console")->info("console");
// spdlog::get("stderr")->info("stderr");
// console->info("console");
