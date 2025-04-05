import binary_tree
from state import *
from binary_tree import BinaryTree
import copy

def print_item(value):
    """
    :param value:单独打印前后件的某一个命题公式
    :return:
    """
    BinaryTree.print_tree(value)


class Inference:
    def __init__(self, l, r, class_tree_instance, rules=S,):
        """
        :param:LHS存储前件所有命题公式对应的表达式二叉树
        :param:RHS存储后件所有命题公式对应的表达式二叉树
        """
        self.rules = rules
        self.cnt = 0
        self.LHS = l
        self.RHS = r
        self.nodes = []
        self.class_tree = class_tree_instance

    def print_prove(self, o, pre, id, test=1):
        # 输出格式化的序号
        print(f"({pre}{id}) $", end='')
        # 输出前件
        fl = False
        for v in self.LHS:
            binary_tree.BinaryTree.print_tree(v, v.root)
            if fl:
                print(", ", end='')
            fl = True
        print(" \\xRightarrow{s} ", end=' ')
        # 输出后件
        fl = False
        for v in self.RHS:
            if fl:
                print(", ", end='')
            binary_tree.BinaryTree.print_tree(v, v.root)
            fl = True
        # 根据operator数输出依据的推理规则
        if o == 0:
            print("$")
            return
        if 1 <= o <= 5:
            print(f"\quad (by $$ {self.rules[o - 1][0]}  $$ \\Rightarrow rule$$)$")
        else:
            print(f"\quad (by $$ \\Rightarrow $$ {self.rules[o - 6][0]} rule $$)$")

    def are_trees_equal(self, tree1, tree2):
        """判断两棵二叉树是否相同"""
        if not tree1 and not tree2:
            return True
        if not tree1 or not tree2:
            return False
        return (tree1.root.value == tree2.root.value and
                self.are_trees_equal(tree1.root.left, tree2.root.left) and
                self.are_trees_equal(tree1.root.right, tree2.root.right))

    def have_common_trees(self, list1, list2):
        """判断两个列表是否有相同的二叉树"""
        for tree1 in list1:
            for tree2 in list2:
                if self.are_trees_equal(tree1, tree2):
                    return True
        return False


    def inference(self, o, pre, id, test):
        """
        :param test: 是否在测试环节
        :param self:
        :return:
        """
        if not test:
            self.print_prove(o, pre, id, test)
        # 没有分支的前件推理规则
        for v in self.LHS:
            if v.root.value[0] != '\\':
                continue
            o = int(v.root.value[1])
            if o in {3, 4, 5}:
                continue
            self.LHS.remove(v)
            if o == 1:
                self.RHS.append(self.class_tree.init_subtree(v.root.right))
                return self.inference(o, pre, id + 1, test)
            if o == 2:
                self.LHS.append(self.class_tree.init_subtree(v.root.right))
                self.LHS.append(self.class_tree.init_subtree(v.root.left))
                return self.inference(o, pre, id + 1, test)
        # 没有分支的后件推理规则
        for v in self.RHS:
            if v.root.value[0] != '\\':
                continue
            o = int(v.root.value[1])
            if o in {2, 5}:
                continue
            self.RHS.remove(v)
            if o == 1:
                self.LHS.append(self.class_tree.init_subtree(v.root.right))
                return self.inference(o+5, pre, id+1, test)
            if o == 3:
                self.RHS.append(self.class_tree.init_subtree(v.root.right))
                self.RHS.append(self.class_tree.init_subtree(v.root.left))
                return self.inference(o+5, pre, id+1, test)
            if o == 4:
                self.RHS.append(self.class_tree.init_subtree(v.root.right))
                self.LHS.append(self.class_tree.init_subtree(v.root.left))
                return self.inference(o+5, pre, id+1, test)
        # 有分支的前件推理规则
        for v in self.LHS:
            if v.root.value[0] != '\\':
                continue
            o = int(v.root.value[1])
            self.LHS.remove(v)
            temp_l = copy.deepcopy(self.LHS)
            temp_r = copy.deepcopy(self.RHS)
            if o == 3:
                self.LHS.append(self.class_tree.init_subtree(v.root.left))
                if not self.inference(o, pre+f"{id}a.", 1, test):
                    return False
                else:
                    self.LHS = copy.deepcopy(temp_l)
                    self.RHS = copy.deepcopy(temp_r)
                # self.LHS.remove(self.class_tree.init_subtree(v.root.left))
                self.LHS.append(self.class_tree.init_subtree(v.root.right))
                return self.inference(o, pre+f"{id}b.", 1, test)
            if o == 4:
                self.LHS.append(self.class_tree.init_subtree(v.root.right))
                if not self.inference(o, pre+f"{id}a.", 1, test):
                    return False
                else:
                    self.LHS = copy.deepcopy(temp_l)
                    self.RHS = copy.deepcopy(temp_r)
                # self.LHS.remove(self.class_tree.init_subtree(v.root.right))
                self.RHS.append(self.class_tree.init_subtree(v.root.left))
                return self.inference(o, pre + f"{id}b.", 1, test)
            if o == 5:
                self.LHS.append(self.class_tree.init_subtree(v.root.left))
                self.LHS.append(self.class_tree.init_subtree(v.root.right))
                if not self.inference(o, pre+f"{id}a.", 1, test):
                    return False
                else:
                    self.LHS = copy.deepcopy(temp_l)
                    self.RHS = copy.deepcopy(temp_r)
                # self.LHS.remove(self.class_tree.init_subtree(v.root.left))
                # self.LHS.remove(self.class_tree.init_subtree(v.root.right))
                self.RHS.append(self.class_tree.init_subtree(v.root.left))
                self.RHS.append(self.class_tree.init_subtree(v.root.right))
                return self.inference(o, pre + f"{id}b.", 1, test)
        # 有分支的后件规则
        for v in self.RHS:
            if v.root.value[0] != '\\':
                continue
            o = int(v.root.value[1])
            self.RHS.remove(v)
            temp_l = copy.deepcopy(self.LHS)
            temp_r = copy.deepcopy(self.RHS)
            if o == 2:
                self.RHS.append(self.class_tree.init_subtree(v.root.left))
                if not self.inference(o+5, pre + f"{id}a.", 1, test):
                    return False
                else:
                    self.LHS = copy.deepcopy(temp_l)
                    self.RHS = copy.deepcopy(temp_r)
                # self.RHS.remove(self.class_tree.init_subtree(v.root.left))
                self.RHS.append(self.class_tree.init_subtree(v.root.right))
                return self.inference(o+5, pre + f"{id}b.", 1, test)
            if o == 5:
                self.LHS.append(self.class_tree.init_subtree(v.root.left))
                self.RHS.append(self.class_tree.init_subtree(v.root.right))
                if not self.inference(o+5, pre + f"{id}a.", 1, test):
                    return False
                else:
                    self.LHS = copy.deepcopy(temp_l)
                    self.RHS = copy.deepcopy(temp_r)
                # self.LHS.remove(self.class_tree.init_subtree(v.root.left))
                # self.RHS.remove(self.class_tree.init_subtree(v.root.right))
                self.LHS.append(self.class_tree.init_subtree(v.root.right))
                self.RHS.append(self.class_tree.init_subtree(v.root.left))
                return self.inference(o+5, pre + f"{id}b.", 1, test)
        # 根据公理进行推理
        return self.have_common_trees(self.LHS, self.RHS)

