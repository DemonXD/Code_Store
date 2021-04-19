# 显示全部内容
sed -n p sample.txt
# 显示第几到第几行
sed -n "1,5"p sample.txt
# 显示有制定内容的行
sed -n "/指定内容/"p sample.txt
# 匹配开始到结束内容
sed -n "/开始内容/,/结束内容/"p sample.txt

# s 命令，替换内容
sed "s/被替换内容/替换内容/g" sample.txt
# 只对第几行进行内容替换
sed "ns/被替换内容/替换内容/g" sample.txt
# 对多行进行内容替换
sed "n1,n2s/被替换内容/日换内容/g" sample.txt
# 只替换第一个匹配内容
sed "s/被替换内容/替换内容/1" sample.txt
# 在开头添加双斜杠注释内容
sed "s/ ^ / \/\/ /" sample.txt
# 在末尾添加双斜杠
sed "s/ $ / \/\/ 末尾 /" sample.txt

# c命令，用于行替换
# 替换第二行内容为gaga
sed "2 c gaga" sample.txt
# 仅替换有指定内容的行, 把有tom的行的tom替换成cat
sed "/tom/c cat" sample.txt

# i命令, 插入行
# 在第一行前面插入i love you
sed "1 i i love you" sample.txt
# 在最后一行前插入
sed "$ i i love you" sample.txt

# a 命令，在行后插入
# 在第一行后插入
sed "1 a i love you" sample.txt
# 在最后一行后插入
sed "$ a i love you" sample.txt

# d 命令，删除匹配行
# 删除有ew的行
sed "/ew/d" sample.txt
# 删除第一行
sed "1d" sample.txt

