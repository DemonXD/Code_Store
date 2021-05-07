### git commit template usage
git commit 模板使用
- `git config --global commit.template /absolute/path/to/git-commit-templ.txt`
- `git commit`

### git 常用设置
**配置windows和Linux平台下自动转义换行符的设置**  
``` Shell
git config --global core.autocrlf false
git config --global core.filemode false
git config --global core.safecrlf true
```
**保存使用https账户密码登录时不需要重复登录**  
```Shell
git config --global credential.help store
```
**配置http代理**  
也可以直接使用Linux_Exp/Shell_Scripts下的git_proxy.sh脚本
```Shell
git config --global http.proxy socks5://127.0.0.1:1080
git config --global https.proxy socks5://127.0.0.1:1080
```