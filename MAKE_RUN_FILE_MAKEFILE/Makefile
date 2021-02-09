SCRIPT=install.sh
INSTALLDIR:=$(shell echo ~/.APPS)
DEBDIR=src
DEBFILE:=$(shell ls -lt $(DEBDIR) | grep deb | head -n 1 | awk '{print $$9}')
BUILDIR=build
RUN=$(BUILDIR)/installer.run


# 逻辑描述
# 判断deb文件是否存在，存在即为最新生成的文件
# 将install.sh 和 待打包的deb文件 使用cat 命令打包到一起生成.run文件，并赋权限

# usage:
# make之前需要新建build目录


all:	
# 	check file is exist or not!
# 	@echo $(DEBFILE)
	@if [ -a "$(DEBFILE)" ]; then echo "found: $(DEBFILE)";fi
# 	cat $(SCRIPT) $(DEBDIR) > $(RUN)
# 	chmod +x $(RUN)
	@echo "目标机器安装目录为：" $(INSTALLDIR)
	@echo "待打包文件在" $(DEBDIR)/$(DEBFILE)
# 	这里因为替换字符中有路径，和原本的/分割符冲突，这里改用#作为sed的分割符
#	将实际要打包的文件名和安装路径写入到install.sh文件中
	@sed -i "s?{FILENAME}?$(DEBFILE)?g; s?{TARGETDIR}?$(INSTALLDIR)?g" $(SCRIPT)
	@mkdir $(BUILDIR)
	@cat $(SCRIPT) $(DEBDIR)/$(DEBFILE) > $(RUN)
	@chmod +x $(RUN)

clean:
	rm -rf $(BUILDIR)



# 	check file is exist or not!
# ifneq ($(wildcard $(DEBDIR)),)
# 	echo "has file!"
# endif

