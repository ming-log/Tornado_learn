import tornado.ioloop  # 主事件循环模块
import tornado.web  # Web框架模块
import os

class MainHandler(tornado.web.RequestHandler):
    """定义get方法用于接收GET请求"""
    def get(self):
        self.write('Hello world!')  # 输出字符串



class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello Index')


class LoginHander(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.get_argument('username', '')  # 接收用户名参数
        password = self.get_argument('password', '')  # 接收密码参数
        self.write(f'username is {username} password is {password}')

def make_app():
    """创建tornado应用，设置相关路由信息"""
    return tornado.web.Application([
        (r"/", MainHandler),  # 设置路由
        (r"/re/RE[abcd]", MainHandler),
        (r"/index", IndexHandler),
        (r"/login", LoginHander)  # 设置登录路由
    ],
    template_path = os.path.join(os.path.dirname(__file__), "templates"),  # 设置模板路径
    debug=True  # 调试模式
    )

if __name__ == '__main__':
    app = make_app()  # 创建Tornado应用
    app.listen(8888)  # 设置监听端口
    print("Starting Server on port 8888...")  # 输出提示信息
    tornado.ioloop.IOLoop.current().start()  # 启动服务
