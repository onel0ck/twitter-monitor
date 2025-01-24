#!/usr/bin/env python3
import requests
import time
import logging
from datetime import datetime
from itertools import cycle
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='twitter_monitor.log',
    filemode='a'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

SMS_LOGIN = 'YOUR_LOGIN'
SMS_PASSWORD = 'YOUR_PASSWORD'
SMS_PHONE = 'YOUR_PHONE' # на него будет приходить СМС

#добавьте прокси 
PROXIES = [
    "http://login:password@ip:port",
    "http://login:password@ip:port",
    "http://login:password@ip:port",
    "http://login:password@ip:port"
]

class TwitterMonitor:
    def __init__(self):
        self.last_count = None
        self.proxy_pool = cycle(PROXIES)
        self.base_url = 'https://api.x.com/graphql/MpOINUGH_YVb2BKjYZOPaQ/UserTweets'

    def get_proxy(self):
        return next(self.proxy_pool)

    def get_guest_token(self, proxy):
        try:
            response = requests.post(
                'https://api.x.com/1.1/guest/activate.json',
                headers={
                    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
                },
                proxies={'http': proxy, 'https': proxy},
                timeout=30
            )
            response.raise_for_status()
            return response.json()['guest_token']
        except Exception as e:
            logging.error(f"Error getting guest token: {e}")
            return None

    def get_headers(self, guest_token):
        return {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'content-type': 'application/json',
            'origin': 'https://x.com',
            'referer': 'https://x.com/',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'x-guest-token': guest_token,
            'x-twitter-active-user': 'yes',
            'x-twitter-client-language': 'ru',
            'priority': 'u=1, i'
        }

    def send_sms_notification(self, message):
        url = 'https://smsc.ru/sys/send.php'
        params = {
            'login': SMS_LOGIN,
            'psw': SMS_PASSWORD,
            'phones': SMS_PHONE,
            'mes': f"today {message}"
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            logging.info(f'SMS sent: today {message}')
        except requests.exceptions.RequestException as e:
            logging.error(f'Error sending SMS: {e}')

    def check_status_count(self):
        proxy = self.get_proxy()
        guest_token = self.get_guest_token(proxy)
        if not guest_token:
            return

        params = {
            "userId": "16228398",
            "count": 20,
            "includePromotedContent": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withVoice": True,
            "withV2Timeline": True
        }

        features = {
            "profile_label_improvements_pcf_label_in_post_enabled": True,
            "rweb_tipjar_consumption_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "premium_content_api_read_enabled": False,
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
            "responsive_web_grok_analyze_post_followups_enabled": False,
            "responsive_web_jetfuel_frame": False,
            "responsive_web_grok_share_attachment_enabled": True,
            "articles_preview_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "creator_subscriptions_quote_tweet_preview_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "rweb_video_timestamps_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_grok_image_annotation_enabled": True,
            "responsive_web_enhance_cards_enabled": False
        }

        field_toggles = {
            "withArticlePlainText": False
        }

        url = f"{self.base_url}?variables={json.dumps(params)}&features={json.dumps(features)}&fieldToggles={json.dumps(field_toggles)}"

        try:
            response = requests.get(
                url,
                headers=self.get_headers(guest_token),
                proxies={'http': proxy, 'https': proxy},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            status_count = data.get('data', {}).get('user', {}).get('result', {}).get('timeline_v2', {}).get('timeline', {}).get('instructions', [{}])[1].get('entry', {}).get('content', {}).get('itemContent', {}).get('tweet_results', {}).get('result', {}).get('core', {}).get('user_results', {}).get('result', {}).get('legacy', {}).get('statuses_count')

            if not status_count:
                logging.error('Could not find status count in response')
                return

            logging.info(f"Current status count: {status_count}")

            if self.last_count is None:
                self.last_count = status_count
                return

            if status_count != self.last_count:
                self.send_sms_notification('New tweet detected')
                self.last_count = status_count

        except Exception as e:
            logging.error(f"Error checking Twitter status: {e}")

    def run(self, interval=60):
        logging.info("Starting Twitter status monitoring...")
        while True:
            try:
                self.check_status_count()
                time.sleep(interval)
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                self.send_sms_notification(f'Error in script: {e}')

if __name__ == '__main__':
    monitor = TwitterMonitor()
    monitor.run()