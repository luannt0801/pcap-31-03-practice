# PCAP-31-03 — Logic Edge Cases & Exam Review Guide

> **Mục tiêu:** Tài liệu này tập trung vào các câu PCAP dễ sai không phải vì cú pháp khó, mà vì **logic thực thi của Python**: thứ tự evaluate, scope, object reference, inheritance, exception flow, lambda/closure và I/O.
> 
> Theo syllabus PCAP-31-03, đề thi gồm 5 phần; trong đó **OOP chiếm 34%**, Miscellaneous 22%, Strings 18%, Exceptions 14%, Modules & Packages 12%. Vì vậy phần OOP, lambda/closure/comprehension và exception nên được ưu tiên khi ôn.

---

# 0. Cách tư duy khi làm câu PCAP

Với những câu code ngắn, **đừng đọc theo nghĩa tiếng Anh**. Hãy chạy code trong đầu theo thứ tự:

1. **Code nào được execute trước?**
    
2. **Biến đang chứa value hay reference tới object?**
    
3. **Scope hiện tại là gì?**
    
4. **Nếu có class: tìm attribute/method ở đâu trước?**
    
5. **Nếu có exception: exception nào được bắt trước?**
    
6. **Nếu có lambda/closure: biến được bind lúc nào?**
    
7. **Nếu có comprehension: thứ tự vòng lặp là gì?**
    
8. **Nếu có I/O: con trỏ file đang ở đâu?**
    
9. Cuối cùng mới tính output.
    

Một nguyên tắc rất hữu ích:

> **PCAP thường không hỏi “Python có syntax này không?” mà hỏi “Python sẽ thực sự execute nó như thế nào?”**

---

# 1. Modules & Packages

Theo syllabus, phần này bao gồm import variants, `dir()`, `sys.path`, `math`, `random`, `platform`, user-defined modules/packages, `__name__`, private/public variables và `__init__.py`.

---

## 1.1 `import` vs `from ... import`

### Case cơ bản

```python
import math

print(math.sqrt(16))
```

`math` là namespace/module object.

Trong khi:

```python
from math import sqrt

print(sqrt(16))
```

thì `sqrt` được đưa trực tiếp vào namespace hiện tại.

---

## Edge case: alias

```python
import math as m

print(m.sqrt(16))
```

Sau `as m`, tên `math` không phải tên bạn sử dụng trong namespace hiện tại nữa.

---

## Edge case: `from ... import *`

```python
from math import *

print(sqrt(16))
```

`*` import các tên public vào namespace hiện tại.

Điểm quan trọng khi thi:

```python
import math

print(sqrt(16))
```

sẽ lỗi vì bạn chưa import `sqrt` trực tiếp.

---

# 1.2 `dir()` — cực kỳ dễ nhầm

```python
import math

print("sqrt" in dir(math))
```

Kết quả:

```text
True
```

`dir(math)` cho danh sách các tên mà object/module expose.

Ví dụ:

```python
x = 10

print("real" in dir(x))
```

Có thể là `True`, bởi vì `int` có nhiều attributes/methods.

### Tư duy

`dir(x)`:

> "Object này có những tên/attribute nào?"

Không phải:

> "Object này có những giá trị nào?"

---

# 1.3 `sys.path`

Python tìm module theo các location trong:

```python
sys.path
```

Ví dụ:

```python
import sys

print(sys.path)
```

Đây là **list các đường dẫn** Python sử dụng khi tìm module.

Edge case:

```python
import sys

print(type(sys.path))
```

Kết quả:

```text
<class 'list'>
```

---

# 1.4 `math.floor()`, `ceil()`, `trunc()`

Đây là nhóm rất đáng luyện.

```python
import math

print(math.floor(3.8))
print(math.ceil(3.2))
print(math.trunc(3.8))
```

Kết quả:

```text
3
4
3
```

Nhưng negative number mới là bẫy.

```python
print(math.floor(-3.8))
print(math.ceil(-3.8))
print(math.trunc(-3.8))
```

Kết quả:

```text
-4
-3
-3
```

### Nhớ:

|Function|Ý nghĩa|
|---|---|
|`floor(x)`|số nguyên lớn nhất `<= x`|
|`ceil(x)`|số nguyên nhỏ nhất `>= x`|
|`trunc(x)`|bỏ phần thập phân về phía 0|

### Mental model

```text
-4 ---- -3.8 ---- -3

floor → -4
ceil  → -3
trunc → -3
```

---

# 1.5 `random.seed()` — deterministic nhưng không phải random hoàn toàn

```python
import random

random.seed(10)

print(random.randint(1, 10))
print(random.randint(1, 10))
```

Nếu chạy lại với cùng seed và cùng sequence calls, kết quả sẽ giống nhau.

Điểm cần nhớ:

```python
random.seed(10)
```

không trả về random number.

Nó **thiết lập trạng thái của pseudo-random generator**.

---

# 1.6 `choice()` vs `sample()`

```python
import random

x = [1, 2, 3, 4]

print(random.choice(x))
```

`choice()`:

- lấy **một phần tử**
    
- không cần trả về list
    

Trong khi:

```python
random.sample(x, 2)
```

trả về **list gồm 2 phần tử khác nhau**.

Ví dụ:

```python
random.sample([1, 2, 3, 4], 2)
```

có thể:

```text
[4, 1]
```

Không được nhầm với:

```python
choice()
```

---

# 1.7 `__name__` — edge case rất quan trọng

File:

```python
test.py
```

có:

```python
print(__name__)
```

Nếu chạy:

```bash
python test.py
```

thì:

```text
__main__
```

Nhưng nếu:

```python
import test
```

thì bên trong `test.py`:

```text
test
```

---

## Pattern phải thuộc

```python
if __name__ == "__main__":
    main()
```

Ý nghĩa:

> Chỉ chạy `main()` khi file được execute trực tiếp, không chạy khi module được import.

---

# 1.8 `__pycache__`

Python có thể tạo:

```text
__pycache__/
```

để lưu bytecode đã compiled.

Đừng nhầm:

```text
.py
```

với:

```text
.pyc
```

`.py` là source code.

`.pyc` là bytecode cache.

---

# 2. Exceptions

Syllabus yêu cầu `except`, nhiều `except`, tuple exception, hierarchy, `raise`, `assert`, `except E as e`, `args` và custom exceptions.

Đây là phần rất hay có câu hỏi logic.

---

# 2.1 Exception hierarchy

Ví dụ:

```text
BaseException
    └── Exception
          ├── ArithmeticError
          │     └── ZeroDivisionError
          ├── LookupError
          │     ├── IndexError
          │     └── KeyError
          └── TypeError
```

Điểm quan trọng:

> **Subclass exception phải được catch trước superclass.**

---

# 2.2 Edge case: thứ tự `except`

```python
try:
    x = 1 / 0
except Exception:
    print("A")
except ZeroDivisionError:
    print("B")
```

Output:

```text
A
```

Tại sao?

`ZeroDivisionError` là subclass của `Exception`.

`except Exception` đã bắt được exception rồi.

`except ZeroDivisionError` phía sau không bao giờ được dùng.

---

## Câu hỏi biến thể

```python
try:
    x = 1 / 0
except ZeroDivisionError:
    print("A")
except Exception:
    print("B")
```

Output:

```text
A
```

### Rule

```text
specific → general
```

không phải:

```text
general → specific
```

---

# 2.3 Multiple exceptions

```python
try:
    x = int("abc")
except (ValueError, TypeError):
    print("error")
```

Một `except` có thể bắt nhiều loại exception bằng tuple.

---

# 2.4 `except Exception as e`

```python
try:
    x = int("abc")
except ValueError as e:
    print(type(e))
    print(e)
```

`e` là **exception object**.

Không phải string.

---

# 2.5 `e.args`

```python
try:
    raise ValueError("wrong value")
except ValueError as e:
    print(e.args)
```

Output:

```text
('wrong value',)
```

`args` là tuple.

---

## Edge case nhiều arguments

```python
try:
    raise ValueError("A", "B", "C")
except ValueError as e:
    print(e.args)
```

Output:

```text
('A', 'B', 'C')
```

---

# 2.6 `raise` vs `raise e`

Đây là edge case khó hơn.

```python
try:
    raise ValueError("error")
except ValueError:
    raise
```

`raise` không có argument:

> re-raise exception hiện tại.

Trong:

```python
except ValueError as e:
    raise e
```

thì bạn explicit raise exception object `e`.

Trong các câu hỏi về traceback, sự khác biệt này có thể quan trọng.

---

# 2.7 `else` của `try`

```python
try:
    x = 10 / 2
except ZeroDivisionError:
    print("error")
else:
    print("success")
```

Output:

```text
success
```

`else` chạy khi **không có exception** trong `try`.

---

## Edge case

```python
try:
    x = 10 / 0
except ZeroDivisionError:
    print("error")
else:
    print("success")
```

Output:

```text
error
```

---

# 2.8 Exception trong `else`

```python
try:
    x = 10
except:
    print("A")
else:
    print(1 / 0)
```

Exception trong `else` **không được catch bởi các `except` của cùng `try`**.

Đây là bẫy logic.

---

# 2.9 `assert`

```python
x = 10

assert x > 5
```

Không có output.

Nếu:

```python
assert x < 5
```

thì:

```text
AssertionError
```

Có message:

```python
assert x < 5, "x is too large"
```

thì exception có message.

---

# 2.10 Custom exception

```python
class MyError(Exception):
    pass

raise MyError("Something went wrong")
```

Custom exception thường kế thừa từ `Exception`.

---

# 3. Strings

Syllabus bao gồm ASCII, Unicode, UTF-8, code points, escape sequences, indexing/slicing, immutability, comparison, `in`, `not in`, `ord`, `chr` và string methods.

---

# 3.1 String immutable

```python
s = "Python"

s[0] = "J"
```

Lỗi:

```text
TypeError
```

Không thể sửa trực tiếp character của string.

---

## Muốn thay đổi

```python
s = "Python"

s = "J" + s[1:]

print(s)
```

```text
Jython
```

Bạn tạo **string object mới**.

---

# 3.2 Negative indexing

```python
s = "Python"

print(s[-1])
print(s[-2])
```

Output:

```text
n
o
```

Mental model:

```text
 P  y  t  h  o  n
 0  1  2  3  4  5
-6 -5 -4 -3 -2 -1
```

---

# 3.3 Slice — endpoint không inclusive

```python
s = "Python"

print(s[1:4])
```

Output:

```text
yth
```

Index:

```text
1 → y
2 → t
3 → h
4 → stop
```

---

# 3.4 Slice với step âm

```python
s = "Python"

print(s[::-1])
```

Output:

```text
nohtyP
```

Đây là pattern cực kỳ đáng nhớ:

```python
[::-1]
```

→ reverse.

---

# 3.5 Empty slice

```python
s = "Python"

print(s[3:3])
```

Output:

```text
""
```

Không phải lỗi.

---

# 3.6 Slice vượt range

```python
s = "Python"

print(s[0:100])
```

Không lỗi.

Output:

```text
Python
```

Trong khi:

```python
print(s[100])
```

sẽ:

```text
IndexError
```

### Rule

```text
slice out of range → thường không lỗi
single index out of range → IndexError
```

---

# 3.7 `ord()` và `chr()`

```python
print(ord("A"))
```

→ `65`

```python
print(chr(65))
```

→ `"A"`

Chúng gần như là hai chiều ngược nhau:

```text
character → ord → code point
code point → chr → character
```

---

# 3.8 String comparison

```python
print("A" < "B")
```

→ `True`

Nhưng:

```python
print("a" < "B")
```

Không nên suy nghĩ theo alphabet tự nhiên.

Python so sánh theo Unicode code points.

Ví dụ:

```python
print(ord("A"))
print(ord("a"))
```

`a` có code point lớn hơn `A`.

---

# 3.9 String vs number

```python
print("10" == 10)
```

→

```text
False
```

Không tự động convert string `"10"` thành integer `10`.

---

# 3.10 `in`

```python
print("py" in "python")
```

→ `True`

Nhưng:

```python
print("Py" in "python")
```

→ `False`

String membership **case-sensitive**.

---

# 3.11 `.find()` vs `.index()`

```python
s = "banana"

print(s.find("na"))
```

→ `2`

Nếu không tìm thấy:

```python
s.find("xyz")
```

→

```text
-1
```

Trong khi:

```python
s.index("xyz")
```

→ `ValueError`

### Đây là bẫy cực phổ biến.

|Method|Không tìm thấy|
|---|---|
|`find()`|`-1`|
|`index()`|`ValueError`|

---

# 3.12 `.rfind()`

```python
s = "banana"

print(s.find("na"))
print(s.rfind("na"))
```

Có thể:

```text
2
4
```

`find()` → vị trí đầu tiên.

`rfind()` → vị trí cuối cùng.

---

# 3.13 `.split()`

```python
s = "a b c"

print(s.split())
```

→

```python
["a", "b", "c"]
```

---

## Edge case

```python
s = "a  b   c"

print(s.split())
```

Vẫn:

```python
["a", "b", "c"]
```

Khi không truyền separator, whitespace được xử lý đặc biệt.

---

## Nhưng:

```python
s = "a  b"

print(s.split(" "))
```

Kết quả khác:

```python
["a", "", "b"]
```

Vì lúc này bạn yêu cầu split chính xác theo ký tự `" "`.

---

# 3.14 `.join()` — cực dễ nhầm

```python
words = ["A", "B", "C"]

print("-".join(words))
```

→

```text
A-B-C
```

Không phải:

```text
-A-B-C-
```

Separator nằm **giữa** các elements.

---

## Edge case

```python
print("".join(["A", "B", "C"]))
```

→

```text
ABC
```

---

# 3.15 `sorted()` vs `.sort()`

```python
x = [3, 1, 2]

y = sorted(x)

print(x)
print(y)
```

→

```text
[3, 1, 2]
[1, 2, 3]
```

`sorted()` tạo list mới.

---

Trong khi:

```python
x = [3, 1, 2]

y = x.sort()

print(x)
print(y)
```

→

```text
[1, 2, 3]
None
```

### Cực kỳ quan trọng:

```python
list.sort()
```

**modify list tại chỗ và return `None`.**

---

# 4. OOP — phần quan trọng nhất

OOP chiếm **34% syllabus**, gồm class/object, instance/class variables, `__dict__`, private components, name mangling, methods, `self`, introspection, inheritance, `isinstance`, overriding, `is`, polymorphism, `__str__`, diamond inheritance và constructors.

---

# 4.1 Class variable vs instance variable

```python
class A:
    x = 10

    def __init__(self):
        self.y = 20
```

Ở đây:

```text
x → class variable
y → instance variable
```

---

# 4.2 Attribute lookup

```python
class A:
    x = 10

a = A()

print(a.x)
```

Python tìm `x` trên object/class hierarchy.

`a` không nhất thiết phải có:

```python
a.__dict__["x"]
```

vẫn có thể:

```python
a.x
```

vì `x` nằm trong class.

---

# 4.3 Edge case: instance override class variable

```python
class A:
    x = 10

a = A()

a.x = 20

print(a.x)
print(A.x)
```

Output:

```text
20
10
```

Tại sao?

Ban đầu:

```text
A.x = 10
```

Sau:

```python
a.x = 20
```

thì tạo:

```text
a.__dict__["x"] = 20
```

---

# 4.4 `__dict__`

```python
class A:
    x = 10

a = A()
a.y = 20

print(a.__dict__)
```

Có:

```python
{'y': 20}
```

Không nhất thiết có `x`, vì `x` thuộc class.

Trong khi:

```python
print(A.__dict__)
```

sẽ chứa class attributes.

---

# 4.5 Câu bẫy rất hay

```python
class A:
    x = 10

a = A()

print("x" in a.__dict__)
print("x" in A.__dict__)
```

Kết quả:

```text
False
True
```

---

# 4.6 Mutable class variable — cực kỳ quan trọng

```python
class A:
    data = []

a = A()
b = A()

a.data.append(1)

print(a.data)
print(b.data)
```

Output:

```text
[1]
[1]
```

Tại sao?

`data` là **class variable**, nên cả `a` và `b` đều lookup tới cùng list.

---

## Cách tạo riêng cho từng object

```python
class A:
    def __init__(self):
        self.data = []
```

Bây giờ:

```python
a = A()
b = A()

a.data.append(1)

print(a.data)
print(b.data)
```

→

```text
[1]
[]
```

### Đây là một trong những edge case OOP cần thuộc.

---

# 4.7 Private variable và name mangling

```python
class A:
    def __init__(self):
        self.__x = 10
```

Bạn không truy cập trực tiếp:

```python
a.__x
```

thông thường sẽ:

```text
AttributeError
```

Python biến tên thành dạng gần giống:

```python
_A__x
```

Đây gọi là **name mangling**.

---

# 4.8 Edge case name mangling

```python
class A:
    def __init__(self):
        self.__x = 10

a = A()

print(a._A__x)
```

Có thể truy cập bằng tên đã mangled.

Điều này cho thấy:

> `__x` không phải private theo nghĩa tuyệt đối của language-level access control.

---

# 4.9 `self`

```python
class A:
    def hello(self):
        print("hello")
```

Khi:

```python
a = A()
a.hello()
```

Python truyền object `a` vào `self`.

Conceptually:

```python
A.hello(a)
```

---

# 4.10 Edge case gọi method qua class

```python
class A:
    def hello(self):
        print(self)

a = A()

a.hello()
```

tương đương về mặt truyền argument với:

```python
A.hello(a)
```

Nhưng:

```python
A.hello()
```

thiếu `self`.

→ `TypeError`.

---

# 4.11 `hasattr()`

```python
class A:
    x = 10

a = A()

print(hasattr(a, "x"))
```

→ `True`

```python
print(hasattr(A, "x"))
```

→ `True`

Vì `x` là class attribute nhưng object vẫn có thể lookup được.

---

# 4.12 `__name__`, `__module__`, `__bases__`

```python
class B:
    pass

class A(B):
    pass
```

Có thể:

```python
print(A.__name__)
```

→

```text
A
```

```python
print(A.__bases__)
```

→ tuple chứa superclass trực tiếp.

---

# 4.13 `isinstance()` — phải cực kỳ chắc

```python
class A:
    pass

class B(A):
    pass

b = B()

print(isinstance(b, B))
print(isinstance(b, A))
```

Cả hai:

```text
True
True
```

Vì object `b` là instance của `B` và cũng là instance theo inheritance hierarchy của `A`.

---

# 4.14 `isinstance()` vs `type()`

```python
class A:
    pass

class B(A):
    pass

b = B()
```

```python
type(b) == B
```

→ `True`

Nhưng:

```python
type(b) == A
```

→ `False`

Trong khi:

```python
isinstance(b, A)
```

→ `True`

### Mental model

```text
type()
    ↓
exact type

isinstance()
    ↓
type + inheritance hierarchy
```

---

# 4.15 Multiple inheritance

```python
class A:
    def hello(self):
        print("A")

class B:
    def hello(self):
        print("B")

class C(A, B):
    pass

c = C()
c.hello()
```

Output:

```text
A
```

Vì Python tìm theo **MRO — Method Resolution Order**.

---

# 4.16 MRO

Có thể kiểm tra:

```python
print(C.__mro__)
```

Python sẽ tìm method theo thứ tự MRO.

Trong case đơn giản:

```text
C → A → B → object
```

---

# 4.17 Overriding

```python
class A:
    def hello(self):
        print("A")

class B(A):
    def hello(self):
        print("B")

b = B()
b.hello()
```

Output:

```text
B
```

`B.hello()` override `A.hello()`.

---

# 4.18 Polymorphism

```python
class Dog:
    def speak(self):
        print("woof")

class Cat:
    def speak(self):
        print("meow")

def make_sound(animal):
    animal.speak()
```

Có thể:

```python
make_sound(Dog())
make_sound(Cat())
```

Function không cần biết object cụ thể là class nào.

Nó chỉ cần object cung cấp method tương ứng.

---

# 4.19 `is` vs `==`

Đây là một trong những câu dễ sai nhất.

```python
a = [1, 2]
b = [1, 2]

print(a == b)
print(a is b)
```

Output:

```text
True
False
```

`==`:

> values/equality

`is`:

> identity — có phải cùng object không?

---

# 4.20 Edge case alias

```python
a = [1, 2]
b = a

print(a == b)
print(a is b)
```

→

```text
True
True
```

Vì:

```text
a ─┐
   ├──> same list object
b ─┘
```

---

# 4.21 Diamond inheritance

Ví dụ:

```python
class A:
    def hello(self):
        print("A")

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass
```

Cấu trúc:

```text
      A
     / \
    B   C
     \ /
      D
```

Python sử dụng MRO để quyết định method lookup.

Không nên đơn giản hóa thành:

> "Python chọn class gần nhất theo hình vẽ."

Phải xem **MRO**.

---

# 4.22 Constructor

```python
class A:
    def __init__(self):
        print("constructor")

a = A()
```

Khi object được tạo:

```python
A()
```

`__init__()` được gọi để initialize object.

---

## Edge case inheritance

```python
class A:
    def __init__(self):
        print("A")

class B(A):
    pass

b = B()
```

`B` không có `__init__`, nên inheritance cho phép sử dụng constructor từ `A`.

Output:

```text
A
```

---

# 4.23 Constructor overriding

```python
class A:
    def __init__(self):
        print("A")

class B(A):
    def __init__(self):
        print("B")

b = B()
```

Output:

```text
B
```

`A.__init__()` không tự động chạy.

Muốn gọi:

```python
class B(A):
    def __init__(self):
        super().__init__()
        print("B")
```

---

# 5. List Comprehension

Syllabus bao gồm `if` và nested comprehensions.

---

# 5.1 Basic

```python
x = [1, 2, 3, 4]

result = [n * 2 for n in x]
```

→

```text
[2, 4, 6, 8]
```

---

# 5.2 Condition

```python
result = [n for n in range(5) if n % 2 == 0]
```

→

```text
[0, 2, 4]
```

Pattern:

```python
[expression for item in iterable if condition]
```

---

# 5.3 Expression vs condition — dễ nhầm

```python
[n * 2 for n in range(5) if n % 2]
```

Điều kiện:

```python
n % 2
```

`0` → False.

`1` → True.

Do đó output:

```text
[2, 6]
```

Không phải `[0, 2, 4, 6, 8]`.

---

# 5.4 Nested comprehension

```python
result = [x + y for x in [1, 2] for y in [10, 20]]
```

Hãy đọc như nested loop:

```python
result = []

for x in [1, 2]:
    for y in [10, 20]:
        result.append(x + y)
```

Output:

```text
[11, 21, 12, 22]
```

### Thứ tự cực kỳ quan trọng

```text
x=1, y=10
x=1, y=20
x=2, y=10
x=2, y=20
```

---

# 5.5 Nested condition

```python
result = [
    x + y
    for x in [1, 2]
    for y in [10, 20]
    if x + y > 20
]
```

Chỉ giữ:

```text
21
22
```

---

# 6. Lambda

Syllabus yêu cầu lambda, function nhận lambda, `map()` và `filter()`.

---

# 6.1 Lambda cơ bản

```python
f = lambda x: x * 2

print(f(5))
```

→

```text
10
```

---

# 6.2 Lambda nhiều argument

```python
f = lambda x, y: x + y

print(f(2, 3))
```

→ `5`

---

# 6.3 Lambda không có return keyword

Sai:

```python
lambda x:
    return x * 2
```

Lambda chứa expression, không viết `return` như function thông thường.

---

# 6.4 `map()`

```python
x = [1, 2, 3]

result = map(lambda n: n * 2, x)

print(result)
```

Điểm quan trọng:

`map()` trả về **iterator**, không phải list trong Python 3.

Muốn thấy các phần tử:

```python
print(list(result))
```

→

```text
[2, 4, 6]
```

---

# 6.5 Iterator bị consume

```python
result = map(lambda x: x * 2, [1, 2, 3])

print(list(result))
print(list(result))
```

Output:

```text
[2, 4, 6]
[]
```

### Tại sao?

`map` là iterator.

Lần đầu:

```text
iterator → consumed
```

Lần thứ hai:

```text
nothing left
```

---

# 6.6 `filter()`

```python
x = [1, 2, 3, 4]

result = filter(lambda n: n % 2 == 0, x)

print(list(result))
```

→

```text
[2, 4]
```

`filter()` giữ những phần tử mà function trả về truthy.

---

# 6.7 `map()` vs `filter()`

```text
map:
input → transform → output

filter:
input → condition → keep/remove
```

Ví dụ:

```python
map(lambda x: x * 2, [1, 2, 3])
```

→

```text
[2, 4, 6]
```

Trong khi:

```python
filter(lambda x: x > 1, [1, 2, 3])
```

→

```text
[2, 3]
```

---

# 6.8 Edge case: truthy value trong filter

```python
result = filter(lambda x: x, [0, 1, "", "A", None])

print(list(result))
```

Kết quả:

```text
[1, "A"]
```

Vì `filter()` kiểm tra truthiness.

---

# 7. Closures — phần dễ bị bẫy

Syllabus yêu cầu hiểu meaning/rationale và defining/using closures.

---

# 7.1 Closure cơ bản

```python
def make_multiplier(x):

    def multiply(y):
        return x * y

    return multiply
```

Sau đó:

```python
multiply_5 = make_multiplier(5)

print(multiply_5(10))
```

→

```text
50
```

Inner function nhớ được `x = 5`.

---

# 7.2 Tại sao closure nhớ `x`?

Sau:

```python
multiply_5 = make_multiplier(5)
```

conceptually:

```text
multiply_5
   |
   +---- function multiply
             |
             +---- captured x = 5
```

Sau khi `make_multiplier()` kết thúc, `x` vẫn được closure giữ lại.

---

# 7.3 Closure với nhiều instances

```python
def make_multiplier(x):
    def multiply(y):
        return x * y
    return multiply

multiply_5 = make_multiplier(5)
multiply_10 = make_multiplier(10)

print(multiply_5(2))
print(multiply_10(2))
```

→

```text
10
20
```

Hai closure có state khác nhau.

---

# 7.4 `nonlocal`

```python
def counter():
    x = 0

    def increment():
        nonlocal x
        x += 1
        return x

    return increment
```

```python
c = counter()

print(c())
print(c())
print(c())
```

→

```text
1
2
3
```

Nếu không có:

```python
nonlocal x
```

thì:

```python
x += 1
```

được hiểu là assignment tới local variable của `increment()`.

---

# 7.5 Closure + loop — bẫy cực mạnh

```python
functions = []

for i in range(3):
    functions.append(lambda: i)

print([f() for f in functions])
```

Nhiều người đoán:

```text
[0, 1, 2]
```

Nhưng kết quả thường là:

```text
[2, 2, 2]
```

Tại sao?

Lambda giữ reference tới biến `i`, không capture snapshot value tại từng vòng.

Sau loop:

```text
i = 2
```

Ba lambda đều đọc `i` khi được gọi.

---

# 7.6 Cách capture value tại thời điểm tạo

```python
functions = []

for i in range(3):
    functions.append(lambda i=i: i)

print([f() for f in functions])
```

→

```text
[0, 1, 2]
```

`i=i` trong default argument tạo giá trị riêng cho từng function.

Đây là một edge case rất đáng luyện.

---

# 8. I/O

Syllabus bao gồm I/O modes, predefined streams, handles vs streams, text/binary modes, `open()`, `errno`, `close()`, `read()`, `write()`, `readline()`, `readlines()` và `bytearray`.

---

# 8.1 `read()`

```python
f = open("test.txt", "r")

data = f.read()
```

Đọc toàn bộ nội dung còn lại.

---

# 8.2 `readline()`

```python
line = f.readline()
```

Đọc một line.

Nếu file:

```text
ABC
DEF
GHI
```

thì:

```python
f.readline()
```

lần 1:

```text
ABC\n
```

lần 2:

```text
DEF\n
```

---

# 8.3 `readlines()`

```python
lines = f.readlines()
```

trả về list các lines.

Ví dụ:

```python
[
    "ABC\n",
    "DEF\n",
    "GHI"
]
```

---

# 8.4 Edge case: `read()` rồi `readline()`

Giả sử file:

```text
ABC
DEF
```

Code:

```python
f = open("test.txt")

print(f.read())
print(f.readline())
```

Sau `read()`:

> file pointer đã ở cuối file.

Do đó:

```python
readline()
```

trả:

```text
''
```

---

# 8.5 `seek()` mental model

Mặc dù trọng tâm syllabus là basic I/O, khi gặp câu đọc file hãy luôn nghĩ:

```text
file
 ↓
current position
```

Mỗi lần `read()`, `readline()`... đều có thể thay đổi position.

---

# 8.6 `write()` return value

```python
f.write("Hello")
```

thường trả về số characters đã ghi.

Ví dụ:

```python
n = f.write("Hello")

print(n)
```

→

```text
5
```

---

# 8.7 Text vs binary

Text mode:

```python
open("file.txt", "r")
```

Binary:

```python
open("file.bin", "rb")
```

Binary data thường làm việc với:

```python
bytes
bytearray
```

---

# 8.8 `bytearray`

```python
x = bytearray(b"ABC")

x[0] = 90

print(x)
```

`bytearray` mutable.

Khác với:

```python
bytes
```

là immutable.

---

# 9. Các “combined traps” rất giống kiểu câu thi

Đây là phần nên luyện kỹ nhất.

---

## Trap 1 — Class variable + mutable object

```python
class A:
    x = []

a = A()
b = A()

a.x.append(1)

print(b.x)
```

### Phân tích

`x` nằm trên class.

Cả `a` và `b` đều lookup cùng list.

Output:

```text
[1]
```

---

# Trap 2 — Instance attribute che class attribute

```python
class A:
    x = 10

a = A()

a.x = 20

print(a.x)
print(A.x)
```

Output:

```text
20
10
```

---

# Trap 3 — `is` vs `==`

```python
a = [1, 2]
b = [1, 2]

print(a == b)
print(a is b)
```

→

```text
True
False
```

---

# Trap 4 — Inheritance + `isinstance`

```python
class A:
    pass

class B(A):
    pass

x = B()

print(isinstance(x, A))
print(type(x) == A)
```

→

```text
True
False
```

---

# Trap 5 — Exception hierarchy

```python
try:
    1 / 0
except Exception:
    print("A")
except ZeroDivisionError:
    print("B")
```

→

```text
A
```

---

# Trap 6 — `find()` vs `index()`

```python
x = "hello"

print(x.find("z"))
```

→

```text
-1
```

Nhưng:

```python
print(x.index("z"))
```

→ `ValueError`.

---

# Trap 7 — `sort()` return value

```python
x = [3, 1, 2]

y = x.sort()

print(y)
print(x)
```

→

```text
None
[1, 2, 3]
```

---

# Trap 8 — `map()` iterator

```python
m = map(lambda x: x + 1, [1, 2, 3])

print(list(m))
print(list(m))
```

→

```text
[2, 3, 4]
[]
```

---

# Trap 9 — Closure late binding

```python
funcs = []

for i in range(3):
    funcs.append(lambda: i)

for f in funcs:
    print(f())
```

→

```text
2
2
2
```

---

# Trap 10 — Nested comprehension order

```python
x = [
    a + b
    for a in [1, 2]
    for b in [10, 20]
]

print(x)
```

→

```text
[11, 21, 12, 22]
```

Không phải:

```text
[11, 12, 21, 22]
```

---

# Trap 11 — `read()` consumes the stream

```python
f = open("data.txt")

a = f.read()
b = f.read()

print(b)
```

`b` thường là:

```text
''
```

vì lần đọc đầu đã đi đến EOF.

---

# Trap 12 — Constructor không tự động gọi superclass constructor

```python
class A:
    def __init__(self):
        print("A")

class B(A):
    def __init__(self):
        print("B")

B()
```

Output:

```text
B
```

Không có:

```text
A
```

Muốn gọi `A.__init__()` phải gọi explicit, thường qua:

```python
super().__init__()
```

---

# 10. Bộ câu hỏi tự kiểm tra

## Question 1

```python
class A:
    x = []

a = A()
b = A()

a.x += [1]

print(a.x)
print(b.x)
```

### Đáp án

```text
[1]
[1]
```

### Lý do

`x` là class variable và list mutable.

---

# Question 2

```python
class A:
    x = 10

a = A()

a.x += 5

print(a.x)
print(A.x)
```

### Đáp án

```text
15
10
```

### Logic

`a.x += 5` tương đương conceptually với việc tạo/gán instance attribute:

```python
a.x = a.x + 5
```

Sau đó `a` có `x` riêng.

---

# Question 3

```python
class A:
    pass

class B(A):
    pass

x = B()

print(type(x) == A)
print(isinstance(x, A))
```

### Đáp án

```text
False
True
```

---

# Question 4

```python
x = [1, 2, 3]

y = x

x = [4, 5]

print(y)
```

### Đáp án

```text
[1, 2, 3]
```

### Tại sao?

Ban đầu:

```text
x ─┐
   └──> [1, 2, 3]
y ─┘
```

Sau:

```python
x = [4, 5]
```

chỉ đổi reference của `x`.

`y` vẫn trỏ tới list cũ.

---

# Question 5

```python
x = [1, 2, 3]
y = x

x.append(4)

print(y)
```

### Đáp án

```text
[1, 2, 3, 4]
```

Khác hoàn toàn Question 4.

Ở đây:

```python
x.append(4)
```

modify object.

Không tạo reference mới cho `x`.

---

# Question 6

```python
def f(x=[]):
    x.append(1)
    return x

print(f())
print(f())
```

### Đáp án

```text
[1]
[1, 1]
```

### Tại sao?

Default argument `[]` được tạo **một lần khi function definition được thực thi**, không phải mỗi lần gọi function.

> Đây là một edge case Python rất đáng nhớ dù trọng tâm syllabus không liệt kê riêng default arguments.

---

# Question 7

```python
funcs = []

for i in range(3):
    funcs.append(lambda: i)

print(funcs[0]())
print(funcs[1]())
print(funcs[2]())
```

### Đáp án

```text
2
2
2
```

Closure/lambda lookup `i` khi function được gọi.

---

# Question 8

```python
funcs = []

for i in range(3):
    funcs.append(lambda i=i: i)

print([f() for f in funcs])
```

### Đáp án

```text
[0, 1, 2]
```

Default argument lưu value tương ứng tại thời điểm tạo lambda.

---

# Question 9

```python
try:
    print("A")
    1 / 0
    print("B")
except ZeroDivisionError:
    print("C")
else:
    print("D")

print("E")
```

### Đáp án

```text
A
C
E
```

`B` không chạy.

`else` không chạy vì có exception.

---

# Question 10

```python
x = "Python"

print(x[100:200])
```

### Đáp án

```text
""
```

Không `IndexError`.

Nhưng:

```python
print(x[100])
```

→ `IndexError`.

---

# 11. Những pattern nên học thuộc trước khi thi

## Pattern A — inheritance

```python
class B(A):
    pass
```

Nhớ:

```python
isinstance(B(), A) == True
```

nhưng:

```python
type(B()) == A
```

là `False`.

---

## Pattern B — identity

```python
a = [...]
b = [...]
```

Thông thường:

```python
a == b   # values
a is b   # identity
```

---

## Pattern C — mutable class attribute

```python
class A:
    x = []
```

→ tất cả instances có thể dùng chung object `x`.

---

## Pattern D — `sort`

```python
x.sort()
```

modify `x`.

Return:

```python
None
```

---

## Pattern E — `find`

```python
find → -1
index → ValueError
```

---

## Pattern F — `map/filter`

```python
map → transform
filter → select
```

Cả hai trong Python 3 trả iterator.

---

## Pattern G — closure

```python
lambda: i
```

trong loop thường gặp **late binding**.

```python
lambda i=i: i
```

→ capture value bằng default argument.

---

## Pattern H — exception

```text
specific exception
        ↓
general exception
```

Ví dụ:

```python
except ZeroDivisionError:
except Exception:
```

Không đảo ngược.

---

## Pattern I — `read()`

```python
f.read()
```

→ đọc từ current position đến EOF.

Sau đó đọc tiếp:

```python
f.read()
```

→ thường `""`.

---

# 12. Checklist cuối trước PCAP

## Modules

-  `import`
    
-  `from ... import`
    
-  `import ... as`
    
-  `dir()`
    
-  `sys.path`
    
-  `__name__`
    
-  `__pycache__`
    
-  `__init__.py`
    
-  `math.floor()`
    
-  `math.ceil()`
    
-  `math.trunc()`
    
-  `random.seed()`
    
-  `choice()`
    
-  `sample()`
    

Các mục này nằm trực tiếp trong Section 1 của syllabus.

---

## Exceptions

-  Exception hierarchy
    
-  thứ tự `except`
    
-  multiple exceptions
    
-  `except E as e`
    
-  `e.args`
    
-  `raise`
    
-  `raise e`
    
-  `assert`
    
-  `try/except/else`
    
-  custom exception
    

Đây là các nội dung được liệt kê trong Section 2.

---

## Strings

-  Unicode/code point
    
-  `ord()`
    
-  `chr()`
    
-  indexing
    
-  negative indexing
    
-  slicing
    
-  negative step
    
-  immutability
    
-  `in`
    
-  `not in`
    
-  `find()`
    
-  `rfind()`
    
-  `index()`
    
-  `split()`
    
-  `join()`
    
-  `sort()`
    
-  `sorted()`
    
-  string comparison
    

Các nội dung này thuộc Section 3.

---

## OOP — ưu tiên cao nhất

-  class vs object
    
-  class variable vs instance variable
    
-  mutable class variable
    
-  `__dict__`
    
-  private variable
    
-  name mangling
    
-  `self`
    
-  `hasattr()`
    
-  `__name__`
    
-  `__module__`
    
-  `__bases__`
    
-  inheritance
    
-  multiple inheritance
    
-  `isinstance()`
    
-  `type()`
    
-  `is`
    
-  `==`
    
-  overriding
    
-  polymorphism
    
-  `__str__`
    
-  MRO
    
-  diamond inheritance
    
-  constructor
    
-  superclass constructor
    

Đây là Section có trọng số **34%**, lớn nhất trong syllabus.

---

## Miscellaneous

-  list comprehension
    
-  nested comprehension
    
-  lambda
    
-  `map()`
    
-  `filter()`
    
-  iterator consumption
    
-  closure
    
-  `nonlocal`
    
-  closure + loop
    
-  I/O modes
    
-  text vs binary
    
-  `read()`
    
-  `readline()`
    
-  `readlines()`
    
-  `write()`
    
-  `bytearray`
    

Section 5 chiếm **22%** và bao phủ chính các nhóm trên.

---

# 13. 15 bẫy logic cần thuộc lòng

Nếu thời gian ôn rất ít, hãy chắc chắn bạn trả lời được 15 câu này mà không cần chạy Python:

|#|Bẫy|Kết luận|
|---|---|---|
|1|`is` vs `==`|identity vs equality|
|2|`type(x)` vs `isinstance(x, A)`|exact type vs inheritance|
|3|mutable class variable|instances có thể share cùng object|
|4|instance attribute|có thể shadow class attribute|
|5|`__dict__`|class/object có namespace khác nhau|
|6|`__x`|name mangling|
|7|`find()`|không thấy → `-1`|
|8|`index()`|không thấy → `ValueError`|
|9|`sort()`|modify in-place, return `None`|
|10|`map()`|iterator|
|11|`filter()`|iterator|
|12|closure trong loop|late binding|
|13|`except Exception` trước subclass|subclass bị bắt bởi general handler|
|14|`read()` hai lần|lần 2 thường EOF → `""`|
|15|nested comprehension|vòng `for` ngoài chạy trước|

---

# 14. Mental model quan trọng nhất

Khi gặp một câu PCAP dài, hãy vẽ 4 thứ trên giấy:

### 1. Object

```text
a ─────────> object #1
b ─────────> object #2
```

### 2. Class

```text
object
   ↓
class
   ↓
superclass
```

### 3. Scope

```text
local
 ↓
enclosing
 ↓
global
 ↓
built-in
```

### 4. Execution flow

```text
try
 ↓
exception?
 ├── yes → matching except
 └── no  → else
 ↓
next statement
```

Nếu câu có lambda/closure:

```text
function
   ↓
captured variable?
   ↓
value được lookup lúc nào?
```

Nếu câu có file:

```text
file
 ↓
current position
 ↓
read()
 ↓
new position
```

Đây là cách giảm đáng kể việc “đoán output”.

---

# 15. Một nguyên tắc cuối cùng cho PCAP

Đừng chỉ học:

```python
isinstance()
```

Hãy học theo **contrast pairs**:

```text
isinstance() ↔ type()
is ↔ ==
find() ↔ index()
sort() ↔ sorted()
readline() ↔ readlines()
map() ↔ filter()
class variable ↔ instance variable
class attribute ↔ instance attribute
raise ↔ assert
raise ↔ raise e
specific exception ↔ general exception
text mode ↔ binary mode
```

PCAP rất phù hợp với kiểu câu hỏi:

> “Hai đoạn code trông gần giống nhau — output/error khác nhau ở đâu?”

Nếu bạn nắm được các **cặp đối lập** này và đặc biệt là **OOP + exception + closure + iterator**, bạn sẽ xử lý được phần lớn các câu logic khó trong phạm vi syllabus PCAP-31-03.