
from .base import FunctionalTest
from unittest import skip

class LayoutAndStylingTest(FunctionalTest):
    @skip
    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 728)

        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertAlmostEqual(inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=10)

        inputbox.send_keys("testing\n")

        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertAlmostEqual(inputbox.location["x"] + inputbox.size["width"] / 2, 512, delta=10)

