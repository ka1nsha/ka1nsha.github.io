Title: Python'da alt çizgi(_)
Date: 2018-05-2 22:55
Tags: python alt çizgi,python alt cizgi nedir?, python altcizgi, python altçizgi, python underscore
Category: python
Slug: python-alt-cizgi
Authors: 0x656e

Selamlar, yazıya giriş yapmadan önce uyarayım bu yazı okuduğum bir makaleden anladıklarımı kapsamaktadır. Direkt olarak çeviri yapmadım kendi yorumlarımı katarak anladığımı aktarmaya çalıştım. Teşekkürler, iyi okumalar!



Python kodlarının çoğunda alt çizgiyi görebilirsiniz. Peki ya hiç anlamını araştırdınız mı? Malesef ben de araştırmamıştım. Aslında Python'da alt çizginin çok özel bir yeri varmış. 



Peki bu alt çizgi Python'da hangi amaçlar için kullanılıyormuş?



* Yorumlayıcı ekranında bir değeri olan son değişkeni tanımlamak için kullanılıyor.

* Fonksiyon veya fonksiyonların değişkenlerine özel işlevler veriyor.

* Yerelleştirme fonksiyonlarında kullanılıyor.

* Sayı değerlerinin rakamlarını ayrıştırmak için kullanılıyor.

* Bir değeri/değişkeni umursamamak için kullanılıyor.

  ### Kullanım Örnekleri

  1. 
  ```python
5
5
     >>>_
     5
     >>>15+35
     50
     >>>_
     50
 ### Eğer aynı şeyi bpython3 gibi bir interpreterde denerseniz aynı sonucu alamayabilirsiniz.
     ```

  2. ```python
     for _ in range(10): ### Burada i yerine _ yazdık ve dedik ki bu range ile atanan değer umurumuzda değil.
         fonksiyon()
     ```

  3. Bir modülü yıldız ile importladığınızda yazdığınız fonksiyonun import olmamasını yani private bir fonksiyon olmasını isterseniz sınıfınızı/fonksiyonunuzu bu şekilde yazabilirsiniz. Referans: 

     [Python Classes]: https://docs.python.org/3/tutorial/classes.html#private-variables-and-class-local-references	"Python Classes"

  4. Bir uygulamada kullanıcının dilini önceden program üzerinde belirtiyorsanız. Kullanıcıya döndüreceğiniz mesajlarda localization/internationalization dosyanızda ki bir texti aşağıda ki şekilde yazmanız yeterlidir.

     ```python
     print(_('Bu metin Türkçe dil dosyasından alınmıştır.')
     ```

  5. Bu kısımda örnek zaten yeterince açıklayıcı olduğu için direkt olarak aynı örneği alıyorum.

     ```python
     dec_base = 1_000_000
     bin_base = 0b_1111_0000
     hex_base = 0x_1234_abcd

     print(dec_base) # 1000000
     print(bin_base) # 240
     print(hex_base) # 305441741
     ```

     ​

Referans ve Orjinal Metin: 

[Buradan!](https://hackernoon.com/understanding-the-underscore-of-python-309d1a029edc)



Eğer yanlış veya bildirmek istediğiniz bir şey var ise bildirmekten çekinmeyiniz. 

