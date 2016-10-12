# coding: utf-8

import requests
import os
import json
import subprocess
import shutil
import sys
import zipfile

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


def svn_checkout(url, path):
    """Call svn checkout"""
    user = config()['SVN_USERNAME']
    password = config()['SVN_PASSWORD']
    p = subprocess.Popen(['svn', 'co', url, path, '--username', user, '--password', password])
    stdout, stderr = p.communicate()


def download_file(url, file_name):
    """Download file from remote host"""

    r = requests.get(url=url, stream=True)
    if r.ok:
        with open(os.path.join(TMP_FOLDER, file_name), 'wb') as f:
            f.write(r.content)
    else:
        r.raise_for_status()


def config():
    """Work with config file"""

    with open('config.json', encoding='utf-8') as conf:
        json_conf = json.load(conf)
    return json_conf


def get_chromedriver():
    """Get chromedriver from internet"""

    ver_chromedriver = config()['VER_CHROMEDRIVER']
    win_filename = 'chromedriver_win32.zip'
    url_chromedriver = 'http://chromedriver.storage.googleapis.com/{}/{}'.format(ver_chromedriver, win_filename)
    download_file(url_chromedriver, win_filename)


def get_standalone_server():
    """Get selenium-standalone-server.jar"""

    ver_standalone_server = config()['VER_STANDALONE_SERVER']
    patch = '1'
    file_standalone_server = 'selenium-server-standalone-{ver}.{p}.jar'.format(ver=ver_standalone_server,
                                                                               p=patch or '0')
    url_selenium_server = 'http://selenium-release.storage.googleapis.com/{}/{}'.format(ver_standalone_server,
                                                                                        file_standalone_server)
    download_file(url_selenium_server, file_standalone_server)


def get_atf():
    """Get automated testing framework"""
    ver_atf = config()['VER_ATF']
    url = 'https://svn.sbis.ru/svn/sbis3-tests/atf/release/{}/'.format(ver_atf)
    path = os.path.join(TMP_FOLDER, 'atf')
    if os.path.exists(path):
        shutil.rmtree(path)
    svn_checkout(url, path)


def get_genie_tests():
    """Get test from svn"""

    ver_genie = config()['VER_GENIE']
    url = 'https://svn.sbis.ru/svn/sbis3-tests/genie/{}/'.format(ver_genie)
    path = os.path.join(TMP_FOLDER, 'tests')
    if os.path.exists(path):
        shutil.rmtree(path)
    svn_checkout(url, path)


def install_lib():
    """Install lib's through pip"""

    p = subprocess.Popen(['pip', 'install', '-r', 'requirement.txt'])
    p.communicate()


def copy_into_site_packages():
    """Copy atf, PO into folder site-packages"""

    site_packages = [path for path in sys.path if 'site-packages' in path][0]
    try:
        shutil.copytree(os.path.join(TMP_FOLDER, 'atf'), os.path.join(site_packages, 'atf'))
        shutil.copytree(os.path.join(TMP_FOLDER, 'tests', 'module_genie'), os.path.join(site_packages, 'module_genie'))
        shutil.copytree(os.path.join(TMP_FOLDER, 'tests', 'pages'), os.path.join(site_packages, 'pages'))
    except FileExistsError:
        pass


def copy_chromedriver():
    """Copy chromedriver in execute path"""

    exec_dir = sys.prefix
    zipfile.ZipFile(os.path.join(TMP_FOLDER, 'chromedriver_win32.zip')).extractall(path=os.path.join(exec_dir, 'bin'))


def main():
    """Common algorithm"""
    if not os.path.exists(TMP_FOLDER):
        print('[*] create tmp folder: ', TMP_FOLDER)
        os.mkdir(TMP_FOLDER)

    print('[*] get chromedriver..')
    get_chromedriver()

    print('[*] get selenium-standalone-server..')
    get_standalone_server()

    print('[*] get atf..')
    get_atf()

    print('[*] get tests..')
    get_genie_tests()

    print('[*] install lib..')
    install_lib()

    print('[*] copy data into site-packages..')
    copy_into_site_packages()

    print('[*] copy chromedriver..')
    copy_chromedriver()


if __name__ == '__main__':
    head()
    main()
