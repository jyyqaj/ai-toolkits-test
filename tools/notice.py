import requests
notice_url = 'https://xz.wps.cn/api/v1/webhook/send?key=7a49df3fa9ec89941263e9abf50e52ff'


def send_test_process_info_by_webhook(test_result, test_time, test_business_type):
    notify = {
        "msgtype": "markdown",
        "markdown": {
            "title": "测试进度",
            "text": "### <font color='DarkRed'>测试进度</font>\n"
                    f"- <font color='black'>测试结果：</font><font color='#34495e'>{test_result}</font>\n\n"
                    f"- <font color='black'>测试时间：</font><font color='#34495e'>{test_time}</font>\n\n"
                    f"- <font color='black'>测试业务：</font><font color='#34495e'>{test_business_type}</font>\n\n"
        }
    }
    requests.post(notice_url, json=notify)