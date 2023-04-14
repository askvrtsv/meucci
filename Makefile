output_prefix = Meucci


.PHONY: _deploy
_deploy:
	pipenv run scrapyd-deploy n3
	pipenv run scrapyd-deploy n4


.PHONY: spider
spider:
	pipenv run scrapy crawl $@ -O output/samokat/$(output_prefix)_`date +%d%m%Y`.csv --logfile=logs/$@.log


.PHONY: samokat
samokat:
	make spider
