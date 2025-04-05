from state import *

# 初始化一个字典，包含所有的逻辑连接词
mp = {}

# init并不能判断：“p q”这样类型的非合式公式
def init():
    for i in range(5):
        for v in S[i]:
            mp[v] = i + 1

def is_lower(ch):
    return 'a' <= ch <= 'z'

def is_upper(ch):
    return 'A' <= ch <= 'Z'

def is_prop(ch):
    return ch not in (' ', "'", '(', ')')

def print_stack(suf):
    print(" ".join(suf))

def trans(s):
    stk = []  # 存储括号对
    res = []  # 存储逆波兰表达式结果
    null = []  # 空列表
    ls = len(s)
    i = 0

    if s == " ":
        return res, 1

    while i < ls:
        if s[i] == ' ':
            i += 1
            continue
        if s[i] == '(':
            stk.append("(")
            i += 1
            continue
        if s[i] == ')':
            while stk and stk[-1] != "(":
                res.append(stk.pop())
            if not stk:
                return null, 0
            stk.pop()  # Pop the '('
            i += 1
            continue
        if s[i] == '\\':
            length = 1
            while i + length < ls and is_lower(s[i + length]):
                length += 1
            symbol = s[i:i + length]
            qwq = mp.get(symbol, 0)
            if qwq == 0:
                return null, 0
            now = "\\" + str(qwq)
            # while stk and stk[-1][0] == "'" and (stk[-1] < now or (stk[-1] == now and stk[-1][1] > '1')):
            #     res.append(stk.pop())
            # stk.append(now)
            # i += length
            # continue
            while (stk and stk[-1][0] == '\\' and
                   (stk[-1] < now or (stk[-1] == now and stk[-1][1] > '1'))):
                res.append(stk.pop())  # 出栈优先级高的运算符
            stk.append(now)  # 入栈当前连接词
            i += length
            continue
        length = 1
        while i + length < ls and is_prop(s[i + length]):
            length += 1
        res.append(s[i:i + length])
        i += length

    while stk:
        if stk[-1] == "(":
            return null, 0
        res.append(stk.pop())

    return res, 1



def test():
    for idx, (input_formula, expected) in enumerate(test_cases):
        result = trans(input_formula)
        assert result == expected, f"测试用例 {idx + 1} 失败: {result} != {expected}"
    print("test success")
    return

test_cases = [
    ("p", (["p"], 1)),
    ("\\neg p", (["p", "\\1"], 1)),
    ("p \\wedge q", (["p", "q", "\\2"], 1)),
    ("p \\vee q", (["p", "q", "\\3"], 1)),
    ("(p \\vee q) \\wedge r", (["p", "q", "\\3", "r", "\\2"], 1)),
    ("(p \\vee q", ([], 0)),
    ("p \\wedge q \\vee r", (["p", "q", "\\2", "r", "\\3"], 1)),
    ("p \\rightarrow (q \\vee r)", (["p", "q", "r", "\\3", "\\4"], 1)),
    ("(p \\wedge (q \\vee r)) \\rightarrow s", (["p", "q", "r", "\\3", "\\2", "s", "\\4"], 1)),
    ("  ", ([], 1)),
]