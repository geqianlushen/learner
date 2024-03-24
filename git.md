# git

## 一、安装和初始化

查看git版本

```
$ git -v
>>>git version 2.44.0.windows.1
```

![常见命令大全](常见命令大全.png)

初始化命令

```
$ git config --global user.name "LinShen" # 配置用户名
$ git config --global user.email linshen@qq.com # 配置用户名和邮箱
$ git config --global credential.helper store # 保存密码
$ git config --global --list # 查看git配置信息
```

## 二、仓库

### 1、创建一个仓库.git

- 法一：直接创建一个仓库

```
$ git init
--------------------
$ git init my-repo # 在当前目录下创建一个文件夹my-repo，并将其作为仓库
```

- 法二：从远程服务器上克隆一个已经存在的仓库

```
$ git clone
--------------------
$ git clone https://github.com/XXXXX/remote-repo.git # 从该链接创建一个名为remote-repo的远程仓库
```

- 查看.git仓库内文件的信息（其中a表示显示隐藏内容，l表示显示详细信息）

```
$ ls -a
```

### 2、工作区域和文件状态

![工作区、暂存区和本地仓库的关系](工作区、暂存区和本地仓库的关系.png)

### 3、添加和提交文件

```
$ git status # 查看工作区内文件的状态
$ git ls-files # 查看暂存区的文件内容
$ git add file1.txt # 将file1.txt文件提交到暂存区
$ git add *.txt
$ git add . # 将所有的修改添加到暂存区
$ git rm --cached file1.txt # 将添加到暂存区的file1.txt文件取消回工作区域
$ git commit -m "第一次提交" # 将暂存区的文件提交到仓库中，并提交信息为第一次提交
```

### 4、查看提交记录

```
$ git log # 查看提交记录（每次提交都有一个唯一的提交ID、作者、邮箱和注释信息）
$ git log --oneline # 查看简洁的提交记录
```

### 5、回退版本

```
$ git reset --soft ID# 回退到对应提交ID的版本
$ git reset --hard ID# 在回退的操作后丢弃工作区和暂存区的内容
$ git reset --mixed ID# 在回退的操作后丢弃暂存区的内容
```

### 6、查看版本差异

```
$ git reflog # 查看操作指令的历史记录
$ git diff # 比较文件的差异化内容，默认是比较工作区和暂存区的内容
$ git diff HEAD # 比较工作区和仓库的差异化内容
$ git diff --cached # 比较暂存区和仓库的差异化内容
$ git diff ID1 ID2 # 比较两份提交ID版本的差异化内容
$ git diff ID1 HEAD # 比较提交ID版本为ID1与仓库的差异化内容
$ git diff HEAD^ HEAD 或$ git diff HEAD~ HEAD # 比较仓库中上一个版本与仓库中当前版本的差异化内容
$ git diff HEAD~2 HEAD # 比较仓库中上两个版本与仓库中当前版本的差异化内容
$ git diff HEAD~2 HEAD file3.txt # 比较仓库中上两个版本与仓库中当前版本的file3.txt差异化内容
```

### 7、删除文件

```
$ rm file1.txt # 在工作区删除file1.txt文件
$ git rm file2.txt # 在工作区和暂存区同时删除file2.txt文件
$ git rm --cached file3.txt # 在暂存区删除file3.txt文件
$ git rm -r* # 递归删除某目录或文件
```

## .gitignore文件

### 1、应该忽略的一些文件（未被添加到暂存区的文件）

- 系统或软件自动生成的文件
- 编译产生的中间文件和结果文件
- 运行时生成日志文件、缓存文件、临时文件
- 涉及身份、密码、口令、秘钥等敏感信息文件

### 2、.gitignore文件的内容

```.gitignore
access.log
*.log
temp/
```

### 3、.gitignore文件的匹配规则

- 空行或者以#开头的行会被git忽略
- 使用标准的Blob模式匹配：
  - *：任意字符
  - ？：单个字符
  - [] ：匹配列表中的单个字符
- **表示匹配任意的中间目录
- ! ：表示取反
