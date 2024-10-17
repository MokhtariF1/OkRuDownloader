# from playwright.sync_api import sync_playwright
# import config
# import json


# def download(url, quality):
#     with sync_playwright() as p:
#         download_url = None
#         if quality not in config.quality:
#             # return json.dumps({"status": 400, "message": "quality invalid!", "code": 2})
#             return 400
#         else:
#              downloads = {
#                  "mobile": config.mobile,
#                  "lowest": config.lowest,
#                  "low": config.low,
#                  "sd": config.sd,
#                  "hd": config.hd,
#              }
#              download_url = downloads[quality]
#         browser = p.chromium.launch(headless=True)  # تغییر به headless=True برای حالت مخفی
#         context = browser.new_context(accept_downloads=True)  # فعال کردن دانلودها
#         page = browser.new_page()
#         page.goto(config.website_url)
#         print(page.title())
#         page.get_by_placeholder("Paste a video URL").fill(url)
#         # اطمینان از بارگذاری دکمه دانلود
#         page.get_by_role("button", name="Download", exact=True).click()
        
#         # صبر برای بارگذاری صفحه جدید
#         page.wait_for_timeout(3000)  # مدت زمان انتظار بیشتر

#         # انتظار برای دانلود
#         with page.expect_download() as download_info:
#         # رفتن به لینک دانلود
#             try:
#                 page.goto(download_url)
#             except:
#                 pass
#             page.on('download', lambda download: print(f'Download started: {download.path}'))
#         # دریافت اطلاعات دانلود
#         download = download_info.value
#         # print(download.path())
#         # ذخیره فایل دانلود شده
#         download.save_as(f"files/{download.suggested_filename}")
        
#         print(f"File downloaded as: {download.suggested_filename}")
        
#         context.close()
#         return {"status": 200, "message": "downloaded", "code": 1, "path": f"files/{download.suggested_filename}"}

from playwright.async_api import async_playwright
import config
import time
import subprocess


async def download(url, quality):
    # async with async_playwright() as p:
    download_url = None
    if quality not in config.quality:
        return {"status": 400, "message": "error in quality", "code": 2}
    else:
        downloads = {
            "mobile": 240,
            "lowest": 360,
            "low": 480,
            "sd": 720,
            "hd": 1080,
        }
        quality = downloads[quality]
        video_url = url
        custom_quality = f"bestvideo[height<={quality}]+bestaudio/best"
        file_name = f"{int(time.time())}"
        command = f'yt-dlp -f "{custom_quality}" -o "files/{file_name}.mp4" {video_url}'
        subprocess.call(command, shell=True)

        # browser = await p.chromium.launch(headless=True)
        # context = await browser.new_context(accept_downloads=True)
        # page = await context.new_page()
        # await page.goto(config.website_url)
        # print(await page.title())
        # await page.locator('[placeholder="Paste a video URL"]').fill(url)
        # await page.locator('button >> text="Download"').click()
        #
        # await page.wait_for_timeout(3000)
        #
        # async with page.expect_download() as download_info:
        #     try:
        #         await page.goto(download_url)
        #     except:
        #         pass
        #     #page.on('download', lambda download: print(f'Download started: {download.path}'))
        #
        # download = await download_info.value
        # download_path = f"files/{download.suggested_filename}"
        # await download.save_as(download_path)
        #
        # print(f"File downloaded as: {download.suggested_filename}")
        #
        # await context.close()
        return {"status": 200, "message": "downloaded", "code": 1, "path": f"{file_name}.mp4"}
