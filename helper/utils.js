const $console = require("./console");
const utils = {};

utils.isLoaded = async page => {
  await page.waitForNavigation();
  return page.evaluate(() => {
    // document.readyState: loading / 加载；interactive / 互动；complete / 完成
    const isCompleted = document.readyState === "complete";
    return Promise.resolve(isCompleted);
  });
};

utils.waitForLoaded = async (page, retryTimes = 100, delayTime = 20) => {
  return new Promise(async (resolve, reject) => {
    const isLoaded = await utils.isLoaded(page);
    let i = 0;
    while (i < retryTimes && !isLoaded) {
      i++;
      $console.success(`The page is not loaded, retry : ${i}times...`);
      await page.waitFor(delayTime);
      isLoaded = await utils.isLoaded(page);
    }
    if (i >= 100) {
      $console.error("✘ Error: Timeout Exceeded: 30000ms exceeded");
      resolve(false);
    } else {
      resolve(true);
    }
  });
};

module.exports = utils;
