# encoding=utf-8

import sys
from testScripts.test_for_redemption import *



#设置此次测试环境编码为utf8
reload(sys)
sys.setdefaultencoding('utf-8')


if __name__=='__main__':
    test_for_redemption()