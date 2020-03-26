Title: Linux Kütüphaneler ve Tipleri, LD_PRELOAD Değişkeni, Strace ve Ltrace. 
Date: 2020-03-26 10:22
Tags: LD_PRELOAD Türkçe, LD_PRELOAD, Strace kullanımı, ltrace kullanımı, linux dinamik kütüphaneler, ldd türkçe, objdump, objdump türkçe, linux kütüphaneler, linux sistem çağrıları, nm komutu, ldd komutu, strace komutu, ltrace komutu, ptrace komutu
Category: linux
Authors: 0x656e



Selamlar, 

Aslında bu yazıda ana konu olarak strace ve ltrace komutlarını kısa olarak açıklayıp örnek çıktılarını koyup anlatmayı düşünüyordum fakat bu komutlar hakkında okuduğum yazılarda bir çok farklı kavram(benim bilmediğim/bildiğim) geçiyordu ki bu konulardan bahsetmezsem yazı eksik kalır diye düşündüm. Bu sebeple bu konular hakkında da bilgi vereyim derken strace ve ltrace yazının yan konusu olup çıktı. Zaten altı üstü bir komut diye düşünülebilir fakat arkaplanda dönen olaylar daha ilgi çekici. Bu sebeple konuya nasıl başlayabileceğimi bulamadım ve aşağıdaki gibi başladım. Direkt olarak konuya dalmış gibi oldu bu sebeple okuyucalardan şimdiden özür dilerim.



Strace ve Ltrace'in çalışma mantığı, nasıl çalıştığını daha iyi anlayabilmek adına aşağıdaki konular hakkında da bilgi sahibi olmalıyız. (Derinlemesine değil, eğer derinlemesine gireceksek hem ben bilmiyorum hem de bu konu hakkında kitap yazılır.)



1. Linux Kütüphaneleri
2. LDD, NM Komutları
3. LD_PRELOAD Değişkeni

## Kütüphaneler ve Linux Kütüphane Tipleri

**Öncelikle yazının devamında kütüphaneler kelimesini değil orjinali olan library kelimesini kullanacağım. **

### Libraryler neden kullanılır ve nedir?

Bir script yazdığımızı düşünelim; bu script bir websitesine giderek site üzerinde link verilmiş olan tüm PDF dosyalarını indirmeye yarayan bir script olsun. Bu script içerisinde bir çok fonksiyon yazmalıyız. Basitçe Websitesine bağlantı kurmalı, websitesini tarayarak pdf linklerini bulmalı ve son olarak bu bulduğu dosyaları indirmeli değil mi? Evet. Scriptimizi yazdık ve çalışıyor. Devam.

2 ay sonra bize bir istek geldi. Bir websitesine bağlanarak burada bulunan JPG dosyalarını indirmemiz isteniyor. Tüm kodu tekrardan mı yazacağız? Hayır.

İşte library kavramı tam burada karşımıza çıkıyor. Şimdi 2.proje için 1.projede bulunan işimize yarayacak fonksiyonları alarak sadece farklı 1 adet fonksiyon yazarak(hatta 1.scriptteki fonksiyonu değiştirerek) bu scripti çok hızlı bir şekilde yapabiliriz. 

Library kavramı da  böyle bir şey aslında.(Umarım kafanızda canlanmıştır. Çünkü benim canlandı.)

Ee tam olarak böyle bir şey de değil aslında. Şimdi tekrar düşünelim.

1 ve 2. projelerimiz cepte ve bunları yazalı 3 yıl olmuş. Biz bu süre zarfında 300(!) adet proje çıkartmış ve bu projelerin 150 adetinde bu kod parçacıklarını kullandığımızı düşünelim. Gel zaman git zaman bizim 1. projede bir güvenlik açığı çıktığını duyuyoruz. Ne yapmalıyız? Şimdi bütün bu projelerdeki kodları tek tek değiştirmekle kim uğraşır? Kimse. Çünkü biz library olarak kullanıyoruz zaten. Tek bir dosyayı 150 projede kullandık. O zaman tek bir dosyayı değiştirerek ilgili projelerde ki tüm güvenlik açıklarını kapatabiliriz. Böyle de bir güzelliği var. Tabi bir de her projede ayrı ayrı aynı kodları yazmadığımız için bolca da disk üzerinde yer kazanmış olduk (Patron alkışlar).

(Terimsel anlam vs.den çok kafamızda canlanması adına bu şekilde yazdım. Hata ettiysem affola.)

Sanırım artık library meselesi kafamızda oturmuştur.

## Linux Kütüphane Tipleri

Yukarıda basit (tamam hadi zor olsun) projelerde yazdığımız kütüphaneleri kullandık. Peki ya bunu işletim sistemi seviyesinde yapacak olsaydık? Bu kısımda bildiğim kadarıyla! mantık olarak aynı işleyişe sahip.

Konumuz olan linux sistemler üzerinde 2 farklı tipte library tipi bulunuyor. Bunlar:

* Statik Libraryler

* Dinamik Libraryler

#### Statik Libraryler(.a)

Derleme esnasında linklenen bu libraryler artık kodumuzun bir parçası olmaktadırlar. Örnek olarak: Yazdığımız scriptin sadece 1 çalıştırılabilir dosya olduğunu düşünün(ELF, PE). Yazılımı çalıştırmak için gereksinim kurmamıza gerek yok. Tek tıkla çalıştır.

Aşağıda dinamik libraryleri kullanan herhangi bir çalıştırılabilir dosyaya ait bilgileri gösteren `ldd` ve `objdump` komutundan bahsettim fakat bu komutlar sadece shared olanları gösteriyor. Eğer statik librarylere ait bilgi görmek istiyorsak bazı sıkıntılarımız var demektir. Çünkü kodlarımız içerisinde kullandığımız librarylerin isimleri derleme esnasında göz ardı edilir. Bu sebeple eğer görmek istiyorsak derleme esnasında `-g` parametresini kullanmalı veya kodumuzun bir map dosyasını çıkartmalıyız. Görebilmek adına kullanacağımız komut `nm` komutudur. Detaylı bilgi için manpages veya [TutorialsPoint](https://www.tutorialspoint.com/unix_commands/nm.htm)



Örn kullanım:

```bash
nm python
nm: python: no symbols
```



#### Dinamik Libraryler(.so)

Bu kısımda ise libraryler derlenme esnasında kod içerisinde linklenerek sistem üzerinde ki konumlarından runtime esnasında çağırılarak/yüklenerek kullanılmaktadır. 

Bir örnek ile bakalım. Tüm linux dağıtımları içerisinde Python diline ait interpreter(yorumlayıcı) yüklü olarak gelmektedir ve hali hazırda bir çok shared kütüphane kullanmaktadır. Şimdi bunlara bakalım.

Bunun için ilk örnekte ldd komutunu kullanacağım.

Python3.7'a ait shared olarak kullanılan libraryler:

```bash
ldd python3.7
        linux-vdso.so.1 (0x00007fff5814e000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fcaef7ec000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007fcaef7cb000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007fcaef7c6000)
        libutil.so.1 => /lib/x86_64-linux-gnu/libutil.so.1 (0x00007fcaef7c1000)
        libexpat.so.1 => /lib/x86_64-linux-gnu/libexpat.so.1 (0x00007fcaef794000)
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007fcaef777000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007fcaef630000)
        /lib64/ld-linux-x86-64.so.2 (0x00007fcaef9dc000)

```

Python'a ait shared olarak kullanılan libraryler:

```bash
ldd python
        linux-vdso.so.1 (0x00007ffdb49b3000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f4e56dbe000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f4e56d9d000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f4e56d98000)
        libutil.so.1 => /lib/x86_64-linux-gnu/libutil.so.1 (0x00007f4e56d93000)
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f4e56d76000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f4e56c31000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f4e57358000)

```

LDD komutu linux sistemler üzerinde çalıştırılabilir scriptinize ait shared object(.so?) bağımlılıklarını gösteren bir komuttur.



Birde objdump ile bakalım. Bu arada objdump komutu ise obje dosyalarına ait bilgileri gösteren bir komuttur.

Çıktı olarak uzun bir çıktı verecektir. Bu sebeple küçük ve sadece python3.7'ye ait kısmını koyuyorum.

Python3.7'a ait çıktı:

```bash
Dynamic Section:
  NEEDED               libc.so.6
  NEEDED               libpthread.so.0
  NEEDED               libdl.so.2
  NEEDED               libutil.so.1
  NEEDED               libexpat.so.1
  NEEDED               libz.so.1
  NEEDED               libm.so.6
  INIT                 0x0000000000421000
  FINI                 0x0000000000679794
  INIT_ARRAY           0x0000000000838db0
  INIT_ARRAYSZ         0x0000000000000008
  FINI_ARRAY           0x0000000000838db8
  FINI_ARRAYSZ         0x0000000000000008
  GNU_HASH             0x0000000000400308
  STRTAB               0x0000000000411d28
  SYMTAB               0x00000000004039e8
  STRSZ                0x000000000000aae8
  SYMENT               0x0000000000000018
  DEBUG                0x0000000000000000
  PLTGOT               0x0000000000839000
  PLTRELSZ             0x0000000000002bc8
  PLTREL               0x0000000000000007
  JMPREL               0x000000000041df08
  RELA                 0x000000000041dcb0
  RELASZ               0x0000000000000258
  RELAENT              0x0000000000000018
  VERNEED              0x000000000041db00
  VERNEEDNUM           0x0000000000000006
  VERSYM               0x000000000041c810

Version References:
  required from libz.so.1:
    0x0827e5c0 0x00 21 ZLIB_1.2.0
  required from libdl.so.2:
    0x09691a75 0x00 15 GLIBC_2.2.5
  required from libutil.so.1:
    0x09691a75 0x00 12 GLIBC_2.2.5
  required from libpthread.so.0:
    0x09691a75 0x00 05 GLIBC_2.2.5
  required from libm.so.6:
    0x06969189 0x00 07 GLIBC_2.29
    0x09691a75 0x00 03 GLIBC_2.2.5
  required from libc.so.6:
    0x06969195 0x00 22 GLIBC_2.15
    0x06969194 0x00 20 GLIBC_2.14
    0x06969190 0x00 19 GLIBC_2.10
    0x0d696916 0x00 18 GLIBC_2.6
    0x06969188 0x00 17 GLIBC_2.28
    0x06969185 0x00 16 GLIBC_2.25
    0x06969186 0x00 14 GLIBC_2.26
    0x0d696914 0x00 13 GLIBC_2.4
    0x0d696913 0x00 11 GLIBC_2.3
    0x0d696917 0x00 10 GLIBC_2.7
    0x09691974 0x00 09 GLIBC_2.3.4
    0x06969197 0x00 08 GLIBC_2.17
    0x09691972 0x00 06 GLIBC_2.3.2
    0x0d696919 0x00 04 GLIBC_2.9
    0x09691a75 0x00 02 GLIBC_2.2.5
```

Daha şimdiden konunun çok fazla dışına çıktık.

Daha detaylı bilgiler için: [Paylaşımlı Kütüphaneler](https://demirten.gitbooks.io/linux-sistem-programlama/content/shared-libraries/)

#### Siber Güvenlik Açısından Dinamik Libraryler

 Linux üzerinde dinamik olarak libraryleri linkleyen veya yükleyen bir library(?) bulunmaktadır. Bunun adı da `ld.so` dur. Bu library içerisinde bizi ilgilendiren(şuanlık) bir fonksiyon bulunmaktadır. Bu fonksiyonun ismi `LD_PRELOAD` . Kendisi environment variable(ortam değişkeni) olarak çalışmaktadır ve uygulamalarımızda kullanıcı tanımlı `.so` dosyalarını değiştirmemize olanak verir. Bu değişkene vermiş olduğumuz libraryler adından anlaşılacağı gibi preload yani her şeyden önce yüklenir veya linklenir.

Şimdi senaryoyu biraz canlandırıp detaylandıralım.

Linux sistem üzerinde güzelce çalışan bir programımız(ELF) var ve `benimadimenes.so` diye bir paylaşılan dinamik bir library kullanıyor. Bu uygulama ayrıca yaptığı işlerden dolayı `root` kullanıcısı ile çalışıyor. Buraya kadar her şey tamam. Bu sistemi ele geçirdiğimizi düşünelim ama kullanıcımız yetkisiz bir kullanıcı(örn:www). Aşağıdaki kısmı çok hızlı geçeceğim. Daha detaylı bir örnek için link vereceğim.

Biz bu yetkisiz kullanıcının izinlerini kontrol ettiğimizde LD_PRELOAD değişkenini değiştirebildiğini görüyoruz.  LD_PRELOAD değişkenini değiştirerek `benimadimenes.so` librarysinin pathini değiştiriyoruz. Bu değişimden sonra `root` kullanıcısı ile çalışan uygulamamız ilk olarak bizim manipüle ettiğimiz libraryi çalıştıracağı için artık `root` kullanıcısı ile her şeyi yapabiliriz.

Daha detaylı bir örnekler için:

[EN] [Abusing Shared Libraries](https://www.boiteaklou.fr/Abusing-Shared-Libraries.html)

[TR] [LD_PRELOAD Değişkeni Kullanımının İstismar Edilerek Hak Yükseltilmesi](https://www.siberportal.org/red-team/linux-penetration-tests/linux-sizma-testlerinde-ld_preload-degiskeni-kullaniminin-istismar-edilerek-hak-yukseltilmesi/)



## Strace

Bu komut linux sistemler üzerinde çalıştırmış olduğumuz uygulamaların yapmış olduğu sistem çağrılarını gösteren bir komuttur. Ben komutun açılımı olarak aklımda `system trace` bir açılım canlandırdım fakat yanlış olabilir. 

Derlenmiş bir uygulama/kodda troubleshooting veya debugging için kullanılan komutlardandır. 

Örnek bir çıktı:

```bash
strace ls ./Desktop
execve("/usr/bin/ls", ["ls", "./Desktop"], 0x7ffecc44f368 /* 67 vars */) = 0
brk(NULL)                               = 0x5582a178e000
access("/etc/ld.so.preload", R_OK)      = 0
openat(AT_FDCWD, "/etc/ld.so.preload", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=0, ...}) = 0
close(3)                                = 0
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=184716, ...}) = 0
mmap(NULL, 184716, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f5ccb9b2000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libselinux.so.1", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0|\0\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0644, st_size=163520, ...}) = 0

```

Daha detaylı bir açıklama için:

[TR] [Strace kullanımı](https://demirten.gitbooks.io/gomulu-linux/misc/strace.html)

[TR] [Strace ne işe yarar ve nasıl kullanılır](https://medium.com/@gokhansengun/strace-ne-i%C5%9Fe-yarar-ve-nas%C4%B1l-kullan%C4%B1l%C4%B1r-c46036ffa0)

[EN] [Debugging using strace](https://medium.com/@adminstoolbox/debugging-using-strace-efda7d65be1d)

[EN] [Understanding System Calls on Linux with Strace](https://opensource.com/article/19/10/strace)

Ayrıca Sistem çağrılarına kanca atma konusunda 2 adet yazı[Siber Güvenlik]

[Linux System Call Hooking](https://alp.run/2019/10/16/linux_system_call_hooking.html)

[Linux System Call Hooking](https://blacknbunny.github.io/2019/05/07/linux-system-call-hooking.html)



## Ltrace

Kendisi strace benzeri bir komut olmakla birlikte paylaşımlı(shared) librarylerden çağrılan fonksiyonları izlemeye yarar. Ayrıca `strace` komutunda olduğu gibi sistem çağrılarını da gösterebilir. Ben yine kafamda `library trace` olarak çevirdim.

Örnek bir çıktıyı aşağıya ekliyorum.

```bash
ltrace ls ./Desktop        
strrchr("ls", '/')                                                      = nil
setlocale(LC_ALL, "")                                                   = "en_US.UTF-8"
bindtextdomain("coreutils", "/usr/share/locale")                        = "/usr/share/locale"
textdomain("coreutils")                                                 = "coreutils"
__cxa_atexit(0x55a148528740, 0, 0x55a14853d388, 0)                      = 0
isatty(1)                                                               = 1
getenv("QUOTING_STYLE")                                                 = nil
getenv("COLUMNS")                                                       = nil
ioctl(1, 21523, 0x7ffeae0ce350)                                         = 0
getenv("TABSIZE")                                                       = nil
getopt_long(2, 0x7ffeae0ce488, "abcdfghiklmnopqrstuvw:xABCDFGHI:"..., 0x55a14853c680, -1) = -1
getenv("LS_BLOCK_SIZE")                                                 = nil
getenv("BLOCK_SIZE")                                                    = nil
getenv("BLOCKSIZE")                                                     = nil
getenv("POSIXLY_CORRECT")                                               = nil
getenv("BLOCK_SIZE")                                                    = nil
__errno_location()                                                      = 0x7f41bcad9258
memcpy(0x55a149d98a00, "\003\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"..., 56) = 0x55a149d98a00
__errno_location()                                                      = 0x7f41bcad9258
memcpy(0x55a149d98a40, "\003\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"..., 56) = 0x55a149d98a40
getenv("TZ")                                                            = nil
__errno_location()                                                      = 0x7f41bcad9258
__ctype_get_mb_cur_max()                                                = 6
strlen("./Desktop")                                                     = 9
__xstat(1, "./Desktop", 0x55a149d98b28)                                 = 0
strlen("./Desktop")                                                     = 9
memcpy(0x55a149d9d940, "./Desktop\0", 10)                               = 0x55a149d9d940
_setjmp(0x55a14853d680, 0, 0x55a149d98bd8, 0x55a149d9d968)              = 0
strlen("./Desktop")                                                     = 9
memcpy(0x55a149d9d9b0, "./Desktop\0", 10)                               = 0x55a149d9d9b0
freecon(0, 0x55a149d93010, 0, 0)                                        = 0
__errno_location()                                                      = 0x7f41bcad9258
opendir("./Desktop")                                                    = 0x55a149d9d9d0
readdir(0x55a149d9d9d0)                                                 = 0x55a149d9da00
readdir(0x55a149d9d9d0)                                                 = 0x55a149d9da18
__errno_location()                                                      = 0x7f41bcad9258
__ctype_get_mb_cur_max()                                                = 6
strlen("README.license")                                                = 14
strlen("README.license")                                                = 14
memcpy(0x55a149d9d940, "README.license\0", 15)                          = 0x55a149d9d940
readdir(0x55a149d9d9d0)                                                 = 0x55a149d9da40
__errno_location()                                                      = 0x7f41bcad9258
__ctype_get_mb_cur_max()                                                = 6
strlen("steam.desktop")                                                 = 13
strlen("steam.desktop")                                                 = 13
memcpy(0x55a149da5a10, "steam.desktop\0", 14)                           = 0x55a149da5a10

```

## Ekstra Bilgi

Linux sistemler üzerinde herhangi bir process'in memory üzerinde maplediği alanları görmek isterseniz aşağıdaki gibi bir komut kullanabilirsiniz.

```bash
cat /proc/[PID numarası]/maps
veya
cat /proc/$(pidof [Process ismi])/maps
```

Bu komutları çalıştırdığınızda devasa bir çıktı görebilir ve memory üzerinde processin aynı library ile birden fazla yer ayırdığını vs görebilirsiniz. Örnek vermek gerekirse 4 tane libgl.so (attım bu ismi) ismi görebilirsiniz. Bunun temel sebebi hepsinin farklı `permission` 'a sahip olmasıdır. 

Proc file systemi hakkındaki manuel'e ulaşmak için: [Tıklayın](https://www.kernel.org/doc/Documentation/filesystems/proc.txt)

## Yazı Sonu

Benimde henüz yeni araştırmış olduğum veya derinine daldığım bir yazı olduğu için hatalar olabilir eğer hatam varsa lütfen en kısa sürede beni bilgilendirin, bilgilendirmekten çekinmeyin. Yazı ilk halinden çok farklı bir hal aldı. Araştırırken gördüğüm şeyleri de eklemek istedim. Biraz uzun oldu.

Neyse. Benim için bir gelenek olan yazı sonu şarkısını aşağıya bırakıyorum.

Okuduğunuz için teşekkürler.

[![](http://img.youtube.com/vi/TFjmvfRvjTc/0.jpg)](http://www.youtube.com/watch?v=TFjmvfRvjTc "")

Biraz modum düşsün böyle şarkılar istiyorum diyen varsa aşağıda spotify playlistimin linkini koydum.

[hafifdertliböyle](https://open.spotify.com/playlist/1YctCQhYvuQ1YVt97qsZ1p?si=L8hz-gcaSIKlsxnJQu5Qlw)

---

**Kullandığım linkler**:

<https://stackoverflow.com/questions/1124571/get-list-of-static-libraries-used-in-an-executable>

<http://www.yolinux.com/TUTORIALS/LibraryArchives-StaticAndDynamic.html>

<http://man7.org/linux/man-pages/man8/ld.so.8.html>

<https://demirten.gitbooks.io/gomulu-linux/misc/strace.html>
