import subprocess
import sys
import importlib

for pkg in ['requests', 'beautifulsoup4']:
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])

import requests
from bs4 import BeautifulSoup
import re
import time
import os
import json
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import logging
from dataclasses import dataclass
import threading

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class Chapter:
    index: int
    title: str
    url: str
    content: str = ''
    downloaded: bool = False
    retry: int = 0


class NovelCrawler:
    def __init__(self, base_url, start_page, end_page, output_dir='download', delay=2, workers=2):
        self.base_url = base_url.rstrip('/')
        self.start_page = start_page
        self.end_page = end_page
        self.output_dir = output_dir
        self.delay = delay
        self.workers = workers
        self.session = requests.Session()
        self.session.headers.update(
            {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36'})
        self.chapters = []
        self.completed = set()
        self.failed = []
        self.lock = threading.Lock()
        self.novel_title = ''
        self.novel_author = ''
        os.makedirs(output_dir, exist_ok=True)
        self.state_file = os.path.join(output_dir, 'state.json')

    def fetch(self, url, retry=3):
        for i in range(retry):
            try:
                time.sleep(self.delay)
                r = self.session.get(url, timeout=10)
                for enc in ['utf-8', 'gbk']:
                    try:
                        r.encoding = enc
                        r.text
                        break
                    except:
                        continue
                return r.text
            except Exception as e:
                logger.error(f'请求失败 {url} ({i + 1}/{retry}): {e}')
                time.sleep(5 * (i + 1))
        return None

    def parse_catalog_pages(self):
        all_chapters = []
        seen_urls = set()
        logger.info(f'遍历目录页 {self.start_page} 到 {self.end_page}')
        for page in range(self.start_page, self.end_page + 1):
            url = f'{self.base_url}_{page}/'
            html = self.fetch(url)
            if not html:
                logger.warning(f'无法获取 {url}')
                continue
            soup = BeautifulSoup(html, 'html.parser')
            if not self.novel_title:
                t = soup.find('h1') or soup.select_one('.title, .book-title')
                self.novel_title = t.get_text().strip() if t else f'小说_{self.start_page}'
            if not self.novel_author:
                a = soup.select_one('.author, .book-author')
                self.novel_author = a.get_text().strip() if a else '未知'
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                text = link.get_text().strip()
                if not href or href.startswith('#') or href.startswith('javascript') or len(text) < 2:
                    continue
                if re.search(r'第[0-9一二三四五六七八九十百千万]+[章回节]', text) or re.search(r'/\d+\.html', href):
                    full = urljoin(url, href)
                    if full in seen_urls:
                        continue
                    seen_urls.add(full)
                    title = re.sub(r'[<>:"/\\|?*]', '', text).strip() or f'第{len(all_chapters) + 1}章'
                    all_chapters.append(Chapter(index=0, title=title, url=full))
        if not all_chapters:
            logger.error('未找到任何章节')
            return False

        def num_key(c):
            m = re.search(r'第\s*(\d+)', c.title)
            if m:
                return int(m.group(1))
            m = re.search(r'/(\d+)', c.url)
            return int(m.group(1)) if m else 0

        all_chapters.sort(key=num_key)
        for i, c in enumerate(all_chapters, 1):
            c.index = i
        self.chapters = all_chapters
        logger.info(f'共发现 {len(self.chapters)} 个章节')
        with open(os.path.join(self.output_dir, 'chapters.txt'), 'w', encoding='utf-8') as f:
            for c in self.chapters:
                f.write(f'{c.index:04d} {c.title}\n{c.url}\n\n')
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file) as f:
                    s = json.load(f)
                if s.get('base') == f'{self.base_url}_{self.start_page}':
                    self.completed = set(s.get('completed', []))
                    logger.info(f'续传进度，已完成 {len(self.completed)} 章')
            except:
                pass
        return True

    def get_content(self, chap):
        html = self.fetch(chap.url)
        if not html:
            return None
        soup = BeautifulSoup(html, 'html.parser')
        for t in soup.find_all(['script', 'style', 'iframe', 'ins', 'noscript', 'footer', 'nav']):
            t.decompose()
        title_tag = soup.find('h1') or soup.select_one('.chapter-title, .title, .article-title')
        if title_tag:
            chap.title = title_tag.get_text().strip()
        content = None
        for sel in ['#content', '.content', '.chapter-content', '.article-content', '.novel-content', '.read-content',
                    'article']:
            elem = soup.select_one(sel)
            if elem:
                content = elem.get_text(separator='\n', strip=True)
                break
        if not content:
            ps = soup.find_all('p')
            lines = [p.get_text().strip() for p in ps if len(p.get_text().strip()) > 20]
            if lines:
                content = '\n\n'.join(lines[:30])
        if content:
            clean = []
            for line in content.split('\n'):
                line = line.strip()
                if line and not any(w in line for w in ['广告', '推荐', '手机阅读', 'www.']):
                    clean.append(line)
            return '\n\n'.join(clean)
        return None

    def download_one(self, chap):
        if chap.downloaded:
            return True
        logger.info(f'下载 [{chap.index}/{len(self.chapters)}] {chap.title}')
        cont = self.get_content(chap)
        if cont:
            chap.content = cont
            chap.downloaded = True
            safe = re.sub(r'[<>:"/\\|?*]', '', chap.title)[:50]
            with open(os.path.join(self.output_dir, f'{chap.index:04d}_{safe}.txt'), 'w', encoding='utf-8') as f:
                f.write(f'{chap.title}\n{"=" * len(chap.title)}\n\n{chap.content}')
            return True
        chap.retry += 1
        return False

    def run(self, max_retry=3):
        if not self.chapters:
            logger.error('无章节可下载')
            return
        total = len(self.chapters)
        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            fut_to_chap = {}
            for c in self.chapters:
                if c.index not in self.completed:
                    fut_to_chap[ex.submit(self.download_one, c)] = c
            done = len(self.completed)
            for fut in as_completed(fut_to_chap):
                c = fut_to_chap[fut]
                try:
                    if fut.result():
                        with self.lock:
                            self.completed.add(c.index)
                            done += 1
                            logger.info(f'进度 {done}/{total} ({done / total * 100:.1f}%)')
                            if done % 5 == 0:
                                self.save_state()
                    else:
                        self.failed.append(c)
                except:
                    self.failed.append(c)
        for retry in range(max_retry):
            if not self.failed:
                break
            logger.info(f'重试第 {retry + 1} 次，剩余 {len(self.failed)} 章')
            still = []
            for c in self.failed:
                if c.retry < max_retry and self.download_one(c):
                    self.completed.add(c.index)
                else:
                    still.append(c)
                time.sleep(self.delay * 2)
            self.failed = still
        self.save_state()
        self.make_book()
        self.report()

    def save_state(self):
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump({
                'base': f'{self.base_url}_{self.start_page}',
                'completed': list(self.completed),
                'failed': [{'index': c.index, 'title': c.title, 'url': c.url} for c in self.failed]
            }, f, ensure_ascii=False, indent=2)

    def make_book(self):
        name = re.sub(r'[<>:"/\\|?*]', '', self.novel_title)
        path = os.path.join(self.output_dir, f'{name}_全集.txt')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f'书名：{self.novel_title}\n作者：{self.novel_author}\n来源：{self.base_url}\n')
            f.write(f'下载：{datetime.now()}\n章节：{len(self.completed)}/{len(self.chapters)}\n\n')
            for c in sorted(self.chapters, key=lambda x: x.index):
                if c.downloaded:
                    f.write(f'\n\n{c.title}\n{"=" * len(c.title)}\n\n{c.content}\n{"-" * 40}\n')

    def report(self):
        with open(os.path.join(self.output_dir, 'report.txt'), 'w', encoding='utf-8') as f:
            f.write(f'书名：{self.novel_title}\n作者：{self.novel_author}\n')
            f.write(f'总章节：{len(self.chapters)}\n成功：{len(self.completed)}\n失败：{len(self.failed)}\n')
            if self.failed:
                f.write('失败列表：\n')
                for c in self.failed:
                    f.write(f'  {c.index:04d} {c.title}\n    {c.url}\n')


if __name__ == '__main__':
    print('=' * 50)
    print('小说爬虫（自动遍历分页）')
    print('=' * 50)
    base = input('请输入基础URL (例如 http://m.shnpxl.com/cnew/528888 ): ').strip()
    if not base:
        base = 'http://m.shnpxl.com/cnew/528888'
    start = input('起始页码 (默认34): ').strip()
    start = int(start) if start.isdigit() else 34
    end = input('结束页码 (默认54): ').strip()
    end = int(end) if end.isdigit() else 54
    out = input('输出目录 (默认download): ').strip() or 'download'
    workers = input('线程数 (默认2): ').strip()
    workers = int(workers) if workers.isdigit() else 2
    delay = input('延迟秒数 (默认2): ').strip()
    delay = float(delay) if delay.replace('.', '').isdigit() else 2.0

    crawler = NovelCrawler(base, start, end, out, delay, workers)
    if crawler.parse_catalog_pages():
        crawler.run()
        print(f'\n完成！文件保存在 {os.path.abspath(out)}')
