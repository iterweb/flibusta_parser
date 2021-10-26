import requests
from bs4 import BeautifulSoup


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931',
}


class Parser:

    def __init__(self):
        self.site = "http://flibusta.is"

    def get_html(self, url):
        resp = requests.get(url=url, headers=header)
        if resp.status_code == 200:
            return resp.content
        else:
            return resp.status_code

    def get_books(self, html, page=False):
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find("div", id="main")
        if page:
            books = []
            title = soup.find("h1", class_="title").text
            for link in div.find_all("a"):
                if str(link['href']).startswith("/b/") and not str(link['href']).endswith("/read"):
                    books.append(self.site + link['href'])
            print(f"{title} -> " + " | ".join(books))
        else:
            books_url = []
            for a in div.find_all('li'):
                for link in a.find_all('a'):
                    if str(link['href']).startswith("/b/"):
                        books_url.append(self.site + link['href'])
            return books_url

    def get_book_links(self, links):
        for link in links:
            resp = self.get_html(link)
            self.get_books(resp, True)

    def parsing(self):
        while True:
            search = input(str("Enter the title of the book: ")).strip().lower().replace(" ", "+")
            if search == "!quit":
                break
            else:
                url = f"{self.site}/booksearch?ask={search}&chb=on"
                html = self.get_html(url=url)
                links = self.get_books(html)
                if len(links) != 0:
                    self.get_book_links(links)
                else:
                    print("The book not found!")


if __name__ == "__main__":
    pars = Parser()
    pars.parsing()
