# -*- coding: utf-8 -*-
#
# author: oldj <oldj.wu@gmail.com>
#

from selenium import webdriver
import time


def capture(url, save_fn="capture.png"):
    browser = webdriver.Chrome()
    #browser = webdriver.Firefox() # Get local session of firefox
    browser.set_window_size(1200, 900)
    page = browser.get(url) # Load page

    browser.file_detector_context("￥")

    print browser.file_detector_context("419")

    browser.execute_script("""
    (function () {
      var y = 0;
      var step = 100;
      window.scroll(0, 0);

      function f() {
        if (y < document.body.scrollHeight) {
          y += step;
          window.scroll(0, y);
          setTimeout(f, 50);
        } else {
          window.scroll(0, 0);
          document.title += "scroll-done";
        }
      }

      setTimeout(f, 1000);
    })();
    """)

    # for i in xrange(30):
    #     if "scroll-done" in browser.title:
    #         break
    # time.sleep(1)

    browser.save_screenshot(save_fn)
    browser.close()


if __name__ == "__main__":
    capture("https://item.jd.com/2724021.html?jd_pop=731b8b9b-c1da-417e-9976-04f4ce649bc1&abt=0")