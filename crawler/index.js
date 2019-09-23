const puppeteer = require("puppeteer");
const $console = require("../helper/console");
const utils = require("../helper/utils");

const site = "https://www.duitang.com";
const keyword = "周杰伦";

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  $console.success(`OK, start go into ${site} ...`);
  await page.goto(site);
  await page.waitFor("#kw");
  $console.success(`start write keyword "${keyword}" ...`);
  writeKeyword(page);
  async function writeKeyword(page) {
    await page.type("#kw", keyword, { delay: 20 });
    await page.click("#dt-search form button", { delay: 20 });
    $console.success("start search...");
    getSearchResult(page);
  }
  async function getSearchResult(page) {
    await utils.waitForLoaded(page);
    $console.success('go into search page success.')
    const pictureWrapper = await page.$("#woo-holder");
    console.log("result: ", pictureWrapper);
  }
})();
