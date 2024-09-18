import unittest
from unittest.mock import patch, mock_open
import datetime
import os
import typer

# Import module for testing
import main as main_module

# Now we can reference the functions from the module for the test cases
class TestMain(unittest.TestCase):

    def test_check_start_with_http_valid_url(self):
        # Test with a valid URL
        try:
            main_module.validate_url("http://example.com")
            main_module.validate_url("https://example.com")
        except typer.Exit:
            self.fail("check_start_with_http() raised Exit unexpectedly!")

    def test_check_start_with_http_invalid_url(self):
        # Test with an invalid URL
        with self.assertRaises(typer.Exit):
            main_module.validate_url("example.com")

    def test_get_number_of_links(self):
        # Test counting <a> tags
        html = "<a href='link1'></a><a href='link2'></a>"
        self.assertEqual(main_module.get_number_of_links(html), 2)

    def test_get_number_of_images(self):
        # Test counting <img> tags
        html = "<img src='image1'><img src='image2'>"
        self.assertEqual(main_module.get_number_of_images(html), 2)

    def test_get_site_name(self):
        # Test removing http/https
        self.assertEqual(main_module.get_site_name("http://example.com"), "example.com")
        self.assertEqual(
            main_module.get_site_name("https://example.com"), "example.com"
        )

    @patch("os.path.exists")
    @patch("os.path.getmtime")
    def test_get_modified_time_existing_file(self, mock_getmtime, mock_exists):
        # Test modified time for an existing file
        mock_exists.return_value = True
        mock_time = datetime.datetime(2023, 1, 1)
        mock_getmtime.return_value = mock_time.timestamp()

        result = main_module.get_modified_time("testfile.html")
        self.assertEqual(result, mock_time)

    @patch("os.path.exists")
    def test_get_modified_time_non_existing_file(self, mock_exists):
        # Test modified time for a non-existing file
        mock_exists.return_value = False
        now = datetime.datetime.now()

        result = main_module.get_modified_time("non_existing_file.html")
        self.assertAlmostEqual(result, now, delta=datetime.timedelta(seconds=1))

    @patch("builtins.open", new_callable=mock_open)
    def test_write_to_file(self, mock_open_file):
        # Test writing to a file
        filename = "testfile.html"
        html_content = "<html></html>"

        main_module.write_to_file(filename, html_content)
        mock_open_file.assert_called_once_with(filename, "w", encoding="utf-8")
        mock_open_file().write.assert_called_once_with(html_content)


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
