Title: Python Hafıza Yönetimi ve Garbage Collection Hakkında
Date: 2019-06-03 13:30
Tags: python memory management, python hafıza yönetim, python yavaş, python çöp toplayıcı, garbage collection types,
Category: python
Slug: python-garbage-collection
Authors: 0x656e

# Python Garbage Collector

## Garbage Collector Neymiş?

Garbage collector Türkçe'ye çevrildiğinde çöp toplayıcı anlamına gelmektedir. Aslında yazılım dillerindeki temel mantığıda aynıdır. Nedir bu olay derseniz de basit anlamda kodunuz üzerinde kullandığınız her nesne/obje memory'de bir alan kaplar. Bu alan verinizin boyutuna göredir. Örnek vermek gerekirse C'de 32bit bir integer değişkeni tanımlamışsanız bu değişken için memory üzerinde 31 bitlik bir alan açılır ve bu alan içerisinde siz değerlerinizi tutabilirsiniz. Geri kalan bir 1 bit ise işaret biti olarak kullanılır.

Buraya kadar her şey tamam. Peki o zaman şöyle yapalım biz programın açılışında bir değişken tanımladık ve bunu 1 kere kullandık ve yazdığımız dil otomatik hafıza yönetimi olmayan bir dil(Örn: C) ne olacak peki? Bu ayırdığımız alan program sonlanana kadar hafızada gereksiz yer kaplayacak.

İşte bu sebepten dolayı günümüzde kullanılan çoğu scripting dili ile birlikte Go, Java, C# otomatik hafıza yönetimine sahiptir. Bununla birlikte isterseniz C ve C++'a da [Boehm-Demers-Weiser](https://github.com/ivmai/bdwgc) ile ekleyebilirsiniz.

Peki bu işlem nasıl yapılıyor? Burada 2 farklı yöntem karşımıza çıkıyor. 
1. Reference Counting
2. Tracing

Bu kısımları kısaca bahsedip geçeceğim. 

### Reference Counting Nedir?
Bu metotda bizim kodumuzu yazarken hafızada kullanacağımız tüm nesne/objelerin reference tablosu tutuluyor. Basit anlamda kafanızda canlanması için örnek veriyorum `A` şeklinde bir değişkenimiz var ve biz bunu `toplama(A)` fonksiyonunda kullanıyoruz. Burada toplama fonksiyonunda A'yı referans aldığımızdan dolayı bu tabloda A'nın reference count'u `1` olacaktır. Tamam şimdi fonksiyondan çıktık artık A'nın bir işlevi kalmadı ve toplama fonksiyonunu bir yere atamadık. Bu sebeple tabloda değişkenimizin reference count'ı `0` oldu ve artık hafızadan kapladığı alan boşaltıldı. Python dilinde de Reference Counting ve Döngü tespiti kullanılır.

Reference counting'in bazı dezavantajları var:
1. Thread-Safe bir yapıda değil. Eğer multithread yapıda bir uygulama yazmışsanız bu sorunlara yol açıyor. Basit anlamda yine örneklendirmeye gideceğim. 1 thread'iniz bir refcount'u artırırken bir thread'iniz bu refcount'u 1 azaltabilir.
2. Her obje için bir referans count değeri oluşturuyor. Bu da memoryde fazladan alan demek.
3. Cyclical Reference'ları tanımlayamıyor. 
Örnek:

```Python
import sys
print(sys.getrefcount(5))
a = 5
b = a
print(sys.getrefcount(5))
del a
print(sys.getrefcount(5))
Output:
69
71
70
```
### Tracing Garbage Collector
En fazla kullanılan yöntemdir.
Bu Garbage collectorümüz ise biraz karışık. Yine de elimden geldiğince basit bir şekilde anlatmaya çalışacağım. Yazılımımız çalıştığında Memory de Root Set'imiz oluşturuyor bu bizim Memoryde ki en üst alanımız bundan sonraki tüm obje ve nesneler child olarak memory içerisinde yer ediniyor. Tracing kısmı işte burada devreye giriyor. 2 fazlı bir çalışması bulunuyor.
1. Root Set'imizin erişebildiği tüm objeler/nesneler kontrol ediliyor ve root setimizden bu objelere/nesnelere erişiliyorsa bu obje/nesne Alive olarak işaretleniyor.(Mark bit)
2. Bu faz ise Sweep olarak geçmekte. Bu kısımda algoritmamız yine tüm memory'i geziyor eğer Alive işaretlenmiş bir memory alanı varsa bu alan üzerinde Mark biti gelecekte ki Garbage Collection döngüsü için kaldırıyor ve sonraki memory adresine geçiyor. Eğer bu adres daha önce ziyaret edilmemiş yani Mark bit verilmemişse bunu Free Memory kısmına ekliyor.

Tabi bu kadarla kalmıyor işin ilerleyen kısımlarında Mark-Compact gibi aşamaları da mevcut ama basit anlamda bu şekilde.

Wiki üzerinden Tracing'i anlatan görsel:
![Tracing Çöp Toplayıcı](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Animation_of_tri-color_garbage_collection.gif/330px-Animation_of_tri-color_garbage_collection.gif)


## Python'da İşler Nasıl Gidiyor?
**Not:** Python'dan kasıt CPython'dır.
Yukarıdaki başlıklarda genel olarak Garbage Collection'ın ne olduğundan vs bahsettik sıra Python'a gelince burada işler biraz karışıyor.

Bu kısımda karşımıza generational garbage collection, gil gibi kavramlar karşımıza çıkıyor. Sırası ile gidelim.

Python'da iki tür garbage collection kullanılıyor bunlardan 1 tanesi yukarıda da bahsedilen Reference Counting, diğeri ise bir Tracing tipi olan Generational Garbage Collection'dır.

### Generational Garbage Collection Nedir?

Bu garbage collection tipinin mottosu "young objects are much more likely to die than old objects" yani kısaca genç olan erken ölür. 

Bu GC tipinde objeler jenerasyonlarına ayrılıyor, 3 adet grup bulunur.
1. Generation 0 - Short live
2. Generation 1 - Medium live
3. Generation 2 - Long live


Bir obje GC sonrası yaşamına devam ediyorsa bir sonraki jenerasyona eklenir. Eğer yeni bir obje tanımlanmışsa bu obje `Gen 0` da başlayacaktır. 
Yine gerçek hayattan bir örneklendirme yapayım.
Yeni birisiyle tanıştınız. Beyninizde bu tanıştığınız kişi `Gen0` grubuna `Ahmet1` olarak yerleştirildi ve aynı anda 5 Ahmet ile tanıştınız. Sonra  Kadıköy'de bir kafede biranızı yudumlarken `Ahmet1` ile karşılaştınız ve oturup karşılıklı sohbet ettiniz. `Ahmet1` artık `Gen1` grubuna girdi ve `Gen0` grubunda ki tüm Ahmetler hafızanızdan silindi. Eh `Ahmet1` ile daha sonraları bir sürü badire atlattınız(Bir sürü GC evresinden tertemiz çıktı) ve hayatınızda vazgeçilmez oldu.(Runtime'da ihtiyaç duyulan bir obje?!). Artık `Ahmet1` `Gen2` grubunda oldu.

Sanırım en kısa bu şekilde anlatabilirim :D 

### GIL (Global Interpreter Lock)

Bu arkadaşımız Python kodumuzun sadece tek bir thread tarafından çalıştırılmasını sağlıyor. Her kod yalnızca 1 thread üstünde çalışıyor. Yani arkaplanda çalışan her interpreter processde o process'e ait bir de GIL bulunuyor. O Process'e ait işlemleri başka bir thread çalıştıramıyor. Bunun sebebi ise yine üst kısımlarda bahsetmiş olduğumuz Reference Counting. Eş zamanlı olarak Reference Counting'in önüne geçebilmek için böyle bir yola gidilmiş.

GIL'in bu özelliği sebebiyle GC süreçleri hızlanıyor fakat Python kodumuzun sadece tek bir Thread'de çalışması gerekiyor. 

**Dipnot:** GIL bir ara kaldırılmak istenmiş hatta Patch'de çıkmış fakat şöyle bir sorun ortaya çıkmış. Yazdığımız kodlar multithread bir yapıdaysa işlemler hızlanmış fakat eğer single thread bir uygulama yazmışsanız performans kaybı **%50** gibi bir sayıya ulaşmış.


### Python'da Objeler

Pythonda bir değişken atadığınızda ne oluyor biliyor musunuz? Bu atadığınız değişken memoryde hali hazırda yaratılmış bir Objeye refererans vererek kullanılıyor. 

Örnek vermek gerekirse siz `a` ve `b` adında iki farklı değişken tanımladınız bu değişkenlerin değeri de `500` diyelim. İşte bu değişkenler aslında Memory üzerinde hali hazırda obje olarak bulunan `500` objesini işaret ediyor. 

Pythonda objelerin memory üzerinde tutulması ise şu şekilde oluyor.
||PyObject|
| -| -|
|type|integer|
|refcount|2|
|value|500|

Kod olarak açıklarsak eğer:
```python
a = 500
b = 500
print(id(500))
print(id(a),id(a)) 
output:
49670448
49670448 49670448
```

Gördüğünüz gibi iki farklı değişkenim, hatta bir integer'ım var ve aslında hepsi temelde memorydeki 500 değerini barındıran PyObject'e referans veriyor. Bir de aşağıdaki koda bakalım.

```python
import sys
print(sys.getrefcount(500))
a = 500
b = 500
print(sys.getrefcount(500))
print(id(500))
print(id(a),id(a))

print(sys.getrefcount(500))

```
Çıktısı aşağıdaki gibi olacaktır.
```python
2
4
49671840
49671840 49671840
4
```

ID'lerini bir kenara bırakırsak başlangıçta 500 değerini tutan Objemizin `count'u` 2 olarak gözükmekte biz bu değeri `a` ve `b` değişkenlerine verdiğimizde `refcount` 4 oluyor fakat `print` ile yazdırdığımız 500 değeri `refcountu` etkilemiyor. Bunun nedeni herhangi bir referans vermeden direkt yazdırmamızdan dolayıdır. 


Aslında yazıyı biraz daha uzatıp `__slots__`dan ve Python üzerindeki veri tipleri ve bu veri tiplerinin kapladıkları alan gibi konulardan bahsetmek istiyordum fakat bir baktım ki zaten sevgili `Mazlum Ağar` bu konudan bahsetmiş. İlgili yazının linkini hemen aşağıya iliştiriyorum.

[Python Tricks __Slots__](https://medium.com/@mazlumagar/python-tricks-1-slots-e0c9b04f4c5a)


Konu biraz dağınık olmuş olabilir bu sebeple kusura bakmayınız. Yazı tamamen benim de bilmediğim konu üzerine yaptığım araştırmalar neticesinde çıkmıştır. Eğer bir yanlışımı görürseniz kesinlikle ve kesinlikle beni uyarabilirsiniz. 

Geleneksel hale getirdiğim yazı sonu şarkısını aşağıya ekliyorum, bilimle kalın.

[![Gökşin Derin- Depresyon](https://img.youtube.com/vi/OYHsJ_h-noc/0.jpg)](https://www.youtube.com/watch?v=OYHsJ_h-noc)
