__author__ = 'bobby'
import requests
from scrapy.selector import Selector
import pymysql
import time

conn = pymysql.connect(host="127.0.0.1", user="root", passwd="root", db="xici", charset="utf8")
cursor = conn.cursor()


def crawl_ips():
    #爬取西刺的免费ip代理
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    for i in range(15):
        re = requests.get("http://www.httpsdaili.com/?stype=1&page={0}".format(i), headers=headers)

        selector = Selector(text=re.text)
        all_trs = selector.xpath("//tr[class='odd']")
        ip_list = []
        for tr in all_trs:
            print(tr)
            # speed_str = tr.css(".td").extract()[0]
            # if speed_str:
            #     speed = float(speed_str.split("秒")[0])
            # all_texts = tr.css("td::text").extract()

        #     ip = all_texts[0]
        #     port = all_texts[1]
        #     proxy_type = all_texts[5]
        #
        #     ip_list.append((ip, port, proxy_type, speed))
        #     ip_list.append(ip)
        #
        # for ip_info in ip_list:
        #     # f = open("list1.txt", "ab")
        #     # f.write(ip_info.encode("utf-8"))
        #     # f.close()
        #     cursor.execute(
        #         "insert ip_list(ip, port, speed, proxy_type) VALUES('{0}', '{1}', {2}, 'HTTP')".format(
        #             ip_info[0], ip_info[1], ip_info[3]
        #         )
        #     )
        #
        #     conn.commit()


class GetIP(object):
    def delete_ip(self, ip):
        #从数据库中删除无效的ip
        delete_sql = """
            delete from ip_list where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port):
        #判断ip是否可用
        http_url = "http://ip.chinaz.com/getip.aspx"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http": proxy_url,
            }
            # s = requests.session()
            # s.config['keep_alive'] = False
            response = requests.get(http_url, timeout=1, proxies=proxy_dict)
        except Exception as e:
            print("invalid ip and port e")
            self.delete_ip(ip)
            time.sleep(5)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print("effective ip")
                return True
            else:
                print ("invalid ip and port a")
                self.delete_ip(ip)
                return False


    def get_random_ip(self):
        #从数据库中随机获取一个可用的ip
        random_sql = """
              SELECT ip, port FROM ip_list
            ORDER BY RAND()
            LIMIT 1
            """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]

            judge_re = self.judge_ip(ip, port)
            if judge_re:
                return "http://{0}:{1}".format(ip, port)
            else:
                return self.get_random_ip()



# print (crawl_ips())
if __name__ == "__main__":
    # crawl_ips()
    get_ip = GetIP()
    get_ip.get_random_ip()