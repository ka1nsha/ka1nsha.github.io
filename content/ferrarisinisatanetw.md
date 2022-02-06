Title: Ferrarisini satan ETW (Event Tracing for Windows)
Date: 2022-2-06 18:00
Tags: ETW, Event Tracing for Windows, ETW Türkçe, ETW Hack, ETW Bypass, ETW Evasion, ETW Blue Team, ETW Red Team, Event Tracing for Windows Türkçe
Category: siber güvenlik
Authors: 0x656e



> Satan kelimesinin gizli bir anlamı yoktur tıpkı araç plakamın sonunun 666 olması gibi.

Selamlar öncelikle. Nasılsınız? Her telden çalan bir insan olduğum için bugün de (1 yıl sonra) tamamen farklı bir konu üzerinden bahsetmek istiyorum. Kendisini çeşitli mail listelerini takip ederken tanıdım. İlgimi çekti ve araştırıp bunun yazısını yazmak istedim. Birbirimizi sevebileceğimizi umuyorum. 

> İş bu blog konusu size hiç bir uzmanlık vermeyecektir, vermeyi tahahhüd etmemektedir. Türkiye piyasasında bir kaç kişi/grup harici genelde teknolojiyi takip eden tarafta olduğumuz için(keşke Numan olsam :D) pek tabii internette okuyup özetini çıkarttığım bilgileri sizlere sağlamış olacağım diye düşünüyorum.


O zaman giriş yapalım. Kağan'dan önce yazmak için bazı konuları atlamış, kaçırmış olabilirim. Affınıza sığınıyorum. (Ulan bir blog konusu yazıyorsun bari bir şeyleri tam yap diyenleri [şuraya alalım.](https://youtu.be/dQw4w9WgXcQ) )

## ETW Ne Demekti? Sevgi demekti, Emek demekti.

[Bknz:About Event Tracing](https://docs.microsoft.com/en-us/windows/win32/etw/about-event-tracing)

Kendisinin açılımı Event Tracing For Windowstur. Kendisi çekirdekteki veya uygulama tanımlı olayları log dosyası veya real time olarak takip etmenize olanak sağlayan verimli bir yöntemdir. Kendisi/kendileri sistemi yeniden başlatmadan tracing'i(takip, izleme) aktif veya pasif hale getirebilmenize olanak sağlayabilen oldukça kullanışlı(Belki de tehlikeli) bir özelliktir. 

Kıymetlilerimiz 3 ana parçaya sahiptir. Bunlar:

* **Controller**: İzleme başlatabilen, etkinleştirebilen, devre dışı bırakabilen uygulamalardır.
* **Providers**: Log oluşturan uygulamalar vs.
* **Consumers**: Providerlar tarafından loglari, aktiviteleri dinleyen abone(??) olan uygulamalardır. 


Bu 3 madde harici ayrıca bilmemiz gereken bazı keyword(anahtar terimler) de var tabii. 

* **Tracing Session**: Bir veya birden fazla providerdan gelen olayları kaydeden mekanizmadır/uygulamadır.
* **Keywords**: Consumerlara bilgiyi sağlayan olay türleridir. Burası önemli.

**ETW üzerinde çok önemli 2 fonksiyon bulunmaktadır. Bunlar: 1.NTTraceControl(Trace fonksiyonlarını yönetiyor) 2. NtTraceEvent (Aktiviteleri/Eventleri yazıyor.)**

```
NTSTATUS
NtTraceControl (
    ULONG FunctionCode,
    PVOID InBuffer,
    ULONG InBufferLen,
    PVOID OutBuffer,
    ULONG OutBufferLen,
    ULONG *ReturnSize);

NTSTATUS
NtTraceEvent (
    HANDLE TraceHandle,
    ULONG Flags,
    ULONG FieldSize,
    PVOID Fields);
```

Bu kadar teori yeter. Şimdi biraz da pratik kısmına bakalım.



## ETW Providerları Görmek

Sisteminiz üzerindeki providerları görebilmek için sistem üzerinde komut istemcisine(command prompt, powershell vb.) `logman providers` yazdığınızda sistem üzerinde zibilyon tane provider görebilirsiniz. Ben PowerShell üzerinde measure dediğimde 1149 tane provider görüyorum. 

![image-20220206165502609](images/image-20220206165502609.png)

![image-20220206165404280](images/image-20220206165404280.png)



İlk ekran görüntüsündeki çıktıda GUID'leri görüyoruz. Bizim için asıl önemli olanlar bunlardır. Bir provider'a subscribe(kayıt/abone/hook ne derseniz artık) olurken kullanacağımız keywordleri bu GUID'i sorgulayarak yapacağız. Pek tabii bu providerları tek tek terminal üzerinden kontrol etmek istemeyebilirsiniz. Bunun için geliştirimiş bazı araçlar bulunmaktadır. Ben genel olarak makalelerde "EtwExplorer" kullanıldığını görmekteyim. Aşağıda ekran görüntülerini ekliyor olacağım.

![image-20220206165808464](images/image-20220206165746333.png)

![image-20220206165849819](images/image-20220206165849819.png)

![image-20220206165935681](images/image-20220206165935681.png)

Burada işaretli alan oldukça önemli. Microsoft-Windows-Kernel-Process Provider'ına ait template'i XML biçiminde görüyorsunuz. Subscribe olduğumuzda işaretli alandan nelere subscribe olacağımızı seçeceğiz. Bu kısımda verdiğimiz değerler toplama olarak gidiyor bu arada. Mesela "0x10, 0x20, 0x40"a subscribe olacağımızı düşünrsek `0x70` yazabiliriz. 

**Uygulamayı geliştiren Pavel abimize saygılar. Kendisi Windows SysInternals kitaplarının yazarı olmakla birlikte Pentester Academyde de eğitmenlik yapmış birisi. Daha fazlasını öğrenmek isterseniz size kalmış araştırabilirsiniz.**

## ETW üzerinde Subscribe Olmak

Şimdi işimize uygun olan provider'ı seçtik diyelim. Bu provider'a subscribe olmak için bizim bir `trace session`a ihtiyacımız var. Bu sebeple logman üzerinden bu session'ı oluşturmalıyız. Varolan sessionları listelemek için aşağıdaki komutu yazabilirsiniz.

```powershell
logman query -ets
```

Hadi bir trace session oluşturalım.

```powershell
logman create trace enesindnsleri -ets
```

Şimdi bunu yazdığımızda aşağıdaki sonuca erişmiş olmamız lazım.

![image-20220206171339464](images/image-20220206171339464.png)

Ama şu an tamamen kullanışsız çünkü herhangi bir provider'a subscribe olmadık. Ben sistem üzerindeki DNS çağrılarımı görmek istiyorum. Çağrıdan kastım DNS istekleri. Bunun için önce hangi provider olduğunu bulmam lazım.

```powershell
logman query providers | Select-String "dns"
```

yazdığımda bana 

`{1C95126E-7EEA-49A9-A3FE-A378B03DDB4D}` GUID'sini verdi. Ben buna subscribe olacağım. Herhangi bir keyword vermeyeceğim bu sebeple direkt olarak aşağıdaki gibi bir komut çalıştırarak benim trace session'ıma provider'ı subscribe edeceğim. Dilerseniz siz fazladan/başka providerlar da ekleyebilirsiniz.

```powershell
logman update enesindnsleri -p "Microsoft-Windows-DNS-Client" -ets
```

Bakalım subscribe olabildik mi?

```powershell
logman query enesindnsleri -ets
```

Çıktımız: 

![image-20220206173433760](images/image-20220206173433760.png)

Burada kendisi bir output belirledi ve keyword olarak All  olarak algıladı fakat .etl dosyamda nedense hata verdi. Bende bu sebeple şöyle bir yola gittim. Siz de dilerseniz output çıktısını değiştirebilirsiniz. Daha fazlası için

[Windows Docs for Logman](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/logman)

```
logman update enesindnsleri -ow -o C:\Users\Enes\enesdns1.etl -p "Microsoft-Windows-DNS-Client" 0x10 -ets
```

![image-20220206175045137](images/image-20220206175045137.png)

Şimdi bir de çıktı dosyamıza bakalım. 

![image-20220206180844358](images/image-20220206180420094.png)

Gördüğünüz gibi arkada Discord açık olduğu için Discord'un CDN sunucuları için bir DNS sorgusu atmışım. Pek tabi bu görüntüler takip açısından çok verimli değil ama bu kısımda Velociraptor kullanabilirsiniz. Bununla ilgili bir linki kullanabileceğiniz kaynaklar altına ekleyeceğim. Daha doğrusu tam halini ekleyeceğim.

![image-20220206181901173](images/image-20220206181901173.png)

Velociraptor VQL'i:

```sql
SELECT System.TimeStamp AS Timestamp,
       EventData.QueryName AS Query,
       EventData.QueryType AS Type,
       EventData.QueryResults AS Answer
FROM watch_etw(guid="{1C95126E-7EEA-49A9-A3FE-A378B03DDB4D}")
WHERE System.ID = 3020
```



Peki şimdi işin bu kısmını hallettik diyelim. Bu ne işimize yarayacak?  Bununla ilgili gördüğüm örnekler: 

* USB Provider'ını kullanarak keylogger
* ETW kullanarak uygulamalarınızı gizleme
* Enumeration/Cihaz keşfi sırasında WMI'a nazaran daha az görünürlük. (Tespit edilememe)
* AV? AV Bypass
* .NET Developerlar için uygulama performans analizi

konularına odaklanmış gibiydi. Benim de yeni öğrendiğim bir konu ve terim oldu. Hatta bu zamana kadar ETW'yi hiç duymamıştım. Ufkunuz açıldıysa ne mutlu bana!

İlgili maddelerle alakalı kullanabileceğiniz, detayına inebileceğiniz veya bu bana yetmedi dediğiniz yerlerde aşağıdaki linkleri kullanabilirsiniz.

* [Keylogging](https://cyberpointllc.com/blog-posts/cp-logging-keystrokes-with-event-tracing-for-windows-etw.php)
* [Keylogging[1]](https://sudonull.com/post/13104-Event-Tracing-for-Windows-on-the-side-of-evil-But-it-is-not-exactly)
* [Source code for Keylogger](https://github.com/CyberPoint/ETWKeyLogger_PSE)
* [Velociraptor Event Tracing For Windows](https://velociraptor.velocidex.com/event-tracing-for-windows-41eb031abd69)
* [Sysmon and ETW for so Much More](https://www.binarydefense.com/using-sysmon-and-etw-for-so-much-more/)
* [Enumeration](https://twitter.com/Arkbird_SOLG/status/1441876714246885381)
* [Blackhat Blind EDR](https://i.blackhat.com/EU-21/Wednesday/EU-21-Teodorescu-Veni-No-Vidi-No-Vici-Attacks-On-ETW-Blind-EDRs.pdf)
* [Sharpsploit tarafından ETW kullanarak nasıl Evasion yapıldığını görmek için](https://github.com/cobbr/SharpSploit/blob/master/SharpSploit/Evasion/ETW.cs)
* [Yine ETW kullanabilen bir Framework](https://github.com/optiv/ScareCrow)

Bir klasik olarak yazı sonu şarkısını da aşağıya ekliyor olacağım.

[![Ateş Olsan - Bubituzak](https://res.cloudinary.com/marcomontalbano/image/upload/v1644161493/video_to_markdown/images/youtube--Qm7mZkEQCaY-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=Qm7mZkEQCaY "Ateş Olsan - Bubituzak")

---

**Referanslar**:

[ETW](https://renenyffenegger.ch/notes/Windows/ETW/index)

[ETW Event Tracing For Windows 101](https://www.ired.team/miscellaneous-reversing-forensics/windows-kernel-internals/etw-event-tracing-for-windows-101)

[Make ETW Great Again](https://ruxcon.org.au/assets/2016/slides/ETW_16_RUXCON_NJR_no_notes.pdf)

[Derbycon Detecting Attacks with ETW](http://www.irongeek.com/i.php?page=videos/derbycon7/s25-tracing-adversaries-detecting-attacks-with-etw-matt-hastings-dave-hull)

