Title: Japronto Neymiş?
Date: 2018-05-1 16:12
Tags: japronto nedir?, introduction of japronto, python web server, python web framework
Category: python
Slug: japronto-neymis
Authors: 0x656e




Uvloop ve picohttpparser tabanlı çok hızlı, ölçeklendirilebilir, asenkron bir HTTP araç takımıdır. Yazan kişi böyle söylüyor en azından. Eğer benchmark grafikleri de doğruysa ben bundan sonra bunu kullanırım.





Hemen grafiği aşağıya iliştiriyorum. 

#### Performans

![Performans](https://github.com/squeaky-pl/japronto/raw/master/benchmarks/results.png)



Bu grafikte yüksek olan iyi demektir. Bu benchmark AWS c4.2xlarge makinesinde yapılmış. Yük testinde 

[wrk]: https://github.com/wg/wrk	"wrk"

 adlı toolu 1 çekirdek 100 bağlantı ve bağlantı başına 24 istek konfigürasyonu ile kullanmışlar.

İlgili testte kullanılan kod örneklerine erişmek isterseniz:

[Benchmarks](https://github.com/squeaky-pl/japronto/tree/master/benchmarks)



#### Basit Bir Web Uygulaması



En basit halde bir web uygulaması yazabilmek için:

```python
from japronto import Application


def hello(request):
    return request.Response(text='Hello world!')


app = Application()
app.router.add_route('/', hello)
app.run(debug=True)
```

#### Özellikler

HTTP 1.x Parçalı yüklemeleri destekliyor. ( Chunk Upload ) : [[Ayrıntı]](https://gist.github.com/CMCDragonkai/6bfade6431e9ffb7fe88)

HTTP pipelining'e tam destek veriyor. ( Aşağıda açıklayacağım )

Canlı bağlantıları yapılandırabilmeye olanak sağlıyor.

Asenkron ve Senkron çalışma biçimlerini destekliyor.

Bunu anlamadım: Master-multiworker model based on forking

Yönlendirmeler basit bir şekilde yapılabiliyor.

Kod değişikliği sonrası HTTP Serverın tekrar çalışıyor.





##### HTTP Pipelining Nedir?

Birden fazla get, head gibi taleplerin tek bir paket içerisinde sunucuya iletilmesi anlamına gelmektedir.

Aşağıda ki grafikte herşey açıkca belli oluyor.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/HTTP_pipelining2.svg/1200px-HTTP_pipelining2.svg.png)

#### Benim Yorumum



Grafiklerin doğruluğunu kabul edersek bence kesinlikle denenmesi gereken bir HTTP server. Fakat kompleks bir uygulama yazacaksanız bence bunu enine boyuna düşünmelisiniz. Çünkü burada uygulama içerisinde ki bir çok fonksiyonu elinizle yazmanız gerekecek. Bunun yerine Django, Flask gibi frameworkleri kullanmak şu aşamada bana daha mantıklı geliyor. Karşılaştırmamın hatalı olduğunu biliyorum sonuçta bu bir Framework değil bir HTTP Server.



İlgili Github Sayfası : [https://github.com/squeaky-pl/japronto](https://github.com/squeaky-pl/japronto)
