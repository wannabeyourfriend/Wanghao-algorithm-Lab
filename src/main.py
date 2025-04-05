import input_proc
import binary_tree
import infer
import test


def work_circ():
    test_examples = test.Test('test.txt')
    expressions = test_examples.get_expressions()
    back_expressions = []
    # print("读取的中缀表达式：")
    for exper in expressions:
        # print(exper)
        back_expressions.append(input_proc.trans(exper))
    # print("转换为后缀表达式")
    rts = []
    for exper in back_expressions:
        # print(exper)
        if exper[1] == 1:
            rts.append(binary_tree.BinaryTree(exper[0]))
    return rts

def main():
    input_proc.init()
    __input0 = ","
    _input0 = input_proc.trans(__input0)
    _tree0 = binary_tree.BinaryTree(_input0[0])
    rts = work_circ()
    count = 0
    for rt in rts:
        right_side = [rt, ]
        left_side = [_tree0, ]
        _infer = infer.Inference(left_side, right_side, _tree0)
        print(count)
        count += 1
        print(" Begin inference!")
        is_true = _infer.inference(0, "", 0, 0)
        if is_true:
            print("Result: T")
        else:
            print("Result: F")


if __name__ == "__main__":
    main()
