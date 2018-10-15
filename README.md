# OnlineParticipationDatasets
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/Liebeck/OnlineParticipationDatasets/blob/master/LICENSE)

This projects aims to share text content from online participation processes by sharing crawlers instead of the text contents themselves which might not be possible due to legal reasons. The text contents of the individual online participation plattforms will be downloaded via [Scrapy](https://scrapy.org/) into a JSON file.

## Dependencies
* [docker](https://www.docker.com/)

## How to setup the project:
This will install all required dependencies:
``` bash
make build
```

## How to start the project:
``` bash
make run
scrapy crawl <dataset>
```

## Supported datasets:


| Dataset name | Link | # Suggestions | # Comments | # Total | Crawl time | Command|
|---|---|---|---|---|---|---|
| Bonn 2011    | [~~bonn-packts-an-2011.de~~](http://bonn-packts-an-2011.de/www.bonn-packts-an.de/dito/forumc0d2.html) <sup>[2](#myfootnote2)</sup>                                     | 1015 | 8903 | 9918 | 50 seconds | scrapy crawl bonn2011 |
| Bonn 2015/2016 |[bonn-macht-mit 2015/2016](https://www.bonn-macht-mit.de/dialog/bürgerbeteiligung-am-haushalt-20152016/bhh/online-diskussion) | 335 | 2937 | 3271 | 27 seconds | scrapy crawl bonn2015 |
| Bonn 2017/2018 |[bonn-macht-mit 2017/2018](https://www.bonn-macht-mit.de/node/871) | 55 | 109 | 164 | 5 seconds | scrapy crawl bonn2017 |
| Bonn 2019/2020 |[bonn-macht-mit 2019/2020](https://www.bonn-macht-mit.de/node/2900) | 232 | 600 | 832 | 1 minute | scrapy crawl bonn2019 |
| Braunkohle<sup>[1](#myfootnote1)</sup>| [~~leitentscheidung-braunkohle.nrw~~](https://www.leitentscheidung-braunkohle.nrw/perspektiven/de/home/beteiligen/draftbill/47589/chap/5#chapter) <sup>[2](#myfootnote2)</sup>| 7 | 1296 | 1296 | 32 minutes | scrapy crawl braunkohle|
| Bürgerbudget Wuppertal |[buergerbudget.wuppertal.de](https://buergerbudget.wuppertal.de/cb/t711bwqTXj3GSGiEVwa3li3YZDqvq4pL?type=phase1) | 261 | | | 4 minutes | scrapy crawl wuppertal2017 |
| Köln 2012 | [buergerhaushalt.stadt-koeln.de/2012/diskussion](https://buergerhaushalt.stadt-koeln.de/2012/diskussion) | 594 | 1879 | 2473 | 18 minutes | scrapy crawl koeln2012|
| Köln 2013 | [buergerhaushalt.stadt-koeln.de/2013/buergervorschlaege](https://buergerhaushalt.stadt-koeln.de/2013/buergervorschlaege?&sort_bef_combine=php+ASC) | 592 | 3095 | 3687 | 5 minutes | scrapy crawl koeln2013|
| Köln 2015 | [buergerhaushalt.stadt-koeln.de/2015/buergervorschlaege](https://buergerhaushalt.stadt-koeln.de/2015/buergervorschlaege?&sort_bef_combine=php+ASC) | 631 | 1855 | 2486 | 10 minutes | scrapy crawl koeln2015|
| Köln 2016 | [buergerhaushalt.stadt-koeln.de/2016/buergervorschlaege](https://buergerhaushalt.stadt-koeln.de/2016/buergervorschlaege?&sort_bef_combine=php+ASC) | 827 | 1314 | 2141 | 9 minutes | scrapy crawl koeln2016|
| Leitbild Bad Godesberg | [bonn-macht-mit.de/dialoge/onlinebeteiligung-zum-leitbild-bad-godesberg](https://www.bonn-macht-mit.de/dialoge/onlinebeteiligung-zum-leitbild-bad-godesberg) | 556 | 698 | 1254 | 2 minutes | scrapy crawl badgodesberg|
| Mängelmelder Braunschweig | [mitreden.braunschweig.de/node/1358](https://www.mitreden.braunschweig.de/node/1358) | ≥ 3220 | | | 34 minutes | scrapy crawl maengelmelder-braunschweig|
| Nahverkehrsplan Ulm | [zukunftsstadt-ulm.de/dialog](https://www.zukunftsstadt-ulm.de/dialog/hier-konnten-sie-mit-uns-zu-den-einzelnen-bus-und-bahnlinien-diskutieren) | 498 | 619 | 1117 | 1 minute | scrapy crawl nahverkehrsplan-ulm |
| Raddialog Bonn | [raddialog.bonn.de/dialoge](https://www.raddialog.bonn.de/dialoge/bonner-rad-dialog?sort_bef_combine=created%20ASC) | 2331 | 2425 | 4756 | 16 minutes | scrapy crawl raddialog-bonn|
| Raddialog Koeln | [raddialog-ehrenfeld.koeln.de/dialoge](http://www.raddialog-ehrenfeld.koeln/dialoge/ehrenfelder-raddialog?sort_bef_combine=created%20ASC) | 378 | 277 | 655 | 2 minutes | scrapy crawl raddialog-koeln|
| Raddialog Moers | [raddialog.moers.de/dialoge](https://www.raddialog.moers.de/node/1384?sort_bef_combine=created%20ASC) | 463 | 300 | 763 | 3 minutes | scrapy crawl raddialog-moers|

<a name="myfootnote1">1</a>: Braunkohle-spider uses javascript to load content and needs to wait for server responses. This results in long crawltimes.Braunkohle-site only provides 7 suggestions.

<a name="myfootnote2">2</a>: Offline
