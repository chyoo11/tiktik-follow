#!/usr/bin/env python3
import requests
import json
import time
import random
import urllib.parse
from typing import Dict, List, Optional, Tuple
import sys
import re
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class TikTokFollowSender:
    def __init__(self):
        self.session_ids = []
        self.proxies = []
        self.base_url = "https://www.tiktok.com/api/commit/follow/user/"
        
    def print_banner(self):
        """Print the application banner"""
        print(f"\n{Fore.CYAN}🚀 TikTok Advanced Follow Sender{Style.RESET_ALL}\n")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                    🚀 TikTok Follow Sender 🚀                 ║")
        print("║              Advanced Multi-Session Follow Bot                ║")
        print("╚══════════════════════════════════════════════════════════════╝\n")

    def load_session_ids(self, file_path: str) -> bool:
        """Load session IDs from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.session_ids = [line.strip() for line in f if line.strip()]
            print(f"🔑 ✅ Loaded {len(self.session_ids)} session IDs")
            return len(self.session_ids) > 0
        except FileNotFoundError:
            print(f"❌ Session file not found: {file_path}")
            return False
        except Exception as e:
            print(f"❌ Error loading session IDs: {str(e)}")
            return False

    def parse_proxy(self, proxy_line: str) -> Optional[Dict[str, str]]:
        """
        Parse proxy from various formats and return properly formatted proxy dict
        
        Supported formats:
        - host:port:username:password
        - http://username:password@host:port
        - host:port@username:password (incorrect format - will fix)
        """
        proxy_line = proxy_line.strip()
        
        # Handle format: http://host:port@username:password (INCORRECT FORMAT)
        if '@' in proxy_line and proxy_line.count(':') >= 3:
            # This is the problematic format from the error
            # Example: http://proxy.ufpr.br:3128@ufpr.br:PvtdAf56
            if proxy_line.startswith('http://'):
                # Remove http:// prefix
                proxy_line = proxy_line[7:]
            
            # Split by @ to separate host:port from username:password
            if '@' in proxy_line:
                parts = proxy_line.split('@')
                if len(parts) == 2:
                    host_port = parts[0]
                    username_password = parts[1]
                    
                    # Parse host:port
                    if ':' in host_port:
                        host, port = host_port.split(':', 1)
                        
                        # Parse username:password
                        if ':' in username_password:
                            username, password = username_password.split(':', 1)
                            
                            return {
                                'http': f'http://{username}:{password}@{host}:{port}',
                                'https': f'http://{username}:{password}@{host}:{port}'
                            }
        
        # Handle format: host:port:username:password (CORRECT FORMAT)
        elif proxy_line.count(':') == 3:
            parts = proxy_line.split(':')
            if len(parts) == 4:
                host, port, username, password = parts
                return {
                    'http': f'http://{username}:{password}@{host}:{port}',
                    'https': f'http://{username}:{password}@{host}:{port}'
                }
        
        # Handle format: http://username:password@host:port (STANDARD FORMAT)
        elif proxy_line.startswith('http://') and '@' in proxy_line:
            return {
                'http': proxy_line,
                'https': proxy_line
            }
        
        # Handle format: host:port (no auth)
        elif proxy_line.count(':') == 1:
            return {
                'http': f'http://{proxy_line}',
                'https': f'http://{proxy_line}'
            }
        
        return None

    def load_proxies(self, file_path: str = "proxies.txt") -> bool:
        """Load and parse proxies from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                proxy_lines = [line.strip() for line in f if line.strip()]
            
            parsed_proxies = []
            failed_count = 0
            
            for line in proxy_lines:
                parsed = self.parse_proxy(line)
                if parsed:
                    parsed_proxies.append(parsed)
                else:
                    failed_count += 1
                    print(f"⚠️  Failed to parse proxy: {line}")
            
            self.proxies = parsed_proxies
            print(f"🔗 ✅ Loaded {len(self.proxies)} proxies")
            if failed_count > 0:
                print(f"⚠️  {failed_count} proxies failed to parse")
            
            return len(self.proxies) > 0
            
        except FileNotFoundError:
            print(f"⚠️  Proxy file not found: {file_path}, continuing without proxies")
            return True
        except Exception as e:
            print(f"❌ Error loading proxies: {str(e)}")
            return False

    def generate_ttwid(self) -> str:
        """Generate a fresh ttwid token"""
        import hashlib
        import time
        
        timestamp = str(int(time.time() * 1000))
        random_part = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))
        raw_ttwid = f"1|{timestamp}_{random_part}"
        
        # URL encode the ttwid
        encoded_ttwid = urllib.parse.quote(raw_ttwid, safe='')
        return encoded_ttwid

    def generate_mstoken(self) -> str:
        """Generate a fresh msToken"""
        import base64
        import secrets
        
        # Generate random bytes and encode to base64
        random_bytes = secrets.token_bytes(32)
        mstoken = base64.b64encode(random_bytes).decode('utf-8').rstrip('=')
        
        # Add some random characters to match TikTok's format
        additional_chars = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
        return mstoken + additional_chars

    def get_user_info(self, username: str) -> Optional[Tuple[str, str]]:
        """Get user ID and sec_user_id from username via scraping"""
        try:
            print(f" 🔍 Looking up user info for @{username}...")
            
            # Use TikTok's web interface to get user info
            url = f"https://www.tiktok.com/@{username}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                
                # Extract user ID and sec_user_id from the page content
                user_id_match = re.search(r'"id":"(\d+)"', content)
                sec_user_id_match = re.search(r'"secUid":"([^"]+)"', content)
                
                if user_id_match and sec_user_id_match:
                    user_id = user_id_match.group(1)
                    sec_user_id = sec_user_id_match.group(1)
                    
                    print(f"👤 ✅ Found user via scraping: @{username}")
                    print(f"    User ID: {user_id}")
                    print(f"    Sec User ID: {sec_user_id[:20]}...")
                    
                    return user_id, sec_user_id
            
            print(f"❌ Could not find user info for @{username}")
            return None
            
        except Exception as e:
            print(f"❌ Error getting user info: {str(e)}")
            return None

    def build_follow_url(self, user_id: str, sec_user_id: str) -> str:
        """Build the follow API URL with proper parameters"""
        params = {
            'WebIdLastTime': str(int(time.time())),
            'action_type': '1',
            'aid': '1988',
            'app_language': 'en-GB',
            'app_name': 'tiktok_web',
            'browser_language': 'en-GB',
            'browser_name': 'Mozilla',
            'browser_online': 'true',
            'browser_platform': 'Linux x86_64',
            'browser_version': '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'channel': 'tiktok_web',
            'cookie_enabled': 'true',
            'device_platform': 'web_pc',
            'from': '18',
            'fromWeb': '1',
            'from_page': 'user',
            'region': 'US',
            'sec_user_id': sec_user_id,
            'type': '1',
            'user_id': user_id,
            'user_is_login': 'true',
        }
        
        query_string = urllib.parse.urlencode(params)
        return f"{self.base_url}?{query_string}"

    def send_follow_request(self, session_id: str, user_id: str, sec_user_id: str, proxy: Optional[Dict] = None) -> Tuple[bool, str]:
        """Send a follow request using the provided session"""
        try:
            # Generate fresh tokens
            ttwid = self.generate_ttwid()
            mstoken = self.generate_mstoken()
            
            print(f" ✅ Fresh ttwid generated: {ttwid[:20]}...")
            print(f" ✅ Fresh msToken generated: {mstoken[:20]}...")
            
            url = self.build_follow_url(user_id, sec_user_id)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://www.tiktok.com',
                'Referer': f'https://www.tiktok.com/@{sec_user_id}',
                'Cookie': f'sessionid={session_id}; ttwid={ttwid}; msToken={mstoken}',
                'X-Requested-With': 'XMLHttpRequest',
            }
            
            # Make the request
            response = requests.post(
                url, 
                headers=headers, 
                proxies=proxy,
                timeout=15,
                allow_redirects=False
            )
            
            # Enhanced response handling
            if response.status_code == 200:
                try:
                    # Try to parse JSON response
                    json_response = response.json()
                    
                    # Check for success indicators
                    if isinstance(json_response, dict):
                        status_code = json_response.get('status_code', 0)
                        status_msg = json_response.get('status_msg', '')
                        
                        if status_code == 0:
                            return True, "Follow sent successfully"
                        elif status_code == 10202:
                            return False, "Login expired"
                        elif status_code == 10201:
                            return False, "Authentication failed"
                        elif 'captcha' in status_msg.lower():
                            return False, "Captcha required"
                        else:
                            return False, f"API error: {status_msg} (code: {status_code})"
                    else:
                        return False, "Unexpected response format"
                        
                except json.JSONDecodeError:
                    # Response is not JSON, check content
                    content = response.text.lower()
                    if 'login' in content or 'sign' in content:
                        return False, "Login expired"
                    elif 'captcha' in content:
                        return False, "Captcha required"
                    elif len(response.text) == 0:
                        return False, "Empty response"
                    else:
                        return False, f"Unexpected response format"
            
            elif response.status_code == 302:
                return False, "Redirect detected - possible login required"
            elif response.status_code == 403:
                return False, "Access forbidden - possible rate limit"
            elif response.status_code == 429:
                return False, "Rate limited"
            else:
                return False, f"HTTP {response.status_code}: {response.reason}"
                
        except requests.exceptions.ProxyError as e:
            return False, f"Proxy error: {str(e)}"
        except requests.exceptions.Timeout:
            return False, "Request timeout"
        except requests.exceptions.ConnectionError:
            return False, "Connection error"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def run_follow_campaign(self, username: str, min_delay: float = 1.0, max_delay: float = 3.0):
        """Run the main follow campaign"""
        # Get user information
        user_info = self.get_user_info(username)
        if not user_info:
            print("❌ Could not get user information. Exiting.")
            return
        
        user_id, sec_user_id = user_info
        
        print(f"🚀 🎯 Starting follow campaign for @{username}")
        print(f" 📊 Sessions to use: {len(self.session_ids)}")
        print("📋")
        
        success_count = 0
        failure_count = 0
        
        for i, session_id in enumerate(self.session_ids, 1):
            print(f"📤 Request {i}/{len(self.session_ids)}")
            
            # Select proxy if available
            proxy = None
            if self.proxies:
                proxy = random.choice(self.proxies)
            
            print(f" 🚀 Sending follow to @{username}...")
            
            # Send follow request
            success, message = self.send_follow_request(session_id, user_id, sec_user_id, proxy)
            
            if success:
                print(f" ✅ {message}")
                success_count += 1
            else:
                print(f" ❌ {message}")
                failure_count += 1
            
            # Wait between requests (except for last request)
            if i < len(self.session_ids):
                delay = random.uniform(min_delay, max_delay)
                print(f"⏱️ ⏰ Waiting {delay:.1f} seconds...")
                time.sleep(delay)
                print("📋")
        
        # Print final statistics
        print(f"\n📊 Campaign Results:")
        print(f"✅ Successful follows: {success_count}")
        print(f"❌ Failed follows: {failure_count}")
        print(f"📈 Success rate: {(success_count / len(self.session_ids) * 100):.1f}%")

def main():
    sender = TikTokFollowSender()
    sender.print_banner()
    
    # Get session file path
    session_file = input("📁 Enter session ID file path: ").strip()
    if not sender.load_session_ids(session_file):
        return
    
    # Load proxies (optional)
    sender.load_proxies()
    
    # Get target username
    username = input("👤 Enter target username (without @): ").strip()
    if not username:
        print("❌ Username cannot be empty")
        return
    
    # Get delay settings
    try:
        min_delay = float(input("⏱️ Minimum delay between requests (seconds) [1]: ") or "1")
        max_delay = float(input("⏱️ Maximum delay between requests (seconds) [3]: ") or "3")
        
        if min_delay < 0 or max_delay < 0 or min_delay > max_delay:
            print("❌ Invalid delay values")
            return
            
    except ValueError:
        print("❌ Invalid delay values")
        return
    
    print()  # Empty line before starting
    
    # Run the campaign
    sender.run_follow_campaign(username, min_delay, max_delay)

if __name__ == "__main__":
    main()