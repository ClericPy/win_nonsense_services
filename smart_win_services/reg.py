# -*- coding: utf-8 -*-
import winreg


class Permission(object):
    KEY_ALL_ACCESS = winreg.KEY_ALL_ACCESS
    KEY_READ = winreg.KEY_READ
    CURRENT = KEY_ALL_ACCESS


class Value(object):
    __slots__ = ('name', 'value_type', 'value', 'service_obj')

    def __init__(self, name, value_type, value, service_obj):
        self.name = name
        self.value_type = value_type
        self.value = value
        self.service_obj = service_obj

    def __str__(self):
        return f'<{self.name}({self.value_type}): {self.value}>'

    def refresh(self):
        value = self.service_obj.get_value(self.name)
        if value:
            self.value_type = value.value_type
            self.value = value.value
        else:
            self.value_type = None
            self.value = None
        return self.value_type is not None

    def update(self, new_value, value_type=None):
        winreg.SetValueEx(self.service_obj.key, self.name, 0,
                          self.value_type if value_type is None else value_type,
                          new_value)
        ok = self.refresh()
        return ok

    @staticmethod
    def update_hex(raw_hex, value='01'):
        return raw_hex[:40] + value + raw_hex[42:56] + value + raw_hex[58:]

    def update_failure_actions(self, enable=True):
        raw_hex = self.value.hex()
        if enable:
            new_hex = self.update_hex(raw_hex, '01')
        else:
            new_hex = self.update_hex(raw_hex, '00')
        self.update(bytes.fromhex(new_hex))

    # def update_start(self, enable=True):


class Service(object):
    key = None
    START = ['自动(延迟启动)', '自动', '手动',
             '禁用']  # {1: '自动(延迟启动)', 2: '自动', 3: '手动', 4: '禁用'}

    def __init__(self, name):
        self.name = name
        self.key = self.get_key()

    def get_key(self):
        try:
            return winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                rf"SYSTEM\CurrentControlSet\Services\{self.name}", 0,
                Permission.CURRENT)
        except FileNotFoundError:
            return None

    def get_value(self, value_name):
        try:
            value, value_type = winreg.QueryValueEx(self.key, value_name)
            return Value(value_name, value_type, value, self)
        except FileNotFoundError:
            return None

    def update_start_type(self, state):
        value = self.get_value('Start')
        if state in self.START:
            state_index = self.START.index(state) + 1
        else:
            state_index = value.value
        result = value.update(state_index)
        if result and self.START[value.value - 1] == state:
            return True
        else:
            return False

    def check_start_type(self):
        value = self.get_value('Start')
        state = self.START[value.value - 1]
        return state

    def update_failure_actions(self, enable):
        value = self.get_value('FailureActions')
        if not value:
            return False
        return value.update_failure_actions(enable)

    def check_failure_actions(self):
        value = self.get_value('FailureActions')
        if not value:
            return False
        _hex = value.value.hex()
        a, b = _hex[40:42], _hex[56:58]
        return (a, b) != ('00', '00')

    def __del__(self):
        if self.key:
            winreg.CloseKey(self.key)


def test_disable():
    Permission.CURRENT = Permission.KEY_READ
    ss = Service('W32Time')
    # ss.update_failure_actions(False)
    # print(ss.update_start_type('禁用'))
    # print(ss.check_failure_actions())
    print(ss.check_start_type())


if __name__ == "__main__":
    test_disable()
