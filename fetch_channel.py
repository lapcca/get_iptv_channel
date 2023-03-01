from bs4 import BeautifulSoup
import requests as req


def parse(contents):
    datas = []
    soup = BeautifulSoup(contents, 'lxml')
    table = soup.find_all("table")[0]
    for tr in table.find_all("tr"):
        tds = tr.find_all("td")
        index = tds[0].getText()
        channel_name = tds[1].getText()
        multicast_address = tds[2].getText()
        replay_days = tds[3].getText()
        channel_id = tds[4].getText()
        comments = tds[5].getText()
        replay_address = tds[6].getText()
        datas.append({
            "index": index,
            "channel_name": channel_name,
            "multicast_address": multicast_address,
            "replay_days": replay_days,
            "channel_id": channel_id,
            "comments": comments,
            "replay_address": replay_address,
        })
    # remove the header
    datas = datas[1:]
    return datas


def fetch_content_from_net():
    resp = req.get("http://epg.51zmt.top:8000/sctvmulticast.html")
    return resp.content.decode("utf-8")


def fetch_content_from_file():
    f = open("C:\\Users\\qinz1\\OneDrive - Dell Technologies\Desktop\\fetch_\\test.html", "r", encoding='utf8')
    contents = f.read()
    f.close()
    return contents


def write_m3u_file(channel_list):
    with open("iptv.m3u", "w", encoding='utf-8') as f:
        f.write('#EXTM3U name="四川电信IPTV"\n')
        for chl in channel_list:
            f.write('#EXTINF:-1,{}\n'.format(chl["channel_name"]))
            f.write('http://192.168.1.253:5555/rtp/{}\n'.format(chl["multicast_address"]))
            f.write('\n')


def main():
    net_content = fetch_content_from_net()
    data = parse(net_content)
    # data = parse(fetch_content_from_file())
    write_m3u_file(data)


if __name__ == "__main__":
    main()
