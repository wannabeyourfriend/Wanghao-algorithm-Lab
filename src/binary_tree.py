from state import *

class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value


class BinaryTree:
    def __init__(self, _input):
        self.root = None
        self.nodes = []
        self.L = []
        self.R = []
        self._input = _input
        self.is_valid = self.init_tree()

    def new_node(self, value):
        """
        :param value: 初始化新节点的字符串
        :return: none
        """
        node = Node(value)
        self.nodes.append(node)
        return node

    def clear(self):
        '''
        :return:None
        '''
        self.nodes.clear()
        self.L.clear()
        self.R.clear()
        self.root = None

    def traverse(self, node, result, is_outer):
        """
        :param node:遍历以node作为根节点的子树
        :param result:储存遍历输出的结果
        :param is_outer:括号操作数
        :return:result
        """
        if not node:
            return
        fl = node.value.startswith('\\') and node.value[1] > '1'
        if fl and is_outer:
            result.append("( ")
        self.traverse(node.left, result, True)
        if node.value.startswith('\\'):
            result.append(S[int(node.value[1]) - int('1')][0])
        else:
            result.append(node.value)
        result.append(' ')
        self.traverse(node.right, result, True)
        if fl and is_outer:
            result.append(") ")

    def print_tree(self, node):
        if node.value == " ":
            print(" ")
        assert node
        result = []
        self.traverse(node, result, False)
        formatted_result = ''.join(result).replace(' )', ')').replace(' (', '(').strip()
        print(formatted_result)

    def init_tree(self):
        """
        从逆波兰表达式构建二叉树，并判断是否是合式公式
        :param _input:输入的逆波兰式列表
        :return:
        """
        if self._input == " ":
            self.root.value = " "
            self.root.left = None
            self.root.right = None
            return True

        stack = []
        for value in self._input:
            node = self.new_node(value)
            if value.startswith('\\'):
                if len(value) != 2 or not ('1' <= value[1] <= '5'):
                    raise ValueError("Invalid input")
                if value[1] == '1':
                    if not stack:
                        return False
                    node.right = stack.pop()
                else:
                    if len(stack) < 2:
                        return False
                    node.right = stack.pop()
                    node.left = stack.pop()
            stack.append(node)
        if len(stack) != 1:
            return False
        self.R.append(stack[-1])
        self.root = stack[-1]
        return True

    def init_subtree(self, node):
        """
        从给定节点初始化一颗新的子树
        :param node: 子树的根节点
        :return: 新的子树的 BinaryTree 实例
        """
        if node is None:
            raise ValueError("Cannot initialize a subtree from a None node")

        # 使用递归创建树
        def build_tree_from_node(node):
            new_tree = BinaryTree([])
            new_tree.root = node  # 直接使用提供的节点
            new_tree.nodes.append(node)
            return new_tree
        return build_tree_from_node(node)


