import scrapy
from selenium import webdriver
from OnlineParticipationDataset import items
from datetime import datetime


class BraunkohleSpider(scrapy.Spider):
    name = "braunkohle"
    start_urls = ['https://www.leitentscheidung-braunkohle.nrw/perspektiven/de/home/beteiligen/draftbill/47589/para/9',
                  'https://www.leitentscheidung-braunkohle.nrw/perspektiven/de/home/beteiligen/draftbill/47589/para/11',
                  'https://www.leitentscheidung-braunkohle.nrw/perspektiven/de/home/beteiligen/draftbill/47589/para/12',
                  'https://www.leitentscheidung-braunkohle.nrw/perspektiven/de/home/beteiligen/draftbill/47589/para/13',
                  'https://www.leitentscheidung-braunkohle.nrw/perspektiven/de/home/beteiligen/draftbill/47589/para/14',
                  'https://www.leitentscheidung-braunkohle.nrw/perspektiven/de/home/beteiligen/draftbill/47589/para/17',
                  'https://www.leitentscheidung-braunkohle.nrw/perspektiven/de/home/beteiligen/draftbill/47589/para/16']

    def __init__(self, **kwargs):
        super(BraunkohleSpider, self).__init__(**kwargs)
        self.driver = webdriver.Firefox()

    def extract_num_comments(self, response):
        '''
        Extracts the number of comments given a response on thread-level
        :param response: Response
        :return: Number of comments as a string
        '''
        return response.css('.row.ecm_commentsHead h2::text').extract()[0].split(' ')[1].strip('()')

    def get_category(self, response):
        '''
        Returns category by manually deciding on the link
        :param response: Response
        :return: category (string)
        '''
        url = response.url
        num = int(url.split('/')[-1])
        cases = {
            9: 'Energie',
            11: 'Umwelt',
            12: 'Holzweiler',
            13: 'Holzweiler',
            14: 'Holzweiler',
            17: 'Holzweiler',
            19: 'Strukturwandel im Rheinischen Revier',
        }
        return cases.get(num, 'Unknown')

    def create_suggestion_item(self, response):
        '''
        Creates a suggestion item based on information in response
        :param response: scrapy response
        :return: suggestion item
        '''
        sug_item = items.SuggestionItem
        title = ' '.join(response.css('.ecm_draftBillParagraphContent.push-top>h1::text').extract())
        suggestion = ' '.join(response.css(
            '.ecm_draftBillParagraphContent.push-top>div>h3::text,.ecm_draftBillParagraphContent.push-top>div>p>strong::text').extract())
        num_comments = int(self.extract_num_comments(response))
        category = self.get_category(response)
        sug_item.title = title
        sug_item.suggestion = suggestion
        sug_item.num_comments = num_comments
        sug_item.category = category
        return sug_item

    def get_datetime(self, comment):
        '''
        Returns datetime of comment
        :param comment: comment (selector)
        :return: datetime
        '''
        com_details = comment.css('.ecm_commentDetails')
        date_time = ' '.join(com_details.css('.ecm_commentDate span::text').extract())
        return datetime.strptime(date_time, "%d.%m.%Y %H:%M")

    def get_author(self, comment):
        '''
        Returns author of comment
        :param comment: comment (selector)
        :return: name of author (string)
        '''
        com_details = comment.css('.ecm_commentDetails')
        return com_details.css('.ecm_userProfileLink span::text').extract_first()

    def get_id(self, comment):
        '''
        Returns ID of comment
        :param comment: comment (selector)
        :return: ID (string) of comment
        '''
        return comment.css('::attr(id)').extract_first()

    def get_content(self, comment):
        '''
        Returns written content of comment as a string
        :param comment: commment (selector)
        :return: content (string) of comment
        '''
        return ' '.join(comment.css('.ecm_commentContent p::text').extract())

    def has_children(self, comment):
        '''
        Checks if comment has children
        :param comment: comment (selector)
        :return: true if comment has children, else: false
        '''
        comment_type = comment.css('::attr(class)').extract()[0]
        if 'ecm_comment_children' in comment_type:
            return True
        else:
            return False

    def get_child_ids(self, comment_sublist):
        '''
        Returns a list of all comment-ids in a comment sublist
        :param comment_sublist: comment-sublist (selector) 
        :return: List of all comment ids (first level)
        '''
        ids = []
        comments = comment_sublist.css('.ecm_commentSublist>.ecm_comment')
        for comment in comments:
            ids.append(self.get_id(comment))
        return ids

    def get_children_comments(self, comment_sublist):
        '''
        Returns a list of all comments in a comment sublist
        :param comment_sublist: comment-sublist (selector) 
        :return: List of all comments (first level)
        '''
        return comment_sublist.css('.ecm_commentSublist>.ecm_comment')

    def get_children_sublists(self, comment_sublist):
        '''
        Returns a list of all sublists in a comment sublist
        :param comment_sublist: comment-sublist (selector) 
        :return: List of all sublists (first level)
        '''
        return comment_sublist.css('.ecm_commentSublist>.ecm_commentSublist')

    def create_comments(self, comments, comment_sublists, parent_id):
        '''
        Creates comment items recursivly based on given list of comments (selectors) and list of comment-sublists (selectors)
        :param comments: list of comments (selectors)
        :param comment_sublists: list of comment-sublists (selectors)
        :param id: ID of parent comment (if there is no parent: None)
        :return: list of items to be yielded
        '''
        comment_list = []
        sub_iterator = iter(comment_sublists)
        for comment in comments:
            # Populate current item
            tmp_comment = items.CommentItem
            tmp_comment.author = self.get_author(comment)
            tmp_comment.date_time = self.get_datetime(comment)
            tmp_comment.id = self.get_id(comment)
            tmp_comment.parent = parent_id
            tmp_comment.content = self.get_content(comment)
            # Check if comment has children
            if self.has_children(comment):
                # Get next sublist
                comment_sublist = sub_iterator.next()
                tmp_comment.post_children = self.get_child_ids(comment_sublist)
                #TODO Get all comments and sublists for function call
                #children = self.create_comments()
                #TODO Recursivly call this function

    def parse(self, response):
        '''
        Parses thread-level information
        :param response: Response
        :return: Yields items and new requests
        '''
        # Create, populate and yield suggestion item:
        yield (self.create_suggestion_item(response))
        # Get comments (regular and with child comments):
        comments = response.css('#comment-area>div>.ecm_comment')
        # Get comment sublists (each corresponds to one comment with child comments in <comments>)
        comment_sublists = response.css('#comment-area>div>.ecm_commentSublist')
        sub_iterator = iter(comment_sublists)
        #TODO Replace with call of create_comments
        for comment in comments:
            author = self.get_author(comment)
            date_time = self.get_datetime(comment)
            id = self.get_id(comment)
            content = self.get_content(comment)
            # Check if comment has children
            if self.has_children(comment):
                pass
        #TODO Load further (javascript: selenium). Question: Load before parsing information or after? Missing child problem.