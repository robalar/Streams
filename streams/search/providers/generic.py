"""
Author: robalar <rbthales@gmail.com>
URL: github.com/Streams

This file is part of streams

Streams is free software, and is distributed under the MIT licence.
See LICENCE or opensource.org/licenses/MIT
"""

import logging

logger = logging.getLogger(__name__)

class GenericProvider(object):
    """A generic provider which must be inherited by all other providers.

        All methods here must be overloaded for the provider to function
        properly

        Attributes:
            name (string): name of provider
            url (string): url of provider
    """
    def __init__(self, name, url):
        """Initialises provider with name and url"""
        self.name = name
        self.url = url

    def do_search(self, search_term):
        """Contains the search logic of the provider"""
        logger.warning('Search not implemented in provider {0}'.format(self.name))
