# 🚀 TikTok Follow Sender

Advanced Multi-Session Follow Bot for TikTok

## Features

✅ **Multi-Session Support** - Use multiple TikTok session IDs for mass following  
✅ **Smart User Lookup** - Robust user information detection with multiple fallback methods  
✅ **Proxy Support** - Optional proxy configuration for enhanced privacy  
✅ **Rate Limiting** - Configurable delays between requests to avoid detection  
✅ **Error Handling** - Graceful handling of failed requests and invalid sessions  
✅ **Beautiful UI** - Clean console interface with progress tracking  

## Prerequisites

- Python 3.x
- `requests` library
- Valid TikTok session IDs

## Installation

1. **Install Python dependencies:**
   ```bash
   # On Ubuntu/Debian
   sudo apt update && sudo apt install -y python3-requests
   
   # Or using pip
   pip3 install requests
   ```

2. **Clone or download this repository**

## Session Setup

1. **Get TikTok Session IDs:**
   - Open TikTok in your browser
   - Login to your account
   - Open Developer Tools (F12)
   - Go to Application/Storage → Cookies → https://www.tiktok.com
   - Find the `sessionid` cookie value
   - Copy the value (long string like `33b0ccd42ce0abbe487a58503e70ccf4`)

2. **Create session file:**
   ```bash
   # Create a file (e.g., sessions.txt) with one session ID per line
   echo "your_first_session_id_here" > sessions.txt
   echo "your_second_session_id_here" >> sessions.txt
   # Add more session IDs as needed
   ```

## Usage

1. **Run the bot:**
   ```bash
   python3 tiktok_follow_sender.py
   ```

2. **Follow the prompts:**
   - **Session file path:** Enter the path to your session IDs file (e.g., `sessions.txt`)
   - **Proxy file path:** Enter proxy file path or press Enter to skip
   - **Target username:** Enter the TikTok username to follow (without @)
   - **Min/Max delays:** Configure request timing (default: 1-3 seconds)

## Example Run

```
╔══════════════════════════════════════════════════════════════╗
║                    🚀 TikTok Follow Sender 🚀                 ║
║              Advanced Multi-Session Follow Bot                ║
╚══════════════════════════════════════════════════════════════╝

📁 Enter session ID file path: sessions.txt
🔑 ✅ Loaded 5 session IDs
🌐 Enter proxy file path (or press Enter to skip): 
🌐 No proxy file provided or found. Running without proxies.
👤 Enter target username (without @): example_user
⏱️ Minimum delay between requests (seconds) [1]: 2
⏱️ Maximum delay between requests (seconds) [3]: 5

🔍 Looking up user info for @example_user...
✅ Found user: Example User (@example_user)

🚀 Session 1/5: Attempting to follow...
✅ Session 1: Successfully followed @example_user
⏱️ Waiting 3.2 seconds...
...

📊 Final Results:
✅ Successful follows: 4
❌ Failed follows: 1
📊 Success rate: 80.0%
```

## File Formats

### Session File (sessions.txt)
```
33b0ccd42ce0abbe487a58503e70ccf4
a1b2c3d4e5f6789abcdef123456789ab
b2c3d4e5f6789abcdef123456789abc2
```

### Proxy File (proxies.txt) - Optional
```
http://proxy1:8080
socks5://proxy2:1080
http://user:pass@proxy3:3128
```

## Important Notes

⚠️ **Use Responsibly**
- This bot is for educational purposes only
- Follow TikTok's Terms of Service
- Use reasonable delays to avoid rate limiting
- Don't spam users or abuse the platform

⚠️ **Session Security**
- Keep your session IDs private
- Don't share session files
- Sessions can expire and may need to be refreshed

⚠️ **Rate Limits**
- TikTok has rate limiting mechanisms
- Use delays between requests (recommended: 2-5 seconds)
- Monitor for errors and adjust accordingly

## Troubleshooting

**"Could not find user info" Error:**
- The bot now handles this gracefully with fallback methods
- Ensure the username exists and is spelled correctly
- Check if your session IDs are valid

**"Failed to follow" Errors:**
- Session ID might be expired or invalid
- User might have privacy settings preventing follows
- Rate limits might be hit - increase delays

**Connection Errors:**
- Check your internet connection
- Try using proxies if needed
- Some regions might have TikTok access restrictions

## Features Detail

### Smart User Lookup
The bot uses multiple methods to find user information:
1. TikTok API user detail endpoint
2. Direct profile page scraping
3. Search API fallback
4. Fallback user info generation

### Error Recovery
- Continues operation even if some sessions fail
- Provides detailed error reporting
- Graceful handling of network issues

### Security Features
- No hardcoded credentials
- Session-based authentication
- Optional proxy support

## License

This project is for educational purposes only. Use responsibly and in accordance with TikTok's Terms of Service.