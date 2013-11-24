# panforte

Отладка XSL шаблонов с выводом последовательности применения шаблонов,
контекста к которому они применялись и профайлинга по времени.

В данный момент proof-of-concept.

Для работы потребуется lxml.

## Использование

`python lxml_debug.py XSL XML`

## Демо

```bash
git clone https://github.com/maizy/panforte.git
cd panforte/
python lxml_debug.py samples/simple-xsl-xslt1/pages/breakfast.xsl samples/data/food-menu.xml
```

Проверено на:
* python=2.6 + lxml=2.2.8
* python=2.7 + lxml=3.2.4
* python=2.7 + lxml=2.2.8

## TODO

См. [список в lxml_debug.py](lxml_debug.py).

## Лицензция

The MIT License
