Title: Windows Sistemlerde Borular(PIPE)
Date: 2023-09-13 22:00
Tags: windows pipes, windows borular, pipe nedir, windows pipes türkçe, işletim sistemi borular, işletim sistemlerinde borular, işletim sistemlerinde pipelar, pipe ne demek
Category: windows
Authors: 0x656e


# Windows Sistemlerde İsimli Borular - Named Pipes

## Pipe neymiş?

Kendileri iki process arasında iletişim ve veri aktarımını sağlayan basit ve küçük bir teknolojidir. Processler arası iletişim kurmak için kullanılır. Pek tabii **Named Pipes** 2 uzak makine arasında da iletişim kurabilir. Aslında PIPE olarak bahsedilen 2 tür alt kategori var fakat bunlardan bizi ilgilendiren en geniş kapsamlısı olan **Named Pipes**dır.

- Named Pipes
- Anonymous Pipes

Burada PIPE’ın çocukluğuna inmeyeceğim. Geçmişim bir çöptür, çöpü karıştıran… tamam tamam. 

PIPE aslında temelinde Windows sistemlerde **FILE_OBJECT** objesidir ve kendisine ait NPFS(Named Pipe File System) dosya sistemi bulunur. Aslında bu konuda PIPE’lara erişim de, dosyaya erişim kadar basit düzeylere indirilebilir. 

- Server tarafında Named pipe oluşturmak için WinAPI’nin **CreateNamedPipe** fonksiyonu kullanılır. Bağlantıları beklemek veya kabul etmek için ise **ConnectedNamedPipe** fonksiyonundan yararlanılır.
- Client tarafında ise normal dosya açarmış gibi **CreateFile** veya **CallNamedPipe** fonksiyonları kullanılmaktadır.

**CreateNamedPipe** 

```cpp
HANDLE CreateNamedPipeA(
  [in]           LPCSTR                lpName,
  [in]           DWORD                 dwOpenMode,
  [in]           DWORD                 dwPipeMode,
  [in]           DWORD                 nMaxInstances,
  [in]           DWORD                 nOutBufferSize,
  [in]           DWORD                 nInBufferSize,
  [in]           DWORD                 nDefaultTimeOut,
  [in, optional] LPSECURITY_ATTRIBUTES lpSecurityAttributes
);
```

**CallNamedPipe**

```cpp
BOOL CallNamedPipeA(
  [in]  LPCSTR  lpNamedPipeName,
  [in]  LPVOID  lpInBuffer,
  [in]  DWORD   nInBufferSize,
  [out] LPVOID  lpOutBuffer,
  [in]  DWORD   nOutBufferSize,
  [out] LPDWORD lpBytesRead,
  [in]  DWORD   nTimeOut
);
```

Ref: 

[https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipes](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipes)

Ee tamam PIPE serverı oluşturduk. Client ile uzağa bağlanacağız diyelim. Bağlantı nasıl olacak? Aklınıza bir şey geliyor mu? Aslında cevabı çok basit biz uzak bir isimli boruya bağlanacaksak eğer bu işlem SMB üzerinden oluyor. Yani temelde SMB üzerinden bağlantı olduğu için aslında bir SMB’nin bize sunduğu tüm Authentication metodlarını kullanabiliriz. Yani bu Authentication işlemini network üzerinden (Network Authentication) SMB üstlenir. Bu sebeple de aslında tıpkı SMB gibi borulara yapılan bağlantılarda, tıpkı normal file system gibi CreateFile gibi fonksiyonları görürüz. 

## Allah’ın Borusunun Modları

Bu kısma bu şekilde isim vermemin sebebi aslında temelde basit bir düzene sahip olsa bile gevurlar bu işin detayını düşünüp borulara 2 adet mesaj iletim modu eklemelerinden dolayıdır. 

Neymiş bu 2 mesaj iletim modu:

1. Byte Mod
2. Message Mod

### Byte Mod

Kısaca bu mod, eğer gönderilen ve alınan verinin boyutu bilinmiyorsa veya tahmin edilemiyorsa kullanılıyor. Bu modda veri stream edilecek şekilde kullanılır.

### Message Mod

Bu modda ise gönderilen ve alınan veri bilinen bir veri boyutuna sahipse kullanılmaktadır. Pek tabii veri boyutunu aşan bir durum olursa bunu partlara/partionlara ayırmak yerine **234 (0xEA, ERROR_MORE_DATA)** hatası vermektedir.

Diğer hatalar ve ref. için:

[https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-](https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-)

**Önemli Not**: Boruları eğer OVERLAP yapısında oluşturmamışsanız borularda yapılan tüm işlemler **senkron** olarak yapılacaktır. Eğer **asenkron** bir şekilde işlem yapmak isterseniz OVERLAPED bir biçimde işlemler yapabilmek için **FILE_FLAG_OVERLAPPED** değerinin CreateNamedPipe fonksiyonunda belirtilmesi gerekmektedir.

Detaylı bilgi için:

[https://learn.microsoft.com/en-gb/windows/win32/ipc/synchronous-and-overlapped-input-and-output](https://learn.microsoft.com/en-gb/windows/win32/ipc/synchronous-and-overlapped-input-and-output)

 [https://learn.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-overlapped](https://learn.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-overlapped) 

### Blocking Mod

Yukarıdaki iletişim metodlarından farklı olarak önemli nota istinaden bu başlık girilmiştir. Aslında notla büyük bir bağlantısı vardır. Blocking mode içerisinde 2 adet ana başlık/ayar vardır. Bunlar:

1. PIPE_WAIT: İletişim sağlanırken, veri aktarılırken veya okunurken boru iletişimin tamamlanmasını bekler. 
2. PIPE_NOWAIT: İletişim sağlanırken, veri aktarılırken veya okunurken boru iletişimin tamamlanmasını beklemeden callback döner. Eğer bu mod kullanılıyorsa verinin okunması veya yazılmasının tamamlandığından emin olmak/kontrolünü sağlamak gerekmektedir. 

### Gelen, Giden Buffer

Bu başlık tıpkı viral olan aşağıdaki tirad gibidir.

[https://www.youtube.com/watch?v=xcmuBXAzwGc](https://www.youtube.com/watch?v=xcmuBXAzwGc)

Borular yapıları gereği diskte tutulmazlar. Yani geçici veri taşırlar. Bu sebeple bizim yazdığımız okuduğumuz veriler **non-paged memory'i** kullanır. Bu sebepledir ki konunun başında belirttiğimiz gibi boruları oluştururken verdiğimiz buffer boyutları önemlidir. 

Vereceğimiz bufferSizelar bizim ne kadar veri okuyabileceğimizi veya yazabileceğimizi belirtir. Burada belirtilen değerlerin dışına çıkılırsa sistem üzerinde hataya veya borular üzerinde gecikmeye sebebiyet verebilir. 

Windows’un x64 sistemlerinde en yüksek olabilecek bufferSize işletim sistemine bağlı olarak 4gb kadarcıktır. Eğer bufferSize 0 olarak verilirse işletim sistemi akıllıdır bunu anlar ve sizin aslında minimum veriye ihtiyacınız olduğunu düşünür. Bu sebeple gelen veriyi kontrol eder ve buna göre bir bufferSize ayırır fakat bu da ekstra maliyet demektir. Çünkü gelen veriyi kontrol et → bufferı genişler → veriyi kabul et akışı oluşur. Bu sebeple sunucu ve istemci(client) arasında gecikmeye sebebiyet verir.

## Boruların Güvenliği

Başlık biraz “anamın ruhunu ortaya koyuyorum (JoJo)” gibi oldu ama kusura bakmayın artık. İşin çokomelli yerine geldik. 

Yukarıda da linkini vermiştim diye hatırlıyorum ama boruları oluştururken kullandığımız, windows structure’ına aşağıdan ulaşabilirsiniz. 

[https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createnamedpipea](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createnamedpipea)

Konu boruları oluşturmaya gelince aslında elimizde çok fazla bir seçeneğimiz yok. Yukarıdaki linke bakarsanız eğer (bakın bir zahmet) aşağıdaki tanımlamayı görebilirsiniz.

```cpp
[in, optional] LPSECURITY_ATTRIBUTES lpSecurityAttributes
```

Buradaki değerin **optional** olduğunu görüyoruz. Boruyu yani PIPE’ı oluştururken ilgili değer eğer değer vermemişsek ********NULL******** olarak tanımlanacaktır fakat ilgili değer default olarak ACL’lerde belirtilen “default security descriptor” ile tanımlanacaktır. Bu da LocalSystem kullanıcılarına, boruyu oluşturana, yöneticilere full control vermekle birlikte herkese de read yetkisi verecektir. 

Bu sebeple ilgili flaglerin güvenli bir şekilde verilmesi önem arz etmektedir. Düzgün verilmeyen sistemler “Impersonation” ataklarına izin vermektedir.

İlgili ataklarla alakalı daha detaylı bilgi:

[https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation/named-pipe-client-impersonation](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation/named-pipe-client-impersonation)

Eveet bu yazının da sonuna geldik ama bu yazıyı tek başına burada tutmak istemiyorum. Bu yazıyı diğer işletim sistemleri ve windows özelinde “İşletim Sistemleri Arası İletişim Serisi” haline getirmeyi düşünüyorum.

Şimdilik not aldığım konular aşağıdaki gibi:

1- Named Pipes

2- RPC

3- WMI

Velhasıl kelam yine yazı sonu şarkı önerisiyle sizlere veda ediyorum. Esen kalın.


[![I don't have money](https://i.ytimg.com/vi/b_S732Wl1cA/maxresdefault.jpg)](https://www.youtube.com/watch?v=b_S732Wl1cA "I don't have money")


## Referanslar

[https://blog.stephencleary.com/2010/03/io-limitation-in-windows.html](https://blog.stephencleary.com/2010/03/io-limitation-in-windows.html)
