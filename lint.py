# 使用 https://github.com/harttle/md-padding 格式化文档

import os
import re
import time
import sys
import getopt


def get_all_post_name(path):
  post_name_list = []
  for root, dirs, files in os.walk(path):
    for file in files:
      if file.endswith(".md"):
        post_name_list.append(path+file)
  return post_name_list


def get_the_lastest_post_name(path):
  # 获取最后修改的文件名
  ori_time = 0
  last_modified_file = ""
  for root, dirs, files in os.walk(path):
    for file in files:
      if os.path.getmtime(path+file) > ori_time:
        ori_time = os.path.getmtime(path+file)
        last_modified_file = file
  print("最后修改的文件是："+last_modified_file)
  mode = input("\n输入y确认格式化，其他键退出：")
  if mode == "Y" or mode == "y":
    return [path+last_modified_file]
  else:
    exit()


def func(names):
  for name in names:
    with open(f"{name}", 'r', encoding='utf-8') as f:
      content = f.read()
      # 修改数学公式中含有的*,改为\times
    pattern1 = re.compile(r'\$.*?(\*)?.*?\$')
    content = pattern1.sub(lambda m: m.group().replace(
        '*', r' \times '), content)
    with open(f"{name}", 'w', encoding='utf-8') as f:
      f.write(content)

    # 调用mdp
    os.system(f"mdp -i {name}")
    print(f"{name} mdp格式化完成")
  for name in names:
    with open(f"{name}", 'r', encoding='utf-8') as f:
      content = f.read()
    pattern2 = re.compile(r'date: \d{4}-\d{2}-\d{2} \d{2}: \d{2}: \d{2}')
    # YAML日期格式更新
    content = pattern2.sub(lambda m: m.group().replace(
        ': ', ':').replace('date:', 'date: '), content)
    # markdown数学公式前后添加空格
    pattern3 = re.compile(r'\x20*\$(.+?)\$\x20*')
    content = pattern3.sub(lambda m: ' $'+m.group(1)+'$ ', content)
    with open(f"{name}", 'w', encoding='utf-8') as f:
      f.write(content)
    print(f"{name} YAML及数学公式格式化完成")


if __name__ == '__main__':
  # 输入 -a 目录 更新该目录下所有的文件
  # 输入 -s 目录 更新该目录下最新的文件
  # 输入 -h 查看帮助
  # 直接输入文件路径 更新该文件
  # 判断是否有参数
  if len(sys.argv) == 1:
    print("""
  使用方法：
  python3 lint.py -a 目录 更新该目录下所有的文件
  python3 lint.py -s 目录 更新该目录下最新的文件
  python3 lint.py 文件路径 更新该文件
        """)
    exit()
  if len(sys.argv) == 2:
    # 判断参数是否为md文件
    if os.path.isfile(sys.argv[1]) and sys.argv[1].endswith(".md"):
      func([sys.argv[1]])
    else:
      print(f"输入的文件 {sys.argv[1]} 不是md文件，或者文件不存在")
      exit()
  try:
    opts, args = getopt.getopt(sys.argv[1:], "-a:-s:-h")
  except getopt.GetoptError:
    print("使用python ./lint.py -h 查看帮助")
    exit()
  for opt, arg in opts:
    if opt == '-a':
      print(f"更新 {arg} 下所有文件")
      # 检测arg是否是目录
      if os.path.isdir(arg):
        if not arg.endswith("\\"):
          arg = arg+"\\"
        names = get_all_post_name(arg)
        func(names)
      else:
        print("输入的路径不存在，或者不是目录")
        exit()
    elif opt == '-s':
      print(f"更新 {arg} 下最新的文件")
      # 检测arg是否是目录
      if os.path.isdir(arg):
        if not arg.endswith("\\"):
          arg = arg+"\\"
        names = get_the_lastest_post_name(arg)
        func(names)
      else:
        print("输入的路径不存在，或者不是目录")
        exit()
    elif opt == '-h':
      print("""
  使用方法：
  python3 lint.py -a 目录 更新该目录下所有的文件
  python3 lint.py -s 目录 更新该目录下最新的文件
  python3 lint.py 文件路径 更新该文件
        """)
    else:
      assert False, "unhandled option"
