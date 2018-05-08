Title: Python İstisnalar ve İstisna Yönetimi
Date: 2018-05-08 23:12
Tags: Python exceptions, python istisna, python istisna yönetimi, python hata yönetimi, python exceptions managing
Category: python
Slug: python-hata-yonetimi
Authors: 0x656e

Bildiğiniz gibi yazdığınız program/uygulama bazı yazım yanlışları veya veri girişi kısımlarında gerekli kontroller ve yönetimler yapılmamışsa  programınız/uygulamanız bir hata FIRLATARAK sonlanacaktır. Üstelik bu konu zararlı kişilerce kullanılarak son kullanıcıyı mağdur etmeye kadar gidebiliyor. Konu bu haliyle zaten oldukça önemli, bu kısımda yazılımcıya oldukça fazla yük düşmekte. Nedir bunlar?



1. Yazdığı kodların genel istisna durumlarını yönetmelidir.
2. Kullanıcı girişlerini kontrol etmelidir. ( Her konuda edilmeli )
3. Zararsız kullanıcının yerine zararlı bir kişinin bu girdi kısımlarına neler girebileceğini tahmin edebilmedir.

Şu anlık aklıma gelen bu kadar ama eminim fazlası da vardır. Bu konu hakkında beni yeşillendirebilirsiniz. Evet istisna yönetimi bu kadar önemliyken ben de bu konu hakkında yazmak istedim. Peki Python'da istisnalar nedir? Nasıl yönetilir? Hadi başlayalım.

## Python'da istisnalar

Python'da istisnalar Exception ile yönetilir. Python üstünde Built-in olarak gelen bir sürü istisna yöntemi ve yönetimi vardır. Bunların listesine [Built-in Exceptions](https://docs.python.org/3/library/exceptions.html) linkine tıklayarak ulaşabilirsiniz. Kod olaraksa en basit şekilde aşağıda ki gibi bir kullanımı vardır.


```
try: # Çalışacak kodunuz.
	print(0/0)
except:
	print("Hata var")
```

veya aşağıda ki gibi bir kullanım daha uygundur. Çünkü yukarıda ki kod bloğunda ne hata verirse versin hata var yazacaktır.

```
try:
	print(0/0)
except ZeroDivisionError:
	print("Sıfırı sıfıra bölüyon")
```
Yukarıda ki kod bloğunda kullandığımız ZeroDivisionError farkettiğiniz üzere bir built-in bir istisnadır.

Peki karşımıza gelecek bu istisnaları nasıl yöneteceğiz?

Örnek bir kod bloğunu aşağıda görebilirsiniz.

```
liste = [i for i in range(0,10)]
try:
	for i in liste:
		print(int(i)/0)
except ZeroDivisionError as hata:
	print(hata)
```

Burada hatayı gördük ve bununla ilgili ekrana bastırdık. Peki bu kadarla mı sınırlıyız? Tabi ki de hayır. Bu kısımda karşımıza 3 deyim daha çıkıyor.

Bu deyimler: 
1. Raise
2. Assert
3. Else
4. Finally


Peki bunlar ne işe yarar? Kısaca açıklayacak olursam:

**Raise**
Raise bize istisna çıktılarını tanımlamamızı sağlar. Nasıl yani derseniz şu şekilde. Bir yazılımın sadece stringler üzerinde işlem yaptığını düşünün buraya integer bir değer girdiğimizde bize TypeError verecektir. Fakat burada Error çıktısı son kullanıcı için anlamsız olabilir veya bunu değiştirmek isteyebilirsiniz. Base bir exception üzerinden Raise ile bunu yapabilirsiniz. Aslında raise bize istediğimiz zaman bir istisna fırlatmamıza olanak sağlar. Örnek:

```
i = 5
if type(i) is int:
	raise TypeError("Integer lan bu")
```

**Assert**
Bir modül yazdınız mesela bu modül sadece Linux'da çalışsın. Bunun kontrolünü assert ile kontrol ederek gerekli bir istisnayı sağlayabilirsiniz. Yazacağınız 1 satırlık assert ile bu kontrolü sağlayabilirsiniz. Örnek kod:

```
def meminfo():
	assert ('linux' in sys.platform)
	ac = open("/proc/meminfo")
meminfo()
```

Şimdi yukarıda ki kod da eğer sisteminiz Linuxsa bu kodu çalıştıracaktır. Fakat sisteminiz linux değilse sizlere istisna olarak AssertionError dönecektir. Peki bu durumda biz ne yapacağız?
```
try:
	meminfo()
except AssertionError:
	print("Windows haram")
```

Gördüğünüz gibi işletim sistemi kontrolünü sağlamış olduk.

**Else**

Else ise muazzam bir özelliğe sahiptir. Nedir bu ? Bir üst örnekte yapmış olduğumuz kodu hatırlayın. Eğer Linux sisteminde çalıştırıyorsak bize hata vermeyecekti. Peki hata vermedi o zaman? Finally kullanabiliriz evet haklısınız fakat farklı bir istisna yönetimi de koymak istiyorum. Mesela hata vermedi ve ben bu dosyayı okudum ama daha sonra parse etmek istiyorum? İşte burada else koşulunun içerisine yazdığımız kod ile bunu kontrol edebiliyoruz. 

```
try:
	meminfo()
except AssertionError:
	print("Windows haram")
else:
	try:
		dosya = open("memoryokuyucu.txt","a")
		for i in meminfo():
			i =i.replace("kb","kilobayt")
			dosya.write(i)
	except FileNotFoundError:
		print("Memory okuyucu diye bir dosya yok")
```

Örnek sanırım yeterince açıklayıcı olmuştur.

** Finally **

İşte geldik en güzel terime Finally. Finally şu işe yaramaktadır. İstisna yönetimlerinden sonra kodumuza ne yapacağımızı söyler. Yani her istisnayı geçti bu kod artık ne yapalım demektir? Burada hiç bir hata almadım veya sürekli çalışsın dediğiniz kodlarınız durabilir.



Finally konusunda örnek yazmadım zaten yeterince açık olduğu için.


Yazımı okuduğunuz için teşekkür ederim. Bir hatam veya yanlışım olmuş ise yeşillendirirseniz sevinirim.
**Unutmadan** bu haftanın şarkısını aşağıda paylaşıyorum.

[![Skunk Anansie - Weak](https://img.youtube.com/vi/nPglNjxVHiM/0.jpg)](https://www.youtube.com/watch?v=nPglNjxVHiM)