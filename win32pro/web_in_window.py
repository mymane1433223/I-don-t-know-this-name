import webview
def url_in_window(url, title='示例网页展示'):

    webview.create_window(title, url)
    webview.start()
# 定义要嵌入的网页的URL

def html_in_window(html, title='示例网页展示'):
    webview.create_window(title, html=html)
    webview.start()
