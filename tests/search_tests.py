"""
Author: robalar <rbthales@gmail.com>
URL: github.com/Streams

This file is part of streams

Streams is free software, and is distributed under the MIT licence.
See LICENCE or opensource.org/licenses/MIT
"""

from types import ListType
import unittest

from nose.tools import assert_equals

from streams import search
import streams
from streams.search import torrent, movie

import logging

logger = logging.getLogger(__name__)

class SearchTest(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        logger.info('Running search pre-test setup')
       # streams.start_tor_proxy()

    @classmethod
    def teardown_class(cls):
        logger.info('Running post-test teardown')
       # streams.kill_tor_proxy()

    def test_get_movies(self):
        s = search.do_search('star wars')
        assert_equals(type(s), ListType)
        
    def test_torrent(self):
        t = torrent.Torrent('magnet:?xt=urn:sha1:YNCKHTQCWBTRNJIV4WNAE',
                            '1080p', peers=23, seeds=6)

        assert_equals(t.magnet_link,
                      'magnet:?xt=urn:sha1:YNCKHTQCWBTRNJIV4WNAE')
        assert_equals(str(t), 'magnet:?xt=urn:sha1:YNCKHTQCWBTRNJIV4WNAE')
        assert_equals(t.quality, '1080p')
        assert_equals(t.peers, 23)
        assert_equals(t.seeds, 6)

    def test_movie(self):
        torrent1 = torrent.Torrent('magnet:?xt=urn:sha1:YNCKHTQCWBTRNJIV4WNAE',
                                   '1080p')
        torrent2 = torrent.Torrent('magnet:?xt=urn:sha1:E52SJUQCZO5C', '720p')
        m = movie.Movie('Montage of Heck', [torrent1, torrent2])
        for t in m:
            assert_equals(type(t), torrent.Torrent)
        assert_equals(m.title, 'Montage of Heck')
        assert_equals(str(m), 'Montage of Heck')
        assert_equals(m.torrents[0], torrent1)
        assert_equals(m.torrents[1], torrent2)

        assert_equals(m.imdbID, 'tt4229236')
        assert_equals(m.Rated, 'TV-MA')