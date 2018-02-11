Title: Neymiş bu Vagrant
Date: 2018-01-6 22:14
Tags: vagrant, vagrant 101, introduction of vagrant, vagrant dersleri, vagrant nedir
Category: vagrant
Slug: vagrant-nedir
Authors: 0x656e




### Kısaca Vagrant Nedir?
Kendi anladığım şekilde anlatmam gerekirse Vagrant hazırladığınız text scriptleri ile sanal sunucular oluşturabileceğiniz otomatize bir araçtır. 

### Ne İşe Yarar?

Oluşturduğunuz scriptler ile herhangi bir ortamda (Müşteri ortamı vs.) sizler için hazır bir makine inşa eder. Tabi bir de [ansible](https://ka1nsha.github.io/ansible-nginx.html) ile birleştirirseniz tadından yenmez sanırım. Tabi ki bunda özgürsünüz projenizin içerisinde ki bir sh dosyasını da çalıştırabilirsiniz.


### Birkaç Terim

** Provider ** : Sisteminizin hangi sanallaştırma platformu üzerinde çalıştırılacağını belirtir. Örn: Virtualbox, Vmware, Docker

** Box ** : Binlerce kullanıcı tarafından oluşturulmuş özel kutulardır. Bu kutuları scriptiniz içerisine yazarsanız Vagrant bunu sizin için indirir ve script içerisinde belirttiğiniz özellikler üzerinden çalışmasını sağlar. Örnek vermek gerekirse pfsense box'ını indirirseniz sizlere nur topu gibi bir pfsense makinesi verecektir.

** Provision ** : Sistem kurulduktan sonra çalıştırılacak script vs şeyleri yazdığımız yer ( en azından benim anladığım :D )

### Next, Next, Next

Debian based sistemler üzerinde

```bash
apt install vagrant
```

Tabi ki sadece **vagrant** kurmak yetmeyecektir. Kullanacağınız provider'ı da sisteminize indirmeniz gerekmektedir. Ben **virtualbox** kullanacağım.

### Hadi Başlayalım.

Projeyi oluşturacağınız klasöre gittiğinizde burada vagrant init yaparsanız sizin için bir *__vagrantfile__* oluşacaktır.
İçerisini temizleyerek aşağıda ki satırları ekleyelim.

```bash
Vagrant.configure(2) do |config|
        config.vm.define "nebuvagrantya" do |nbv|
        nbv.vm.box = "ubuntu/trusty64"
        nbv.vm.network :private_network, ip: "10.0.0.2"
        nbv.vm.hostname = "nebuvagrantya"
```

Burada ki kodları açıklamak gerekirse Vagrant.configure(2) do **|config|** yazdığımızda kalın yazdığım kısım aslında bir değişken olarak davranıyor.

Altında Vagrant üzerinde bir makine açacağımızı ve bunu kısaltma olarak nbv olarak çağıracağımızı belirtiyoruz. ( nbv )

Diğer satırlarda bu makinemizin ubuntu kutusunu kullanacağını belirtiyoruz. Bu kutunun hangi ip alacağını ve private networkde olacağını belirtiyoruz. Ayrıca bu makinenin Virtualbox üzerinde ki ismini de belirtmiş oluyoruz. Fakat bu bize yetiyor mu tabi ki yetmiyor. Hadi biraz daha sanal makinemizin ayarları ile oynayalım.

Projemize provider olarak **virtualbox** ekleyelim. 


```bash

Vagrant.configure(2) do |config|
	config.vm.define "nebuvagrantya" do |nbv|
	nbv.vm.box = "ubuntu/trusty64"
	nbv.vm.network :private_network, ip: "10.0.0.2"
	nbv.vm.hostname = "nebuvagrantya"

	nbv.vm.provider "virtualbox" do |vb|
		vb.name = "Ne bu vagrant ya"
		vb.name =  "Ne bu vagrant ya"
		vb.memory = "512"
		vb.cpus = "2"
		vb.customize ["modifyvm", :id, "--vram", "32"]
		end


```

Burada VBoxmanage kullanarak sanal makinemizin ismini, ram miktarını, ekran kartı ram miktarını ve işlemci sayısını belirttik. Ayrıca provision kısmında shell üzerinde proje klasörümüzde bulunan **nginxyukle.sh** dosyasını çalıştıracağız.
İsterseniz provisioning kısmında isterseniz direkt olarak ansible çalıştırabilirsiniz.

Örnek kod:
```bash
    vb.vm.provision "ansible" do |ansible|
        ansible.playbook = "nginxyukle.yml"
        ansible.verbose = "v"
end
```
Sanal makinenizin çok daha fazla ayarını değiştirmek isterseniz eğer aşağıya referans sayfasını ekleyeceğim.

Vagrant dosyamızın son hali 
```bash
Vagrant.configure(2) do |config|
	config.vm.define "nebuvagrantya" do |nbv|
	nbv.vm.box = "ubuntu/trusty64"
	nbv.vm.network :private_network, ip: "10.0.0.2"
	nbv.vm.hostname = "nebuvagrantya"

	nbv.vm.provider "virtualbox" do |vb|
		vb.name = "Ne bu vagrant ya"
		vb.name =  "Ne bu vagrant ya"
		vb.memory = "512"
		vb.cpus = "2"
		vb.customize ["modifyvm", :id, "--vram", "32"]
		end
	nbv.vm.provision :shell, path: "nginxyukle.sh"
		end
		end


```

Hadi çalıştıralım artık.
Terminalinize 
```bash
vagrant up
```

Yazarsanız eğer daha önce aynı box'ı indirmemişseniz aşağıda ki gibi bir ekran göreceksiniz.

**Not:** Nginxyukle.sh dosyanızı oluşturmayı unutmayın :)
![Vagrant1](images/vagrant1.png) 


İşlemler bittikten sonra aşağıda ki gibi bir ekran göreceksiniz

![Vagrant2](images/vagrant2.png)



Artık herşey hazır.

Kullanabileceğiniz komutlar:

| Komut | Açıklama |
| --- | -- |
| vagrant ssh | Eğer bir tane makineniz bulunuyorsa bu makineye direkt olarak ssh üzerinden erişir. |
| vagrant destroy | Makinenizi destroy eder. |
| vagrant global-status | Makineleriniz hakkında sizlere bilgi verir. |
| vagrant reload | Makinenizi update eder |

Komutlar ile ilgili aşağıda referans sayfası vereceğim.
SSH bağlantısı yapalım ve yazıyı sonlandıralım.
![Vagrant3](images/vagrant3.png)

Evet artık nur topu gibi bir sanal makinemiz var.
![Vagrant4](images/vagrant4.png)

### Vagrant Kutuları İçin ###

Vagrant üzerinde kutuları kullanabileceğinizi söylemiştik.
Kullanıcılar tarafından oluşturulmuş public kutulara ulaşmak için aşağıda ki linki kullanabilirsiniz.

[Vagrant Boxes](https://app.vagrantup.com/boxes/search)


##### Ek Linkler ####
[Vagrant CheatSheet](https://2rwky424s9rd179jmbzqsca1-wpengine.netdna-ssl.com/wp-content/uploads/2017/12/vagrant-printerfriendly.png)

[VBoxManage](https://www.virtualbox.org/manual/ch08.html)

[Vagrant CLI](https://www.vagrantup.com/docs/cli/)

[Complex VagrantFile](https://everythingshouldbevirtual.com/virtualization/vagrant-complex-vagrantfile-configurations/)



