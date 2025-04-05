import easygui

def input_window(title='输入框', msg='请输入内容：', default=''):
    return easygui.enterbox(msg, title, default)
