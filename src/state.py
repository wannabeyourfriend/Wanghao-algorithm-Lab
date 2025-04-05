"""
放全局变量S，规定逻辑连接词和优先级
联结词优先级：
否定>合取>析取>蕴含>等价
\neg \wedge \vee \rightarrow \leftrightarrow
1   2   3   4   5
"""

S = [
    ["\\neg"],  # 非
    ["\\wedge", "\\and"],  # 与
    ["\\vee", "\\or"],  # 或
    ["\\rightarrow", "\\to"],  # 蕴含
    ["\\leftrightarrow"]  # 双蕴含
]

