const puppeteer = require("puppeteer");
const $console = require("../helper/console");
const utils = require("../helper/utils");

const site = "https://www.duitang.com";
const keyword = "周杰伦";

const devices = require("puppeteer/DeviceDescriptors");

(async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  $console.success(`开始进入 ${site}`);
  await page.goto(site);
  $console.success(`${site} 页面加载完毕`);
  try {
    await page.click(".mask-body .tt-s a");
  } catch {
    $console.warning("已登录，没有登录弹窗");
  }
  writeKeyword(page);
  async function writeKeyword(page) {
    await page.type("#kw", keyword, { delay: 20 });
    $console.success(`在搜索框输入关键词 "${keyword}" ...`);
    await page.evaluate(() => {
      document.querySelector("#dt-search>form>button").click();
    });
    $console.success("开始搜索 ...");
    operateSearchResult(page);
  }
  async function operateSearchResult(page) {
    await utils.waitForLoaded(page);
    $console.success("go into search page success.");
    for (let i = 0; i < 100; i++) {
      console.log('切换页面开始')
      await new Promise(resolve => {
        setTimeout(() => {
          resolve();
        }, 5000);
      });
      console.log('切换页面结束')
      await page.evaluate(async () => {
        let output = [];
        let hasMore = true;
        let lastLength = 0;
        let currentLength = 0;
        for (let i = 0; hasMore; i++) {
          const elementList = document.querySelectorAll(
            "#woo-holder>.woo-swb.woo-cur>div:nth-of-type(2) .woo"
          );
          const length = elementList.length;
          currentLength = length;
          if (lastLength === currentLength) {
            hasMore = false;
          }

          const data = Array.from(elementList)
            .slice(lastLength)
            .map(element => {
              const info_wrapper = element.querySelector(".wooscr");
              const user_wrapper = info_wrapper.querySelector("ul");
              const user_info = user_wrapper.querySelector("li>p>a");
              const album_info = user_wrapper.querySelector("li>p>span");
              const pop_info = info_wrapper.querySelector(".d");
              return {
                detail_page: element.querySelector(".a").href,
                image: element.querySelector(".a>img").src,
                image_name: info_wrapper.querySelector(".g").innerText,
                user_name: user_info.innerText,
                user_page: user_info.href,
                user_avatar: user_wrapper.querySelector("li>a>img").src,
                album_page: album_info.querySelector("a").href,
                album_name: album_info.querySelector("a").innerText,
                like_count: pop_info.querySelector(".d2>span").innerText,
                collect_count: pop_info.querySelector(".d1>span").innerText
              };
            });
          output = output.concat(data);
          console.log(`第${i + 1}次加载${data.length}条数据`);
          lastLength = currentLength;
          await new Promise(resolve => {
            setTimeout(() => {
              resolve();
            }, 1000);
          });
          const scrollHeight = document.body.scrollHeight;
          window.scrollBy(0, scrollHeight);
          if (document.querySelectorAll(".woo-pager ul li").length) {
            document
              .getElementsByClassName("woo-pager")[0]
              .querySelector("ul>li>a.woo-nxt")
              .click();
              console.log('点击切换')
            return;
          }
          await new Promise(resolve => {
            setTimeout(() => {
              resolve();
            }, 2000);
          });
        }
        console.log(output);
      });
    }
  }
})();
