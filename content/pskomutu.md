Title: PS Komutunun Alabildiği Argümanlar
Date: 2018-02-10 22:19
Tags: ps cheatsheet, process monitoring on linux, ps aux
Category: linux
Slug: ps-command-arguments
Authors: 0x656e


**PS** komutu linux üzerinde processleri ( çalışan işlemleri ) monitoring edebileceğimiz bir komuttur. Pek tabi ki bir çok argüman almaktadır. Şimdi bu argümanların en çok kullanılanlarına aşağıda bahsedeceğiz. PS komutu çıktıları bir çok formatta olabiliyor. İyi okumalar.



### Let's go ###

**NOT**: Önce komutu gösterip daha sonra komutu açıklayacağım bilginize.


```bash
ps -A
```

* Bu komut varsayılan olarak **Linux formatında** çalışan processleri bizlere döndürür. Bu processlerde bizlere PID, hangi TTY'de çalıştığını, zamanını  ve hangi processin çalıştığını bizlere gösterir. Mesela benim ekran görüntümde tty7'de Xorg çalışıyor.

![](/images/psa1.png)


```bash
ps au
ps axu
```



* Yukarıda ki komutun çıktıları **BSD**  formatında olur. Bu formatta Kullanıcı, PID numarası, kullandığı işlemci yüzdesi, kullandığı ram yüzdesi, VSZ değeri, RSS değeri, TTY değeri, İşlemin durumu, zamanını ve komutunun çıktısını verir.

**VSZ** : Bir işlemin kullanacağı, kullanabileceği sanal bellek miktarıdır.

**RSS** : Bu işleme tahsis edilen fiziksel bellek miktarıdır.


![](/images/psaux1.png)

```bash
ps -eF
```

* Yukarıda ki komut full çıktı modudur. Bu çıktıda sizlere UID, PID, PPID, C, SZ, RSS, PSR, STIME, TTY, TIME, CMD değerleri döner.


```bash
ps -fU ka1
```

* Bu komut ile adını verdiğiniz kullanıcıya ait processleri görebilirsiniz.

![](/images/psfu1.png)


```bash
ps -U root -u root
```

* Bu komut ile root kullanıcı tarafından çalıştırılan tüm processleri görebilirsiniz.


```bash
ps -fG postgres
```

* Bu komut ile bir gruba ait tüm çalışan processleri görebilirsiniz. Bu ne demektir? Mesela web diye bir kullanıcı grubunuz var ve bunun altında nginx/gunicorn/celery bulunuyor. Siz direkt olarak bu şekilde çalışan processleri görebilirsiniz.

![](/images/psfg1.png)


```bash
ps -fp PID
```

* Bu komut ile PID değerini verdiğiniz process veya processleri görebilirsiniz. Burada tekli veya çoklu seçim yapabilirsiniz.


```bash
ps -ft tty1
```

* Bu komut ile o TTY'de çalıştırılan komutları görebilirsiniz.


```bash
ps -aux --forest
```

* Bu komut ile yukarıda bahsetmiş olduğumuz **BSD** tarzında bir çıktı alırsınız fakat burada ki tek fark processlerin parent-child ( aslında forest/treeview )  ilişkileri bu çıktı içerisinde gösterilir.

![](/images/psforest1.png)

```bash
ps -eo user,%cpu
```

* Bu komut ile PS çıktısını kendinize göre özelleştirebilirsiniz. Ben yukarıda ki komutta processin hangi kullanıcı tarafından çalıştırıldığını ve yüzde kaç CPU kullandığını görmek istedim.


![](/images/pschangeoutput1.png)


```bash
ps -eo user,%cpu,command,%mem --sort=-%mem |  head
```

* Bu komut ile ps komutu çıktısını sıralayabilirsiniz. Burada -%mem en fazla RAM Kullanan processleri ekrana yazdıracaktır. En az kullananları isterseniz %mem yazabilirsiniz.


![](/images/pssort1.png)