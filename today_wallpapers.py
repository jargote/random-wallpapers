#!/usr/bin/python

import hashlib
import logging
import os
import sys
import urllib2
import xml.etree.ElementTree as ET

from multiprocessing import Process

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


class DeviantRSS(object):
    WALLPAPERS_DIR = '/home/javier/wallpapers'
    TARGET_SIZE = {'width': 1280, 'height': 800}
    RSS_URL = 'http://backend.deviantart.com/rss.xml?q='
    QUERY_MAP = {'base': 'boost:popular in:',
                 'format': '{base}{path} {width}x{height}'}

    def __init__(self, query_map={}):
        self._query_map = query_map
        self._query_map.update(self.QUERY_MAP)
        self._query_map.update(self.TARGET_SIZE)
        assert 'path' in self._query_map

        self._content = self.download_feed()
        assert self._content is not None

        self._root = self.parse_feed(self._content)
        assert self._root is not None

    @property
    def query(self):
        return '{format}'.format(**self._query_map).format(**self._query_map)

    @property
    def rss_url(self):
        return '{url}{query}'.format(url=self.RSS_URL,
                                     query=urllib2.quote(self.query))

    @property
    def root(self):
        return self._root

    def _get_images_data(self):
        # xpath to images content node.
        images = self.root.findall(
            './/item/{http://search.yahoo.com/mrss/}content')
        return [image.attrib for image in images]

    def download_images(self):
        images = [image for image in self._get_images_data()
                  if (int(image['width']) >= self.TARGET_SIZE['width'] and
                      int(image['height']) >= self.TARGET_SIZE['height'])]
        for n, image in enumerate(images):
            logging.info('Downloading Image %s of %s' % ((n + 1),
                                                         len(images)))
            p = Process(target=self.save_image, args=[image['url']])
            p.start()
            p.join()

    def download_feed(self):
        try:
            logging.info('Downloading RSS feed: %s' % self.rss_url)
            response = urllib2.urlopen(self.rss_url)
        except IOError as e:
            logging.error('Error Downloading RSS feed: %s' % str(e))
        else:
            return response.read()

    @classmethod
    def parse_feed(cls, content):
        try:
            logging.info('Parsing RSS feed...')
            return ET.fromstring(content)
        except Exception as e:
            logging.error('An error occurred when parsing RSS feed: %s' %
                          str(e))

    @classmethod
    def download_image(cls, url):
        try:
            return urllib2.urlopen(url).read()
        except IOError as e:
            logging.error('Could not download image: %s (%w)' % (str(e), url))

    @classmethod
    def save_image(cls, url):
        content = cls.download_image(url)
        if content:
            filename = os.path.join(cls.WALLPAPERS_DIR,
                                    '%s.jpg' % hashlib.sha1(url).hexdigest())
            try:
                logging.info('Saving image %s' % filename)
                f = open(filename, 'wb')
                f.write(content)
                f.close()
            except IOError as e:
                logging.error('Could not save image: %s (%s)' %
                              (str(e), filename))


def main():
    # Wallpapers feed 1.
    feed1 = DeviantRSS(query_map={'path': 'customization/wallpaper'})
    feed1.download_images()

    logging.info('\n')

    # Wallpapers feed 2.
    feed2 = DeviantRSS(query_map={'path': 'customization/wallpaper/widescreen'})
    feed2.download_images()

if __name__ == "__main__":
    main()    


