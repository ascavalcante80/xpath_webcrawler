import requests
import random
from time import sleep
from lxml import html
import lxml

__author__ = 'alexandre cavalcante'
__version__ = '1.0'


class Crawler(object):

    def __init(self):
        pass

    def get_page(self, url, max_sleep_time, retry_time=60, max_retries=10, retry=True, verbose=True):
        """
        This function crawls a page passed as argument and returns it in html page object. If it fails to crawl a page,
         it can retry for number of times specified by the user. The sleep time arguments are used to avoid blocks from
         the servers due to a several request in a short time. Do not set it 0.

        :param url: string value with url to be crawled
        :param max_sleep_time: int value to indicate the max time the system will after crawl the page
        :param retry_time: int value to indicate the time the system has to wait before retry crawl the page again, if
        it fails to crawl the page. The default time is 60 seconds
        :param max_retries: int value to indicate the max number of tries the system has to crawl to page. After this
        threshold the function return a None value
        :param retry: boolean value - if True the system retries crawl the page, in case it has previously failed
        :param verbose: boolean value - prints in the stdout the status of pages crawled
        :return: the page crawled
        """

        # variable to keep the structure of the website crawled
        page = None

        tries = 0

        # try to connect
        while tries < 10:

            # try catch connection erros
            try:

                headers = {'User-Agent': 'Mozilla/5.0'}
                session = requests.Session()
                page = session.get(url, headers=headers)

                if not ("NoneType" == type(page)):

                    if page.status_code == 200:
                        # sleep with random intervals
                        # tempo = random.random() * self.sleepTime
                        tempo = random.random() * max_sleep_time

                        if verbose:
                            print('url sucefully crawled- ' + url)
                            print('going to sleep for ' + str(tempo) + ' seconds')
                        sleep(tempo)

                    break

            except requests.exceptions.RequestException as err:

                if not retry:
                    return None

                print(str(err))
                tries += 1

                if tries > max_retries:
                    return None

                if verbose:
                    print("Retrying in ..." + str(retry_time) + 'seconds')

                # go to sleep
                sleep(retry_time)
                pass
            except Exception as err:
                if verbose:
                    print("Error - returning None for URL " + url + str(err))
                return None

        if page is not None:
            page.encoding = 'utf-8'
            return page
        else:
            return None

    def execute_xpath(self, url, xpath_expression, max_sleep_time, retry_time=60, max_tries=10, retry=False,
                      verbose=True):
        """
        This function executes a xpath expressions and returns a list with the extracted objects.
        If it fails to execute the xpath expression or to crawl the page, it returns a empty list.

        :param url: string with the url page
        :param xpath_expression: string with xpath expression
        :param max_sleep_time: int value to indicate the max time the system will after crawl the page
        :param retry_time: int value to indicate the time the system has to wait before retry crawl the page again,
         if it fails to crawl the page. The default time is 60 seconds
        :param max_tries: int value to indicate the max number of tries the system has to crawl to page. After this
         threshold the function return a None value
        :param retry: boolean value - if True the system retries crawl the page, in case it has previously failed
        :param verbose: boolean value - prints in the stdout the status of pages crawled
        :return: array with the crawled objects
        """

        # download page
        page = self.get_page(url, max_sleep_time, retry_time, max_tries, retry, verbose)

        try:

            page_tree = html.fromstring(page.text)

            # perform xpath
            elements_list = page_tree.xpath(xpath_expression)
            return elements_list

        except AttributeError as err:
            if verbose:
                print('Exception caught : ' + str(err) + '\nReturning empty list to the url:' + url)
            return []

        except lxml.etree.XPathEvalError as err:
            if verbose:
                print('Exception caught : ' + str(err) + '\nReturning empty list to the url:' + url)
            return []

        except Exception as err:
            if verbose:
                print('Exception caught : ' + str(err) + '\nReturning empty list to the url:' + url)
            return []
