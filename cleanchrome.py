import psutil


if __name__ == '__main__':
    i= 0
    for ids in psutil.pids():
        try:
            p = psutil.Process(ids)
            if p.cwd() == "C:\\Users\\gaqu\\AppData\\Local\\pyppeteer\\pyppeteer\\local-chromium\\588429\\chrome-win32":
                i += 1
                p.kill()
        except:
            pass
    print("killed", i, "chrome")


