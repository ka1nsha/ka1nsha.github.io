Title: Flask ile Adım Adım Etkinlik Uygulaması Yapalım
Date: 2018-02-13 22:19
Tags: flask event app, flask sqlalchemy, sqlalchemy, flask mvc, flask
Category: flask
Slug: flask-events-app
Authors: 0x656e



## Flask ile Adım Adım Etkinlik APP'i Yapalım

Selamlar arkadaşlar, birkaç yazı yazmak istedim hem bu arada belki bazı arkadaşların isteklerini de yerine getirmiş olurum. Amacım bu yazı serisinde Flask ile basit bir etkinlik uygulaması yapmak. Bunun için adım adım gideceğim, yazı serisinin en sonunda Bootstrap ile bir arayüz yazacağız. Sanırım en uzun yazımız da bu olacak. Neyse bu yazımızda database üzerinde modelleri oluşturacağız. Elimden geldiğince açıklayıcı olmaya çalıştım iyi okumalar dilerim.



### Flask Nedir?

Flask bir hayat biçi.... :)

Flask bir Python frameworküdür. Tabi genelde en fazla Django bilinir. Django gerçekten her şeyiyle tam bir web frameworkdür fakat bazen bazı işleriniz için daha minimal frameworkler isteyebilirsiniz işte bu gibi durumlar için micro frameworkler ortaya çıkmaktadır. Flask ise micro frameworkdür. Hızlıca kod yazarak prototipleme yapabilirsiniz üstelik bunları MVC  yazılım mimarisi ile yapabiliyorsunuz. Flask'i kurmak için

terminalinize:

```bash
pip install flask
```

yazmanız yeterlidir. Ben bu yazıda ve projede SQLite kullanacağım. Siz dilerseniz PostgreSQL veya başka bir DBMS kullanabilirsiniz. Tabi ki SQLite ile birlikte SQLAlchemy kullanmaktan da çekinmeyeceğim. Ben aşağıda ki gibi bir database şeması düşündüm.



![](image/dbschema.png)



### Let's go

Proje klasörünüzü oluşturduğunuzu varsayıyorum. Proje klasörünü oluşturduktan sonra modelleri yazacağımız bir models.py dosyası oluşturalım. Routingleri main.py dosyasında yapacağız.



models.py:

```python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///events.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
```



Şimdi burada ne yaptığımızı anlatayım. Python dosyamıza Flask modülünü kullanacağımızı söyleyerek import ettik. Daha sonra SQLALchemy'i kullanabilmek için Flask_SQLAlchemy modülünü de import ettik. Burada ben direkt olarak pure SQLAlchemy kullanmadım, flask için yazılmış olanını kullandım. Eğer direkt pure SQLAlchemy kullansaydım database kısmında declarative_base ve session fonksiyonlarını kullanmak zorunda kalacaktım. Bu şekilde bana daha kolay geliyor.

App değişkeninde Flask ile bir uygulama başlatıyoruz ve bu Flask uygulamasının adını __name__ veriyoruz. __app.config__ kısmında ise _SQLALCHEMY_DATABASE_URI_ kısmında database'imizin **connection_uri** 'sini yazıyoruz. Bu DBMS'inize göre değişmektedir. PostgreSQL için örn: 

```python3
postgresql://kullaniciadi:password@ip:port/databasename
```



Aşağıda da değişikliklerin takip edilmesini False olarak veriyoruz.



### Hadi artık modellerimizi yazalım

Burada direk olarak kodları aşağıya koyacağım, kod bloğunun altına ise açıklamalarını gireceğim.

```python
class events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.Text(50),nullable=False)
    slug = db.Column(db.Text,nullable=False)
    organizator = db.Column(db.Integer,db.ForeignKey('organization.id'))

class organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.Text(50),nullable=False,unique=True)
    organization_desc = db.Column(db.Text(500),nullable=False)
    organization_img = db.Column(db.Text)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usermail = db.Column(db.Text,unique=True,nullable=False)
    password = db.Column(db.Text,nullable=False)
class eventspeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer,db.ForeignKey('events.id'))
    users_id = db.Column(db.Integer,db.ForeignKey('users.id'))
```

Kod bloğunda ki her class database üzerinde bir tablodur ve Flask üzerinde her biri bir Modeldir. Hepsinin zaten database modeli olduğunu class tanımlarken belirttik.

Burada özel değerler göreceksiniz. Bunlar:

**primary_key** : Database'e eklenen her öğenin bir ID'ye sahip olmasını ve bu ID'nın unique(eşsiz) olmasını sağlar. Otomatik artan bir biçimdedir. Otomatik artmanın terimsel ismi _Auto increment_' dır. 

**nullable**: Burada False verilmiş bu değer, veri eklerken buranın asla boş olamayağını belirtir. Kişiyi buna zorlar.

**unique**: Bu değerimiz ise alacağı değeri database içerisinde arar eğer var ise bu kayıt işlemini kabul etmez. Yani kayıt edilecek her şeyin eşsiz olmasını ister. Bknz: Kullanıcı Adları, Emailler.

**db.Column**: Bu fonksiyonun aldığı değerlerin bir sütun olduğunu gösteriyor. 

**db.Integer**: Bu fonksiyon ise bu sütunun değerlerinin sadece Integer yani sayma sayısı olacağını söylüyor.

**db.Text(500)**: Bu fonksiyon ise bu sütunun değerlerinin text olacağını ( aslında herşeyi kabul edebileceğini ) gösteriyor. Yanına yazılan 500 rakamı ise o sütunun maksimum değerinin 500 olabileceğini belirtir.

**db.ForeignKey()** : Bu fonksiyon aslında tablolar arası ilişki kurmaya yarar terimsel anlamı Relationdır. Bir çok türü vardır. Bunlardan bir kaçı : Foreign Key, ManyToMany, OneToMany . Bu sütuna gelecek değerin aslında diğer bir tabloda ki başka bir veriyi işaret ettiğini belirtir.

Sanırım bu kodda açıklayabileceklerim bu kadar, şimdi sıra geldi database'i oluşturmaya. Kodumuzun en altına 

```python
db.create_all()
```

yazarak kodu çalıştırırsanız artık database'iniz oluşturulacak ve işlem yapmaya hazır hale gelecektir.

![](image/database.png)

