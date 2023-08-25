import os
import subprocess
import concurrent.futures
import sys  # 导入 sys 模块以访问命令行参数
import threading

# 从命令行参数中获取原始 JAR 文件目录和目标目录
if len(sys.argv) != 3:
    print("Usage: python script.py <lib_directory> <output_directory>")
    sys.exit(1)

lib_directory = sys.argv[1]
output_directory = sys.argv[2]

# 获取所有 JAR 文件的列表
jar_files = []
for root, _, files in os.walk(lib_directory):
    for file in files:
        if file.endswith(".jar"):
            jar_file = os.path.join(root, file)
            jar_files.append(jar_file)

# 定义一个函数来处理单个 JAR 文件的解压和反编译
def process_jar(jar_file):
    # 提取 JAR 文件名，用于创建目标目录
    jar_file_name = os.path.splitext(os.path.basename(jar_file))[0]

    # 创建目标目录，以 JAR 文件名命名
    target_dir = os.path.join(output_directory, jar_file_name)
    os.makedirs(target_dir, exist_ok=True)

    # 解压 JAR 文件到目标目录
    subprocess.run(["tar", "-xvf", jar_file, "-C", target_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 构建反编译命令
    decompile_command = f"java -cp java-decompiler.jar org.jetbrains.java.decompiler.main.decompiler.ConsoleDecompiler -hdc=0 -dgs=1 -rsy=1 -rbr=1 -lit=1 -nls=1 -mpm=60 {target_dir} {target_dir}"

    # 执行反编译命令
    subprocess.run(decompile_command, shell=True)

# 使用多线程处理所有 JAR 文件
with concurrent.futures.ThreadPoolExecutor() as executor:
    # 创建并启动线程来处理每个 JAR 文件
    threads = [threading.Thread(target=process_jar, args=(jar_file,)) for jar_file in jar_files]
    for thread in threads:
        thread.start()

    # 主线程等待所有线程完成
    for thread in threads:
        thread.join()

# 至此，所有 .class 文件都已经被反编译并按照 lib 目录下的层级组织在相应的文件夹中
