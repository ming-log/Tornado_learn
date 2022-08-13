---
Date: 2022-08-13 17:25:12
---

`Tornado`是一个`Python Web`框架和异步网络库，起初由`FriendFeed`开发，通过使用非阻塞网络`I/O`，`Tornado`可以支撑上万级的连接，处理长连接，`WebSockets`和其他需要与每个用户保持长久连接的应用。

# 编写第一个`Tornado`程序

首先创建`Tornado`工程，`tornado_demo`，在该工程下创建一个`hello.py`文件。

输入以下代码：

```python
import tornado.ioloop  # 主事件循环模块
import tornado.web  # Web框架模块


class MainHandler(tornado.web.RequestHandler):
    """定义get方法用于接收GET请求"""
    def get(self):
        self.write('Hello world!')  # 输出字符串

def make_app():
    """创建tornado应用，设置相关路由信息"""
    return tornado.web.Application([
        (r"/", MainHandler),  # 设置路由
    ],
    debug=True)

if __name__ == '__main__':
    app = make_app()  # 创建Tornado应用
    app.listen(8888)  # 设置监听端口
    print("Starting Server on port 8888...")  # 输出提示信息
    tornado.ioloop.IOLoop.current().start()  # 启动服务
```

然后在`cmd`控制台中运行该脚本。

![image-20220813154353678](C:/Users/log_ming/AppData/Roaming/Typora/typora-user-images/image-20220813154353678.png)

可以看到该`Tornado`项目已经运行起来了。

在浏览器中输入`http://127.0.0.1:8888/`即可访问`Web`界面。

![image-20220813154517337](Tornado%E6%A1%86%E6%9E%B6.assets/image-20220813154517337.png)

这样我们的第一个`Tornado`项目就创建好了，在指定端口下可以访问当index页面。

其中：

- `ioloop`是主事件循环模块。
- `web是WEB`框架模块
- `MainHandler`类用于处理用户请求。
- `make_app`函数，用于创建`Tornado`应用，并设置路由信息。`debug=True`表示进入调试模式，每次修改代码后会重启服务。在创建好应用后，还需要指定监听的端口，调用其`listen()`方法。

# 设置多个路由

前面我们已经创建了一个简单的`Tornado`项目，在网页根目录上输出`Hello world`。

能够输出该内容是因为我们在`make_app`函数中设置了路由对应规则，将根目录`'/'`，对应到了`MainHandler`类，在访问根目录的时候就会调用`MainHandler`类中的`get`方法给用户返回相应的页面内容。

但是一个`Web`项目不可能只有单个页面，当出现多个页面的时候如何进行处理呢？这个时候就需要设置多条路由规则，将不用的页面内容对应到不同的`Handler`类，处理不同的任务。

例如，我们再定义一个`/index`路由规则。

此时只需要做两个改动。

1. 增加一个`IndexHandler`类。

```python
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello Index')
```

2. 在`make_app`中设置路由

```python
def make_app():
    """创建tornado应用，设置相关路由信息"""
    return tornado.web.Application([
        (r"/", MainHandler),  # 设置路由
        (r"/index", IndexHandler)
    ],
    debug=True)
```

- 访问：`http://127.0.0.1:8888/index`

![image-20220813164134853](Tornado%E6%A1%86%E6%9E%B6.assets/image-20220813164134853.png)

同时路由规则还支持使用正则表达式进行匹配。

- 修改路由让路径`http://127.0.0.1:8888/re/REa`、`http://127.0.0.1:8888/re/REb`、`http://127.0.0.1:8888/re/REc`、`http://127.0.0.1:8888/re/REd`均返回`MainHandler`。

  修改`make_app`代码如下：

  ```python
  def make_app():
      """创建tornado应用，设置相关路由信息"""
      return tornado.web.Application([
          (r"/", MainHandler),  # 设置路由
          (r"/index", IndexHandler)，
          (r"/re/RE[abcd]", MainHandler)
      ],
      debug=True)
  ```

- 访问`http://127.0.0.1:8888/re/REa`、`http://127.0.0.1:8888/re/REb`、`http://127.0.0.1:8888/re/REc`、`http://127.0.0.1:8888/re/REd`发现均返回以下页面。

![image-20220813172121232](Tornado%E6%A1%86%E6%9E%B6.assets/image-20220813172121232.png)

# HTTP方法

`Tornado`同样支持各种请求，请求需要在`Handler`中进行定义，继承自`tornado.web.RequestHander`父类。

`RequestHander`提供了如下方法：

- `RequestHander.get(*args, **kwargs)`
- `RequestHander.head(*args, **kwargs)`
- `RequestHander.post(*args, **kwargs)`
- `RequestHander.delete(*args, **kwargs)`
- `RequestHander.patch(*args, **kwargs)`
- `RequestHander.put(*args, **kwargs)`
- `RequestHander.options(*args, **kwargs)`

所以，只需要在自定义的操作类中创建对应方法，即可实现增删改查等功能。

例如：创建一个既可以接收`GET`请求，又可以接收`POST`请求的`LoginHander`类，代码如下：

```python
class LoginHander(tornado.web.RequestHandler):
    def get(self):
        self.write("This is login page")

    def post(self):
        username = self.get_argument('username', '')  # 接收用户名参数
        password = self.get_argument('password', '')  # 接收密码参数
        self.write(f'username is {username} password is {password}')
```

在`make_app`中添加路由信息：

```python
def make_app():
    """创建tornado应用，设置相关路由信息"""
    return tornado.web.Application([
        (r"/", MainHandler),  # 设置路由
        (r"/index", IndexHandler),
        (r"/login", LoginHander)  # 设置登录路由
    ],
    debug=True)
```

- 访问`http://127.0.0.1:8888/login`

![image-20220813164919289](Tornado%E6%A1%86%E6%9E%B6.assets/image-20220813164919289.png)

可以发现**get请求成功**。

然后打开一个`cmd`终端，测试`post`请求，输入以下代码：

```powershell
curl -d "username=minglog&password=123456" "http://127.0.0.1:8888/login" 
```

返回结果：

![image-20220813165203770](Tornado%E6%A1%86%E6%9E%B6.assets/image-20220813165203770.png)

发现**post请求成功**

# 模板

前面我们响应的结果都是简单的文字，在实际需求中仅仅返回文字内容肯定是不够的，我们一般会返回相对应的HTML页面内容，返回的HTML页面内容我们称为模板文件。

使用模板时，需要先在应用中设置`template_path`模板路径【在`make_app`函数中设置`template_path`的值，一般设置为当前工程路径下的`templates`文件夹】，然后使用`render()`方法渲染模板。

## 设置模板路径

```python
def make_app():
    """创建tornado应用，设置相关路由信息"""
    return tornado.web.Application([
        (r"/", MainHandler),  # 设置路由
        (r"/index", IndexHandler),
        (r"/login", LoginHander)  # 设置登录路由
    ],
    template_path = os.path.join(os.path.dirname(__file__), "templates"),  # 设置模板路径
    debug=True  # 调试模式
    )
```

## 创建`templates`文件夹，并编写模板文件

模板文件代码如下：

```HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>login</title>
</head>
<body>
    <form class="form-horizontal" action="" method="post">
        <div class=""form-group>
            <label for="username" class="col-sm-2 control-label">用户名</label>
            <div class="col-sm-10">
                <input type="text" class="form-control" id="username" name="username" placeholder="请输入用户名">
            </div>
        </div>
        <div class=""form-group>
            <label for="password" class="col-sm-2 control-label">密 码</label>
            <div class="col-sm-10">
                <input type="password" class="form-control" id="password" name="password" placeholder="请输入密码">
            </div>
        </div>
        <div class="form-group">
            <div class="col-sm-offset-2 col-sm-10">
                <button type="submit" class="btn btn-primary"> 登录</button>
            </div>
        </div>
    </form>
</body>
</html>
```

## 修改`LoginHander`

为了让响应返回指定的模板文件，需要对前面的`LoginHander`类中的`get`方法进行相应的修改，让其返回`login.html`页面。

```python
class LoginHander(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.get_argument('username', '')  # 接收用户名参数
        password = self.get_argument('password', '')  # 接收密码参数
        self.write(f'username is {username} password is {password}')
```

## 测试结果

- 再次访问`http://127.0.0.1:8888/login`

![image-20220813171000575](Tornado%E6%A1%86%E6%9E%B6.assets/image-20220813171000575.png)

- 输入用户名和密码，点击登录。

![image-20220813171029949](Tornado%E6%A1%86%E6%9E%B6.assets/image-20220813171029949.png)

发现可以直接返回我们输入的内容。