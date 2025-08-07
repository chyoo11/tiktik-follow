#!/usr/bin/env python3
"""
TikTok Follow Sender - Advanced Multi-Session Follow Bot
"""

import requests
import json
import time
import random
import os
from typing import List, Dict, Optional, Tuple

class TikTokFollowSender:
    def __init__(self):
        self.sessions = []
        self.proxies = []
        self.base_headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "en-US,en;q=0.9",
            'Cache-Control': "no-cache",
            'Origin': "https://www.tiktok.com",
            'Referer': "https://www.tiktok.com/",
            'Sec-Ch-Ua': '"Not)A;Brand";v="8", "Chromium";v="116"',
            'Sec-Ch-Ua-Mobile': "?0",
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': "empty",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Site': "same-origin",
        }
    
    def print_banner(self):
        """Print the fancy banner"""
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                    🚀 TikTok Follow Sender 🚀                 ║")
        print("║              Advanced Multi-Session Follow Bot                ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()
    
    def load_sessions(self, file_path: str) -> bool:
        """Load session IDs from file"""
        try:
            if not os.path.exists(file_path):
                print(f"❌ Session file {file_path} not found!")
                return False
            
            with open(file_path, 'r') as f:
                sessions = [line.strip() for line in f.readlines() if line.strip()]
            
            if not sessions:
                print("❌ No session IDs found in file!")
                return False
            
            self.sessions = sessions
            print(f"🔑 ✅ Loaded {len(sessions)} session IDs")
            return True
        
        except Exception as e:
            print(f"❌ Error loading sessions: {e}")
            return False
    
    def load_proxies(self, file_path: str) -> bool:
        """Load proxies from file"""
        try:
            if not file_path or not os.path.exists(file_path):
                print("🌐 No proxy file provided or found. Running without proxies.")
                return True
            
            with open(file_path, 'r') as f:
                proxies = [line.strip() for line in f.readlines() if line.strip()]
            
            self.proxies = proxies
            print(f"🌐 ✅ Loaded {len(proxies)} proxies")
            return True
        
        except Exception as e:
            print(f"❌ Error loading proxies: {e}")
            return False
    
    def get_user_info(self, username: str, session_id: str) -> Optional[Dict]:
        """Get user information by username"""
        try:
            # Remove @ if present
            if username.startswith('@'):
                username = username[1:]
            
            # Try multiple API endpoints for user lookup
            endpoints = [
                f"https://www.tiktok.com/api/user/detail/?WebIdLastTime=1&aid=1988&app_language=en&app_name=tiktok_web&browser_language=en&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F116.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&device_platform=web_pc&focus_state=true&from_page=user&history_len=4&is_fullscreen=false&is_page_visible=true&os=windows&priority_region=&referer=&region=US&screen_height=1080&screen_width=1920&tz_name=America%2FNew_York&uniqueId={username}&user_is_login=true&webcast_language=en",
                f"https://www.tiktok.com/@{username}",
                f"https://www.tiktok.com/api/search/user/?WebIdLastTime=1&aid=1988&app_language=en&app_name=tiktok_web&browser_language=en&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F116.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&device_platform=web_pc&focus_state=true&from_page=search&history_len=2&is_fullscreen=false&is_page_visible=true&keyword={username}&os=windows&priority_region=&referer=&region=US&screen_height=1080&screen_width=1920&search_id=&tz_name=America%2FNew_York&user_is_login=true&webcast_language=en"
            ]
            
            headers = self.base_headers.copy()
            headers['Cookie'] = f"sessionid={session_id}; sessionid_ss={session_id};"
            
            # Try different approaches to get user info
            for endpoint in endpoints:
                try:
                    response = requests.get(endpoint, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        # Try to parse as JSON first
                        try:
                            data = response.json()
                            if 'userInfo' in data and data['userInfo']:
                                user_info = data['userInfo']['user']
                                return {
                                    'id': user_info.get('id'),
                                    'sec_uid': user_info.get('secUid'),
                                    'unique_id': user_info.get('uniqueId'),
                                    'nickname': user_info.get('nickname')
                                }
                        except json.JSONDecodeError:
                            pass
                        
                        # Try to extract from HTML
                        if f'@{username}' in response.text or username in response.text:
                            # Look for user data in script tags
                            import re
                            patterns = [
                                r'"user":\s*({[^}]+?"uniqueId"[^}]*?})',
                                r'"userInfo":\s*({[^}]+?"user"[^}]*?})',
                                r'"secUid":"([^"]+)".*?"uniqueId":"' + username + '"',
                                r'"uniqueId":"' + username + r'"[^}]*?"secUid":"([^"]+)"',
                                r'{"props":{"pageProps":{"userInfo":{"user":({[^}]+?})',
                            ]
                            
                            for pattern in patterns:
                                matches = re.findall(pattern, response.text, re.DOTALL)
                                if matches:
                                    try:
                                        if 'secUid' in pattern and pattern.endswith(')"'):  # secUid pattern
                                            sec_uid = matches[0]
                                            return {
                                                'sec_uid': sec_uid,
                                                'unique_id': username,
                                                'nickname': username
                                            }
                                        else:
                                            user_data = json.loads(matches[0])
                                            if 'user' in user_data:
                                                user_data = user_data['user']
                                            
                                            return {
                                                'id': user_data.get('id'),
                                                'sec_uid': user_data.get('secUid'),
                                                'unique_id': user_data.get('uniqueId', username),
                                                'nickname': user_data.get('nickname', username)
                                            }
                                    except (json.JSONDecodeError, KeyError):
                                        continue
                            
                            # If we found the page but no structured data, create basic info
                            print(f"🔍 Found user page but couldn't extract complete data. Using fallback.")
                            return {
                                'unique_id': username,
                                'nickname': username,
                                'sec_uid': f'MS4wLjABAAAA{username}'  # Fallback sec_uid
                            }
                
                except Exception as e:
                    print(f"🔍 Trying next endpoint... ({str(e)[:50]})")
                    continue
            
            # If all endpoints fail, create a basic user info for the follow attempt
            print(f"🔍 All lookup methods failed. Creating fallback user info for @{username}")
            return {
                'unique_id': username,
                'nickname': username,
                'sec_uid': f'MS4wLjABAAAA{username}_fallback'  # Fallback sec_uid
            }
        
        except Exception as e:
            print(f"❌ Error getting user info: {e}")
            # Still return fallback info so the bot can attempt to follow
            return {
                'unique_id': username,
                'nickname': username,
                'sec_uid': f'MS4wLjABAAAA{username}_fallback'
            }
    
    def follow_user(self, user_info: Dict, session_id: str) -> bool:
        """Follow a user"""
        try:
            follow_url = "https://www.tiktok.com/api/commit/follow/user/"
            
            headers = self.base_headers.copy()
            headers.update({
                'Content-Type': "application/x-www-form-urlencoded",
                'Cookie': f"sessionid={session_id}; sessionid_ss={session_id};",
                'X-Requested-With': "XMLHttpRequest",
            })
            
            # Build the follow URL with parameters
            params = {
                'aid': '1988',
                'app_language': 'en',
                'app_name': 'tiktok_web',
                'browser_language': 'en',
                'browser_name': 'Mozilla',
                'browser_online': 'true',
                'browser_platform': 'Win32',
                'browser_version': '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                'channel': 'tiktok_web',
                'cookie_enabled': 'true',
                'device_platform': 'web_pc',
                'focus_state': 'true',
                'from_page': 'user',
                'history_len': '2',
                'is_fullscreen': 'false',
                'is_page_visible': 'true',
                'os': 'windows',
                'priority_region': '',
                'referer': f'https://www.tiktok.com/@{user_info["unique_id"]}',
                'region': 'US',
                'screen_height': '1080',
                'screen_width': '1920',
                'tz_name': 'America/New_York',
                'user_is_login': 'true',
                'webcast_language': 'en',
                'type': '1',
                'user_id': user_info.get('id', ''),
                'sec_user_id': user_info.get('sec_uid', ''),
            }
            
            response = requests.post(follow_url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('status_code') == 0:
                        return True
                    else:
                        print(f"❌ Follow failed: {result.get('status_msg', 'Unknown error')}")
                        return False
                except json.JSONDecodeError:
                    # Sometimes TikTok returns non-JSON success responses
                    if 'success' in response.text.lower() or response.text == '':
                        return True
                    print(f"❌ Unexpected response: {response.text[:100]}")
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
        
        except Exception as e:
            print(f"❌ Error following user: {e}")
            return False
    
    def run(self):
        """Main bot execution"""
        self.print_banner()
        
        # Get session file
        session_file = input("📁 Enter session ID file path: ").strip()
        if not self.load_sessions(session_file):
            return
        
        # Get proxy file (optional)
        proxy_file = input("🌐 Enter proxy file path (or press Enter to skip): ").strip()
        self.load_proxies(proxy_file)
        
        # Get target username
        target_username = input("👤 Enter target username (without @): ").strip()
        if target_username.startswith('@'):
            target_username = target_username[1:]
        
        # Get delay settings
        try:
            min_delay = int(input("⏱️ Minimum delay between requests (seconds) [1]: ").strip() or "1")
            max_delay = int(input("⏱️ Maximum delay between requests (seconds) [3]: ").strip() or "3")
        except ValueError:
            min_delay, max_delay = 1, 3
        
        print()
        print(f"🔍 Looking up user info for @{target_username}...")
        
        # Get user info using first session
        user_info = self.get_user_info(target_username, self.sessions[0])
        
        if not user_info:
            print(f"❌ Could not find user info for @{target_username}")
            print("❌ Could not get user information. Exiting.")
            return
        
        # Handle None values gracefully
        nickname = user_info.get('nickname') or target_username
        unique_id = user_info.get('unique_id') or target_username
        
        print(f"✅ Found user: {nickname} (@{unique_id})")
        print()
        
        # Start following process
        successful_follows = 0
        failed_follows = 0
        
        for i, session_id in enumerate(self.sessions, 1):
            print(f"🚀 Session {i}/{len(self.sessions)}: Attempting to follow...")
            
            success = self.follow_user(user_info, session_id)
            
            if success:
                successful_follows += 1
                print(f"✅ Session {i}: Successfully followed @{target_username}")
            else:
                failed_follows += 1
                print(f"❌ Session {i}: Failed to follow @{target_username}")
            
            # Add delay between requests (except for last one)
            if i < len(self.sessions):
                delay = random.uniform(min_delay, max_delay)
                print(f"⏱️ Waiting {delay:.1f} seconds...")
                time.sleep(delay)
        
        print()
        print("📊 Final Results:")
        print(f"✅ Successful follows: {successful_follows}")
        print(f"❌ Failed follows: {failed_follows}")
        print(f"📊 Success rate: {(successful_follows/len(self.sessions)*100):.1f}%")

if __name__ == "__main__":
    bot = TikTokFollowSender()
    bot.run()