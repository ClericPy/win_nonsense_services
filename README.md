# Windows服务优化工具

## 程序原理

比较简单, 就是把我尽量优化过后的系统剩余 running 的服务列出来. 肯定会有误杀, 所以 建议="无" 的先搜再关.

## 下载 exe

https://github.com/ClericPy/win_nonsense_services/releases

## 使用说明:

1. 点击 [刷新] 按钮, 列出当前 "运行中" 的非核心服务

2. 点击 [服务] 按钮, 启动系统服务管理工具, 根据上述列表的建议, 对服务进行操作
    2.1 禁用成功后, 再次点击 [刷新] 按钮, 可以看到改变
    2.2 如果遇到无法禁用的服务, 可以暂不处理
    2.3 无法禁用的服务, 需要在注册表编辑器 regedit 中专业操作
        "计算机\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services"
