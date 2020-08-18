vscode官方sample配置项，基于MinGW-x64,同时使用clang++  
配置参考：  
- https://www.jianshu.com/p/afe0ffa7839d
- https://www.zhihu.com/question/30315894/answer/154979413

使用时，请修改部分文件的路径索引:
`task.json`: command, cwd
`launch.json`: miDebuggerPath,
`c_cpp_properties.json`: compilerPath, (PS: includePath 按需添加)