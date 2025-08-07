# 🚀 TikTok Advanced Follow Sender

A robust, multi-session TikTok follow bot with advanced proxy support and comprehensive error handling.

## 🌟 Features

### ✅ Fixed Issues from Original Version:
- **Robust Proxy Parsing**: Handles special characters (@, #, :, !, etc.) in passwords
- **Multiple User Lookup Methods**: Uses 3 different API endpoints and HTML parsing
- **Better Session Management**: Supports session rotation and validation
- **Comprehensive Error Handling**: Graceful failure handling with detailed logging
- **Rate Limiting**: Configurable delays between requests

### 🔧 Key Improvements:
- **Smart Proxy Parser**: Automatically handles complex passwords with special characters
- **Fallback User Discovery**: If one method fails, tries alternative approaches
- **Session Rotation**: Distributes requests across multiple sessions
- **Proxy Rotation**: Automatically rotates proxies on failures
- **Detailed Logging**: Both file and console logging for debugging

## 📦 Installation

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Prepare Your Files**:
   - Create a session IDs file (one session ID per line)
   - Create a proxy file (format: `host:port:username:password`)

## 🚀 Usage

### Basic Usage:
```bash
python tiktok_follow_bot.py
```

### Follow the Interactive Prompts:
1. **Session File**: Enter path to your session IDs file
2. **Proxy File**: Enter path to your proxy file (optional)
3. **Target Username**: Enter the username to follow (without @)
4. **Delay Settings**: Configure request delays for rate limiting

## 📁 File Formats

### Session IDs File (`s2.txt`):
```
session_id_1_here
session_id_2_here
session_id_3_here
...
```

### Proxy File (Supports Multiple Formats):
```
# Standard format (recommended)
proxy.server.com:3128:username:password

# Complex passwords with special characters
proxy.server.com:3128:user@domain.com:P@ssw0rd!#$
proxy.server.com:3128:email@test.com:complex:password:with:colons

# URL format (also supported)
http://username:password@proxy.server.com:3128
```

## 🛡️ Error Handling

The bot now handles various error scenarios:
- **Proxy Parse Failures**: Invalid proxy formats are skipped with warnings
- **User Not Found**: Multiple lookup methods prevent false negatives
- **Request Failures**: Automatic proxy rotation on connection issues
- **Session Issues**: Graceful handling of invalid sessions
- **Rate Limiting**: Built-in delays to avoid being blocked

## 📊 Output Example

```
🚀 TikTok Advanced Follow Sender
Advanced Multi-Session Follow Bot

📁 Enter session ID file path: s2.txt
🔑 ✅ Loaded 10 session IDs
🌐 Enter proxy file path: proxies.txt
🔗 ✅ Loaded 25 proxies
⚠️  5 proxies failed to parse
👤 Enter target username: example_user
⏱️ Minimum delay: 1
⏱️ Maximum delay: 3

🔍 Looking up user info for @example_user...
✅ Found user: @example_user (Example User)
🆔 User ID: 1234567890
🔐 Sec UID: MS4wLjABAAAA...

🤖 Ready to follow? (y/N): y

🚀 Starting follow operation...
📊 Sessions: 10
🌐 Proxies: 25
⏱️ Delay: 1-3 seconds

🔄 Session 1/10: session_abc123...
✅ Follow successful (1/1)
⏱️ Waiting 2.3 seconds...

📊 Final Results:
✅ Successful follows: 8
❌ Failed follows: 2
📈 Success rate: 80.0%
```

## 📝 Logging

The bot creates detailed logs in `tiktok_bot.log` for:
- Proxy parsing results
- API request attempts
- User lookup methods tried
- Follow operation results
- Error debugging information

## ⚠️ Important Notes

1. **Session IDs**: Use valid TikTok session IDs from authenticated accounts
2. **Proxies**: Ensure your proxies support HTTPS and TikTok access
3. **Rate Limiting**: Use appropriate delays to avoid being detected
4. **Compliance**: Ensure your usage complies with TikTok's Terms of Service
5. **Testing**: Test with a small number of sessions first

## 🔧 Troubleshooting

### Common Issues:

**"Failed to parse proxy"**:
- Check proxy format: `host:port:username:password`
- Ensure no extra spaces or characters
- Verify proxy credentials are correct

**"Could not find user info"**:
- Verify the username exists and is public
- Check if the target account is accessible
- Ensure your sessions are valid

**"Request failed"**:
- Check proxy connectivity
- Verify session validity
- Reduce request frequency

## 📄 License

MIT License - See LICENSE file for details.

## ⚡ Performance Tips

1. **Use Quality Proxies**: Residential proxies work better than datacenter ones
2. **Valid Sessions**: Ensure all session IDs are from active, verified accounts
3. **Reasonable Delays**: Use 1-5 second delays to avoid detection
4. **Monitor Logs**: Check `tiktok_bot.log` for optimization insights

---

**Disclaimer**: This tool is for educational purposes. Users are responsible for complying with TikTok's Terms of Service and applicable laws.