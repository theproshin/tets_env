# coding: utf-8

import requests
import os

"""
Setup environment for run test
"""

TMP_FOLDER = os.sep.join([os.getcwd(), 'install'])


def head():
    """Print head"""

    title = """\n
    #####################################################
    # Setup environment for run tests.                  #
    # Install:                                          #
    # - chromedriver                                    #
    # - selenium-standalone-server                      #
    # - test                                            #
    # - Page Objects                                    #
    # - lib selenium                                    #
    #####################################################
    """

    print(title)


def download_file(url, file_name):
    """Download file from remote host"""

    r = requests.get(url=url, stream=True)
    if r.ok:
        with open(file_name, 'wb') as f:
            f.write(r.content)
    else:
        r.raise_for_status()


def get_chromedriver():
    """Get chromedriver from internet"""

    ver_chromedriver = '2.24'
    win_filename = 'chromedriver_win32.zip'
    url_chromedriver = 'http://chromedriver.storage.googleapis.com/{}/{}'.format(ver_chromedriver, win_filename)
    download_file(url_chromedriver, win_filename)


def get_standalone_server():
    """Get selenium-standalone-server.jar"""

    ver_standalone_server = '2.53'
    patch = '1'
    file_standalone_server = 'selenium-server-standalone-{ver}.{p}.jar'.format(ver=ver_standalone_server,
                                                                               p=patch or '0')
    url_selenium_server = 'http://selenium-release.storage.googleapis.com/{}/{}'.format(ver_standalone_server,
                                                                                        file_standalone_server)
    download_file(url_selenium_server, file_standalone_server)


def main():
    """Common algorithm"""
    if not os.path.exists(TMP_FOLDER):
        print('[*] create tmp folder: ', TMP_FOLDER)
        os.mkdir(TMP_FOLDER)
    os.chdir(TMP_FOLDER)

    print('[*] get chromedriver..')
    get_chromedriver()

    print('[*] get selenium-standalone-server..')
    get_standalone_server()


if __name__ == '__main__':
    head()
    main()
