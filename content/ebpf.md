Title: eBPF Diye Bir Şey Varmış
Date: 2022-11-21 15:00
Tags: ebpf, ebpf türkçe, ebpf nedir, linux, ring0, user space, kernel space, bpf, python ebpf
Category: linux
Authors: 0x656e


# eBPF Diye Bir Şey Varmış

Not: Yazının altı Awesome gibi oldu amacım asla böyle bir şey değil fakat ekstra bilgi göz çıkartmaz diye. Hem de kendime not sonuçta.

Konuya nasıl girsem bilemedim. Aslında yazılarımda genel olarak giriş/girizgah için konunun ana hatlarıyla ne olduğundan bahsederim ama burada farklı mevzular da karşımıza çıktığı için sanırım işin temelinden almak gerekiyor. 

Bu yazı içerisinde çalışırken aldığım notlar ve çıkarımlardan bahsedeceğim. Hali hazırda uzmanı olduğum bir konu değil ve öğrenirken bahsetmek veya bahsetmek(blog yazısı) için öğrenme taraftarıyım. Benim açımdan bu daha efektif bir öğrenme biçimi oluyor. Her neyse. Ana odak noktamız eBPF olacak. eBPF’i anlatabilmek için kıyısından köşesinden user space ve kernel space, BPF ve tarihinden bahsedeceğim. 

## User Space ve Kernel Space

Bildiğiniz üzere günümüz modern işletim sistemlerinde işlemler “virtual memory” üzerinden işletilmektedir. İlgili “virtual memory sistemleri” sistem üzerinde çalışan processlerin memory üzerindeki adreslerini sanal bir adres üzerinden fiziksel sanal adresten ayırır. İlgili yöntem dolayısıyla biz processlere RAM üzerinde paging veya swapping yaptırtabiliyoruz. Konumuz memory management olmadığı için detaylı aramayı Google üzerinden yapabilirsiniz. Keywordler: Memory Management, Dynamic Allocation, Virtual Memory. 

Bir üst paragrafta bahsedilen “virtual memory” üzerinde de işlemler aslında ayrılmıştır. Günümüzde işletim sistemleri genellikle “virtual memory’i” user space ve kernel space olarak ayırmaktadır. Bunun temel sebeplerinden en önemlisi güvenlik kaygısı ve donanım güvenliğidir. “Kernel Space” işletim sisteminin kernelini, kernel eklentilerini ve genellikle donanım sürücüleri tarafından kullanılmaktadır. Kernel space’in donanıma sınırsız bir erişimi vardır ve bilin bakalım eğer 2 ana bölgeye ayrılmasaydı donanımlarımızın hali nice olurdu? User space de ise bizim günlük kullandığımız uygulamalara ayrılmıştır bunlar nadiren hardware ile konuşur ve yetkileri de (donanıma erişim) kısıtlanmıştır. Bu ana 2 bölgeye ayrılması sonucu aslında karşımıza bir farklı terim çıkmaktadır bu da “protection ring” olarak tanımlanmaktadır.

Bknz:

![Untitled](images/ring0.png)

## eBPF’e Geçmede Önce BPF

İlk olarak 1992 yılında BSD OS için geliştirmiştir. Linux içinse 2.1.75 içerisinde duyurulmuştur. Açılımı Berkeley Packet Filter’dır. Temel amacı data paketlerini filtrelemek ve bunu kernel içerisine gömmektir. Aslında güvenlik katmanlarıyla birlikte verilere ve programlara arayüz sunmaktadır. Bizim yazmış olduğumuz filtrelere göre herhangi bir paketin kabul veya red edileceğine karar verebiliyor ve karşılaştırmasını yapabilmektedir. 

![Untitled](images/bpf.png)

## BPF Nasıl Çalışır

BPF sanal makineni bir parçası olarak makine diline bir yorumlayıcı olarak yerleştirilmiştir. Önceden tanımlanmış “instructionları” yürüterek paketleri, dataları okur analiz eder ve adım adım çalıştırır. Yazılan “instructionlar” makine diline çevrilerek ve kernel içerisinde doğrudan çalıştılır. Bu sayede önemli bir hesaplama gücü elde edilmiş olur. **tcpdump** da tam olarak BPF’i kullanmaktadır. Yüksek seviyede bizim yazdığımız filtreleri bu şekilde çalıştırır. Tabi ki BPF sadece paket filtreleme için değil ayrıca Secure Computing için de kullanılmaktadır. Daha detaylı bilgi için: **seccomp** keywordünü kullanabilirsiniz. 

Gerisi için:

1.  [https://man7.org/linux/man-pages/man2/bpf.2.html](https://man7.org/linux/man-pages/man2/bpf.2.html)
2. [https://www.kernel.org/doc/html/latest/networking/filter.html](https://www.kernel.org/doc/html/latest/networking/filter.html)

Örnek bir BPF Syntax:

```c
#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <linux/if_ether.h>
/* ... */

/* From the example above: tcpdump -i em1 port 22 -dd */
struct sock_filter code[] = {
        { 0x28,  0,  0, 0x0000000c },
        { 0x15,  0,  8, 0x000086dd },
        { 0x30,  0,  0, 0x00000014 },
        { 0x15,  2,  0, 0x00000084 },
        { 0x15,  1,  0, 0x00000006 },
        { 0x15,  0, 17, 0x00000011 },
        { 0x28,  0,  0, 0x00000036 },
        { 0x15, 14,  0, 0x00000016 },
        { 0x28,  0,  0, 0x00000038 },
        { 0x15, 12, 13, 0x00000016 },
        { 0x15,  0, 12, 0x00000800 },
        { 0x30,  0,  0, 0x00000017 },
        { 0x15,  2,  0, 0x00000084 },
        { 0x15,  1,  0, 0x00000006 },
        { 0x15,  0,  8, 0x00000011 },
        { 0x28,  0,  0, 0x00000014 },
        { 0x45,  6,  0, 0x00001fff },
        { 0xb1,  0,  0, 0x0000000e },
        { 0x48,  0,  0, 0x0000000e },
        { 0x15,  2,  0, 0x00000016 },
        { 0x48,  0,  0, 0x00000010 },
        { 0x15,  0,  1, 0x00000016 },
        { 0x06,  0,  0, 0x0000ffff },
        { 0x06,  0,  0, 0x00000000 },
};

struct sock_fprog bpf = {
        .len = ARRAY_SIZE(code),
        .filter = code,
};

sock = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
if (sock < 0)
        /* ... bail out ... */

ret = setsockopt(sock, SOL_SOCKET, SO_ATTACH_FILTER, &bpf, sizeof(bpf));
if (ret < 0)
        /* ... bail out ... */

/* ... */
close(sock);
```

## Gelelim eBPF’e

Ortaya çıkış amacı aslıda küçük bir ekibin BPF’i dtrace benzeri kullanılabilirliğe eriştirebilmesi içindir. Zaten Solaris ve BSD üzerinde dinamik takip için kullanılan “dtrace’den” etkilendikleri belirtilmektedir.

Bknz: Referanslar[6]

eBPF ilk olarak kısıtlı bir kapasiteyle Linux 3.18 kernelinde release edilmiştir. Tam bir kullanım için en düşük Linux 4.4 Kernel’ına sahip olmalısınız. Kendisi Kernel Space üzerinde networking, debugging, tracing, firewall ve daha fazlası için kullanılabilmektedir. Zaten kendisi kernel sistem çağrılarına ve fonksiyonlarına hook atabilmenizi sağlamaktadır. 

Bir eBPF programı yazdığımızda ilgili kod **BCC** ile compile edilir ve ilgili program önemli bir çok ciddi denetimden geçer. 

İlgili denetimler için: [https://github.com/torvalds/linux/blob/master/kernel/bpf/verifier.c](https://github.com/torvalds/linux/blob/master/kernel/bpf/verifier.c)

Çünkü ilgili kod direkt olarak kernel space de çalışacaktır. Bu sebeple ilgili kodun herhangi bir döngüde kernel lockup durumuna düşürmemesi gerekmekte ve bazı güvenlik endişelerini barındırmaması gerekmektedir. 

![Untitled](images/ebpfschema.png)

Linux sistemler üzerinde **kernel.unprivileged_bpf_disabled** ayarı (sysctl) yetkisiz kullanıcıların, eBPF programlarını çalıştırıp çalıştıramayacağını kontrol eder. 

Tamam hadi eBPF programımızı yazdık her şey güzel ama bizim bu programları birbiriyle iletişim kurdurmamız gerekirse ne olacak diyebilirsiniz. Bunun için eBPF’de **Maps** denilen kavram vardır. Basit olarak key/value şeklinde bir veri yapısına sahip olmakla birlikte programların birbiriyle etkileşime girmesine izin verir. eBPF Maps **BPF_MAP_CREATE** sistem çağrısıyla oluşturulup **BPF_MAP_UPDATE_ELEM**

komutuyla güncellenir. Yani maps’lerle ilgili sistem çağrılarına **BPF_MAP_* ** ile bakabilirsiniz. 

Buradan yararlanabilirsiniz: [https://prototype-kernel.readthedocs.io/en/latest/bpf/ebpf_maps.html](https://prototype-kernel.readthedocs.io/en/latest/bpf/ebpf_maps.html)

![Untitled](images/ebpf.png)

Yukarıdaki görsel de zaten eBPF’i ana hatlarıyla göstermektedir. En üst kısımda use-caseslarımız yeterince açıklayıcıdır umarım. 

**Ekstra not**: Sitenin ismini tam olarak hatırlamıyorum fakat, site önünde bulunan load-balancer yapısını eBPF based bir load balancer’a geçiren yönetim sistemin data çıkışında 2x bir artış, CPU kullanımında ise 72x bir düşüş görmüş. Bu neden önemli? Eğer bir cloud provider ile çalışıyorsanız ve hesaplama başına ücret ödüyorsanız bu size mükemmel bir geri dönüş sağlayacaktır. Örnek bir load balancer olarak Open Source Katran incelenebilir.

## eBPF ile Python

Çok fazla efektif olmasa da aslında Python için bir wrapper bulunmaktadır. Temel bPF ile ilgili işlemleri yine **C** ile yapıp geri kalan işlemleri örneğin stringleri işlemek veya işleme tabi tutmak gibi kısımlar sadece Python ile yapılabilmektedir. Aşağıda bir kod bloğu örneği koyacağım bu kod bloğu örneğine veya daha fazlasına erişebileceğiniz linki de kod bloğunun altına ekleyeceğim. 

Modül ismi: python3-bpfcc fakat genel olarak kurmak isterseniz debian sistemlerde **sudo apt-get install bpfcc-tools linux-headers-$(uname -r)**

Aşağıdaki kod bloğu TCP IPv4 bağlantılarını trace etmek amacıyla yazılmıştır (Help textten okuyorum :) ) . İlgili kod bloğunda göreceğiniz üzere **bpf_text** altında C kodumuz bulunuyor. Daha sonra ilgili kod **b = BPF(text=bpf_text)** ile initialize ediliyor. Burada **text** yerine isterseniz **file** diyerek bir C dosyasının konumunun verebilirsiniz. Geriye kalan **string** işlemlerinde **b** değişkeninin **b.trace_fields()** fonksiyonu kullanılıyor. Bundan sonra yapacaklarınızı tamamen pure python ile yapabiliyorsunuz. 

```python
#!/usr/bin/python
#
# disksnoop.py	Trace block device I/O: basic version of iosnoop.
#		For Linux, uses BCC, eBPF. Embedded C.
#
# Written as a basic example of tracing latency.
#
# Copyright (c) 2015 Brendan Gregg.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# 11-Aug-2015	Brendan Gregg	Created this.

from __future__ import print_function
from bcc import BPF
from bcc.utils import printb

REQ_WRITE = 1		# from include/linux/blk_types.h

# load BPF program
b = BPF(text="""
#include <uapi/linux/ptrace.h>
#include <linux/blk-mq.h>

BPF_HASH(start, struct request *);

void trace_start(struct pt_regs *ctx, struct request *req) {
	// stash start timestamp by request ptr
	u64 ts = bpf_ktime_get_ns();

	start.update(&req, &ts);
}

void trace_completion(struct pt_regs *ctx, struct request *req) {
	u64 *tsp, delta;

	tsp = start.lookup(&req);
	if (tsp != 0) {
		delta = bpf_ktime_get_ns() - *tsp;
		bpf_trace_printk("%d %x %d\\n", req->__data_len,
		    req->cmd_flags, delta / 1000);
		start.delete(&req);
	}
}
""")

if BPF.get_kprobe_functions(b'blk_start_request'):
        b.attach_kprobe(event="blk_start_request", fn_name="trace_start")
b.attach_kprobe(event="blk_mq_start_request", fn_name="trace_start")
if BPF.get_kprobe_functions(b'__blk_account_io_done'):
    b.attach_kprobe(event="__blk_account_io_done", fn_name="trace_completion")
else:
    b.attach_kprobe(event="blk_account_io_done", fn_name="trace_completion")

# header
print("%-18s %-2s %-7s %8s" % ("TIME(s)", "T", "BYTES", "LAT(ms)"))

# format output
while 1:
	try:
		(task, pid, cpu, flags, ts, msg) = b.trace_fields()
		(bytes_s, bflags_s, us_s) = msg.split()

		if int(bflags_s, 16) & REQ_WRITE:
			type_s = b"W"
		elif bytes_s == "0":	# see blk_fill_rwbs() for logic
			type_s = b"M"
		else:
			type_s = b"R"
		ms = float(int(us_s, 10)) / 1000

		printb(b"%-18.9f %-2s %-7s %8.2f" % (ts, type_s, bytes_s, ms))
	except KeyboardInterrupt:
		exit()
```

Diğer örnekler için: [https://github.com/iovisor/bcc/tree/master/examples](https://github.com/iovisor/bcc/tree/master/examples)

![Untitled](images/disknoop.png)


Örnekler üzerinden ilerleyerek ufkunuzu daha da genişletebilirsiniz fakat bu kısımda önemli bir vurgu yapmak istiyorum. Bazı örnekleri eğer çalıştıramazsanız bu genelde kernel ve bcc-tools uyumsuzluğundan kaynaklanıyor olabilir. Bunun için bpfcc-tools'u baştan derlemeniz gerekiyor. Aşağıdaki bunun için bir cheatsheet şeklinde kod bloğu paylaşıyorum.


```sh
apt purge bpfcc-tools libbpfcc python3-bpfcc
wget https://github.com/iovisor/bcc/releases/download/v0.25.0/bcc-src-with-submodule.tar.gz
tar xf bcc-src-with-submodule.tar.gz
cd bcc/
apt install -y python-is-python3
apt install -y bison build-essential cmake flex git libedit-dev   libllvm11 llvm-11-dev libclang-11-dev zlib1g-dev libelf-dev libfl-dev python3-distutils
apt install -y checkinstall
mkdir build
cd build/
cmake -DCMAKE_INSTALL_PREFIX=/usr -DPYTHON_CMD=python3 ..
make
checkinstall
```




## eBPF’e Farklı Açılardan Bakmak:

1. [https://github.com/citronneur/pamspy](https://github.com/citronneur/pamspy)
2. [https://doublepulsar.com/bpfdoor-an-active-chinese-global-surveillance-tool-54b078f1a896](https://doublepulsar.com/bpfdoor-an-active-chinese-global-surveillance-tool-54b078f1a896)

## Yazı sonu

Genel hatlarıyla bahsettiğimi düşünüyorum zaten devam etmek isteyen aşağıdaki kaynaklardan devam edecektir. Bunu oku eBPF bitmiştir gibi bir amacım bulunmuyor. Yazı sonuna yine şarkımı iliştiriyorum. Umarım keyif almışsınızdır. 


[![Video](http://img.youtube.com/vi/KZg3CrPuuWI/0.jpg)](http://www.youtube.com/watch?v=KZg3CrPuuWI)


---

## Ekstra kaynaklar (Bunlara da bakarsanız iyi olur):

1. [https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-3490](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-3490)
2. Üstteki CVE’nin Root Cause’nu açıklayan yazı: [https://www.graplsecurity.com/post/kernel-pwning-with-ebpf-a-love-story](https://www.graplsecurity.com/post/kernel-pwning-with-ebpf-a-love-story)
3. [https://github.com/chompie1337/Linux_LPE_eBPF_CVE-2021-3490](https://github.com/chompie1337/Linux_LPE_eBPF_CVE-2021-3490)
4. [https://ebpf.io/](https://ebpf.io/)
5. [https://stackoverflow.com/questions/tagged/ebpf+or+bpf+or+xdp-bpf](https://stackoverflow.com/questions/tagged/ebpf+or+bpf+or+xdp-bpf)
6. [https://github.com/isovalent/eCHO](https://github.com/isovalent/eCHO)
7. **[https://qmonnet.github.io/whirl-offload/2016/09/01/dive-into-bpf/](https://qmonnet.github.io/whirl-offload/2016/09/01/dive-into-bpf/)**
8. **[https://github.com/iovisor/bpf-docs/](https://github.com/iovisor/bpf-docs/)**
9. [https://twitter.com/krisnova](https://twitter.com/krisnova)
10. [https://www.containiq.com/](https://www.containiq.com/)

---

## Referanslar:

1. [https://en.wikipedia.org/wiki/Memory_management](https://en.wikipedia.org/wiki/Memory_management)
2. [https://en.wikipedia.org/wiki/User_space_and_kernel_space](https://en.wikipedia.org/wiki/User_space_and_kernel_space)
3. [https://en.wikipedia.org/wiki/Protection_ring](https://en.wikipedia.org/wiki/Protection_ring)
4. [https://amslaurea.unibo.it/19622/1/berkeleypacketfilter_distefano.pdf](https://amslaurea.unibo.it/19622/1/berkeleypacketfilter_distefano.pdf)
5. [https://www.kernel.org/doc/html/latest/networking/filter.html](https://www.kernel.org/doc/html/latest/networking/filter.html)
6. [https://illumos.org/books/dtrace/chp-intro.html](https://illumos.org/books/dtrace/chp-intro.html)
