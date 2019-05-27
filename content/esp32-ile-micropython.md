Title: ESP32 üzerinde Python yazmak - Micropython 
Date: 2019-05-27 12:00
Tags: esp32 türkçe, micropython türkçe, esp32 micropython türkçe, esp32 ile micropython kullanmak, python ve elektronik, elektronik aletlerde python yazmak, 
Category: iot & elektronik
Slug: esp32-ile-micropython
Authors: 0x656e





ESP32 ile nasıl çalışacağımıza ve cihaza hali hazırda daha önceki bir blog konusunda değinmiştik. 



İlgili yazı linki: [ESP32 İle Çalışmak](https://enesergun.net/esp32-ile-calismak.html)



Yukarıda linkini vermiş olduğum yazıda ESP-IDF ve pip ile birlikte kurduğumuz ESPTool kullanıyorduk. İnternet üzerindeki bir çok elektronik konulu blog yazılarını incelediğinizde elektronik cihazlara ait kodlamaların genellikle C ile yazıldığını görebilirsiniz. C bilmeyen birisi için(Örn:Ben) projeyi ilerlettikçe bu oldukça içinden çıkılamaz bir durum halini alabiliyor. İşte bu sebepledir ki bazı arkadaşlarımız elektronik cihazlar üzerinde Python yazabilmemize olanak sağlayan bir dil yazmışlar. Kendileri bu dili yine C ile yazmış olup ismine de **MicroPython** ismini vermişler.

![](images/micropython1.png)

## MicroPython Nedir?



Kendileri ESP32 veya diğer boardlar üzerinde Python(Python'a benzer kod) kodu yazmamızı sağlayan bir dil. İçerisinde implente olmuş bir biçimde Python 3.4 kullanıyor fakat normal bir Python'a göre farklılıkları da bulunmuyor değil. 

İlgili farklılıklara ulaşmak için: [MicroPython differences from CPython](http://docs.micropython.org/en/latest/genrst/index.html)

MicroPython'ın desteklemiş olduğu boardlar: 

* Micro:bit
* ESP8266
* ESP32
* Pyboard D-Series
* WiPy ve CC3200
* MicroPython pyboard

## MicroPython'ı ESP32'ye Nasıl Yükleriz?

Bunun için aslında çok fazla bir ihtiyacımız bulunmamaktadır. MicroPython'ı yüklemek için "bin" dosyasını flashlamamız yeterli.

Cihazınıza uygun firmware'i indirmek için : [MicroPython Firmware for ESP32](https://micropython.org/download#esp32)

Yukarıda verilmiş link üzerinden en son sürüm "bin" dosyasını indirmeniz gerekmektedir. İndirdikten sonra aşağıda verilmiş olan komut ile **"Linux"**  üzerinde bu işlemi yapabilirsiniz. Değiştirilmesi gereken parametreler komut  altında açıklanacaktır.

```bash
sudo esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 921600 write_flash -z 0x1000 esp32-20190526-v1.10-387-g1470184bd.bin
```

Değiştirilmesi gereken argümanlar/parametreler:

* esp32-20190526-v1.10-387-g1470184bd.bin
* 921600
  * İlgili değer baud değeridir. Bu değer saniye başı serial port üzerinden transfer edilebilecek bit sayısını belli etmektedir. flash atarken bu değerle yazdırdık, dinlerkende 115200 baud değerinde dinleme yapmamız gerekmektedir. 
* /dev/ttyUSB0
  * İlgili değer ise ESP32 cihazınızın hangi portundan bağlandığını göstermektedir.

## Yükledikten Sonra Nasıl Kod Yazacağız?

Şimdi her şeyi yükledik. Ama kodu nasıl yazacağız derseniz terminal'e aşağıdaki komutu yazmanız yeterlidir.

`screen /dev/ttyUSB1 115200` 

2 kere enter'a bastığınızda direkt olarak interactive prompt'a düşeceksinizdir. Örnek bir ekran görüntüsünü aşağıya ekliyor olacağım.

![Micropython Türkçe](images/micropython3.png)

![Micropython Türkçe](images/micropython4.png)



Eğer bu şekilde(REPL) kod yazmak hoşunuza gitmiyorsa yazdığınız kodu ampy(dilerseniz rshell) ile ESP32 Boardınıza yükleyebilirsiniz.

`sudo ampy --port /dev/ttyUSB0 put main.py` 

Ampy ile attığımız kod artık her boot edilişte otomatik olarak çalışacaktır.

Ben aşağıdaki kodu attım ve sürekli çalışmasını sonsuz bir while döngüsü ile sağladım. Eğer sıcaklık 30 derece üstüne çıkarsa bize haber verecektir. Ekran görüntüsünü de aşağıda gösteriyor olacağım.

```python
import dht
import machine
d = dht.DHT11(machine.Pin(32))
while True:
    temp = d.temperature()
    if temp > 30:
        print("Çok sıcak acil durum olarak API bilgi gönderildi")
        break
    else:
        print("Oda sıcaklığındayız mükemmel")

```

![Micropython Türkçe](images/micropython5.png)



Bu yazı şimdilik bu kadar. Belki ileride (üşenmezsem) ESP32 üzerinden sürekli olarak sıcaklık değerlerini ağda bulunan bir API'a alarak onun veri görselleştirmesini yapabiliriz veya bir sunucu odasında olduğumuzu düşünüp belirli bir sıcaklık üstüne çıktığında farklı bir porttan veri göndermesini sağlayabiliriz.



Okuduğunuz için teşekkür ederim. Yine bir klasik olarak şarkı paylaşacağım fakat bu sefer yine 2 tane paylaşacağım.

[![Nothing burns like the 
cold](http://img.youtube.com/vi/5hNT2wtVIBI/0.jpg)](http://www.youtube.com/watch?v=5hNT2wtVIBI
"Nothing burns like the cold")

[![Biig Piig 
Perdida](http://img.youtube.com/vi/1gdihQ_cnfQ/0.jpg)](http://www.youtube.com/watch?v=1gdihQ_cnfQ
"Biig Piig Perdida")