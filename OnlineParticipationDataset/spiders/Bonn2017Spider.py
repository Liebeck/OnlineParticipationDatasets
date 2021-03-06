import scrapy
from OnlineParticipationDataset import items
from datetime import datetime
import re
import locale


class Bonn2017Spider(scrapy.Spider):
    name = "bonn2017"
    start_urls = ['https://www.bonn-macht-mit.de/node/871']

    def __init__(self, *args, **kwargs):
        super(Bonn2017Spider, self).__init__(*args, **kwargs)
        locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

    def get_suggestion_id(self, response):
        return int(response.xpath('.//article[starts-with(@class,"node-proposal")]/@data-nid').extract_first() or 0)

    def get_suggestion_author(self, response):
        return response.xpath('.//span[@class="username"]/text()').extract_first().strip()

    def get_suggestion_title(self, response):
        return response.xpath('.//h2[@class="node__title node-title"]/text()').extract_first().strip()

    def get_suggestion_category(self, response):
        try:
            return response.xpath(
                './/div[@class="nmw m-auto"]/div[@class="button-small"]/text()').extract_first().strip()
        except AttributeError:
            return None

    def get_suggestion_type(self,response):
        return response.xpath(
            './/div[contains(@class,"field-name-field-proposal-financial-type")]//div[@class="field-item even"]/text()').extract_first()

    def parse_content(self, lines):
        # return ''.join(map(lambda s: s.strip(), lines))
        return ''.join(lines)

    def get_suggestion_content(self, response):
        return self.parse_content(response.xpath('.//div[@class="nmw m-auto"]//div[@class="field-items"]//p/text()').extract())

    def get_suggestion_approval(self, response):
         return self.parse_split_int(response.xpath('.//span[@class="count-icon count-votes-up"]/text()')
                    .extract_first())

    # def get_suggestion_refusal(self, response):
    #     return int(response.xpath('.//span[@title="Contra votes"]/text()')
    #         .extract_first() or 0)

    # def get_suggestion_abstention(self, response):
    #     return int(response.xpath('.//span[@title="Neutral votes"]/text()')
    #         .extract_first() or 0)

    def parse_split_int(self, s):
        try:
            return int(s.split()[0])
        except (TypeError, AttributeError) as _:
            return 0

    def get_suggestion_comment_count(self, response):
        return self.parse_split_int(response.xpath('.//span[@class="count-comments count-icon"]/text()')
                .extract_first())

    def get_suggestion_parse_datetime(self, s):
        return datetime.strptime(
            re.sub(r"(\s|[a-z])+", "", s.lower(), flags=re.UNICODE), '%d.%m.%Y')

    def get_suggestion_datetime(self, response):
        return self.get_suggestion_parse_datetime(
                response.xpath('.//p[@class="user-and-date inline"]/text()').extract()[1])

    def parse_comment_id(self, s):
        if s is not None:
            return int(re.search(r"comment\-(\d+)", s)[1],0)

    def get_comment_id(self, response):
        return self.parse_comment_id(response.xpath('./@id').extract_first())

    def get_comment_content(self, response):
        return self.parse_content(response.xpath('./div/div[@class="comment-body"]//p/text()').extract())

    def get_comment_title(self, response):
        return response.xpath('./div/div[@class="comment-body"]//a[@rel="bookmark"]/text()').extract_first().strip()

    def get_comment_author(self, response):
        return response.xpath('./div/div[@class="comment-meta"]//span/text()').extract_first().strip()

    def parse_datetime_comment(self, l):
        s = ' '.join([s.strip() for s in l])
        s = s.replace('von','').strip()
        return datetime.strptime(s, 'am %d. %b. %Y at %H:%MUhr')

    def get_comment_datetime(self, response):
        return self.parse_datetime_comment(response.xpath('./div/div[@class="comment-meta"]/header/div/text()').extract())

    def create_comment_item(self, response, suggestion_id, parent_id=None, level=1):
        """
        Create a CommentItem, see :class:`~OnlineParticipationDataset.items.CommentItem`, from given response.

        :param response: scrapy response
        :return: scrapy item
        """
        comment_item = items.CommentItem()

        comment_item['level'] = level
        comment_item['comment_id'] = self.get_comment_id(response)
        comment_item['suggestion_id'] = suggestion_id
        if parent_id:
            comment_item['parent_id'] = parent_id
        comment_item['date_time'] = self.get_comment_datetime(response)
        comment_item['author'] = self.get_comment_author(response)
        comment_item['title'] = self.get_comment_title(response)
        comment_item['content'] = self.get_comment_content(response)

        children_list = []

        if level == 1:
            children_xpath = 'following-sibling::div/div[@class="indented"]/article'
        else:
            children_xpath = 'following-sibling::div[@class="indented"]/article'

        for child in response.xpath(children_xpath):
            children_list.append(self.create_comment_item(child, suggestion_id, comment_item['comment_id'], level+1))

        comment_item['children'] = children_list

        return comment_item

    def create_comment_item_list(self, response, suggestion_id):
        """
        Create a list of CommentItems, see :class:`~OnlineParticipationDataset.items.CommentItem`, from given response.

        :param response: scrapy response
        :return: list with CommentItems
        """
        comment_items = []
        # Get first level comments
        for comment in response.xpath('//section[@id="comments"]/div/article'):
            comment_items.append(self.create_comment_item(comment, suggestion_id))
        return comment_items

    def create_suggestion_item(self, response):
        """
        Create a SuggestionItem, see :class:`~OnlineParticipationDataset.items.SuggestionItem`, from given response.

        :param response: scrapy response
        :return: scrapy item
        """
        suggestion_item = items.SuggestionItem()
        suggestion_item['suggestion_id'] = self.get_suggestion_id(response)
        suggestion_item['title'] = self.get_suggestion_title(response)
        suggestion_item['suggestion_type'] = self.get_suggestion_type(response)
        suggestion_item['date_time'] = self.get_suggestion_datetime(response)
        suggestion_item['category'] = self.get_suggestion_category(response)
        suggestion_item['author'] = self.get_suggestion_author(response)
        suggestion_item['approval'] = self.get_suggestion_approval(response)
        # suggestion_item['refusal'] = self.get_suggestion_refusal(response)
        # suggestion_item['abstention'] = self.get_suggestion_abstention(response)
        suggestion_item['content'] = self.get_suggestion_content(response)
        suggestion_item['comment_count'] = self.get_suggestion_comment_count(response)
        return suggestion_item

    def parse(self, response):
        """
        Parse given response and yield items for suggestions and comments of all
        pages of bonn-packts-an-2017.

        :param response: scrapy response
        :return: generator
        """
        for thread in response.xpath('//div[@class="view-content"]/div/div/a[@data-rel="#main-content"]'):
            thread_url = thread.xpath('@href').extract_first()
            yield response.follow(thread_url, self.parse_thread)


        # Parse next Site
        next_page = response.xpath(
            './/li[starts-with(@class, "pager-next")]/a/@href').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_thread(self, response):
        """
        Parse thread and yield a SuggestionItem, see :class:`~OnlineParticipationDataset.items.SuggestionItem`.

        :param response: scrapy response
        :return: generator
        """
        suggestion = self.create_suggestion_item(response)
        suggestion['comments'] = self.create_comment_item_list(response, suggestion['suggestion_id'])
        yield suggestion
