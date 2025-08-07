#!/usr/bin/env python3
"""
🚀 TikTok Advanced Follow Sender
Advanced Multi-Session Follow Bot

This bot addresses the following issues:
1. Robust proxy parsing with special character handling
2. Multiple user lookup methods
3. Better session management
4. Comprehensive error handling
5. Rate limiting and delays
"""

import requests
import json
import time
import random
import re
import sys
import os
from urllib.parse import quote, unquote
from typing import List, Dict, Optional, Tuple
import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tiktok_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ProxyConfig:
    """Represents a proxy configuration"""
    host: str
    port: int
    username: str
    password: str
    
    def to_dict(self) -> Dict[str, str]:
        return {
            'http': f'http://{self.username}:{self.password}@{self.host}:{self.port}',
            'https': f'http://{self.username}:{self.password}@{self.host}:{self.port}'
        }
    
    def __str__(self) -> str:
        return f"{self.host}:{self.port}:{self.username}:****"

@dataclass
class SessionConfig:
    """Represents a TikTok session configuration"""
    session_id: str
    user_id: str = ""
    csrf_token: str = ""
    cookies: Dict[str, str] = None
    
    def __post_init__(self):
        if self.cookies is None:
            self.cookies = {}

class TikTokFollowBot:
    """Advanced TikTok Follow Bot with multi-session support"""
    
    def __init__(self):
        self.sessions: List[SessionConfig] = []
        self.proxies: List[ProxyConfig] = []
        self.current_session_index = 0
        self.current_proxy_index = 0
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Origin': 'https://www.tiktok.com',
            'Referer': 'https://www.tiktok.com/',
        }
        
        # TikTok API endpoints
        self.user_info_endpoints = [
            'https://www.tiktok.com/api/user/detail/',
            'https://www.tiktok.com/api/user/profile/',
            'https://m.tiktok.com/api/user/detail/',
        ]
        
        self.follow_endpoints = [
            'https://www.tiktok.com/api/commit/follow/user/',
            'https://m.tiktok.com/api/commit/follow/user/',
        ]
    
    def print_banner(self):
        """Print the application banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🚀 TikTok Follow Sender 🚀                 ║
║              Advanced Multi-Session Follow Bot                ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(banner)
    
    def parse_proxy_line(self, line: str) -> Optional[ProxyConfig]:
        """
        Parse proxy line with robust handling of special characters in passwords
        Supports multiple formats:
        - host:port:username:password
        - http://username:password@host:port
        - username:password@host:port
        """
        line = line.strip()
        if not line:
            return None
        
        try:
            # Method 1: Try standard format host:port:username:password
            if line.count(':') >= 3:
                parts = line.split(':')
                if len(parts) >= 4:
                    host = parts[0]
                    port = int(parts[1])
                    username = parts[2]
                    # Join remaining parts as password (handles passwords with colons)
                    password = ':'.join(parts[3:])
                    return ProxyConfig(host, port, username, password)
            
            # Method 2: Try URL format
            if line.startswith('http://') or line.startswith('https://'):
                # Remove protocol
                line = line.replace('http://', '').replace('https://', '')
                
            # Method 3: Try format username:password@host:port
            if '@' in line:
                auth_part, host_part = line.rsplit('@', 1)
                if ':' in auth_part and ':' in host_part:
                    username, password = auth_part.split(':', 1)
                    host, port = host_part.split(':', 1)
                    return ProxyConfig(host, int(port), username, password)
            
            return None
            
        except Exception as e:
            logger.debug(f"Failed to parse proxy line '{line}': {e}")
            return None
    
    def load_proxies(self, file_path: str) -> int:
        """Load proxies from file with improved parsing"""
        loaded_count = 0
        failed_count = 0
        
        if not os.path.exists(file_path):
            logger.error(f"Proxy file not found: {file_path}")
            return 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    proxy = self.parse_proxy_line(line)
                    if proxy:
                        self.proxies.append(proxy)
                        loaded_count += 1
                        logger.debug(f"Loaded proxy: {proxy}")
                    else:
                        if line.strip():  # Only count non-empty lines as failures
                            failed_count += 1
                            logger.warning(f"⚠️  Failed to parse proxy: {line.strip()}")
        
        except Exception as e:
            logger.error(f"Error reading proxy file: {e}")
            return 0
        
        print(f"🔗 ✅ Loaded {loaded_count} proxies")
        if failed_count > 0:
            print(f"⚠️  {failed_count} proxies failed to parse")
        
        return loaded_count
    
    def load_sessions(self, file_path: str) -> int:
        """Load session IDs from file"""
        if not os.path.exists(file_path):
            logger.error(f"Session file not found: {file_path}")
            return 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    session_id = line.strip()
                    if session_id:
                        self.sessions.append(SessionConfig(session_id))
            
            print(f"🔑 ✅ Loaded {len(self.sessions)} session IDs")
            return len(self.sessions)
            
        except Exception as e:
            logger.error(f"Error reading session file: {e}")
            return 0
    
    def get_current_proxy(self) -> Optional[Dict[str, str]]:
        """Get current proxy configuration"""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_proxy_index]
        return proxy.to_dict()
    
    def rotate_proxy(self):
        """Rotate to next proxy"""
        if self.proxies:
            self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
    
    def get_current_session(self) -> Optional[SessionConfig]:
        """Get current session configuration"""
        if not self.sessions:
            return None
        return self.sessions[self.current_session_index]
    
    def rotate_session(self):
        """Rotate to next session"""
        if self.sessions:
            self.current_session_index = (self.current_session_index + 1) % len(self.sessions)
    
    def make_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """Make HTTP request with proxy and session support"""
        session = self.get_current_session()
        proxy_config = self.get_current_proxy()
        
        headers = self.base_headers.copy()
        if session:
            headers['Cookie'] = f"sessionid={session.session_id}"
            if session.csrf_token:
                headers['X-CSRFToken'] = session.csrf_token
        
        # Merge additional headers
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
            del kwargs['headers']
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, proxies=proxy_config, timeout=30, **kwargs)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, proxies=proxy_config, timeout=30, **kwargs)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            return response
            
        except Exception as e:
            logger.error(f"Request failed: {e}")
            # Try rotating proxy on failure
            self.rotate_proxy()
            return None
    
    def search_user_by_username(self, username: str) -> Optional[Dict]:
        """Search for user using multiple methods"""
        username = username.strip().lstrip('@')
        
        # Method 1: Direct user detail API
        for endpoint in self.user_info_endpoints:
            try:
                params = {
                    'uniqueId': username,
                    'language': 'en',
                }
                
                response = self.make_request(endpoint, params=params)
                if response and response.status_code == 200:
                    try:
                        data = response.json()
                        if 'userInfo' in data and data['userInfo']:
                            user_info = data['userInfo']['user']
                            return {
                                'id': user_info.get('id'),
                                'sec_uid': user_info.get('secUid'),
                                'unique_id': user_info.get('uniqueId'),
                                'nickname': user_info.get('nickname'),
                                'verified': user_info.get('verified', False)
                            }
                    except json.JSONDecodeError:
                        continue
                        
            except Exception as e:
                logger.debug(f"User search method failed: {e}")
                continue
        
        # Method 2: Try accessing user profile page directly
        try:
            profile_url = f"https://www.tiktok.com/@{username}"
            response = self.make_request(profile_url)
            
            if response and response.status_code == 200:
                # Extract user data from HTML using regex
                patterns = [
                    r'"uniqueId":"([^"]+)"',
                    r'"id":"(\d+)"',
                    r'"secUid":"([^"]+)"',
                    r'"nickname":"([^"]+)"'
                ]
                
                html_content = response.text
                user_data = {}
                
                for pattern in patterns:
                    match = re.search(pattern, html_content)
                    if match:
                        if 'uniqueId' in pattern:
                            user_data['unique_id'] = match.group(1)
                        elif 'id' in pattern and 'secUid' not in pattern:
                            user_data['id'] = match.group(1)
                        elif 'secUid' in pattern:
                            user_data['sec_uid'] = match.group(1)
                        elif 'nickname' in pattern:
                            user_data['nickname'] = match.group(1)
                
                if user_data.get('id') and user_data.get('sec_uid'):
                    return user_data
                    
        except Exception as e:
            logger.debug(f"Profile page parsing failed: {e}")
        
        # Method 3: Search API
        try:
            search_url = "https://www.tiktok.com/api/search/user/"
            params = {
                'keyword': username,
                'count': 10,
                'cursor': 0
            }
            
            response = self.make_request(search_url, params=params)
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    if 'user_list' in data:
                        for user in data['user_list']:
                            user_info = user.get('user_info', {})
                            if user_info.get('unique_id', '').lower() == username.lower():
                                return {
                                    'id': user_info.get('uid'),
                                    'sec_uid': user_info.get('sec_uid'),
                                    'unique_id': user_info.get('unique_id'),
                                    'nickname': user_info.get('nickname'),
                                    'verified': user_info.get('verified', False)
                                }
                except json.JSONDecodeError:
                    pass
                    
        except Exception as e:
            logger.debug(f"Search API failed: {e}")
        
        return None
    
    def follow_user(self, user_data: Dict) -> bool:
        """Follow a user"""
        if not user_data.get('sec_uid'):
            logger.error("Missing sec_uid for follow operation")
            return False
        
        session = self.get_current_session()
        if not session:
            logger.error("No session available for follow operation")
            return False
        
        for endpoint in self.follow_endpoints:
            try:
                # Prepare follow data
                follow_data = {
                    'sec_user_id': user_data['sec_uid'],
                    'type': 1,  # Follow action
                    'from': 19,
                    'from_pre': 0,
                }
                
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest',
                }
                
                response = self.make_request(
                    endpoint, 
                    method='POST', 
                    data=follow_data, 
                    headers=headers
                )
                
                if response and response.status_code == 200:
                    try:
                        result = response.json()
                        if result.get('status_code') == 0:
                            logger.info(f"✅ Successfully followed @{user_data.get('unique_id')}")
                            return True
                        else:
                            logger.warning(f"Follow failed: {result.get('status_msg', 'Unknown error')}")
                    except json.JSONDecodeError:
                        logger.warning("Invalid JSON response from follow API")
                
            except Exception as e:
                logger.error(f"Follow request failed: {e}")
                continue
        
        return False
    
    def run(self):
        """Main bot execution"""
        self.print_banner()
        
        # Load session IDs
        session_file = input("📁 Enter session ID file path: ").strip()
        if not self.load_sessions(session_file):
            print("❌ Could not load session IDs. Exiting.")
            return
        
        # Load proxies
        proxy_file = input("🌐 Enter proxy file path (or press Enter to skip): ").strip()
        if proxy_file:
            self.load_proxies(proxy_file)
        
        # Get target username
        target_username = input("👤 Enter target username (without @): ").strip()
        if not target_username:
            print("❌ Username is required. Exiting.")
            return
        
        # Get delay settings
        try:
            min_delay = int(input("⏱️ Minimum delay between requests (seconds) [1]: ") or "1")
            max_delay = int(input("⏱️ Maximum delay between requests (seconds) [3]: ") or "3")
        except ValueError:
            min_delay, max_delay = 1, 3
        
        print(f"\n🔍 Looking up user info for @{target_username}...")
        
        # Search for user
        user_data = self.search_user_by_username(target_username)
        if not user_data:
            print(f"❌ Could not find user info for @{target_username}")
            print("❌ Could not get user information. Exiting.")
            return
        
        print(f"✅ Found user: @{user_data.get('unique_id')} ({user_data.get('nickname')})")
        print(f"🆔 User ID: {user_data.get('id')}")
        print(f"🔐 Sec UID: {user_data.get('sec_uid')[:20]}...")
        
        # Confirm follow operation
        confirm = input(f"\n🤖 Ready to follow @{target_username} with {len(self.sessions)} sessions? (y/N): ")
        if confirm.lower() != 'y':
            print("❌ Operation cancelled.")
            return
        
        print(f"\n🚀 Starting follow operation...")
        print(f"📊 Sessions: {len(self.sessions)}")
        print(f"🌐 Proxies: {len(self.proxies)}")
        print(f"⏱️ Delay: {min_delay}-{max_delay} seconds\n")
        
        successful_follows = 0
        failed_follows = 0
        
        # Execute follow operations
        for i, session in enumerate(self.sessions):
            try:
                print(f"🔄 Session {i+1}/{len(self.sessions)}: {session.session_id[:20]}...")
                
                # Set current session
                self.current_session_index = i
                
                # Attempt to follow
                if self.follow_user(user_data):
                    successful_follows += 1
                    print(f"✅ Follow successful ({successful_follows}/{i+1})")
                else:
                    failed_follows += 1
                    print(f"❌ Follow failed ({failed_follows}/{i+1})")
                
                # Rotate proxy for next request
                self.rotate_proxy()
                
                # Add delay between requests
                if i < len(self.sessions) - 1:  # Don't delay after last request
                    delay = random.uniform(min_delay, max_delay)
                    print(f"⏱️ Waiting {delay:.1f} seconds...")
                    time.sleep(delay)
                
            except KeyboardInterrupt:
                print("\n⚠️ Operation interrupted by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in session {i+1}: {e}")
                failed_follows += 1
                continue
        
        # Print final results
        print(f"\n📊 Final Results:")
        print(f"✅ Successful follows: {successful_follows}")
        print(f"❌ Failed follows: {failed_follows}")
        print(f"📈 Success rate: {(successful_follows / len(self.sessions) * 100):.1f}%")
        print(f"\n[Program finished]")

def main():
    """Entry point for the application"""
    try:
        bot = TikTokFollowBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n⚠️ Program interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error occurred: {e}")

if __name__ == "__main__":
    main()