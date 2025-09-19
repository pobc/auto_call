import unittest
from utils import u2_tools

class MyTestCase(unittest.TestCase):
    def test_find_exists(self):
        u2_tools.init()
        #             com.wuba:id/chat_text_content_container
        resourceId = '//*[@resource-id="com.wuba:id/im_ugc_card_content_layout"]'
        print(u2_tools.find_exists(path=resourceId))
        pass