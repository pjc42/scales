import random
from gevent import monkey

import gevent
from gevent.event import Event

from scales.tmux.thriftmux import ThriftMux
from scales.varzsocketwrapper import VARZ_DATA

monkey.patch_all(thread=False)

if __name__ == '__main__':
  def fn():
    from gen_py.hello import Hello
    client = ThriftMux.newClient(Hello.Iface, 'tcp://localhost:8080')
    ret = client.hi_async('test')
    print ret.get()
    def fn2(n):
      x = 0
      while True:
        x+=1
        try:
          print '%d %s' % (n, client.hi('test'))
        except:
          import traceback
          traceback.print_exc()

        gevent.sleep(random.random() / 2)

    gevent.spawn(fn2, 1)
    gevent.spawn(fn2, 2)

    e = Event()
    e.wait(10)

    import pprint
    pprint.pprint(VARZ_DATA)


  fn()
