# 🚀 TikTok Advanced Follow Sender

A comprehensive and powerful tool for sending follows on TikTok with dynamic token generation, proxy support, and beautiful colored output.

## ✨ Features

### 🔄 Dynamic Cookie & Token Generation
- **Fresh cookies for each request** - no more static cookies!
- **Dynamic URL tokens** (msToken, X-Bogus, ttwid)
- **Random User Agents** with different Android versions, Chrome versions, and device models
- **CSRF tokens** and device fingerprints generation
- **Automatic token refresh** for each follow request

### 🌐 Comprehensive Proxy Support
- **Multiple proxy formats** supported:
  - `host:port` (basic)
  - `host:port:user:pass` (with authentication)
  - `user:pass@host:port` (standard format)
- **Proxy file support** (`proxies.txt`)
- **Random proxy selection** for each request
- **Error handling** for invalid proxy formats

### 🎨 Beautiful Random Colors & Design
- **Colorama integration** for cross-platform colored output
- **Random colors** for each message and section
- **Beautiful progress indicators** with emojis
- **Colorful status messages** (✅ success, ❌ errors, ⚠️ warnings)

### 🚀 Enhanced Features
- **Progress tracking** with detailed statistics
- **Random delays** between requests (1-3 seconds)
- **Comprehensive error handling**
- **Success/failure counters**
- **Beautiful summary** with statistics
- **Automatic user lookup** by username (finds sec_user_id and user_id automatically)

## 📋 Requirements

- Python 3.7 or higher
- Required packages (install with `pip install -r requirements.txt`):
  - `requests>=2.31.0`
  - `colorama>=0.4.6`
  - `urllib3>=2.0.0`

## 🛠️ Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📁 Setup

### 1. Session IDs Setup
1. **Edit `sessions.txt`** file
2. **Add your TikTok session IDs**, one per line
3. **Remove the example/comment lines**

Example `sessions.txt`:
```
33b0ccd42ce0abbe487a58503e70ccf4
a1b2c3d4e5f6789012345678901234567
your_session_id_1
your_session_id_2
```

**How to get Session IDs:**
1. Open TikTok in your browser
2. Login to your account
3. Open Developer Tools (F12)
4. Go to Application/Storage → Cookies → https://www.tiktok.com
5. Find the `sessionid` cookie value
6. Copy and paste it into `sessions.txt`

### 2. Proxies Setup (Optional)
1. **Edit `proxies.txt`** file (optional but recommended)
2. **Add your proxies** in any of the supported formats:

```
# Basic format
127.0.0.1:8080

# With authentication (format 1)
proxy.example.com:8080:username:password

# With authentication (format 2)  
username:password@proxy.example.com:8080
```

## 🚀 Usage

### Basic Usage
```bash
python tiktok_follow_sender.py
```

The script will prompt you for:
1. **Session ID file path** (default: `sessions.txt`)
2. **Target username** (without @)
3. **Delay settings** (optional)

### Example Run
```
🚀 TikTok Advanced Follow Sender

📁 Enter session ID file path: sessions.txt
👤 Enter target username (without @): username_to_follow
⏱️ Minimum delay between requests (seconds) [1]: 1
⏱️ Maximum delay between requests (seconds) [3]: 3
```

## 🔧 How It Works

### 1. **Token Generation**
- **Fresh ttwid**: Fetched from TikTok signup page
- **Fresh msToken**: Generated via TikTok tracking endpoint
- **X-Bogus**: Dynamically generated security token
- **Device fingerprints**: Random Android devices and Chrome versions

### 2. **User Lookup**
- **Automatic detection** of `user_id` and `sec_user_id` from username
- **Multiple fallback methods** (API + page scraping)
- **Real-time user verification**

### 3. **Follow Process**
- **Session-based authentication** using your provided session IDs
- **Dynamic headers** with randomized user agents
- **Proxy rotation** (if proxies are configured)
- **Comprehensive error handling**

### 4. **Progress Tracking**
- **Real-time progress** with colored output
- **Success/failure counters**
- **Detailed error messages**
- **Beautiful summary** at the end

## 📊 Output Example

```
╔══════════════════════════════════════════════════════════════╗
║                    🚀 TikTok Follow Sender 🚀                 ║
║              Advanced Multi-Session Follow Bot                ║
╚══════════════════════════════════════════════════════════════╝

✅ Loaded 5 session IDs 🔑
✅ Loaded 3 proxies 🔗
🔍 Looking up user info for @target_user...
✅ Found user: @target_user 👤
   User ID: 1234567890
   Sec User ID: MS4wLjABAAAA...

🎯 Starting follow campaign for @target_user 🚀
📊 Sessions to use: 5

📤 Request 1/5 📋
✅ Fresh ttwid generated: 1%7CukNwLx53lmrQ...
✅ Fresh msToken generated: NXgYnKJgDNoo0wtq...
🚀 Sending follow to @target_user...
✅ Successfully followed @target_user! 🎉
⏰ Waiting 2.3 seconds... ⏱️

╔══════════════════════════════════════════════════════════════╗
║                        📊 CAMPAIGN SUMMARY                    ║
╠══════════════════════════════════════════════════════════════╣
║  ✅ Successful Follows: 4                                    ║
║  ❌ Failed Attempts: 1                                       ║
║  📊 Total Requests: 5                                        ║
║  🎯 Success Rate: 80.0%                                      ║
╚══════════════════════════════════════════════════════════════╝
```

## ⚠️ Important Notes

### Security & Ethics
- **Use responsibly** and respect TikTok's terms of service
- **Don't spam** or harass users
- **Use delays** between requests to avoid being detected
- **Use quality proxies** to protect your IP address

### Session Management
- **Keep session IDs secure** and don't share them
- **Sessions may expire** - replace them if you get authentication errors
- **Use multiple sessions** from different accounts for better success rates

### Error Handling
- The script handles **network errors**, **proxy failures**, and **authentication issues**
- **Invalid usernames** are detected and reported
- **Rate limiting** is respected with configurable delays

## 🐛 Troubleshooting

### Common Issues

1. **"Session file not found"**
   - Make sure `sessions.txt` exists and contains valid session IDs

2. **"Could not find user info"**
   - Check if the username exists and is spelled correctly
   - The user might have a private account

3. **"Authentication failed"**
   - Your session IDs might be expired - get fresh ones
   - Make sure session IDs are correctly formatted

4. **"Proxy errors"**
   - Check your proxy format and credentials
   - Test proxies manually before using them

## 📝 License

This project is for educational purposes only. Use responsibly and at your own risk.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

---

**Disclaimer**: This tool is for educational purposes only. The authors are not responsible for any misuse or violations of TikTok's terms of service.