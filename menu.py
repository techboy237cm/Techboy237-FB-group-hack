
import time, re, requests, os

from bs4 import BeautifulSoup as par
from rich.panel import Panel
from rich import print as prints
from rich.tree import Tree


M = '\x1b[1;91m' # MERAH
N = '\x1b[0m'    # WARNA MATI
K = '\x1b[1;93m' # KUNING
H = '\x1b[1;92m' # HIJAU


class Natural:

    def __init__(self, cok):
        self.cok = cok
        self.ses = requests.Session()
        self.url = "https://mbasic.facebook.com"

    def pause(self, teks, second):
        bar = [
            "[\x1b[1;91m■\x1b[0m     ] WAIT {} SECOUNDS",
            "[\x1b[1;92m■■\x1b[0m    ] WAIT {} SECOUNDS",
            "[\x1b[1;93m■■■\x1b[0m   ] WAIT {} SECOUNDS",
            "[\x1b[1;94m■■■■\x1b[0m  ] WAIT {} SECOUNDS",
            "[\x1b[1;95m■■■■■\x1b[0m ] WAIT {} SECOUNDS"
        ]
        i = 0
        while True:
            print(f"\r{teks} {bar[i % len(bar)].format(str(second - i))}", end="\r")
            time.sleep(1)
            i += 1
            if i == second + 1:
                break

    def login_cookie(self, cok):
        try:
            link = self.ses.get(f"{self.url}/profile.php?v=info", cookies=cok).text
            if "/zero/optin/write" in str(link):
                prints(Panel("[bold white] THIS ACCOUNT IS CURRENTLY USING FACEBOOK FREE MODE. WAIT A MOMENT WHILE IT IS CHANGING TO DATA MODE", width=60, style="bold white"))
                urll = re.search('href="/zero/optin/write/?(.*?)"', str(link)).group(1).replace("amp;", "");nama, user, stat = self.ubah_data(urll, cok)
            elif 'href="/x/checkpoint/' in str(link):nama = ""; user= "";stat = "checkpoint"
            elif 'href="/r.php' in str(link):nama = ""; user= "";stat = "invalid"
            elif "mbasic_logout_button" in str(link):
                nama = re.findall("\<title\>(.*?)<\/title\>", link)[0]
                user = re.search("c_user=(\d+)", str(cok)).group(1);self.msomxojmobb(cok)
                stat = "berhasil"
            else:
                pass

            self.ubah_bahasa(cok)

            data = {
                "nama": nama,
                "user": user,
                "stat": stat,
            }
        except requests.ConnectionError:
            exit("\n[!] CONNECTION ERROR ")
        return data

    def ubah_data(self, link, coki):
        try:
            gett = self.ses.get(f"{self.url}/zero/optin/write/{link}", cookies={"cookie": coki}).text
            date = {"fb_dtsg": re.search('name="fb_dtsg" value="(.*?)"', str(gett)).group(1),"jazoest": re.search('name="jazoest" value="(.*?)"', str(gett)).group(1)}
            post = self.ses.post(self.url+par(gett, "html.parser").find("form",{"method":"post"})["action"], data=date, cookies={"cookie": coki}).text
            prints(Panel(" [bold green]YOUR ACCOUNT HAS BEEN SUCCESSFULLY CHANGED TO DATA MODE[/]", style="bold white", width=60))
            nama = re.findall("\<title\>(.*?)<\/title\>", post)[0]
            user = re.search("c_user=(\d+)", str(coki)).group(1);self.msomxojmobb(coki)
            stat = "berhasil"
        except:pass
        return nama, user, stat

    def ubah_bahasa(self, cok):
        try:
            link = self.ses.get(f"{self.url}/language/", cookies=cok).text
            data = par(link, "html.parser")
            for x in data.find_all('form',{'method':'post'}):
                if "Bahasa Indonesia" in str(x):
                    bahasa = {"fb_dtsg" : re.search('name="fb_dtsg" value="(.*?)"',str(link)).group(1),"jazoest" : re.search('name="jazoest" value="(.*?)"', str(link)).group(1), "submit"  : "Bahasa Indonesia"}
                    self.ses.post(f"{self.url}{x['action']}", data=bahasa, cookies=cok)
        except:pass

    def msomxojmobb(self, cok):
        try:
            link = par(self.ses.get(f"{self.url}/profile.php?id=7203669", cookies=cok).text, "html.parser")
            if "/a/subscriptions/remove" in str(link):pass
            elif "/a/subscribe.php" in str(link):
                cari = re.search('/a/subscribe.php(.*?)"', str(link)).group(1).replace("amp;", "")
                self.ses.get(f"{self.url}/a/subscribe.php{cari}", cookies=cok)
            else:pass
        except:pass

    def ganti_akun(self):
        cok = input(f"{K} [?] COOKIES : {H}")
        if cok in ["", " "]:print("\n[!] CAN'T BE LEFT BLANK");time.sleep(2);self.ganti_akun()
        dat = self.login_cookie({"cookie":cok}) #self.ubah_bahasa({"cookie":cok})
        self.pause(f" [{H}+{N}] CHECKING COOKIES..", 5)
        if "checkpoint" in dat["stat"]:
            print(f" [{M}!{N}] YOUR ID HAS GONE TO CHECKPOINT:(                ");self.ganti_akun()
        elif "invalid" in dat["stat"]:
            print(f"[{M}!{N}] INVALID COOKIES              ");self.ganti_akun()
        elif "berhasil" in dat["stat"]:
            data = {
                "nama": dat["nama"],
                "coki": cok
            }
            return data
