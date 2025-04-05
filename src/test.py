class Test:
    def __init__(self, filename):
        """
        初始化 Test 类，读取指定文件中的测试用例。

        :param filename: 包含中缀表达式的文件名
        """
        self.expressions = []  # 用于存储中缀表达式的列表
        self.load_expressions(filename)

    def load_expressions(self, filename):
        """
        从指定文件中读取中缀表达式并存储到列表中。

        :param filename: 文件名
        """
        try:
            with open(filename, 'r') as file:
                for line in file:
                    expression = line.strip()  # 去除行首尾空白字符
                    if expression:  # 确保不是空行
                        self.expressions.append(expression)
        except FileNotFoundError:
            print(f"错误: 文件 {filename} 未找到。")
        except Exception as e:
            print(f"发生错误: {e}")

    def get_expressions(self):
        """
        获取所有读取的中缀表达式。

        :return: 存储中缀表达式的列表
        """
        return self.expressions