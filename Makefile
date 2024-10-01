output_prefix = Meucci

.PHONY: _deploy
_deploy:
	pipenv run scrapyd-deploy -a

.PHONY: _install
_install:
	pipenv install
	mkdir -p logs

.PHONY: catalog
catalog: _install
	pipenv run scrapy crawl $@ -O result/$(output_prefix)_`date +%d%m%Y`.csv --logfile=logs/$@.log

