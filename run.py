import pytest
import os


if __name__ == '__main__':   # pytest运行模式
    pytest.main()
    os.system("allure generate ./temp -o ./reports --clean")

