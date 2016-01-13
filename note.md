###模块调用流程
```python
(venv)$:python manage runserver--->app.create_app()--->main.main(Blueprint)--->views.py && errors.py--->templates/db/static等资源
```
###关于可能存在的循环依赖错误
1. main/__init_.py中：
```python
from flask import Blueprint
main = Blueprint('main', __name__)
from . import views, errors
```
main/views.py中：
```python
from . import main

```
？？？因为在同一模块中，所以没有问题？？？，若将`from . import views, errors` 提前到main的定义前则出现错误。

2.在app/__init_.py中：`from .main import main as main_blueprint`必须放在`db = SQLAlchemy()`的后面，因为：

main/__init_.py中：
```python
from flask import Blueprint
main = Blueprint('main', __name__)
from . import views, errors
```
main/views.py中：
```python
from .. import db
```
app/__init_.py中：
```python
from .main import main as main_blueprint
db = SQLAlchem()
```
**猜测：**在app.create_app中`from .main import main as main_blueprint`时间接引用了views，而views.py又import了app.db，循环依赖啦？
**疑问：**在app.create_app中`from .main import main as main_blueprint`时main已经定义，且`from . import views, errors`在main的定义之后，为什么views中对db的依赖会造成 “pp/__init_.py中：`from .main import main as main_blueprint`必须放在`db = SQLAlchemy()`的后面”？？

3.总结：为什么在mian/__init_.py中`import views`时只需要放在蓝本main的定义之后views.py中`from . import main`就不存在依赖问题，而在app/__init_.py中的`from .main import main as main_blueprint`为什么必须放在db的定义之后，否则将由于views.py中的`import db`导致循环依赖错误？？ import main的时候main应该已经被定义并赋值了，为什么还会牵涉到views.py里面的import db呢？难道在app/__init_.py中 from .main import main as main_blueprint时候就已经要把views.py执行一遍吗，它的引入可是放在main的定义之后哟，想不通。。。

4.解答：import时候被导入的文件中所有还是最外层语句都将被执行一遍？(被引入文件中的所有声明语句都需要被执行，import views时views.py中的import main只涉及main/__init_.py中main的定义和import views, errors，此部分暂不存在问题（由于在同一包中，且导入自己等）；from .main import main as main_blueprint时也涉及到了main/__init_.py中main的定义和import views, errors。在此两种情况下views.py中的import db语句都会到app/__init_.py中找db的定义。此时若将from .main import main as main_blueprint放入create_app()函数的定义外部，import db时又需要from .main import main，导致循环依赖；若将from .main import main as main_blueprint放入create_app()函数的定义内部则由于import db语句不会执行create_db()函数，因此不会执行from .main import main语句，因此不会引起循环依赖错误。

**from .main import main as main_blueprint  # 将此句放入create_app()函数的定义内部，这样在import db时就不会需要回到main/__init__.py去执行views.py而造成循环依赖错误啦。。。***







































