#!/bin/bash

#########################################################
# Module : mk_go_pro.sh
# Author : Blair Zhong
# Created : 2013.07.23
# Modify :
# Version : 1.0
# Useage : ./mk_go_pro.sh
# ./mk_go_pro.sh porject_name
# Description: 创建一个go可编译的工程
#————————————–————————————–
#
# 根据 Go语言学习园地博客的帖子编写，如有侵权请联系本人
# http://blog.studygolang.com/2012/12/go项目的目录结构/
#
# 默认情况下运行本程序，会生成如下目录和文件:
# test
# ├── bin
# ├── install.sh
# ├── pkg
# └── src
# ├── config
# │   └── config.go
# └── test
# └── main.go
#————————————–————————————–
# 5 directories, 3 files
#
# 其中:
# 1, install.sh为安装文件，
# 2, config.go为test项目的配置文件
# 3, main.go这个你懂的
#
# 生成完毕之后运行进入test目录，运行install.sh会生成如下文件和目录
# ├── bin
# │   └── test
# ├── install.sh
# ├── pkg
# │   └── darwin_amd64
# │   └── config.a
# └── src
# ├── config
# │   └── config.go
# └── test
# └── main.go
# 6 directories, 5 files
#
# 多了两个文件
# 1, bin目录下的test，这个是可执行稳健
# 2, pkg/darwin_amd64下的config.a，这个是config编译后产生的文件
#
# enjoy it!
#########################################################



PWD=$(pwd)
cd $PWD

if [[ "$1" = "" ]]; then
echo "Useage: ./mk_go_pro.sh porject_name"
echo -ne "Please input the Porject Name[test]"
read Answer
if [ "$Answer" = "" ]; then
echo -e "test";
PRO_NAME=test;
else
PRO_NAME=$Answer;
fi
else
PRO_NAME=$1;
fi

#########################################################

#创建目录
echo "Init Directory …"
mkdir -p $PRO_NAME/bin
mkdir -p $PRO_NAME/pkg
mkdir -p $PRO_NAME/src/config
mkdir -p $PRO_NAME/src/$PRO_NAME


#########################################################
#创建 install.sh 文件
echo "Create install/install.sh …"
cd $PRO_NAME
echo "#!/bin/bash" > install.sh
echo "if [ ! -f install.sh ]; then" >> install.sh
echo "echo "install must be run within its container folder" 1>&2" >> install.sh
echo "exit 1" >> install.sh
echo "fi" >> install.sh
echo >> install.sh
echo "CURDIR=\`pwd\`" >> install.sh
echo "OLDGOPATH=\"\$GOPATH\"" >> install.sh
echo "export GOPATH=\"\$CURDIR\"" >> install.sh
echo >> install.sh
echo "gofmt -w src" >> install.sh
echo "go install $PRO_NAME" >> install.sh
echo "export GOPATH=\"\$OLDGOPATH\"" >> install.sh
echo >> install.sh
echo "echo "finished"" >>install.sh
chmod +x install.sh

#创建 config.go 文件
echo "Create src/config/config.go …"
cd src/config
echo package config > config.go
echo >> config.go
echo func LoadConfig\(\) { >> config.go
echo >> config.go
echo "}" >> config.go

#创建 main.go
echo "Create src/$PRO_NAME/main.go …"
cd ../$PRO_NAME/
echo "package main" > main.go
echo >> main.go
echo "import (" >> main.go
echo " \"config\"" >> main.go
echo " \"fmt\"" >> main.go
echo ")" >> main.go
echo >> main.go
echo "func main() {" >> main.go
echo " config.LoadConfig()" >> main.go
echo " fmt.Println(\"Hello $PRO_NAME!\")" >> main.go
echo "}" >> main.go
echo "All Done!"