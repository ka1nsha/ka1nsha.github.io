Title: String.Format() Kullanırken Dikkatli Olun
Date: 2018-06-10 02:41
Tags: Python string formatting, python format, python string injection, python injection, python input verification
Category: python
Slug: python-format-kullanirken-dikkatli-olun
Authors: 0x656e





Bildiğiniz üzere uygulamalar da kullanıcı girdisi çok önemlidir. Bu girdilerin serialize edilmesi ve güvenli hale getirilmesi gerekmektedir. Güvenlik bilinci olmayan bir yazılımcı ise bu girdilerde kullanıcıya güvenerek hiç bir önlem almaz ise ne olur? Tabi ki hacklenir. Bu girdilerin güvenli hale getirilmesi için dile özgü bir çok yöntem vardır. Bu yöntem metadolojilerinden (metadoloji miydi bilemedim.) white list kullanılması da oldukça önemlidir. Ama bazen öyle şeyler vardır ki direkt olarak Yazılımın Core'unda çıkmaktadır ve burada olay artık yazılımcıdan çıkmaktadır. Örnek vermek gerekirse tam olarak fonksiyonu hatırlamıyorum fakat PHP'de kötü karakterlerden kaçmak için escape fonksiyonu bulunuyordu ve bu fonksiyon bypasslanabiliyordu. Artık deprecated olduğundan dolayı kullanılmıyor bildiğim kadarıyla.



Çok fazla uzattım sanırım uzatmadan mevzuya geçeceğim. 



### Python'da Güvenli Girdi Almak



Python'da girdi almak için input fonksiyonu kullanılmaktadır. Yanlış hatırlamıyorsam Python2'de ki input fonksiyonu da yukarıda bahsettiğim gibi güvenli hale getirilmediğinden dolayı sistem üzerinde kod çalıştırılabiliyordu. Tıpkı eval fonksiyonu gibi. Python3 de ise herhangi bir sorun yok gözüküyor. Peki kullanıcı girdisini yaptı buraya kadar her şey güvenli. Peki ya sonra?



Örnek üzerinden gitmek gerekirse login formu üzerinde kullanıcı adı aldığımızı düşünelim. Buraya yazılan kullanıcı adı için aşağıda ki yöntem uygulanırsa sisteminizde açık oluşacaktır.



```python
cursor.execute('SELECT password FROM users WHERE username=%s',%(username,))
```

Burada username kısmına yazılacak herhangi bir tırnak hacker'ın database üzerinde hatta daha ileri aşamalarda sistem üzerinde kod çalıştırabileceği anlamına gelmektedir.



Peki güvenlisi?

O da şöyle:

```python
query = "SELECT password FROM users WHERE username='{}'".format(username)
cursor.execute(query)
```

Not: Ben bu şekilde güvenli olduğunu düşünüyorum ama hatam olabilir. Eğer bir hata varsa okuyucuları bilgilendirmek adına hiç çekinmeden yazabilirsiniz. Yanlış göstermek istemem.



Evet yukarıda ki örneğimiz daha güvenli(?!)



### Aslında Güvenli Değilmiş



Evet format güvenli diye biliyorduk ama okuduğum makaleye göre güvenli değilmiş. Bunun sebebi ise format değeri ile birlikte kod üzerinde ki başka özellikleri çağırıp ekrana yazdırabilirmişiz.



Hemen örnek ile göstereyim:

```python
string = "Selamlar {0} {0.__contains__}".format('Enes')
```

Bunu yazdığımızda çıktısı aşağıda ki gibi olacaktır:



```python
"Selamlar Enes <method-wrapper '__contains__' of str object at 0x7f4f4a9f5c70>"
```



### Neden Böyle Oluyor?



Aslında bu bir bug değil feature. Şaka değil gerçekten. Python3 ile birlikte format ile değerlere ve öğelere ulaşabilir duruma gelmekteyiz. Fakat burada öğelere ve bu öğelerin değerlerine erişmek işte karşımıza bu sorunu çıkartmaktadır.



Peki bunda ne var diyebilirsiniz. Bir hacker eğer kullanıcı girdinize bu şekilde injection yapabiliyorsa kod bloğunuz içerisinde ki örnek vermek gerekirse `db_password` gibi değerlere ulaşabilecektir.



### Nasıl Engelleriz



Engellemek amacıyla bu yazıyı referans aldığım adreste aşağıda ki şekilde bir fonksiyon ve sınıf verilmiştir. 



```python
from string import Formatter
from collections import Mapping

class MagicFormatMapping(Mapping):
    """This class implements a dummy wrapper to fix a bug in the Python
    standard library for string formatting.

    See http://bugs.python.org/issue13598 for information about why
    this is necessary.
    """

    def __init__(self, args, kwargs):
        self._args = args
        self._kwargs = kwargs
        self._last_index = 0

    def __getitem__(self, key):
        if key == '':
            idx = self._last_index
            self._last_index += 1
            try:
                return self._args[idx]
            except LookupError:
                pass
            key = str(idx)
        return self._kwargs[key]

    def __iter__(self):
        return iter(self._kwargs)

    def __len__(self):
        return len(self._kwargs)

# This is a necessary API but it's undocumented and moved around
# between Python releases
try:
    from _string import formatter_field_name_split
except ImportError:
    formatter_field_name_split = lambda \
        x: x._formatter_field_name_split()

class SafeFormatter(Formatter):

    def get_field(self, field_name, args, kwargs):
        first, rest = formatter_field_name_split(field_name)
        obj = self.get_value(first, args, kwargs)
        for is_attr, i in rest:
            if is_attr:
                obj = safe_getattr(obj, i)
            else:
                obj = obj[i]
        return obj, first

def safe_getattr(obj, attr):
    # Expand the logic here.  For instance on 2.x you will also need
    # to disallow func_globals, on 3.x you will also need to hide
    # things like cr_frame and others.  So ideally have a list of
    # objects that are entirely unsafe to access.
    if attr[:1] == '_':
        raise AttributeError(attr)
    return getattr(obj, attr)

def safe_format(_string, *args, **kwargs):
    formatter = SafeFormatter()
    kwargs = MagicFormatMapping(args, kwargs)
    return formatter.vformat(_string, args, kwargs)

Now you can use the safe_format method as a replacement for str.format:

>>> '{0.__class__}'.format(42)
"<type 'int'>"
>>> safe_format('{0.__class__}', 42)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: __class__

```



Yazımızın da sonuna geldik. Bu yazıyı okuduğum bir makale üzerinden aldım. Alıntı diyebiliriz isterseniz çalıntıda diyebilirsiniz fakat en azından bildirmeyi görevim bildiğimden dolayı bu yazıyı okumaktasınız. 



Yazının orjinali: [Careful with STR Format](http://lucumr.pocoo.org/2016/12/29/careful-with-str-format/)



Evet bu yazıyı da bitirdiğimize göre geleneğim haline getirmeye çalıştığım yazı sonu şarkısını aşağıda paylaşıyorum.



[![Rosey - Love](https://img.youtube.com/vi/AlwQZAtlTFU/0.jpg)](https://youtu.be/AlwQZAtlTFU)



