Title:Python ile basit vulnhub yazarlarını çeken bot
Date: 2016-06-17 10:20
Tags: python, requests, parser, lxml,vulnhub
Category: python
Slug: python-vulnhub-author-scraper
Author: 0x656e

Daha önceden yazmış olduğum bu scripti bugün güncellemek zorunda kaldım.Nedeni vulnhub önceden her türlü bağlantıyı kabul etsede bugün etmiyordu.Bende scripte Chrome Dev Tools'dan kopyaladığım header bilgilerini çaktım script şimdi bağlantı kuruyordu fakat regex patterni boş olarak dönüyordu.İlk scriptte
```
urllib.request.urlopen(url).read()
```

şeklinde bir yapı vardı ve bu yapı response'u byte code olarak döndürüyordu.Byte code döndüren response içinde regex ile arama yapmak için basit bir harf argüman var hemen onu da göstereyim.

```
rp = re.findall(b'pattern',text)
```

şeklinde bir argüman ile bytecode olarak arama yapıyor fakat bu debug yaparken sorun nerde ? veya pattern neden bulmuyor şeklinde ki sorunlarınızı çözerken zorluk çıkartıyordu.Bende kodu bu yüzden güncelledim.

urllib yerine artık requests kullanıyorum.(Respect david beazley)

Neyse lafı fazla uzatmayalım. Sonuç görüntüsü aşağıdadır.

![Vulnhub](images/vulnhub.png  "Vulnhub")

### Kodlar 

```
#!/usr/bin/python3
import requests,re
headers = {
':authority':'www.vulnhub.com',
':method':'GET',
#':path':'/?page=1'
':scheme':'https',
'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'accept-encoding':'gzip, deflate, sdch, br',
'accept-language':'tr,en;q=0.8',
'cache-control':'max-age=0'
,'cookie':'__cfduid=db8361564d5291910653bb1219526d1051468106057; cf_clearance=bba81bf5ad85eef7974fd7ffe76cc5c022a83ca1-1468752269-2592000; _ga=GA1.2.1086152234.1468106055'
,'upgrade-insecure-requests':'1',
'user-agent' :'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36' }
liste = []
linkler = []
def getir(x):
    url = 'https://www.vulnhub.com/?page=%s' %x
    linkler.append(url)
def yazartopla(x):
    print("Acılan link : "+x) #debug için eklemiştim

    ac = requests.get(x,headers=headers).text ## Siteyi get metodu ile çekiyoruz ve içindeki textleri alıyoruz

    ac = re.findall('\/author\/(.*)\/',ac) # Text içinden /author/Arasındaki herşeyi alıyoruz/

    for i in ac:  # Tüm sayfadan arayıp liste şeklinde bir sonuç döndüğü için for döngüsüne sokup tek tek listeye ekliyoruz.

        if i in liste:
            pass
        else:
            liste.append(i)



def git(i):
    try: ### Hata yakalama blokları

        url = "https://www.vulnhub.com/author/"+i+"/"
        ac = requests.get(url,headers=headers).text

        name = re.findall('<li><b>Name<\/b>:(.*)<\/li>',ac)
        website = re.findall('<li><b>Website.*<a href="(.*)">',ac)
        contact = re.findall('<li><b>.*<\/b>: <a href=\"(.*)\">.*<\/a><\/li>',ac)
        series = re.findall('<a href="\/series\/.*\/">(.*)<\/a>',ac)
        if len(contact) == 2:

            author = {"İsim" : name,"Websitesi" : website,"İletişim" : contact[1],"Seriler" : series}
            dosyayaz(author)
        elif len(name) == 0:
            pass

        else:
            author = {"İsim" : name,"Websitesi" : website,"İletişim" : contact,"Seriler" : series}

            dosyayaz(author)
    except urllib.error.HTTPError: ## Eğer herhangi bir şekilde ulaşamazsa sayfaya hata var diye uyarı veriyor.Nedense break etmemişim
        print('Hata var')
def dosyayaz(x):
    x = str(x)
    ac = open('yazarlar.txt',mode="a")
    ac.write(x+"\n")
    ac.close()

for i in range(1,16):
    getir(i)

for i in linkler:
    yazartopla(i)

for i in liste:
    i = i
    git(i)

```
