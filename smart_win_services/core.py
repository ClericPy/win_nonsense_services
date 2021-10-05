# -*- coding: utf-8 -*-

import ctypes
import re
import subprocess

import psutil
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import _BuildResults
from .reg import Service

OKS = {
    'Appinfo': '手动',
    'AudioEndpointBuilder': '自动',
    'Audiosrv': '自动',
    'BFE': '自动',
    'BrokerInfrastructure': '自动',
    'BthAvctpSvc': '手动',
    'camsvc': '手动',
    'CDPSvc': '自动',
    'CoreMessagingRegistrar': '自动',
    'CryptSvc': '自动',
    'DcomLaunch': '自动',
    'DeviceAssociationService': '自动',
    'Dhcp': '自动',
    'DispBrokerDesktopSvc': '自动',
    'Dnscache': '自动',
    'DolbyDAXAPI': '自动',
    'EventLog': '自动',
    'EventSystem': '自动',
    'FontCache': '自动',
    'hidserv': '手动',
    'HipsDaemon': '自动',
    'hkosdservice': '自动',
    'HRWSCCtrl': '自动',
    'InstallService': '手动',
    'jhi_service': '自动',
    'LSM': '自动',
    'MacType': '自动',
    'mpssvc': '自动',
    'NcbService': '手动',
    'netprofm': '手动',
    'NlaSvc': '自动',
    'nsi': '自动',
    'NvContainerLocalSystem': '自动',
    'PlugPlay': '手动',
    'PolicyAgent': '手动',
    'Power': '自动',
    'ProfSvc': '自动',
    'QPCore': '自动',
    'RasMan': '自动',
    'RpcEptMapper': '自动',
    'RpcSs': '自动',
    'RtkAudioUniversalService': '自动',
    'SamSs': '自动',
    'Schedule': '手动',
    'seclogon': '手动',
    'SecurityHealthService': '手动',
    'SENS': '自动',
    'ShellHWDetection': '自动',
    'SSDPSRV': '手动',
    'SstpSvc': '手动',
    'StateRepository': '手动',
    'StorSvc': '手动',
    'SysMain': '自动',
    'SystemEventsBroker': '自动',
    'TabletInputService': '禁用',
    'TimeBrokerSvc': '手动',
    'UserManager': '自动',
    'VaultSvc': '手动',
    'Wcmsvc': '自动',
    'WinHttpAutoProxySvc': '手动',
    'Winmgmt': '自动',
    'WlanSvc': '自动',
    'wscsvc': '自动',
    'CDPUserSvc_46c92': '自动',
    'Intel(R) TPM Provisioning Service': '自动',
    'gpsvc': '自动',
    'WpnUserService_46c92': '手动'
}
NOT_OKS = {
    'AJRouter': '手动',
    'ALG': '手动',
    'AppIDSvc': '手动',
    'AppMgmt': '手动',
    'AppReadiness': '手动',
    'AppXSvc': '手动',
    'autotimesvc': '手动',
    'AxInstSV': '手动',
    'BDESVC': '手动',
    'BITS': '禁用',
    'Browser': '手动',
    'BTAGService': '禁用',
    'bthserv': '禁用',
    'CertPropSvc': '手动',
    'ClipSVC': '禁用',
    'COMSysApp': '手动',
    'cphs': '手动',
    'cplspcon': '手动',
    'debugregsvc': '自动',
    'defragsvc': '手动',
    'DeveloperToolsService': '手动',
    'DeviceInstall': '手动',
    'DevQueryBroker': '手动',
    'diagnosticshub.standardcollector.service': '手动',
    'diagsvc': '手动',
    'DiagTrack': '手动',
    'DisplayEnhancementService': '手动',
    'DmEnrollmentSvc': '手动',
    'dmwappushservice': '手动',
    'DoSvc': '手动',
    'dot3svc': '手动',
    'DPS': '禁用',
    'DsmSvc': '手动',
    'DsSvc': '手动',
    'DusmSvc': '手动',
    'Eaphost': '手动',
    'EFS': '手动',
    'embeddedmode': '手动',
    'EntAppSvc': '手动',
    'Fax': '手动',
    'fdPHost': '手动',
    'FDResPub': '手动',
    'fhsvc': '手动',
    'Flash Helper Service': '禁用',
    'FontCache3.0.0.0': '禁用',
    'FrameServer': '手动',
    'GamingBoxHost': '禁用',
    'GoogleChromeElevationService1d58942908d8e1a': '禁用',
    'GraphicsPerfSvc': '手动',
    'gupdate': '手动',
    'gupdatem': '手动',
    'HvHost': '手动',
    'icssvc': '手动',
    'igfxCUIService2.0.0.0': '禁用',
    'IKEEXT': '手动',
    'Intel(R) Capability Licensing Service TCP IP Interface': '手动',
    'iphlpsvc': '手动',
    'IpxlatCfgSvc': '手动',
    'KeyIso': '禁用',
    'KtmRm': '手动',
    'LanmanServer': '禁用',
    'LanmanWorkstation': '禁用',
    'lfsvc': '禁用',
    'LicenseManager': '手动',
    'lltdsvc': '手动',
    'lmhosts': '禁用',
    'LMS': '手动',
    'LxpSvc': '手动',
    'MapsBroker': '手动',
    'MSDTC': '手动',
    'MSiSCSI': '手动',
    'msiserver': '手动',
    'NaturalAuthentication': '手动',
    'NcaSvc': '手动',
    'NcdAutoSetup': '手动',
    'Netlogon': '手动',
    'Netman': '手动',
    'NetSetupSvc': '手动',
    'NetTcpPortSharing': '禁用',
    'NgcCtnrSvc': '手动',
    'NgcSvc': '手动',
    'NvContainerNetworkService': '手动',
    'NVDisplay.ContainerLocalSystem': '手动',
    'p2pimsvc': '手动',
    'p2psvc': '手动',
    'PcaSvc': '禁用',
    'perceptionsimulation': '手动',
    'PerfHost': '手动',
    'PhoneSvc': '手动',
    'pla': '手动',
    'PNRPAutoReg': '手动',
    'PNRPsvc': '手动',
    'PrintNotify': '手动',
    'PushToInstall': '手动',
    'qmbsrv': '手动',
    'QQPCRTP': '禁用',
    'QWAVE': '手动',
    'RasAuto': '手动',
    'RemoteAccess': '禁用',
    'RemoteRegistry': '禁用',
    'RetailDemo': '手动',
    'RmSvc': '手动',
    'RpcLocator': '手动',
    'SCardSvr': '手动',
    'ScDeviceEnum': '手动',
    'SCPolicySvc': '手动',
    'SDRSVC': '手动',
    'SEMgrSvc': '手动',
    'SensorDataService': '手动',
    'SensorService': '手动',
    'SensrSvc': '手动',
    'SessionEnv': '手动',
    'SgrmBroker': '手动',
    'SharedAccess': '手动',
    'SharedRealitySvc': '手动',
    'shpamsvc': '禁用',
    'smphost': '手动',
    'SmsRouter': '手动',
    'SNMPTRAP': '手动',
    'spectrum': '手动',
    'Spooler': '手动',
    'sppsvc': '手动',
    'ssh-agent': '禁用',
    'sshd': '手动',
    'SshdBroker': '手动',
    'Steam Client Service': '手动',
    'stisvc': '手动',
    'svsvc': '手动',
    'swprv': '手动',
    'TapiSrv': '手动',
    'TermService': '手动',
    'TesService': '手动',
    'TGuardSvc': '手动',
    'Themes': '禁用',
    'TieringEngineService': '手动',
    'TokenBroker': '禁用',
    'TrkWks': '禁用',
    'TroubleshootingSvc': '手动',
    'TrustedInstaller': '手动',
    'tzautoupdate': '禁用',
    'UmRdpService': '手动',
    'upnphost': '手动',
    'UsoSvc': '禁用',
    'VacSvc': '手动',
    'VBoxSDS': '禁用',
    'vds': '手动',
    'vmicguestinterface': '手动',
    'vmicheartbeat': '手动',
    'vmickvpexchange': '手动',
    'vmicrdv': '手动',
    'vmicshutdown': '手动',
    'vmictimesync': '手动',
    'vmicvmsession': '手动',
    'vmicvss': '手动',
    'VSS': '手动',
    'W32Time': '手动',
    'WaaSMedicSvc': '手动',
    'WalletService': '手动',
    'WarpJITSvc': '手动',
    'wbengine': '手动',
    'WbioSrvc': '禁用',
    'wcncsvc': '手动',
    'WdiServiceHost': '手动',
    'WdiSystemHost': '手动',
    'WdNisSvc': '手动',
    'WebClient': '手动',
    'WebManagement': '禁用',
    'Wecsvc': '手动',
    'WEPHOSTSVC': '手动',
    'wercplsupport': '手动',
    'WerSvc': '手动',
    'WFDSConMgrSvc': '手动',
    'WiaRpc': '手动',
    'WinDefend': '手动',
    'WinRM': '手动',
    'wisvc': '手动',
    'wlidsvc': '手动',
    'wlpasvc': '手动',
    'WManSvc': '手动',
    'wmiApSrv': '手动',
    'WMPNetworkSvc': '手动',
    'workfolderssvc': '手动',
    'WpcMonSvc': '手动',
    'WPDBusEnum': '手动',
    'WpnService': '手动',
    'WSearch': '禁用',
    'wuauserv': '禁用',
    'WwanSvc': '手动',
    'XblAuthManager': '禁用',
    'XblGameSave': '手动',
    'XboxGipSvc': '手动',
    'XboxNetApiSvc': '手动',
    'AarSvc_46c92': '手动',
    'BcastDVRUserService_46c92': '手动',
    'BluetoothUserService_46c92': '手动',
    'CaptureService_46c92': '手动',
    'cbdhsvc_46c92': '禁用',
    'ConsentUxUserSvc_46c92': '手动',
    'CredentialEnrollmentManagerUserSvc_46c92': '手动',
    'DeviceAssociationBrokerSvc_46c92': '手动',
    'DevicePickerUserSvc_46c92': '手动',
    'DevicesFlowUserSvc_46c92': '手动',
    'MessagingService_46c92': '手动',
    'OneSyncSvc_46c92': '禁用',
    'PimIndexMaintenanceSvc_46c92': '手动',
    'PrintWorkflowUserSvc_46c92': '手动',
    'UnistoreSvc_46c92': '手动',
    'UserDataSvc_46c92': '手动'
}

user32 = ctypes.windll.user32
# (2560, 1440)
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
WINDOW_SIZE = [int(screensize[0] * 0.6), int(screensize[1] * 0.6)]


def show_me():
    OKS = {}
    alias = {'automatic': '自动', 'manual': '手动', 'disabled': '禁用'}
    for i in psutil.win_service_iter():
        try:
            item = i.as_dict()
            item['start_type'] = alias.get(item['start_type'],
                                           item['start_type'])
            if item['status'] == 'running':
                OKS[item['name']] = item['start_type']
        except (psutil.NoSuchProcess, FileNotFoundError):
            pass
    print('OKS = ', OKS)
    NOT_OKS = {}
    for i in psutil.win_service_iter():
        try:
            item = i.as_dict()
            item['start_type'] = alias.get(item['start_type'],
                                           item['start_type'])
            if item['name'] not in OKS:
                NOT_OKS[item['name']] = item['start_type']
        except (psutil.NoSuchProcess, FileNotFoundError):
            pass
    print('NOT_OKS = ', NOT_OKS)


def get_recommend(i):
    if re.match(r'^(WpnUserService|CDPUserSvc)', i['name']):
        return '保持原样'
    return NOT_OKS.get(i["name"], "无")


def get_text():
    items = []
    alias = {'automatic': '自动', 'manual': '手动', 'disabled': '禁用'}
    for i in psutil.win_service_iter():
        try:
            item = i.as_dict()
            item['start_type'] = alias.get(item['start_type'],
                                           item['start_type'])
            if item['status'] == 'running' and item['name'] not in OKS:
                items.append(item)
        except (psutil.NoSuchProcess, FileNotFoundError):
            pass
    if not items:
        return '没有多余服务'
    result = []
    for i in items:
        string = f'[全称]: {i["display_name"]}\n[名称]: {i["name"]}\n[启动]: {i["start_type"]}\n[建议]: {get_recommend(i)}\n[进程]: {i["pid"]} "{i["binpath"]}"\n[简介]: {i["description"]}'
        result.append(string)
    sep = '\n' + '=' * 30 + '\n'
    text = f'总共 {len(result)} 个非核心服务' + sep
    text += sep.join(result)
    return text


def get_help():
    return '''
使用说明:

1. 点击 [刷新] 按钮, 列出当前 "运行中" 的非核心服务

2. 点击 [服务] 按钮, 启动系统服务管理工具, 根据上述列表的建议, 对服务进行操作
    2.1 禁用成功后, 再次点击 [刷新] 按钮, 可以看到改变
    2.2 如果遇到无法禁用的服务, 可以暂不处理
    2.3 无法禁用的服务, 需要在注册表编辑器 regedit 中专业操作
        "计算机\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services"

3. 对列出的服务自行判断是否可关闭
    3.1 如果需要关闭, 首先要保证是管理员模式启动
    3.2 将 '服务名称' 填入输入框, 自行选择是否禁用
    3.3 必要时需要禁用 FailureActions
'''


def run_services():
    subprocess.Popen("services.msc", shell=True)


def get_st_fa(service_name):
    if not service_name:
        return ('', '')
    serv = Service(service_name.strip())
    if not serv.key:
        return ('', '')
    start_type = serv.check_start_type()
    fa = '启用' if serv.check_failure_actions() else '禁用'
    return start_type, fa


def update_st_fa(window):
    _, values = _BuildResults(window, False, window)
    service_name = values['service_name'] or ''
    service_name = service_name.strip()
    if not service_name:
        return ('', '')
    serv = Service(service_name)
    if not serv.key:
        return ('', '')
    start_type = values['start_type']
    if start_type:
        serv.update_start_type(start_type)
    failure_actions = values['failure_actions']
    if failure_actions:
        enable = True if failure_actions == '启用' else False
        serv.update_failure_actions(enable)


def refresh_reg_window(window):
    try:
        _, values = _BuildResults(window, False, window)
        service_name = values['service_name']
        st, fa = get_st_fa(service_name)
        window.find_element('start_type').Update(st)
        window.find_element('failure_actions').Update(fa)
        pid = psutil.win_service_get(
            service_name).pid() if service_name else '0'
    except (psutil.NoSuchProcess, FileNotFoundError, PermissionError) as err:
        pid = '0'
        sg.PopupOK(repr(err), title='error')
    window.find_element('service_pid').Update(pid)


def refresh_output(window):
    window.find_element('output').Update(get_text())


def _main():
    # show_me()
    # return
    layout = [[
        sg.Button('刷新',
                  size=(10, 2),
                  button_color=('black', 'white'),
                  key='refresh'),
        sg.Button('服务',
                  size=(10, 2),
                  button_color=('black', 'white'),
                  key='serv'),
        sg.Button('退出',
                  size=(10, 2),
                  button_color=('black', 'white'),
                  key='Exit'),
        sg.Button('帮助',
                  size=(10, 2),
                  button_color=('black', 'white'),
                  key='help'),
        sg.Text('服务名称\n(注册表):', size=(10, 2)),
        sg.Input(key='service_name',
                 size=(15, 1),
                 change_submits=True,
                 tooltip='填入名称, 而不是全称'),
        sg.Text('启动类型'),
        sg.InputCombo(['', '自动(延迟启动)', '自动', '手动', '禁用'],
                      change_submits=True,
                      size=(6, 2),
                      key='start_type'),
        sg.Text('FailureActions'),
        sg.InputCombo(['', '启用', '禁用'],
                      change_submits=True,
                      size=(6, 2),
                      key='failure_actions'),
        sg.Text('PID'),
        sg.Input(size=(6, 1), key='service_pid'),
        sg.Button('KILL',
                  size=(4, 1),
                  button_color=('red', 'white'),
                  key='kill_pid'),
    ], [sg.Output(size=(999, 999), key='output', font=("", 16))]]
    try:
        Service('W32Time').get_key()
    except PermissionError:
        layout[0] = layout[0][:4]
        layout[0].append(sg.Text('非管理员模式, 无法修改', text_color='red'))
    window = sg.Window(title='服务优化工具',
                       layout=layout,
                       size=WINDOW_SIZE,
                       resizable=True)
    window.Read(timeout=0)
    refresh_output(window)
    while 1:
        event, values = window.Read()
        # print(event, values)
        if event == 'refresh':
            refresh_output(window)
        elif event == 'serv':
            run_services()
        elif event == 'help':
            window.find_element('output').Update(get_help())
        elif event == 'service_name':
            refresh_reg_window(window)
        elif event == 'kill_pid':
            pid = values.get('service_pid') or 0
            if pid and int(pid):
                try:
                    psutil.Process(int(pid)).kill()
                except Exception as err:
                    sg.PopupOK(repr(err))
            window.find_element('service_pid').Update('0')
            refresh_reg_window(window)
            refresh_output(window)
        elif event in {'start_type', 'failure_actions'}:
            try:
                update_st_fa(window)
                refresh_reg_window(window)
                refresh_output(window)
            except Exception as err:
                sg.PopupOK(repr(err))
        elif event in (None, 'Cancel', 'Exit'):
            break
    window.Close()


def main():
    try:
        _main()
    except Exception as err:
        sg.PopupOK(repr(err), title='error')


if __name__ == "__main__":
    main()
