
import trollius
import time
import random

@trollius.coroutine
def x(k):
    t = random.random()
    print k, t
    trollius.sleep(t)

loop = trollius.get_event_loop()
tasks =[]
for k in range(0,10):
    tasks.append(
        loop.create_task(x(k))
    )
    # trollius.ensure_future(loop.create_task(x(k)), loop)
# trollius.ensure_future(tasks,loop)

loop.run_until_complete(trollius.wait(tasks))
my_var =1
ok= True
def watch():
    old_var =0
    while ok:
        if my_var != old_var:
            print my_var
            old_var = my_var

loop = trollius.get_event_loop()

loop.run_in_executor(trollius.executor,watch)
