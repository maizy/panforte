# panforte

Отладка XSL шаблонов с выводом последовательности применения шаблонов,
контекста к которому они применялись и профайлинга по времени.

В данный момент proof-of-concept.

Для работы потребуется lxml.

## Использование

`python lxml_debug.py XSL XML`

Или с exslt расширениями, аналогичным используемыми в HeadHunter:

`python lxml_debug.py XSL XML --hh-exslt`

Проверено на:
* python=2.6 + lxml=2.2.8
* python=2.7 + lxml=3.2.4
* python=2.7 + lxml=2.2.8

## TODO

См. [список в lxml_debug.py](lxml_debug.py).

## Лицензция

The MIT License


## Демо

```bash
git clone https://github.com/maizy/panforte.git
cd panforte/
python lxml_debug.py samples/simple-xsl-xslt1/pages/breakfast.xsl samples/data/food-menu.xml
```


Выдаёт такой отчёт:
```
======== XSL FILE ========
samples/simple-xsl-xslt1/pages/breakfast.xsl
======== DATA FILE ========
samples/data/food-menu.xml
======== preprocessed root xsl ========
> processing /Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/item.xsl
> processing /Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/description.xsl
> processing /Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/description-tag.xsl
> processing /Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/calories.xsl
> reuse /Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/description-tag.xsl
======== RESULTS ========
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:pn="https://github.com/maizy/panforte">
  <body>
    <h1>Breakfast</h1>
    <h3>Belgian Waffles</h3>
    <span style="color: gray;">$5.95</span>
    <br/>
    <div class="description">Two of our famous Belgian Waffles with plenty of real maple syrup</div>
    <br/>
    <span style="color: orange;">650</span>
    <br/>
    <h3>Strawberry Belgian Waffles</h3>
    <span style="color: gray;">$7.95</span>
    <br/>
    <div class="description">Light Belgian waffles covered with strawberries and whipped cream</div>
    <br/>
    <span style="color: red;">900</span>
    <br/>
    <h3>Русский текст</h3>
    <span style="color: gray;">$8.95</span>
    <br/>
    <div class="description">Light Belgian waffles covered with an assortment of fresh berries and whipped cream</div>
    <br/>
    <span style="color: red;">900</span>
    <br/>
    <h3>French Toast</h3>
    <span style="color: gray;">$4.50</span>
    <br/>
    <div class="description">Thick slices made from our homemade sourdough bread</div>
    <br/>
    <h3>Homestyle Breakfast</h3>
    <span style="color: gray;">$6.95</span>
    <br/>
    <div class="description">Two eggs, bacon or sausage, toast, and our ever-popular hash browns</div>
    <br/>
  </body>
</html>

======== PROFILE ========
<profile>
  <template rank="1" match="food" name="" mode="food_menu" calls="5" time="21" average="4"/>
  <template rank="2" match="*" name="" mode="description-tag" calls="5" time="10" average="2"/>
  <template rank="3" match="" name="price-label" mode="" calls="5" time="9" average="1"/>
  <template rank="4" match="food" name="" mode="description" calls="5" time="8" average="1"/>
  <template rank="5" match="" name="calories-label" mode="" calls="3" time="8" average="2"/>
  <template rank="6" match="/breakfastMenu" name="" mode="" calls="1" time="8" average="8"/>
  <template rank="7" match="food[key('calories', @key) &gt;= 800]" name="" mode="calories" calls="2" time="4" average="2"/>
  <template rank="8" match="food" name="" mode="calories" calls="2" time="4" average="2"/>
  <template rank="9" match="*" name="" mode="path" calls="1" time="4" average="4"/>
  <template rank="10" match="food[key('calories', @key) &gt;= 650]" name="" mode="calories" calls="1" time="2" average="2"/>
</profile>
None
======== MESSAGES ========
TPL: context="/breakfastMenu", mode="None", match="/breakfastMenu", file="samples/simple-xsl-xslt1/pages/breakfast.xsl:12"
TPL: context="/breakfastMenu", mode="path", match="*", file="samples/simple-xsl-xslt1/pages/breakfast.xsl:24"
MSG: mes="/breakfastMenu", column="0", file="<string>:0"
TPL: context="/breakfastMenu/food[1]", mode="food_menu", match="food", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/item.xsl:6"
NAMED TPL: context="/breakfastMenu/food[1]", name="price-label", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/item.xsl:13"
TPL: context="/breakfastMenu/food[1]", mode="description", match="food", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/description.xsl:8"
TPL: context="/breakfastMenu/food[1]/description", mode="description-tag", match="*", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/description-tag.xsl:6"
TPL: context="/breakfastMenu/food[1]", mode="calories", match="food[key('calories', @key) >= 650]", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/calories.xsl:8"
MSG: mes="bw650", column="0", file="<string>:0"
NAMED TPL: context="/breakfastMenu/food[1]", name="calories-label", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/calories.xsl:22"
TPL: context="/breakfastMenu/food[2]", mode="food_menu", match="food", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/item.xsl:6"
NAMED TPL: context="/breakfastMenu/food[2]", name="price-label", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/item.xsl:13"
TPL: context="/breakfastMenu/food[2]", mode="description", match="food", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/description.xsl:8"
TPL: context="/breakfastMenu/food[2]/description", mode="description-tag", match="*", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/description-tag.xsl:6"
TPL: context="/breakfastMenu/food[2]", mode="calories", match="food[key('calories', @key) >= 800]", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/calories.xsl:15"
MSG: mes="850", column="0", file="<string>:0"
NAMED TPL: context="/breakfastMenu/food[2]", name="calories-label", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/calories.xsl:22"
TPL: context="/breakfastMenu/food[3]", mode="food_menu", match="food", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/item.xsl:6"
NAMED TPL: context="/breakfastMenu/food[3]", name="price-label", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/item.xsl:13"
TPL: context="/breakfastMenu/food[3]", mode="description", match="food", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/description.xsl:8"
TPL: context="/breakfastMenu/food[3]/description", mode="description-tag", match="*", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/description-tag.xsl:6"
TPL: context="/breakfastMenu/food[3]", mode="calories", match="food[key('calories', @key) >= 800]", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/calories.xsl:15"
MSG: mes="850", column="0", file="<string>:0"
NAMED TPL: context="/breakfastMenu/food[3]", name="calories-label", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/calories.xsl:22"
TPL: context="/breakfastMenu/food[4]", mode="food_menu", match="food", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/item.xsl:6"
NAMED TPL: context="/breakfastMenu/food[4]", name="price-label", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/item.xsl:13"
TPL: context="/breakfastMenu/food[4]", mode="description", match="food", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/description.xsl:8"
TPL: context="/breakfastMenu/food[4]/description", mode="description-tag", match="*", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/description-tag.xsl:6"
TPL: context="/breakfastMenu/food[4]", mode="calories", match="food", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/calories.xsl:30"
MSG: mes="default", column="0", file="<string>:0"
TPL: context="/breakfastMenu/food[5]", mode="food_menu", match="food", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/item.xsl:6"
NAMED TPL: context="/breakfastMenu/food[5]", name="price-label", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/item.xsl:13"
TPL: context="/breakfastMenu/food[5]", mode="description", match="food", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/description.xsl:8"
TPL: context="/breakfastMenu/food[5]/description", mode="description-tag", match="*", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/description-tag.xsl:6"
TPL: context="/breakfastMenu/food[5]", mode="calories", match="food", file="/Users/nikita/Dev/panforte/samples/simple-xsl-xslt1/blocks/calories.xsl:30"
MSG: mes="default", column="0", file="<string>:0"
```
