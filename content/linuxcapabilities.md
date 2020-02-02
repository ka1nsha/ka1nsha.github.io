Title: Linux Capabilities API 
Date: 2020-02-02 14:00
Tags: Capabilities API Türkçe, Linux Yetkilendirme, SUID Bit İstismarı, Linux Yetki Yükseltme, Capabilities Nedir, Linux Capabilities Nedir, Linux Yetkilendirme Sistemleri
Category: linux
Authors: 0x656e


Selamlar,

Günlük olarak RSS feedlerimi takip etmeye özen gösteren birisiyim(Feedly). Bu feedler arasında bolca HTB(HackTheBox)  write-up kaynağı da bulunuyor doğal olarak. İşte yine bir HTB makinesi ile ilgili write-up'ı okurken bunca yıldır Linux(End-User olarak) kullanan biri olarak karşılaşmadığım ve karşılaştığımda şaşırdığım bir komut gördüm. Neydi bu komut?

```bash
getcap -r / 2>/dev/null
```

Komutu anlatmak gerekirse recursive bir biçimde `/` yani en üst dizinden başlayarak tüm dosyaların kabiliyetlerini kontrol edecek ve eğer return code olarak `2` kodu dönülüyorsa bunu `/dev/null` uzayına gönderecek.

## Linux Yetkilendirme Sistemleri

Bu zamana kadar genelde dosya yetkilerini kontrol ederken, sadece sembolik olan yetkilendirme sistemini kontrol ederdim. Bu sembolik yetkilendirme sistemi nedir derseniz, kendisi `chmod, chown ` komutları ile birlikte kullandığınız `octal` numerik olarak belirtilen(sembolik) dosya yetkilendirme sistemidir.

Eğer bu konu hakkında bilgi sahibi değilseniz aşağıda vermiş olduğum kaynağı, kaynağın tümünü tüketebilirsiniz. Çok güzel bir kaynaktır.

[Linux Sistem Programlama](https://demirten.gitbooks.io/linux-sistem-programlama/content/users/)

## Peki Enes Bunlar Ne İşe Yarayacak

Öncelikle bir hacker olduğunuzu düşünün, bir linux sistemi ele geçirdiniz fakat o da ne? Sistem üzerinde Nginx'in tüm işlemleri özel bir kullanıcı ile yürütülüyor ve siz bu sistemde at koşturamıyorsunuz. Ne yapmamız gerek? Sistem üzerinde yetkimizi yükseltebileceğimiz bir şeyler aramamız gerekmekte.

Ne yapabiliriz? Mesela SUID Bit içeren dosyaları arayabiliriz.

```bash
find / -perm -4000 -type f 2>/dev/null
```

Tamam bir executable dosya bulduk ama bunu nasıl kullanacağımızı bilmiyoruz? İster Google üzerinde aratın ya da bu iş için çok güzel bir site hazırlamışlar ona bakabilirsiniz.

[GTFOBins](https://gtfobins.github.io/) (Linux)

[LOLBAS](https://lolbas-project.github.io/#) (Windows)



vs.vs bir sürü senaryo üretilebilir fakat hiç dosya kapasiteleri(capabilities) aklınıza gelmiş miydi? Benim şahsen böyle bir şey olduğundan bile haberim yoktu. Zaten bu yüzden bu blog yazısının konusu bu.

## Capabilities API'a Neden İhtiyaç Var

Eski kernel sürümlerinde Linux üzerinde yetkilendirme sistemi bu kadar gelişmiş değildi ve bazı kısıtlamalar yüzünden siber güvenlik açısından büyük riskler barındıran işlemler gerçekleştiriliyordu. 

Örnek: Linux üzerinde Port olarak 1024'ün altında bir portta socket açacaksanız `root` kullanıcısı olmak zorundasınız. Peki sunucunuza Nginx kurdunuz ve web servisi yayınlayacaksınız. Bunu `root` kullanıcısı olarak kurup çalıştırdığınızda geçmiş olsun. 

Örnek1: 1024 altında port açmak için `root` kullanıcısına ihtiyacınız var demiştik. Peki günlük olarak troubleshooting için kullandığımız `ping` komutu? Ping bildiğiniz üzere port kullanan bir yapıda değil ki zaten farklı bir protokol. Bknz: ICMP. Ping atabilmek için raw_socket açmak zorundasınız ve bu sadece `root` kullanıcısına özgü bir yetki. Takılıp kaldık mı? Hayır.

Bu arada ICMP temelli çalışan fakat işletim sistemine göre değişen `traceroute` ile ilgili aşağıya güzel bir link iliştiriyorum.

[ping ve traceroute nasıl çalışır](https://medium.com/@gokhansengun/ping-ve-traceroute-nas%C4%B1l-%C3%A7al%C4%B1%C5%9F%C4%B1r-146e151ff83b)

Neyse devam. İşte bu kısımda takılıp kalmıyoruz SUID Bit devreye giriyor. Bu da ayrı bir yazı konusu aslında o yüzden direkt olarak size konu ile ilgili link vereceğim.

[SUID ve SGID Bit](https://www.syslogs.org/suid-ve-sgid-bitler-ve-bu-bitlere-sahip-dosyalarin-bulunmasi/)

Tamam bunu okuduk ama diğer taraftan aşağıdakini de okumakta fayda var.

[SUID Bit İstismarı](https://canyoupwn.me/tr-suid-bit-istismari/)

Evet zararlı kısmını da gösterdik. Şimdi konu gerçekten Capabilities API'a geldi. Şu an kullandığınız distroda ping komutunun nasıl çalıştığına(yetkisiz kullanıcı ile) baktınız mı hiç?

Hadi yetkilerine bakalım. Direkt olarak komutları ve çıktılarını aşağıya kopyalıyorum. Sonra üstünde konuşacağız.

```bash
➜  /bin ls -la | grep ping
-rwxr-xr-x  1 root root          75760 Jan  5  2019 atk6-thcping6
-rwxr-xr-x  1 root root          48032 Aug  7 02:48 fping
lrwxrwxrwx  1 root root              5 Jan  4 18:47 fping6 -> fping
-rwxr-xr-x  1 root root         106344 Jul 14  2019 l2ping
-rwxr-xr-x  1 root root          43248 Oct 23 15:53 mate-typing-monitor
-rwxr-xr-x  1 root root         752656 Nov 26 12:21 nping
-rwxr-xr-x  1 root root          73496 Oct  5 17:34 ping
lrwxrwxrwx  1 root root              4 Oct  5 17:34 ping4 -> ping
lrwxrwxrwx  1 root root              4 Oct  5 17:34 ping6 -> ping
-rwxr-xr-x  1 root root           6773 May 21  2019 wifiping
➜  /bin id
uid=1000(ka1) gid=1000(ka1) groups=1000(ka1),20(dialout),24(cdrom),25(floppy),27(sudo),29(audio),30(dip),44(video),46(plugdev),109(netdev),119(debian-tor),126(bluetooth),136(scanner),998(docker)
➜  /bin ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=54 time=15.4 ms

```

Gördüğünüz gibi ping komutu `root:root` olarak yetkilendirilmiş bir biçimde üstelik herhangi bir `SUID Bit vb.` bir şey de yok fakat ben nasıl çalıştırabiliyorum?

Yine terminal çıktısı atayım.

 ```bash
➜  /bin sudo getcap /usr/bin/ping
/usr/bin/ping = cap_net_raw+ep
➜  /bin 
 ```

Gördüğünüz gibi `ping` çalıştırılabilir dosyasında bir kapasite sınırı sonunda + olarak belirtilmiş bir yetkilendirme biçimi var.

**Not:** Ping komutunun artık kullanıcı tarafında çalıştırılabilmesi için herhangi bir izne ihtiyacı yok. Sebebi ping socketinin direkt olarak kernela eklenmesi.(Ben öyle anladım?)

Kaynak: [      net: ipv4: add IPPROTO_ICMP socket kind    ](https://github.com/torvalds/linux/commit/c319b4d76b9e583a5d88d6bf190e079c4e43213d)

## Capabilities API

Öncelik olarak Kernel sürümümüze özel olarak sistem üzerinde ne kadar farklı yetkilendirme yapabileceğimize bakalım. (Tüm Capabilities Yetkilerine)

```bash
➜  ~ sudo capsh --print
Current: = cap_chown,cap_dac_override,cap_dac_read_search,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_linux_immutable,cap_net_bind_service,cap_net_broadcast,cap_net_admin,cap_net_raw,cap_ipc_lock,cap_ipc_owner,cap_sys_module,cap_sys_rawio,cap_sys_chroot,cap_sys_ptrace,cap_sys_pacct,cap_sys_admin,cap_sys_boot,cap_sys_nice,cap_sys_resource,cap_sys_time,cap_sys_tty_config,cap_mknod,cap_lease,cap_audit_write,cap_audit_control,cap_setfcap,cap_mac_override,cap_mac_admin,cap_syslog,cap_wake_alarm,cap_block_suspend,cap_audit_read+ep
Bounding set =cap_chown,cap_dac_override,cap_dac_read_search,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_linux_immutable,cap_net_bind_service,cap_net_broadcast,cap_net_admin,cap_net_raw,cap_ipc_lock,cap_ipc_owner,cap_sys_module,cap_sys_rawio,cap_sys_chroot,cap_sys_ptrace,cap_sys_pacct,cap_sys_admin,cap_sys_boot,cap_sys_nice,cap_sys_resource,cap_sys_time,cap_sys_tty_config,cap_mknod,cap_lease,cap_audit_write,cap_audit_control,cap_setfcap,cap_mac_override,cap_mac_admin,cap_syslog,cap_wake_alarm,cap_block_suspend,cap_audit_read
Ambient set =
Securebits: 00/0x0/1'b0
 secure-noroot: no (unlocked)
 secure-no-suid-fixup: no (unlocked)
 secure-keep-caps: no (unlocked)
 secure-no-ambient-raise: no (unlocked)
uid=0(root)
gid=0(root)
groups=0(root)
```

Gördüğünüz gibi yetkileri görmek için `capsh --print` komutunu kullanabilirsiniz. Daha detaylı bir kullanım için: 

[Capsh manpages](http://man7.org/linux/man-pages/man1/capsh.1.html)

Bir dosyaya ait kapasiteyi öğrenmek için de

`sudo getcap dosya` komutunu kullanabilirsiniz. 

Ping komutuna getcap ile baktığımızda yetkilendirme sonrasında +ep olarak bir şey görmüştük peki bu ifadeler neydi diye görmek isterseniz aşağıdaki tabloya bakabilirsiniz. 

**Not:** Direkt olarak [buradan](https://demirten.gitbooks.io/linux-sistem-programlama/content/capabilities/) kopyalanmıştır.

|   Capability    | Açıklama                                                     |
| :-------------: | :----------------------------------------------------------- |
|  **permitted**  | Bu kümede ilgili process'in izin verilen ek  capability listesi bulunur. İzin verilmesi o an aktif olarak  kullanılabileceği anlamına gelmeyebilir, ek bir işlemle buradaki  yetkilerin etkin (effective) capability kümesine dahil edilmesi  mümkündür. |
|  **effective**  | İlgili process'in o anki etkin capability  listesini gösterir. Capability sistemini düzenleyen yardımcı  fonksiyonlarla bir capability'den vazgeçilebileceği gibi tekrar geri de  alınabilir. Ancak her durumda bu işlem sadece *permitted* grubunda zaten izin verilmiş olanlar arasından yapılabilir. |
| **inheritable** | Process tarafından yeni bir process çalıştırıldığında, yeni çalıştırılan process'in *permitted* listesine miras yoluyla aktarılacak capability listesini gösterir. |

`capsh` ile gördüğümüz bir sürü yetkilendirme ne işe yarıyor peki derseniz onunla ilgili de aşağıdaki sayfayı kullanabilirsiniz.

[Capabilities man pages](http://man7.org/linux/man-pages/man7/capabilities.7.html)

## Bitiş

Bu yazıda amacım derin bir biçimde `Capabilities API` ı incelemek değildi bu sebeple ilgili yazıyı yetersiz bulmuş olabilirsiniz. Amacım tamamen bakın böyle bir şey de varmış. Şuraya, buraya bakabilirsiniz veya hacklediğiniz bir sistemde bakabileceğiniz bir kapı daha açabilmektedir. Yorumlarınızı site üzerinden (Disqus) veya Twitter üzerinden [0x656e](https://twitter.com/0x656e) yapabilirsiniz. Olumlu olumsuz benim için farketmez.

Yazı sonuna geldik. Evet bu yazının hazırlanmasında okuduğum, kullandığım linkleri aşağıda referanslar olarak görebilirsiniz. Bir klasik olarak yazı sonu şarkı paylaşımlarıma da aşağıdan ulaşabilirsiniz.

[![](http://img.youtube.com/vi/DdcusOXh_f8/0.jpg)](http://www.youtube.com/watch?v=DdcusOXh_f8 "")

[![](http://img.youtube.com/vi/iIwNthexyNM/0.jpg)](http://www.youtube.com/watch?v=iIwNthexyNM "")



------



Referanslar:

[Linux Capabilities 101](https://linux-audit.com/linux-capabilities-101/)

[Linux Sistem Programlama Capabilities](https://demirten.gitbooks.io/linux-sistem-programlama/content/capabilities/)

[HTB Waldo Writeup](https://0xrick.github.io/hack-the-box/waldo/)
