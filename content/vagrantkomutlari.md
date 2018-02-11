Title: Vagrant Komutları ( Cheatsheet )
Date: 2018-01-08 23:12
Tags: vagrant for beginners , vagrant cheatsheet, vagrant commands , vagrant all commands
Category: vagrant
Slug: vagrant-komutlari
Author: 0x656e



## Vagrant Komutları

Selamlar, geçtiğimiz hafta Vagrant ile ilgili bir blog post yayınlamıştım hatırlarsanız. Biraz daha üzerine gitmek istedim. Bu yazıda Vagrant komutlarının kısa açıklamalarına değineceğim.

Sayfayı print ederek elinize güzel bir döküman geçmesini amaçlamaktayım.


| Komut | Açıklama | Ek Alan |
| --- | --- | --- |
| vagrant box | Bir ana fonksiyondur kutuları kontrol etmenizi sağlar. | 
| vagrant box add | Vagrantınıza kutu eklemeye yarar. | Detaylı açıklama 1.1 Nolu başlıktadır.|
| vagrant box list | İndirmiş olduğunuz veya eklemiş olduğunuz kutuların listesinin çıktısını verir. | 
| vagrant box outdated | Kutularınızın güncelliğini kontrol eder. Eğer --global parametresini verirseniz tüm kutularınızı kontrol eder| 
| vagrant box prune | Eski versiyon kutularınızı siler. | Detaylı açıklama 1.2 Nolu başlıktadır. |
|vagrant box remove | Ismını verdiğiniz kutuyu siler. | Detaylı açıklama 1.3 Nolu başlıktadır. |
| vagrant box repackage | Isım,Provider,Version değerlerini alarak kutunuzu yeniden paketler. | 
| vagrant box update | box parametresi ile kutunuzu günceller. | provider parametresini de alabilmektedir. |
| vagrant connect | Public olarak paylaşılmış bir sanal makinenize bağlanmanızı sağlar. | Detaylı açıklama 1.4 Nolu başlıktadır. |
| vagrant destroy | Vereceğiniz isim veya id'ye sahip sanal makinenizi siler. | 
| vagrant global-status | Çalışma ortamınızda çalışan tüm sanal makineler hakkında bilgi verir. | Sadece vagrant tarafından ayaklandırılmış sunucuları/bilgisayarları kapsar. |
| vagrant halt | Vereceğiniz isim veya id'ye sahip sanal makinenizi kapatır.( shutdown ) |
| vagrant init | Eğer bir vagrantFile'ınız yoksa bulunduğunuz konumda örnek bir vagrantFile oluşturur. | Bir isim ve URL verirseniz URL'de ki kutuya ait örnek bir dosya oluşturur. Örnek komut: vagrant init [ubuntu/precise64 [url]] |
| vagrant login | Vagrant Cloud'a bağlanmanızı sağlar. | Eğer gizli kutularınız bulunuyorsa gerekir. |
| vagrant package | Vereceğiniz isim veya id'ye sahip sanal makinenizi bir kutuya paketler |
| vagrant plugin | Ana fonksiyondur pluginleri kontrol etmenizi sağlar |
| vagrant plugin expunge | Bütün pluginleri bağımlılıkları kaldırabilmenizi sağlar. | 
| vagrant plugin install {} | Ismını verdiğiniz plugini kurar. |
| vagrant plugin list | Yüklemiş olduğunuz pluginleri listeler | 
| vagrant plugin repair | plugins.json içerisinde ki  otomatik onarmaya çalışır | Eğer onarma işe yaramaz ise expunge komutuna --reinstall parametresi vererek deneyiniz.  |
| vagrant plugin uninstall {}| Ismını vermiş olduğunuz plugini siler. |
| vagrant plugin update {} | Ismını vermiş olduğunuz plugini günceller. |
| vagrant port {} | Ismını veya id'sini vermiş olduğunuz makinenizin açık portlarını gösterir |
| vagrant powershell |  Eğer sanal sunucunuz powershell'i destekliyorsa PowerShell ekranını açar |
| vagrant provision | Ismını vereceğiniz sanal sunucu üzerinde provision kısmında ki değişiklikleri hızlıca yapmanızı sağlar |
| vagrant rdp | Eğer sanal sunucunuz Uzak Masaüstü bağlantısı destekliyorsa, Uzak Masaüstü bağlantısını açar.
| vagrant reload |  Vagrantfile'ınızda yaptığınız değişiklikleri uygular | 
| vagrant resume | Suspend edilmiş sanal sunucunuzu çalışır hale getirir | 
| vagrant share | Sanal sunucunuzu paylaşmanızı sağlar. | Detaylar 1.5 Nolu başlıktadır.
| vagrant snapshot | Vagrant üzerinden snapshot(anlık imaj) almanızı olanak veren ana fonksiyondur. |
| vagrant snapshot delete | Ismını vereceğiniz anlık imajı siler. |
| vagrant snapshot restore | Ismını vermiş olduğunuz sanal sunucunuzu ismini vermiş olduğunuz anlık imaja geri döndürür. |
| vagrant snapshot list | Alınmış olan anlık imajlarınızın listesini verir. |
| vagrant snapshot save | Ismını vermiş olduğunuz sanal sunucu üzerinde vermiş olduğunuz isimle bir anlık imaj alır. |
| vagrant ssh | Ismını vermiş olduğunuz sanal sunucunuza ssh üzerinden bağlanır. | -c parametresi ile direkt olarak kod çalıştırabilirsiniz. Örn: vagrant ssh -c echo "Selam naber?" | 
| vagrant ssh-config | Ismını veya id'sini vermiş olduğunuz makinenin ssh-configini sizlere verir. | Vagrant ssh kullanmak istemediğiniz durumlarda kullanılabilir. |
| vagrant status | Ismini veya id'sini vermiş olduğunuz makinenin durumunu döndürür. |
| vagrant suspend | Sanal sunucunuzu uyku moduna alır. | suspend edilen sunucunuza resume komutu iletirseniz kaldığınız yerden çalışmaya devam edecektir. |
| vagrant up | VagrantFile'ınıza göre sanal bir sunucu oluşturur ve bunu konfigure eder. |

## 1.1 Vagrant box add 
<pre>Vagrant public reposunda bulunan kutuların kısa isimlerini kabul etmektedir. Örn: ubuntu/precise64
Dosya yolu veya HTTP URL kabul etmektedir. HTTP/S desteği bulunmaktadır. HTTP üzerinden basic authentication desteklemektedir. 
URL üzerinden direkt olarak bir kutu eklenebilmektedir.</pre>

Ayrıca bu komutun alabileceği options parametleri vardır.
** --box-version {} ** : süslü parantezler arasına yazacağınız özel bir versionu indirecektir.

** --clean ** : Eğer bu komutu verirseniz daha önce eğer varsa önbelleğe alınmış verileri, yarım kalmış indirme işlemlerini siler ve yeniden indirmeye başlar. 

** --force ** : Aynı isimde bir kutunuz var ise bunu dikkate almadan üzerine yazar.

** --insecure ** : Hatalı SSL Sertifikalarını görmezden gelir.


### 1.1.1 Vagrant box add Dosya Kontrolü 

** --checksum {} ** : Dosya bütünlüğü kontrolü yapar.

** --checksum-type {Tip} ** : MD5, Sha1 veya Sha256 değerleri verilerek dosya bütünlüğü kontrolünü sağlamanıza olanak verir.

##1.2 Vagrant box prune 
Bu komutun da alabileceği parametreler vardır.

** --provider {} ** : Özel olarak belirttiğiniz provider'a ait kutuları siler.

** --dry-run ** : Silinebilecek kutuları yazdırır.

** --name {} ** : Özel olarak ismini belirttiğiniz kutuyu silecektir.

** --force ** : Hiç bir uyarıyı gözetmeksizin kutularınızı silecektir.

##1.3 Vagrant box remove

Bu komutun alabileceği parametreler aşağıda ki gibidir.

** --box-version {} ** : Sadece belirli versiyona sahip olan kutularınızı silebilirsiniz.

** --all **: Versiyona bakılmaksızın kutunuzu silecektir.

** --force **: Kutuyu kullanıyor olsanız bile silecektir.

** --provider {} ** : Belirli provider'a ait kutularınızı silecektir.

## 1.4 Vagrant connect 
Komutun alabileceği 3 parametre bulunmaktadır.

** --disable-static-ip ** : Vermiş olduğunuz static IP'yi iptal eder.

** --static-ip ** : Kutunuza Static IP atarsınız.

** --ssh ** : Eğer sanal makineniz sadece --ssh ile paylaşılmış ise bu kutuya bağlanmanızı sağlar.


## 1.5 Vagrant share 

Komutun alabileceği parametreler aşağıda ki gibidir.

** --disable-http ** : HTTP paylaşımınızı iptal eder.

** --HTTP {PORT} ** : Vermiş olduğunuz port üzerinden HTTP sunucusunu paylaşır. Eğer --disable-http yapılmışsa kullanmanız efektif değildir.

** --HTTPS ** : Yukarıda ki maddenin HTTPS için olanıdır.

** --ssh ** : SSH paylaşımını açar.

** --ssh-no-password ** : Bunu bilmiyorum.

** --ssh-once ** : Yalnızca 1 kerelik SSH bağlantısını açar.


Yazımız buraya kadardı. Başka bir yazı da görüşmek üzere esen kalın.