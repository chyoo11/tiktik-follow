#!/usr/bin/env python3
"""
TikTok Advanced Follow Sender
A comprehensive tool for sending follows on TikTok with dynamic token generation,
proxy support, and beautiful colored output.
"""

import requests
import json
import random
import time
import re
import os
import sys
from urllib.parse import quote
from colorama import init, Fore, Back, Style
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class TikTokFollowSender:
    def __init__(self):
        self.session = requests.Session()
        self.proxies = []
        self.success_count = 0
        self.error_count = 0
        self.colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
        self.session_ids = []
        
        # Hard-coded Android User Agents with different versions and devices
        self.user_agents = [
            "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; OnePlus 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; Xiaomi 13 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SAMSUNG SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; Huawei P50 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 14; Google Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
        ]
        
        # Device fingerprint data
        self.device_models = [
            "SM-G998B", "Pixel 6 Pro", "SM-S918B", "OnePlus 9 Pro", 
            "Xiaomi 13 Pro", "SM-G973F", "Huawei P50 Pro", "Pixel 8"
        ]
        
        self.android_versions = ["11", "12", "13", "14"]
        self.chrome_versions = ["115.0.0.0", "116.0.0.0", "117.0.0.0", "118.0.0.0", "119.0.0.0", "120.0.0.0", "121.0.0.0", "122.0.0.0"]

    def print_colored(self, message, color=None, emoji=""):
        """Print colored message with random color if not specified"""
        if color is None:
            color = random.choice(self.colors)
        print(f"{color}{emoji} {message}{Style.RESET_ALL}")

    def print_banner(self):
        """Print beautiful banner"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    🚀 TikTok Follow Sender 🚀                 ║
║              Advanced Multi-Session Follow Bot                ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
        
    def get_ttwid(self):
        """Fetches fresh ttwid cookie from TikTok signup page"""
        try:
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Referer': 'https://www.tiktok.com/',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9',
                'Sec-Ch-Ua': f'"Not)A;Brand";v="8", "Chromium";v="{random.choice(self.chrome_versions).split(".")[0]}", "Android WebView";v="{random.choice(self.chrome_versions).split(".")[0]}"',
                'Sec-Ch-Ua-Mobile': '?1',
                'Sec-Ch-Ua-Platform': '"Android"'
            }
            
            response = requests.get('https://www.tiktok.com/signup', headers=headers, timeout=10)
            
            for cookie in response.cookies:
                if cookie.name == 'ttwid':
                    self.print_colored(f"✅ Fresh ttwid generated: {cookie.value[:20]}...", Fore.GREEN)
                    return cookie.value
            return None
        except Exception as e:
            self.print_colored(f"❌ Error getting ttwid: {str(e)}", Fore.RED)
            return None

    def get_mstoken(self):
        """Fetches fresh msToken cookie from TikTok tracking endpoint"""
        try:
            headers = {
                'Origin': 'https://www.tiktok.com',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'x-mssdk-info',
                'User-Agent': random.choice(self.user_agents),
                'Referer': 'https://www.tiktok.com/',
                'Accept-Language': 'en-US,en;q=0.9',
                'Sec-Ch-Ua': f'"Not)A;Brand";v="8", "Chromium";v="{random.choice(self.chrome_versions).split(".")[0]}", "Android WebView";v="{random.choice(self.chrome_versions).split(".")[0]}"',
                'Sec-Ch-Ua-Mobile': '?1',
                'Sec-Ch-Ua-Platform': '"Android"'
            }
            
            response = requests.options('https://mssdk-va.tiktok.com/web/report', headers=headers, timeout=10)
            
            for cookie in response.cookies:
                if cookie.name == 'msToken':
                    self.print_colored(f"✅ Fresh msToken generated: {cookie.value[:20]}...", Fore.GREEN)
                    return cookie.value
            return None
        except Exception as e:
            self.print_colored(f"❌ Error getting msToken: {str(e)}", Fore.RED)
            return None

    def generate_x_bogus(self):
        """Generate X-Bogus token (simplified version)"""
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        return ''.join(random.choice(chars) for _ in range(40))

    def generate_device_id(self):
        """Generate random device ID"""
        return str(random.randint(7000000000000000000, 7999999999999999999))

    def generate_csrf_token(self):
        """Generate CSRF token"""
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        return ''.join(random.choice(chars) for _ in range(32))

    def generate_verify_fp(self):
        """Generate verify fingerprint"""
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        return f"verify_{''.join(random.choice(chars) for _ in range(8))}_{''.join(random.choice(chars) for _ in range(8))}_{''.join(random.choice(chars) for _ in range(4))}_{''.join(random.choice(chars) for _ in range(4))}_{''.join(random.choice(chars) for _ in range(12))}"

    def load_proxies(self, proxy_file="proxies.txt"):
        """Load proxies from file with support for multiple formats"""
        if not os.path.exists(proxy_file):
            self.print_colored(f"⚠️ Proxy file {proxy_file} not found. Running without proxies.", Fore.YELLOW)
            return []
        
        try:
            with open(proxy_file, 'r') as f:
                raw_proxies = [line.strip() for line in f.readlines() if line.strip()]
            
            for proxy in raw_proxies:
                try:
                    if '@' in proxy:
                        # Format: user:pass@host:port
                        auth_host = proxy.split('@')
                        user_pass = auth_host[0].split(':')
                        host_port = auth_host[1].split(':')
                        
                        proxy_dict = {
                            'http': f'http://{user_pass[0]}:{user_pass[1]}@{host_port[0]}:{host_port[1]}',
                            'https': f'http://{user_pass[0]}:{user_pass[1]}@{host_port[0]}:{host_port[1]}'
                        }
                    elif proxy.count(':') == 3:
                        # Format: host:port:user:pass
                        parts = proxy.split(':')
                        proxy_dict = {
                            'http': f'http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}',
                            'https': f'http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}'
                        }
                    elif proxy.count(':') == 1:
                        # Format: host:port
                        host, port = proxy.split(':')
                        proxy_dict = {
                            'http': f'http://{host}:{port}',
                            'https': f'http://{host}:{port}'
                        }
                    else:
                        continue
                    
                    self.proxies.append(proxy_dict)
                except Exception as e:
                    self.print_colored(f"❌ Invalid proxy format: {proxy}", Fore.RED)
                    continue
            
            self.print_colored(f"✅ Loaded {len(self.proxies)} proxies", Fore.GREEN, "🔗")
            return self.proxies
        except Exception as e:
            self.print_colored(f"❌ Error loading proxies: {str(e)}", Fore.RED)
            return []

    def get_random_proxy(self):
        """Get random proxy from loaded proxies"""
        if self.proxies:
            return random.choice(self.proxies)
        return None

    def load_session_ids(self, session_file):
        """Load session IDs from file"""
        try:
            with open(session_file, 'r') as f:
                sessions = [line.strip() for line in f.readlines() if line.strip()]
            
            self.session_ids = sessions
            self.print_colored(f"✅ Loaded {len(sessions)} session IDs", Fore.GREEN, "🔑")
            return sessions
        except FileNotFoundError:
            self.print_colored(f"❌ Session file {session_file} not found!", Fore.RED)
            return []
        except Exception as e:
            self.print_colored(f"❌ Error loading session IDs: {str(e)}", Fore.RED)
            return []

    def get_user_info(self, username):
        """Get user_id and sec_user_id from username using TikTok API"""
        try:
            # Remove @ if present
            username = username.replace('@', '')
            
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.tiktok.com/',
                'Origin': 'https://www.tiktok.com'
            }
            
            # Try to get user info from TikTok web API
            url = f"https://www.tiktok.com/api/user/detail/?WebIdLastTime={int(time.time())}&aid=1988&app_language=en&app_name=tiktok_web&browser_language=en&browser_name=Mozilla&browser_online=true&browser_platform=Linux&browser_version=5.0&channel=tiktok_web&cookie_enabled=true&device_platform=web_pc&focus_state=true&from=18&history_len=2&is_fullscreen=false&is_page_visible=true&os=linux&priority_region=&referer=&region=US&screen_height=1080&screen_width=1920&tz_name=America%2FNew_York&uniqueId={username}&user_is_login=false&webcast_language=en"
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if 'userInfo' in data and 'user' in data['userInfo']:
                    user_data = data['userInfo']['user']
                    user_id = user_data.get('id', '')
                    sec_user_id = user_data.get('secUid', '')
                    
                    if user_id and sec_user_id:
                        self.print_colored(f"✅ Found user: @{username}", Fore.GREEN, "👤")
                        self.print_colored(f"   User ID: {user_id}", Fore.CYAN)
                        self.print_colored(f"   Sec User ID: {sec_user_id[:20]}...", Fore.CYAN)
                        return user_id, sec_user_id
            
            # Fallback: Try scraping from user page
            page_url = f"https://www.tiktok.com/@{username}"
            response = requests.get(page_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # Look for user data in page source
                patterns = [
                    r'"id":"(\d+)".*?"secUid":"([^"]+)"',
                    r',"userId":"(\d+)".*?"secUid":"([^"]+)"',
                    r'"user_id":"(\d+)".*?"sec_user_id":"([^"]+)"'
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, response.text)
                    if match:
                        user_id, sec_user_id = match.groups()
                        self.print_colored(f"✅ Found user via scraping: @{username}", Fore.GREEN, "👤")
                        self.print_colored(f"   User ID: {user_id}", Fore.CYAN)
                        self.print_colored(f"   Sec User ID: {sec_user_id[:20]}...", Fore.CYAN)
                        return user_id, sec_user_id
            
            self.print_colored(f"❌ Could not find user info for @{username}", Fore.RED)
            return None, None
            
        except Exception as e:
            self.print_colored(f"❌ Error getting user info: {str(e)}", Fore.RED)
            return None, None

    def send_follow(self, session_id, user_id, sec_user_id, username):
        """Send follow request using session ID"""
        try:
            # Generate fresh tokens for each request
            ttwid = self.get_ttwid()
            mstoken = self.get_mstoken()
            x_bogus = self.generate_x_bogus()
            device_id = self.generate_device_id()
            csrf_token = self.generate_csrf_token()
            verify_fp = self.generate_verify_fp()
            
            if not ttwid or not mstoken:
                self.print_colored("❌ Failed to generate fresh tokens", Fore.RED)
                return False
            
            # Build follow URL with dynamic parameters
            timestamp = int(time.time())
            url = (
                f"https://www.tiktok.com/api/commit/follow/user/"
                f"?WebIdLastTime={timestamp}&action_type=1&aid=1988&app_language=en-US"
                f"&app_name=tiktok_web&browser_language=en-US&browser_name=Mozilla"
                f"&browser_online=true&browser_platform=Linux%20aarch64"
                f"&browser_version=5.0&channel=tiktok_web&cookie_enabled=true"
                f"&data_collection_enabled=true&device_id={device_id}&device_platform=web_pc"
                f"&focus_state=true&from=18&fromWeb=1&from_page=user&history_len=1"
                f"&is_fullscreen=false&is_page_visible=true&os=linux&priority_region=US"
                f"&referer=https%3A%2F%2Fwww.tiktok.com%2F%40{username}&region=US"
                f"&root_referer=https%3A%2F%2Fwww.tiktok.com%2F%40{username}"
                f"&screen_height={random.randint(800, 1200)}&screen_width={random.randint(400, 800)}"
                f"&sec_user_id={sec_user_id}&type=1&tz_name=America%2FNew_York"
                f"&user_id={user_id}&user_is_login=true&verifyFp={verify_fp}"
                f"&webcast_language=en-US&msToken={mstoken}&X-Bogus={x_bogus}"
            )
            
            # Generate dynamic headers
            user_agent = random.choice(self.user_agents)
            device_model = random.choice(self.device_models)
            android_version = random.choice(self.android_versions)
            chrome_version = random.choice(self.chrome_versions)
            
            headers = {
                'User-Agent': user_agent,
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Content-Length': '0',
                'Sec-Ch-Ua-Platform': '"Android"',
                'Sec-Ch-Ua': f'"Not)A;Brand";v="8", "Chromium";v="{chrome_version.split(".")[0]}", "Android WebView";v="{chrome_version.split(".")[0]}"',
                'Sec-Ch-Ua-Mobile': '?1',
                'Tt-Csrf-Token': csrf_token,
                'X-Secsdk-Csrf-Token': f"0001000000018cb65c07668641b42705aa0cf8fbba52405761ab922c3c0b73b9dad5e10feb9818597cb69c24a215",
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://www.tiktok.com',
                'X-Requested-With': 'mark.via.gp',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': f'https://www.tiktok.com/@{username}',
                'Accept-Language': 'en-US,en;q=0.9',
                'Priority': 'u=1, i',
                'Cookie': (
                    f'sessionid={session_id}; sessionid_ss={session_id}; '
                    f'tt_csrf_token={csrf_token}; ttwid={ttwid}; msToken={mstoken}; '
                    f's_v_web_id={verify_fp}; '
                    f'tiktok_webapp_theme=light; '
                    f'store-country-code=us; store-country-code-src=uid'
                )
            }
            
            # Get random proxy if available
            proxy = self.get_random_proxy()
            
            # Send follow request
            self.print_colored(f"🚀 Sending follow to @{username}...", Fore.YELLOW)
            
            response = requests.post(
                url, 
                headers=headers, 
                proxies=proxy, 
                timeout=15,
                allow_redirects=False
            )
            
            # Parse response
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('status_code') == 0:
                        self.success_count += 1
                        self.print_colored(f"✅ Successfully followed @{username}!", Fore.GREEN, "🎉")
                        return True
                    else:
                        error_msg = data.get('status_msg', 'Unknown error')
                        self.print_colored(f"❌ Follow failed: {error_msg}", Fore.RED)
                        self.error_count += 1
                        return False
                except json.JSONDecodeError:
                    if "follow" in response.text.lower() and "success" in response.text.lower():
                        self.success_count += 1
                        self.print_colored(f"✅ Successfully followed @{username}!", Fore.GREEN, "🎉")
                        return True
                    else:
                        self.print_colored(f"❌ Unexpected response format", Fore.RED)
                        self.error_count += 1
                        return False
            else:
                self.print_colored(f"❌ HTTP Error {response.status_code}", Fore.RED)
                self.error_count += 1
                return False
                
        except requests.exceptions.Timeout:
            self.print_colored("❌ Request timeout", Fore.RED)
            self.error_count += 1
            return False
        except requests.exceptions.ProxyError:
            self.print_colored("❌ Proxy error", Fore.RED)
            self.error_count += 1
            return False
        except Exception as e:
            self.print_colored(f"❌ Error sending follow: {str(e)}", Fore.RED)
            self.error_count += 1
            return False

    def run_follow_campaign(self, session_file, username, delay_range=(1, 3)):
        """Run follow campaign using multiple sessions"""
        self.print_banner()
        
        # Load session IDs
        session_ids = self.load_session_ids(session_file)
        if not session_ids:
            return
        
        # Load proxies
        self.load_proxies()
        
        # Get target user info
        self.print_colored(f"🔍 Looking up user info for @{username}...", Fore.CYAN)
        user_id, sec_user_id = self.get_user_info(username)
        
        if not user_id or not sec_user_id:
            self.print_colored("❌ Cannot proceed without user information", Fore.RED)
            return
        
        self.print_colored(f"🎯 Starting follow campaign for @{username}", Fore.MAGENTA, "🚀")
        self.print_colored(f"📊 Sessions to use: {len(session_ids)}", Fore.CYAN)
        
        # Send follows
        for i, session_id in enumerate(session_ids, 1):
            self.print_colored(f"\n📤 Request {i}/{len(session_ids)}", Fore.BLUE, "📋")
            
            success = self.send_follow(session_id, user_id, sec_user_id, username)
            
            # Random delay between requests
            if i < len(session_ids):  # Don't delay after last request
                delay = random.uniform(delay_range[0], delay_range[1])
                self.print_colored(f"⏰ Waiting {delay:.1f} seconds...", Fore.YELLOW, "⏱️")
                time.sleep(delay)
        
        # Print final summary
        self.print_summary()

    def print_summary(self):
        """Print beautiful summary of results"""
        total_requests = self.success_count + self.error_count
        success_rate = (self.success_count / total_requests * 100) if total_requests > 0 else 0
        
        summary = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                        📊 CAMPAIGN SUMMARY                    ║
╠══════════════════════════════════════════════════════════════╣{Style.RESET_ALL}
{Fore.GREEN}║  ✅ Successful Follows: {self.success_count:<32}║{Style.RESET_ALL}
{Fore.RED}║  ❌ Failed Attempts: {self.error_count:<35}║{Style.RESET_ALL}
{Fore.YELLOW}║  📊 Total Requests: {total_requests:<36}║{Style.RESET_ALL}
{Fore.MAGENTA}║  🎯 Success Rate: {success_rate:.1f}%{' ' * (37 - len(f'{success_rate:.1f}%'))}║{Style.RESET_ALL}
{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(summary)

def main():
    """Main function"""
    sender = TikTokFollowSender()
    
    # Get user input
    print(f"{Fore.CYAN}🚀 TikTok Advanced Follow Sender{Style.RESET_ALL}\n")
    
    session_file = input(f"{Fore.YELLOW}📁 Enter session ID file path: {Style.RESET_ALL}").strip()
    if not session_file:
        session_file = "sessions.txt"  # Default
    
    username = input(f"{Fore.YELLOW}👤 Enter target username (without @): {Style.RESET_ALL}").strip()
    if not username:
        print(f"{Fore.RED}❌ Username is required!{Style.RESET_ALL}")
        return
    
    # Optional delay configuration
    try:
        min_delay = float(input(f"{Fore.YELLOW}⏱️ Minimum delay between requests (seconds) [1]: {Style.RESET_ALL}").strip() or "1")
        max_delay = float(input(f"{Fore.YELLOW}⏱️ Maximum delay between requests (seconds) [3]: {Style.RESET_ALL}").strip() or "3")
        delay_range = (min_delay, max_delay)
    except ValueError:
        delay_range = (1, 3)
    
    # Run the campaign
    sender.run_follow_campaign(session_file, username, delay_range)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️ Campaign interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Unexpected error: {str(e)}{Style.RESET_ALL}")