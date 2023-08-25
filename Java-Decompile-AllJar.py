import os
import shutil
import subprocess
import concurrent.futures
import sys  # 导入 sys 模块以访问命令行参数

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

    # unizp 解压 JAR 文件到目标目录
    # subprocess.run(["unzip", "-d", target_dir, jar_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # jar 解压 复制 JAR 文件到目标目录
    shutil.copy(jar_file, target_dir)

    # 获取当前目录
    original_directory = os.getcwd()

    # 切换到 JAR 文件所在的目录
    os.chdir(target_dir)

    # 使用 jar 命令解压 JAR 文件到当前目录
    result = subprocess.run(["jar", "-xvf", f"{jar_file_name}.jar"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error: {result.stderr.decode('utf-8')}")

    # 返回到原始目录
    os.chdir(original_directory)

    # 删除copy的jar包
    os.remove(os.path.join(target_dir, f"{jar_file_name}.jar"))
    # 构建反编译命令
    decompile_command = f"java -cp java-decompiler.jar org.jetbrains.java.decompiler.main.decompiler.ConsoleDecompiler -hdc=0 -dgs=1 -rsy=1 -rbr=1 -lit=1 -nls=1 -mpm=60 {target_dir} {target_dir}"

    # 执行反编译命令
    subprocess.run(decompile_command, shell=True)

# 使用多线程处理所有 JAR 文件
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(process_jar, jar_files)

# 至此，所有 .class 文件都已经被反编译并按照 lib 目录下的层级组织在相应的文件夹中
