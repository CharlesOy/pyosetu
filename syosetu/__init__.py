"""
A Crawler for http://yomou.syosetu.com
"""

import urllib2
import bs4
import datetime


def get_soup(_url):
    """get soup object for a url"""
    try:
        c = urllib2.urlopen(_url)
        return bs4.BeautifulSoup(c.read(), 'html.parser')
    except Exception, e:
        print(Exception, e)


def prepare_str(_str):
    """remove all '\n's, ','s and ' 's"""
    return _str.replace('\n', '').replace(',', '').replace(' ', '')


class User:
    """User class, decompose key information with a user id"""

    def __init__(self, user_id):
        """init function"""
        # user id
        self.id = user_id
        # user state, 1 means active, 0 means inactive.
        self.state = 1
        # user name
        self.name = self.get_username()

        # novels written by current user
        self.novels = []
        # user's blog
        self.blogs = []
        # bookmarked novels
        self.bookmarks = []
        # user id list followed by current user
        self.following_users = []
        # commented novels
        self.commented_novels = []
        # reviews received
        self.reviews = []

    def init(self, _novels=False, _blogs=False, _bookmarks=False, _following_users=False,
             _commented_novels=False, _review_list=False, _all=False):
        """get info from web"""
        if _all:
            self.list_novel()
            self.list_blog()
            self.list_bookmark()
            self.list_following_user()
            self.list_commented_novels()
            self.list_reviews()
            return

        if _novels:
            self.list_novel()
        if _blogs:
            self.list_blog()
        if _bookmarks:
            self.list_bookmark()
        if _following_users:
            self.list_following_user()
        if _commented_novels:
            self.list_commented_novels()
        if _review_list:
            self.list_reviews()

    @staticmethod
    def correct_page_num(page):
        if page < 0 or page > 200:
            return 1
        return page

    def page_home(self):
        """home page url"""
        return 'http://mypage.syosetu.com/' + self.id + '/'

    def page_novel_list(self, page=1):
        """novel list page url"""
        self.correct_page_num(page)
        return 'http://mypage.syosetu.com/mypage/novellist/userid/' \
               + self.id + '/index.php?1=2&all=1&all2=1&all3=1&all4=1&p=' + str(page)

    def page_blog_list(self, page=1):
        """blog list page url"""
        self.correct_page_num(page)
        return 'http://mypage.syosetu.com/mypageblog/list/userid/' \
               + self.id + '/index.php?p=' + str(page)

    def page_bookmark_list(self, page=1):
        """bookmark list page url"""
        self.correct_page_num(page)
        return 'http://mypage.syosetu.com/mypagefavnovelmain/list/userid/' \
               + self.id + '/index.php?p=' + str(page)

    def page_following_list(self, page=1):
        """following list page url"""
        self.correct_page_num(page)
        return 'http://mypage.syosetu.com/mypagefavuser/list/userid/' \
               + self.id + '/index.php?p=' + str(page)

    def page_commented_novel_list(self, page=1):
        """commented novel list page url"""
        self.correct_page_num(page)
        return 'http://mypage.syosetu.com/mypagenovelhyoka/list/userid/' \
               + self.id + '/index.php?p=' + str(page)

    def page_review_list(self, page=1):
        """review list page url"""
        self.correct_page_num(page)
        return 'http://mypage.syosetu.com/mypage/reviewlist/userid/' \
               + self.id + '/index.php?p=' + str(page)

    def get_username(self):
        """get username"""
        soup = get_soup(self.page_home())
        if soup is None:
            self.state = 0
            return None
        return soup.title.string

    @staticmethod
    def get_count(url, pos_to=-2):
        """decompose count from specific url"""
        soup = get_soup(url)
        if soup is None:
            return 0
        if soup.find(class_='allcount') is None:
            return 0
        return int(soup.find(class_='allcount').string[1:pos_to])

    def list_novel(self, page_num=10):
        """get novel list"""
        count = self.get_count(self.page_novel_list())
        if count == 0:
            return
        for i in range(1, (count - 1) / page_num + 2):
            soup = get_soup(self.page_novel_list(i))
            if soup is None:
                continue
            soup_novel_list = soup.find(id='novellist')
            if soup_novel_list is not None:
                div_titles = soup_novel_list.find_all(class_='title')
                for div_title in div_titles:
                    self.novels.append(div_title.find('a')['href'][25:-1].encode('unicode-escape'))

    @staticmethod
    def page_novel_info(novel_id):
        """novel detailed url"""
        return 'http://ncode.syosetu.com/novelview/infotop/ncode/' + novel_id + '/'

    def list_blog(self, page_num=10):
        """get blog list"""
        count = self.get_count(self.page_blog_list())
        if count == 0:
            return
        for i in range(1, (count - 1) / page_num + 2):
            soup = get_soup(self.page_blog_list(i))
            if soup is None:
                continue
            soup_blog_list = soup.find(id='bloglistbg')
            if soup_blog_list is not None:
                div_titles = soup_blog_list.find_all(class_='title')
                for div_title in div_titles:
                    self.blogs.append(div_title.find('a')['href'][39:-1].encode('unicode-escape'))

    def page_blog(self, blog_id):
        """blog page url"""
        return 'http://mypage.syosetu.com/mypageblog/view/userid/' + self.id + '/blogkey/' + blog_id + '/'

    def list_bookmark(self, page_num=10):
        """get bookmark list"""
        count = self.get_count(self.page_bookmark_list())
        if count == 0:
            return
        for i in range(1, (count - 1) / page_num + 2):
            soup = get_soup(self.page_bookmark_list(i))
            if soup is None:
                continue
            soup_bookmark_list = soup.find(id='novellist')
            if soup_bookmark_list is not None:
                li_titles = soup_bookmark_list.find_all(class_='title')
                for li_title in li_titles:
                    self.bookmarks.append(li_title.find('a')['href'][25:-1].encode('unicode-escape'))

    def list_following_user(self, page_num=10):
        """get following user list"""
        count = self.get_count(self.page_following_list(), -1)
        if count == 0:
            return
        for i in range(1, (count - 1) / page_num + 2):
            soup = get_soup(self.page_following_list(i))
            if soup is None:
                continue
            soup_fav_user = soup.find(id='favuser')
            if soup_fav_user is not None:
                a_links = soup_fav_user.find_all('a')
                for soupLink in a_links:
                    self.following_users.append(soupLink['href'][1:-1].encode('unicode-escape'))

    def list_commented_novels(self, page_num=10):
        """get commented novel list"""
        count = self.get_count(self.page_commented_novel_list())
        if count == 0:
            return
        for i in range(1, (count - 1) / page_num + 2):
            soup = get_soup(self.page_commented_novel_list(i))
            if soup is None:
                continue
            soup_commented_novel_list = soup.find(id='novelpointlist')
            if soup_commented_novel_list is not None:
                li_titles = soup_commented_novel_list.find_all(class_='title')
                for li_title in li_titles:
                    self.commented_novels.append(li_title.find('a')['href'][25:-1].encode('unicode-escape'))

    def list_reviews(self, page_num=10):
        """get review novel list"""
        count = self.get_count(self.page_review_list())
        if count == 0:
            return
        for i in range(1, (count - 1) / page_num + 2):
            soup = get_soup(self.page_review_list(i))
            if soup is None:
                continue
            soup_review_novel_list = soup.find(id='novelreviewlist')
            if soup_review_novel_list is not None:
                li_review_titles = soup_review_novel_list.find_all(class_='review_title')
                for li_review_title in li_review_titles:
                    self.reviews.append(li_review_title.find('a')['href'][51:-1].encode('unicode-escape'))

    @staticmethod
    def page_review(review_id):
        """review page"""
        return 'http://novelcom.syosetu.com/novelreview/list/ncode/' + review_id + '/'


class Novel:
    """Novel class, decompose key information with a novel id"""

    def __init__(self, novel_id):
        """init function"""
        self.id = novel_id
        # title
        self.title = None
        # writer's id
        self.user_id = None
        # category
        self.category = None
        # publication date
        self.publication_date = None
        # last update date
        self.last_date = None
        # impression count
        self.impression_count = 0
        # review count
        self.review_count = 0
        # bookmark count
        self.bookmark_count = 0
        # assessment
        self.assessment = 0
        # writing point
        self.point_writing = 0
        # story point
        self.point_story = 0
        # character count
        self.chara_count = 0

    def page_info(self):
        """info page url"""
        return 'http://ncode.syosetu.com/novelview/infotop/ncode/' + self.id + '/'

    def get_info(self):
        """retrieve detailed info from web"""
        soup = get_soup(self.page_info())
        if soup is None:
            return

        self.title = soup.title.string[:-6]
        table_novel_1 = soup.find(id='noveltable1')
        self.user_id = table_novel_1.find('a')['href'][26:-1]
        self.category = table_novel_1.find_all('td')[3].string
        table_novel_2 = soup.find(id='noveltable2')
        td_infos = table_novel_2.find_all('td')

        year = int(td_infos[0].string[:4])
        month = int(td_infos[0].string[6:8])
        day = int(td_infos[0].string[9:11])
        hour = int(td_infos[0].string[13:15])
        minute = int(td_infos[0].string[16:18])
        self.publication_date = datetime.datetime(year, month, day, hour, minute)

        year = int(td_infos[1].string[:4])
        month = int(td_infos[1].string[6:8])
        day = int(td_infos[1].string[9:11])
        hour = int(td_infos[1].string[13:15])
        minute = int(td_infos[1].string[16:18])
        self.last_date = datetime.datetime(year, month, day, hour, minute)

        self.impression_count = int(prepare_str(td_infos[2].contents[0].string)[:-1])
        self.review_count = int(prepare_str(td_infos[3].string)[:-1])
        self.bookmark_count = int(prepare_str(td_infos[4].string)[:-1])
        self.assessment = int(prepare_str(td_infos[5].string)[:-2])
        raw_points = prepare_str(td_infos[6].contents[0].string).split('pt')
        self.point_writing = int(raw_points[0])
        self.point_story = int(raw_points[1][2:])
        self.chara_count = int(prepare_str(td_infos[8].string)[:-2])
