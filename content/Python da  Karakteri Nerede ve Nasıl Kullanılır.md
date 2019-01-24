Title: Python da "*" Karakteri Nerede ve Nasıl Kullanılır
Date: 2019-01-24 18:50
Tags: python3, python3 yıldız, python3 yıldız işareti, python3 asterisk, python3 args ve kwargs, python args, python kwargs
Category: python
Slug: python-asterisk-nerede-ve-nasil
Authors: 0x656e




Merhabalar,

Vardiyalı çalıştığımdan dolayı bu ay nasıl olduysa 5 gün ard arda tatil iznim olmuş. Bu tatili çok verimli geçirmek istediğimden dolayı çalışacağım konulara çalışmaya, yazacağım kodları yazmaya, bloguma özen vermeye çalıştım. Tabi burada oyun oynamaktan da vazgeçmedim :)



İşte bu sebeple bu isteklerimin 3.cüsü olan bloguma özen vermeye çalışmanın bir sonucu olarak bu yazıyı okuyucularıma veya araştırmacı arkadaşlara sunuyorum. Eksik gördüğünüz bir kısım veya burası yanlış dediğiniz bir kısım var ise twitter üzerinden veya mail üzerinden belirtmekten çekinmeyin lütfen.

[Mail](mailto:info@enesergun.net)

[Twitter](twitter.com/0x656e)

Bu yazıyı okumadan önce eğer Python hakkında bir fikre sahip değilseniz, henüz dün okumuş olduğum ve çok beğendiğim Fatih ERİKLİ'nin yazısını sizlere önereyim.



[Yılan Hikayesi İlk Bölüm](https://medium.com/@fthrkl/y%C4%B1lan-hikayesi-i%CC%87lk-b%C3%B6l%C3%BCm-869f212bb1a2)





## Nedir Bu "*"  Karakteri

Yıldız işareti ingilizce de asterisk olarak geçmektedir. Eğer kodlarınızı yazarken "*" işareti ile ilgili bir problem yaşarsanız asterisk diye aratarak, diğer arama sonuçlarından daha hızlı bir arama sonucuna ulaşabilirsiniz.

**Yıldız kelimesi İngilizce de star olarak, yıldız işareti kelimesi ise asterisk olarak geçer. **



## İlk Yıldız İşaretimizi Ne Zaman Gördük

Python programlama dilinde yıldız işareti ilk olarak karşımıza **Matematiksel Operatorler** konusunda çıkmaktadır.

Bu işaret ile vermiş olduğumuz değişkenleri çarpabilir veya bu işareti iki kere kullanarak vermiş olduğumuz integer değerlerinin kuvvetini,üssünü(Power) alabiliriz.

Örnekle açıklamak gerekirse:

```python
# Çarpma
a = [5,4]
b = a*2 # A değişkenine tanımlanmış olan liste veri tipini 2 ile çarpıyoruz.
> [5,4,5,4]
# Kuvvet Alma
c = a**2 # Eğer bu şekilde yaparsak listenin kuvvetini alamayacağından dolayı bizlere zaten hata verecektir.
c = [i**4 for i in a] # A değişkenini for döngüsüne sokarak tüm sonuçları c değişkenine atadım.
> [625, 256]
```

Yukarıdaki örnekte  farketmiş olacağınız üzere "çarpma" örneğininde bize içinde ki karakterleri değil değişkene tanımlamış olduğumuz değeri 2 ile çarpacaktır. 

```python
a = "enes"
print(a*2)
> enesenes
a = 3
print(a*2)
>6
```

Yine yukarıdaki örneklere ait benzer bir işlem yaptık fakat burada liste değil string veri tipinde bir değer tanımladık. İlk çarpma işlemimizde gördüğünüz gibi stringi iki kere çarparak yan yana yazdı. İkinci işlemimizde ise direkt olarak integer değer verdiğimizden dolayı matematiksel bir işleme sokup bize çıktısını üretti.



## Gelelim Yıldız İşaretinin Gelişmiş Kullanımlarına

Asterisk yani yıldız işaretini bir liste veya sözlük veri tiplerini açarken(unpacking) kullanabiliriz. Burada sözlük ve liste olarak bahsettim fakat iterable olan tüm veri tiplerinde de bu işareti kullanabiliriz. Iterable'ın türkçesi olarak direkt bir çeviri yok bildiğim kadarıyla ama bu konuda en güzel açıklamayı ekşisözlükte "aaron" kullanıcısı entry olarak girmiş. Direkt olarak yazılan entry'i aşağıda belirtiyorum.

"bir döngü vasıtası ile üzerinde dönülebilen elemanların oluşturduğu bir nesnedir."

**R.I.P Aaron Swartz**

[İterable](https://eksisozluk.com/iterable--5154245)



**Örnek 1 **

```python
isimler = ['Enes','Yasin','Emir','Basri','Mustafa']
# Burada isimleri yazdırabilmek için string'e çevirip yazdırabiliriz pek tabii fakat konumuz "*" ve bu yolun pekte efektif olduğu söylenemez.
print(*isimler) #Unpacking 
print(' '.join(isimler)) # List to str
```



Yukarıdaki örnekte eğer bir listeyi yazdıracaksak bize cidden büyük bir kolaylık sağlıyor. Şimdi diğer örneklerle ve açıklamalarıyla birlikte devam edelim.

**Örnek 2**

```python
def yazdir(*args,**kwargs):
    print(args)
    print(kwargs)
ogrenci  = {'İsim':'Enes', 'Soyisim':'Ergün', 'Okul No': '1234'}
yazdir(a="Enes",b="0x656e",c=ogrenci)
> {'a': 'Enes', 'b': '0x656e', 'c': {'İsim': 'Enes', 'Soyisim': 'Ergün', 'Okul No': '1234'}}
```

**Örnek 2.1**

```python
def yazdir(*utanırım,**ben):
    print(utanırım)
    print(ben)
ogrenci  = {'İsim':'Enes', 'Soyisim':'Ergün', 'Okul No': '1234'}
yazdir(a="Enes",b="0x656e",c=ogrenci)
```



Burada ki kullanımda bir fonksiyonu çağırırken alabileceği tüm argümanları yakalamak için yıldız karakterini kullanıyoruz ama örnekte 2 farklı kullanım görmekteyiz. Bunları açıklamak istersek eğer:

1. Args değerinde kullandığımız tek yıldız argüman olarak vereceğimiz tüm değerleri yakalayacaktır. Burada *args kullanımı zorunlu değildir. İsterseniz ` *selamnaber`  bile kullanabilirsiniz. 
2. Kwargs değerinde kullandığımız 2 yıldız ise burada ki unpacking işleminin keyworded arguments ile olacağını belirtiyor. Bu ne demek? Fonksiyona göndermiş olduğumuz parametrelerin anahtar kelimelere sahip parametreler olacağını söylüyor.



**Örnek 3**

```python
ogrenci  = {'İsim':'Enes', 'Soyisim':'Ergün', 'Okul No': '1234'}
ogrenci_karnenotu = "Okulumuz öğrencilerinden {Okul No} okul numarasına sahip {İsim} {Soyisim} adlı öğrenci mezun olmaya hak kazanmıştır.".format(**ogrenci)
print(ogrenci_karnenotu)
> Okulumuz öğrencilerinden 1234 okul numarasına sahip Enes Ergünadlı öğrenci mezun olmaya hak kazanmıştır.
```

Buradaki kullanımda yine bir unpacking ile karşı karşıyayız. Bu örnekte Sözlük veri tipindeki bir değişkeni string formatting işlemi sırasında açıyoruz. Burada tek tek `ogrenci['İsim'] ` yazmaktansa bu şekilde bir kullanım bize büyük kolaylıklar sağlayabilir.



## Kapanış

Sanırım diğer yazılara görece daha kısa bir yazı oldu ama blogun temasını değiştirmek için bir yazı yazma fikrine ihtiyacım vardı. Bu arada yeni tema nasıl? Temayı MinimalXY ile Onur'un Medius temasını birleştirerek yaptım.

Ayrıca yine bir klasiğim olan yazı sonu şarkısı paylaşmadan edemeyeceğim. Bu sefer 2 adet şarkı paylaşıyorum.

[![Kings of Leon - Sex on Fire](https://i.ytimg.com/vi/RF0HhrwIwp0/hqdefault.jpg)](https://www.youtube.com/watch?v=RF0HhrwIwp0)

[![Frazey Ford - One More Cup Of Coffee](https://i.ytimg.com/vi/3oMb06O2wXo/hqdefault.jpg)](https://i.ytimg.com/vi/3oMb06O2wXo/hqdefault.jpg)