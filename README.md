# Windows 服务优化工具 v0.2.0

## 免责声明!!!!!!!!!

自用优化工具, 优化有风险, 禁用需谨慎

## 程序原理

比较简单, 就是把我尽量优化过后的系统剩余 running 的服务列出来. 肯定会有误杀, 所以 建议="无" 的先搜再关.

然后通过 **winreg** 内置库对注册表进行修改, 避免 **services.msc** 权限不够.

## 使用方法

1. 下载 exe

https://github.com/ClericPy/win_nonsense_services/releases

2. 或者下载源码, 执行 python run.pyw

## 使用说明:

1. 点击 [刷新] 按钮, 列出当前 "运行中" 的非核心服务
2. 点击 [服务] 按钮, 启动系统服务管理工具, 根据上述列表的建议, 对服务进行操作
    1. 禁用成功后, 再次点击 [刷新] 按钮, 可以看到改变
    2. 如果遇到无法禁用的服务, 可以暂不处理
    3. 无法禁用的服务, 需要在注册表编辑器 regedit 中专业操作
        1.  "计算机\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services"
        2. start_type, start, FailureActions 三个地方要动, 尤其第三个, 会导致 Windows Update 僵尸复活
3. 对列出的服务自行判断是否可关闭
    1. 如果需要关闭, 首先要保证是**管理员模式**启动
    2. 将 '服务名称' 填入输入框, 自行选择是否禁用
    3. 必要时需要禁用 FailureActions

