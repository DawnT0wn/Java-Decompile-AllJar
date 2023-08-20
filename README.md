# Java-Decompile-AllJar

这个 Python 脚本用于解压和反编译指定目录下的 JAR 文件，并将结果按原始 JAR 文件的层级结构组织在目标目录中。

## Usage

确保你的系统已经安装了 Python 3 和所需的依赖。你还需要拥有 java-decompiler.jar 文件，以供脚本使用。

1. 下载 java-decompiler.jar 文件并将其放置在与脚本相同的目录下。

2. 运行脚本，提供以下命令行参数：

   ```bash
   python script.py <lib_directory> <output_directory>

## 注意事项

- 脚本可能会在某些情况下无法正确反编译一些类。这些情况通常涉及复杂的类结构或与反编译器的兼容性问题。
- 请确保你有适当的权限来执行脚本并访问输入和输出目录。
- 脚本仅处理 .jar 文件，不会处理其他类型的文件。

目前能解决大多数反编译问题，但是由于java-decompiler.jar的问题

```
BeanMap.class
BeanMap$1.class
BeanMap$2.class
```

对于以上情况java-decompiler.jar只会反编译BeanMap.class

