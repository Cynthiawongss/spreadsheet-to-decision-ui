/** Offline example checks. Requires Playwright and Chromium (or an explicit executable). */
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const output = path.join(root, 'output/browser');
const pages = {
  finance: 'skills/spreadsheet-to-decision-ui/examples/profit-vs-cash'
};
async function run() {
  fs.mkdirSync(output, {recursive:true});
  const browser = await chromium.launch({headless:true, executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || undefined});
  const results=[];
  try {
    for (const [device,width,height] of [['desktop',1280,900],['mobile',390,844]]) {
      for (const [name,folder] of Object.entries(pages)) for (const lang of ['en','zh-CN']) {
        const context=await browser.newContext({viewport:{width,height},hasTouch:device==='mobile'});
        const network=[],errors=[];
        await context.route(/^https?:\/\//,route=>{network.push(route.request().url());return route.abort();});
        const page=await context.newPage();page.on('pageerror',e=>errors.push(String(e)));
        await page.goto(pathToFileURL(path.join(root,folder,lang==='en'?'index.html':'index.zh-CN.html')).href);
        assert.equal(await page.locator('html').getAttribute('lang'),lang);
        assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`overflow ${name}/${lang}/${device}`);
        const checks=['no horizontal overflow','no JavaScript exceptions','no external network requests'];
        if(name==='reference') {
          await page.evaluate(()=>{window.passEvents=[];document.addEventListener('pass-change',e=>passEvents.push(e.detail));});
          await page.locator('input[value=violet]').check();await page.locator('#choose').click();
          assert((await page.locator('#status').innerText()).includes(lang==='en'?'Dusk violet':'暮紫'));
          assert(await page.locator('#choose').isDisabled());
          await page.locator('input[value=blue]').check();
          assert((await page.locator('#status').innerText()).includes(lang==='en'?'Ocean blue':'海蓝'));
          await page.locator('#reset').click();assert(await page.locator('#reset').isDisabled());
          assert.equal(await page.evaluate(()=>passEvents.length),4);
          await page.locator('#choose').focus();await page.keyboard.press('Enter');assert(await page.locator('#choose').isDisabled());
          await page.locator('#reset').click();
          await page.emulateMedia({reducedMotion:'reduce'});await page.locator('#card').hover();
          assert.equal(await page.locator('#card').evaluate(e=>getComputedStyle(e).transform),'none');
          await page.reload();assert(await page.locator('#reset').isDisabled());assert(await page.locator('input[value=blue]').isChecked());
          checks.push('finish and selection state','event contract','keyboard activation','reduced motion','reload resets local state');
        } else if(name==='finance') {
          assert.equal(await page.locator('#profit').innerText(),'$300');assert.equal(await page.locator('#cash').innerText(),'$300');
          const slider=page.locator('#collections');
          await slider.evaluate(e=>{e.value='1000';e.dispatchEvent(new Event('input',{bubbles:true}));});
          assert.equal(await page.locator('#cash').innerText(),'$700');assert.equal(await page.locator('#receivables').innerText(),'$0');assert.equal(await page.locator('#profit').innerText(),'$300');
          await slider.evaluate(e=>{e.value='0';e.dispatchEvent(new Event('input',{bubbles:true}));});
          assert.equal(await page.locator('#cash').innerText(),'−$300');assert((await page.locator('#funding').innerText()).includes(lang==='en'?'Funding gap':'资金缺口'));
          await page.locator('#reset').click();assert.equal(await slider.inputValue(),'600');
          await slider.focus();await page.keyboard.press('ArrowRight');assert.equal(await slider.inputValue(),'650');await page.locator('#reset').click();
          checks.push('collections change cash but not profit','visible negative cash','reset','keyboard slider');
        } else {
          for(let i=0;i<3;i++) {
            const button=page.locator(`[data-segment="${i}"]`);await button.click();assert.equal(await button.getAttribute('aria-pressed'),'true');
            assert.equal(await page.locator('.beat').count(),3);assert((await page.locator('#prompt').textContent()).length>500);
          }
          assert((await page.locator('#closing').innerText()).includes('room 12'));
          await page.locator('[data-segment="0"]').focus();await page.keyboard.press('Enter');assert.equal(await page.locator('[data-segment="0"]').getAttribute('aria-pressed'),'true');
          checks.push('three segment views','copyable prompt text','keyboard segment selection');
        }
        assert.deepEqual(errors,[]);assert.deepEqual(network,[]);
        const file=`${name}-${lang}-${device}.png`;
        await page.screenshot({path:path.join(output,file),fullPage:true});
        results.push({page:name,language:lang,device,viewport:[width,height],checks,passed:true,screenshot:file});
        await context.close();
      }
    }
  } finally {await browser.close();}
  fs.writeFileSync(path.join(output,'results.json'),JSON.stringify(results,null,2)+'\n');
  console.log(`Passed ${results.length} page/language/viewport checks.`);
}
run().catch(e=>{console.error(e);process.exitCode=1;});
