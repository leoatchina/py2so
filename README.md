# py2so

从[https://github.com/cckuailong/py2so](https://github.com/cckuailong/py2so) fork 并根据自己的需要进行了改动

## 例子
```
python py2so -c -l ~/anaconda3/include/python3.6m -d ~/source/server -o ~/release/server -m server.py
```
会先把`~/source/server`里的全部文件同步到`~/release/server`，然后把除了`server.py`外的所有py文件编译成`.so`文件

## py2so简介
1. py2so可以将python文件转化为so文件，达到加密python文件的目的
2. py2so加密一个py文件，也可以直接加密一整个python项目
3. 生成的.so文件可以被主文件通过 "from module import \*" 调用
4. 可以自动识别项目中的py文件,可以指定哪些文件或文件夹不被加密
5. 你可以选择是否保留加密前的文件或项目
6. 采用了把源文件目录同步到指定输出文件夹的方式，默认是 "./output"
7. 可以指定用python2或者python3，默认是 python3
8. 碰到无法编译的情况会退出

## 环境配置
```
sudo bash install_cython.sh
```
安装cython

## 使用说明
#### Python
```
使用:
  python py2so.py [选项] ...
```

```
选项:
  -v,  --version    显示py2so版本
  -h,  --help       显示帮助菜单
  -l,  --lib        指定要include的python库文件,必填。这个是和源文件的重要区别之一
  -c,  --clear      编译后是否删除python文件
  -p,  --py         Python的子版本号, 默认值为 3。 次重要区别
                    例: -p 2  (比如你使用python2)
  -d,  --directory  Python项目路径 (如果使用-d参数, 将加密整个Python项目)
  -f,  --file       Python文件 (如果使用-f, 将加密单个Python文件)
                    -d 或 -f 必填
  -o,  --output     指定输出目录，如果不存在会自动建立
  -m,  --maintain   标记你不想加密的文件或文件夹路径
                    注意: 文件夹路径需要使用'[]'包起来, 并且需要和-d参数一起使用
                    例: -m __init__.py,setup.py,[poc,resource,venv,interface]
```

```
例:
  python py2so.py -f test_file.py
  python py2so.py -d ../test_dir -m __init__.py -c
  python py2so.py -d /home/test/test_dir -m [poc/,resource/,venv/,interface/]
  python py2so.py -d test_dir -m __init__.py,setup.py,[poc/,resource/,venv/,interface/] -c
```
