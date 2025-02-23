import pytest
import os

###这是主函数
if __name__ == '__main__':   # pytest运行模式
    pytest.main()
    os.system("allure generate ./temp -o ./reports --clean")

