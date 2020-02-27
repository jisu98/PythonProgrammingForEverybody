from tornado.ioloop import IOLoop
from tornado.web import Application,RequestHandler,url
import myutil
import time
import pickle

history = []
users = []

class MainHandler(RequestHandler):
    def get(self):
        self.render('main.html')

class JoinHandler(RequestHandler):
    def post(self):
        name = self.get_body_argument('name')
        password = self.get_body_argument('password')
        errmesg = ''

        for i in range(len(users)+1):
            if i == len(users):
                errmesg = 'Please enter a valid name'
            elif name == users[i]['name'] and password == users[i]['password']:
                name = users[i]['name']
                password = users[i]['password']
                break
            elif name == users[i]['name']:
                errmesg = 'Wrong password'
                break

        if errmesg == '':
            self.render('join.html', name=name, id_time=time.asctime())
        else:
            self.render('join-fail.html', errmesg=errmesg)

class TalkHandler(RequestHandler):
    def post(self):
        global history
        id = self.get_body_argument('id')
        name = self.get_body_argument('name')
        mesg = self.get_body_argument('mesg')
        ip = self.request.remote_ip
        d = {'name': name, 'mesg': mesg, 'time':time.asctime(), 'ip': ip}
        history.append(d)
        self.render('talk.html', id=id, name=name, history=history)

class LogoutHandler(RequestHandler):
    def post(self):
        name = self.get_body_argument('name')
        if history != []:
            history[len(history) - 1]['time'] += '(logged out)'
        self.render('logout.html', name=name)

class RegisterHandler(RequestHandler):
    def get(self):
        self.render('register.html')

class ConfirmHandler(RequestHandler):
    def post(self):
        name = self.get_body_argument('name')
        password = self.get_body_argument('password')
        errmesg = ''
        confirm = self.get_body_argument('confirm')
        if name == '' or password == '' or confirm == '':
            errmesg = 'Please enter all items'
        elif password != confirm:
            errmesg = 'The password and the confirm should be the same'
        elif name in [n['name'] for n in users]:
            errmesg = 'This name already exists'
        if errmesg == '':
            d = {'name': name, 'password': password}
            users.append(d)
            self.render('reg-confirm.html')
        else:
            self.render('reg-fail.html', errmesg=errmesg)

class AdminHandler(RequestHandler):
    def get(self):
        global history
        self.render('admin.html', history=history)
    def post(self):
        global history
        cmd = self.get_body_argument('cmd')
        if cmd == 'dump':
            f = open('talk.hist', 'wb')
            pickle.dump(history,f)
            f.close()
        elif cmd == 'load':
            f = open('talk.hist', 'rb')
            history = pickle.load(f)
            f.close()
        self.render('admin.html', history=history)

def make_app():
    handlers = []
    handlers.append(url(r"/",MainHandler))
    handlers.append(url(r'/join',JoinHandler))
    handlers.append(url(r'/talk',TalkHandler))
    handlers.append(url(r'/logout',LogoutHandler))
    handlers.append(url(r'/register',RegisterHandler))
    handlers.append(url(r'/reg-confirm',ConfirmHandler))
    handlers.append(url(r'/admin',AdminHandler))
    
    return Application(handlers)
if __name__ == "__main__":
    fs = myutil.FastStop()
    fs.enable()
    app = make_app()
    app.listen(8080)
    IOLoop.current().start()
