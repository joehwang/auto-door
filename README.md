# auto-door 台灣四大超商爬蟲

台灣4大超商店鋪資料爬蟲，使用python/scrapy框架
支援`7-11` `全家` `萊爾富` `okmart`資料抓取

## 

![image](https://github.com/joehwang/auto-door/blob/master/doc/kv.gif?raw=true)


## 環境

已打包為docker映像檔
[[https://hub.docker.com/r/joehwang/tw-cvs-crawl]]

python 3.6

scrapy 2.0

## 使用

### 7-11便利商店

`docker-compose run scrapy scrapy crawl seveneleven -o /crawl_output/seveneleven.csv`

### 全家便利商店

`docker-compose run scrapy scrapy crawl familymart -o /crawl_output/familymart.csv`

### 萊爾富便利商店

`docker-compose run scrapy scrapy crawl hilife -o /crawl_output/hilife.csv`

### OK便利商店

`docker-compose run scrapy scrapy crawl okmart -o /crawl_output/okmart.csv`


