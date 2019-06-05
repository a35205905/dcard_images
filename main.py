import requests
import os

post_id = input('Post Id: ')
if not post_id.isdigit():
    print('Wrong format, please enter again!')
    exit()

res = requests.get('https://www.dcard.tw/_api/posts/{}'.format(post_id))
if not res.ok:
    print('Can not find post!')
    exit()

# 建立存放圖檔目錄
path = os.path.join('images', post_id)
if not os.path.isdir('images'):
    os.mkdir('images')
if not os.path.isdir(path):
    os.mkdir(path)

post_title = res.json().get('title')
post_media = res.json().get('media')
# 文章不含圖片
if post_media is None or len(post_media) <= 0:
    print('This article has no pictures!')
    exit()

print(post_title)
for media in post_media:
    url = media.get('url')
    if url is None:
        continue
    res = requests.get(url)
    if not res.ok:
        continue

    # wb 以二進位方式寫入並產生圖檔
    name = url.split('/')[-1]
    with open(os.path.join(path, '{}-{}'.format(post_id, name)), 'wb') as f:
        f.write(res.content)

    print('{} success.'.format(url))
print('Download finish!')