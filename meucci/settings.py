import os

BOT_NAME = 'meucci'

SPIDER_MODULES = ['meucci.spiders']
NEWSPIDER_MODULE = 'meucci.spiders'

CONCURRENT_REQUESTS = 1

COOKIES_ENABLED = False
COOKIES_DEBUG = False

DEFAULT_REQUEST_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'accept-language': 'en',
}

DOWNLOAD_DELAY = 0.25
DOWNLOAD_TIMEOUT = 10

DUPEFILTER_DEBUG = True

FEED_EXPORTERS = {
    'csv': 'meucci.ext.TabbedCsvItemExporter',
}

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 60 * 60 * 24 * 14
HTTPCACHE_DIR = os.environ.get('HTTPCACHE_DIR', 'httpcache')
HTTPCACHE_ALLOW_HTTP_CODES = [200]
HTTPCACHE_POLICY = 'meucci.ext.WhitelistCodesCachePolicy'
HTTPCACHE_STORAGE = 'meucci.ext.OneMoreSubDirFilesystemCacheStorage'

LOG_FILE_APPEND = False

REFERRER_ENABLED = False
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html#std-setting-REFERRER_POLICY
REFERRER_POLICY = 'no-referrer'

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'

RETRY_HTTP_CODES = [403]
RETRY_PRIORITY_ADJUST = -100
RETRY_TIMES = 3

ROBOTSTXT_OBEY = False

TELNETCONSOLE_ENABLED = not bool(os.environ.get('SCRAPYD'))
TELNETCONSOLE_USERNAME = 'scrapy'
TELNETCONSOLE_PASSWORD = os.environ.get('SCRAPY_TELNETCONSOLE_PASSWORD', 'scrapy')

USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
)
