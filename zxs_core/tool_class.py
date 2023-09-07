class ZXSPrint:
    """
    自定义的打印类，控制打印
    lev：整体打印优先级
    """
    lev = int

    def __init__(self, lev=0):
        self.lev = lev

    # pri：本次打印优先级，该数字大于整体打印优先级的时候才会打印
    def print(self, *objects, sep=' ', end='\n', file=None, flush=False, pri=0):
        if self.lev <= pri:
            print(*objects, sep=' ', end='\n', file=None, flush=False)
        else:
            pass
