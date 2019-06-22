import sys
import getopt

def usage():
    print('usage: python main.py [-k keyword]  [-t txt_path] ')
    print('\t%-16s %s' % ('-h --help ', '帮助'))
    print('\t%-16s %s' % ('-k --keyword= ', '搜索关键字'))
    print('\t%-16s %s' % ('-t --txt= ', '包含歌名的文本路径'))
    print('example1: python main.py -k 只是太爱你')
    print('example1: python main.py -t ./musiclist.txt')

def set_opts(args):
    '''
    根据命令行输入的参数修改全局变量
    :param args: 命令行参数列表
    :return:
    '''
    try:
        opts, others = getopt.getopt(args, 'hk:t:', ['help', 'keyword=', 'txt='])
    except getopt.GetoptError as e:
        print('get error params!')
        echo.usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(2)

        elif o in ('-k', '--keyword'):
            set_option('keyword', a)
        elif o in ('-t', '--txt'):
            set_option('txt', a)
        else:
            assert False, 'unhandled option'

def init_option():
    # 命令行参数，写到函数里防止被意外初始化
    global OPTS
    OPTS = {
        # 搜索关键字
        'keyword': '',
        # 搜索文本中的多个曲目
        'txt': '',
    }

def set_option(opt, value):
    OPTS[opt] = value

def get_option(opt):
    return OPTS.get(opt, '')

if __name__ == '__main__':
    # 初始化全局变量
    init_option()

    if len(sys.argv) > 1:
        set_opts(sys.argv[1:])
    try:
        print(OPTS)
    except KeyboardInterrupt:
        sys.exit(0)

