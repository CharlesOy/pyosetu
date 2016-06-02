import urllib2
import bs4


def get_soup(url):
    """get soup object for a url"""
    c = urllib2.urlopen(url)
    return bs4.BeautifulSoup(c.read(), 'html.parser')


class User:
    def __init__(self, user_id, _novels=False, _blogs=False, _bookmarks=False, _following_users=True,
                 _commented_novels=False, _review_list=False):
        """init function"""
        self.id = user_id
        self.name = self.get_username()

        self.novels = []
        self.blogs = []
        self.bookmarks = []
        self.following_users = []
        self.commented_novels = []
        self.reviews = []

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
        return soup.title.string

    @staticmethod
    def get_count(url, pos_to=-2):
        """decompose count from specific url"""
        soup = get_soup(url)
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
            soup_review_novel_list = soup.find(id='novelreviewlist')
            if soup_review_novel_list is not None:
                li_review_titles = soup_review_novel_list.find_all(class_='review_title')
                for li_review_title in li_review_titles:
                    self.reviews.append(li_review_title.find('a')['href'][51:-1].encode('unicode-escape'))

    @staticmethod
    def page_review(review_id):
        """review page"""
        return 'http://novelcom.syosetu.com/novelreview/list/ncode/' + review_id + '/'
