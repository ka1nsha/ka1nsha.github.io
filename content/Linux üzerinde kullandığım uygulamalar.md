Title: Linux Üzerinde Kullandığım ve Tavsiye Ettiğim Uygulamalar
Date: 2019-05-03 20:00
Tags: linux kurulum sonrası, linux tavsiye uygulamalar, yazılımcılar için linux, en güzel linux uygualamaları
Category: linux
Slug: linux-uzerinde-kullandigim-uygulamalar
Authors: 0x656e



Selamlar, 



Uzun süredir kendimi oyunlara verdiğimden dolayı kendimi geliştirmek adına bir şey yapmadığımı farkettim, belki de daha önce farkettim ama ihtiyacım vardı bilemiyorum. Bu sebeple 3 gün önce radikal bir karar alarak Windows sistemimi geri gelmeyecek şekilde (diskimi 0 ile dolduracak şekilde) sildim. Hoş SSD için böyle bir data destruction'a gerek var mı bilmiyorum fakat yaptım. Hatta öyle bir radikal karar ki şuan kullandığım sisteme Steam'e dair herhangi bir şey kurmadım.



Velhasılkelam. Sistem olarak herkes tarafından linç yediğim bir dağıtım kurdum(Kali). Tabi gerekli ayarlamaları yaparak. Neden kali kurdum sorusuna gelirsek:



* Hackthebox ile uğraşmak istiyorum.
* Sanalda bir sistem kullanmaktan nefret ediyorum.
* İhtiyacım olabilecek her şeyin elimin altında olmasını istiyorum. (Toollar)
* Uygulamaları tek tek kurmak istemiyorum (GOTO [2] veya direkt 1 den başlıyorsanız GOTO[3])



Girizgahı geçelim. Bu yazıyı neden yazdım? Hem kendi işlerim için kullandığım (Pentest harici onlar başka bir yazı konusu) hemde yeni görüp beğendiğim yazılımları paylaşmak istedim.

## Yeni Neler Buldum

### Flog

Kendisi GOLang ile yazılmış bir araç olmak ile birlikte bir çok standart formatta sahte log üretebiliyor. Bu sahte loglar geliştirdiğimiz uygulamalar için yararlı olabiliyor veya ihtiyacımız olduğunda bu şekilde log üretebiliyor olmamız mükemmel bir şey. Eğer Log'lar üzerinde bir iş veya proje yapıyorsanız kesinlikle kullanmalısınız.

[Flog Github Linki](https://github.com/mingrammer/flog)

### Glances

Kendisi htop gibi bir monitoring aracı fakat biraz daha gelişmiş ve işlevsel hali. Aklınıza gelebilecek temel sistemleri izliyor. Bunlar Disk I/O, Network, Processler, Memory durumu, Swap durumu, System load durumu gibi şeyler.

[Glances Official Sitesi](https://nicolargo.github.io/glances/)

### Flameshot

Kendisi benim bundan sonra vazgeçilmezim olacak bir screenshooter yazılımı. Bundan önce XFCE üzerinde kendi screenshooter'ı olan xfce4-screenshooter'ı kullanmakla birlikte onun yetersiz geldiği yerlerde Shutter kullanıyordum fakat Shutter'dan nedense nefret ediyordum. İşte şuan imdadıma `Flameshot` yetişti.

Kendisi Windows üzerinde kullandığım `Greenshot` uygulamasının bir çok özelliğine sahip üstelik bunu SS aldığınız yerde yapıyorsunuz, başka herhangi bir pencere ile uğraşmıyorsunuz.

**Bu arada xfce4-screenshooter'ın Telegram'a resim gönderirken donma sorununun allah belasını versin.**

[FlameShot Github Linki](https://github.com/lupoDharkael/flameshot)

### Kupfer

Kendisi bir uygulama başlatıcı. XFCE4 sistemlerde ben genellikle start menüyü kullanmayı sevmiyordum. Mouse'u oraya götür uygulamayı bul tıkla bana zor geliyordu bu sebeple `xfce4-appfinder`  uygulamasını kullanıyordum. Öyle muhabbet ortasında konuşurken `1v3m` adlı arkadaşa `erfur` `kupfer` diye bir uygulama önermiş. Sağolsun `1v3m` de bana önerdi. (Amma çok mention oldu.) Kendisini severek kullanmaktayız efendim. Tavsiye ederiz.

[Kupfer Github Linki](https://kupferlauncher.github.io/)

### Cheat

Kendisi, terminal üzerinde kendi cheatsheetlerimizi hazırlamaya yarayan bir araç. Tabi kendi içerisinde de bir sürü cheatsheet default olarak bulunuyor. Bunları home klasörünüz altında `cheat` klasörüne atarsanız terminalden `cheat bash` yazdığınızda size vermiş olduğunuz argümana göre cheatsheet gösteriyor. Gayet güzel bir uygulama

[Cheat Github Linki](https://github.com/cheat/cheat)

### Add-Gitignore

Kendisi seçtiğimiz argümanlara göre bir `.gitignore` dosyasını bulunduğunuz dizine bırakıveriyor. Argüman olarak vermeyip uygulama içerisinden seçmeniz gerekiyor bunu belirtmeme gerek yok umarım. Birden fazla argüman alabiliyor.

Örnek:

![add-gitignore demo](https://raw.githubusercontent.com/TejasQ/add-gitignore/master/demo.gif)


[Add-Gitignore Github Linki](https://github.com/TejasQ/add-gitignore)

### Joplin

Kendisi bir not alma uygulaması ve Dropbox üzerinde çalışıyor bu sayede tüm cihazlarınızda senkronize bir şekilde note alabiliyorsunuz. Benzer ama daha basit ve web üzerinden çalışan bir uygulama için `hackmd` 'ye  bakabilirsiniz.

[Joplin Official Site](https://joplinapp.org/)

### Translate-Shell

Terminal üzerinden Google Translate kullanmanıza yarayan basit ama etkili bir araç. Çok fazla bir açıklama girme gereği duymuyorum.

[Translate-Shell Github Linki](https://github.com/soimort/translate-shell)

### Qucs-s

Kendisi elektronik devre simulasyon uygulaması. Henüz kullanma fırsatım olmadı ama umarım olacaktır. 

[Qucs-s Official Site](https://ra3xdh.github.io/)

### fsearch

Kendisi sistem üzerinde hızlıca dosya arayıp bulmamıza olanak sağlayan bir çok özelliği(Örn:Regex) olan bir arama aracı.

[fsearch Github Linki](https://github.com/cboxdoerfer/fsearch)

## Daha önce kullandığım ve yüklediğim uygulamalar/araçlar

### XMind

Kendisi beyin haritalama uygulaması, ben proje geliştirirken bu tür uygulamalar kullanıyorum.

[X-Mind Official Site](https://www.xmind.net/zen/)

### Fish Shell

Önceden ne kadar zsh kullansamda artık Fish-shell kullanıyorum. Kendisinin otomatik tamamlama vs gibi özellikleri muazzam.

[Fish-Shell Official Site](https://fishshell.com/)

### Fisher

Fish-shell için bir paket yöneticisi.

[Fisher Github Linki](https://github.com/jorgebucaran/fisher)

### HTTPie

Kendisi CLI üzerinden HTTP Client görevini sağlıyor. Tıpkı cURL gibi ama daha insancılı. Gayet başarılı bir uygulama. API'lara vs istek atarken sıkça kullanabilirsiniz. 


![httpie demo](https://raw.githubusercontent.com/jakubroztocil/httpie/master/httpie.gif)


[HTTPie Github Linki](https://github.com/jakubroztocil/httpie)

### QuiteRSS

Kendisi bir RSS Feeder. Sevgili `Emir`'in tavsiyesi üzerine kullanmaya başladım.

[QuiteRSS Official Site](https://quiterss.org/)

### tldr

Kendisini yukarıda bahsetmiş olduğum `cheat` aracı ile `man` komutunun ortaya karışımı gibi düşünebilirsiniz. Herhangi bir komut hakkında size bilgi ve örnekler gösteriyor. Tl-dr'ı başka nasıl açıklayabilirim bilmiyorum.

Örnek bir ekran görüntüsü:

![tldr](https://raw.githubusercontent.com/tldr-pages/tldr/master/screenshot.png)

[TL-DR Github Linki](https://github.com/tldr-pages/tldr)

### fx

Kendisi bir JSON aracı. Terminal üzerinde Pipe ile verdiğiniz json çıktısı üzerinde gezmenize olanak sağlıyor. Sürekli API, JSON çıktıları ile uğraşıyorsanız işinize yarayacak bir araç olacaktır. Biliyorum bir çok alternatifi var ama ben bunu kullanıyorum. :)

[FX Github Linki](https://github.com/antonmedv/fx)

### Typora

Geldik bu yazıyı yazdığım editöre. Kendisi bir markdown editor. Yazdığınız anda bulunduğunuz sayfada Markdown'ı render ediyor ve o göz karmaşasından kurtuluyorsunuz. Kendisini severek kullanıyoruz efendim. Basit ve güzel bir arayüz kullanma nedenlerim arasında tabi ki.

[Typora Official Site](https://typora.io/)

### DBeaver

Kullanmayan kaldı mı ya bunu? Kendisi bir çok DBMS'e bağlantı kurmanıza olanak sağlayan bir Database yöneticisi. Java ile yazılmış. Sanırım tek sevmediğim tarafı bu. 

[DBeaver Official Site](https://dbeaver.io/)

### Ascicinema

Kendisini uzun zamandır biliyordum fakat script veya projelerimde hiç kullanmamıştım. Kullanmak nasip oldu. Terminal üzerinde kayıt almanıza ve bu kayıdı paylaşmanıza olanak sağlayan mükemmel bir uygulama. Linkini aşağıda paylaşıyor olacağım. Kullanmak için kayıt olmanız gerekmekte. Kayıt olduktan sonra bir link ile siz olduğunuzu doğruluyorsunuz ve record edip direkt olarak upload edebiliyorsunuz. Kullanımı çok rahat ve pratik. Örnek bir kullanımımı aşağıda görebilirsiniz.


[![Örnek kullanım](https://asciinema.org/a/oRY2H6RUf87aCN2xpNngFQ0iX.svg)](https://asciinema.org/a/oRY2H6RUf87aCN2xpNngFQ0iX)


[Asciicinema](https://asciinema.org/)

**Aslında kurmuş, bulmuş olduğum transfer.sh adlı bir uygulama daha mevcut fakat sanırım sistemlerde bir problem var ve çalışmıyor. İlgili tool terminal üzerinden dosya paylaşmanıza olanak sağlayan bir uygulama. **



Geldik yazının sonuna. Bundan sonraki yazım muhtelemelen güvenlik araçları ile ilgili olacaktır.

Benim için bir gelenek olan yazı sonu şarkımı aşağıya iliştiriyorum. 

Oldukça sert ve protest olarak nitelendirdiğim bu şarkıyı umarım keyifle dinlersiniz :)


[![Saian K"st Uçurum Çiçeği](http://img.youtube.com/vi/J-KUtPPlUqs/0.jpg)](https://www.youtube.com/watch?v=J-KUtPPlUqs "saian <3")
