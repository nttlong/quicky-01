def test():
    import gevent

    def foo():
        print('Running in foo')
        gevent.sleep(10)
        print('Explicit context switch to foo again')

    def bar():
        print('Explicit context to bar')
        gevent.sleep(5)
        print('Implicit context switch back to bar')

    # gevent.joinall([
    #     gevent.spawn(foo),
    #     gevent.spawn(bar),
    # ])
    gevent.spawn(bar).run()
    return 1
import threading
th = threading.Thread(target=test)
th.start()