"""
用于格式校验的模板
"""

import re

# 1. 手机号校验（中国大陆手机号）
MOBILE_REGEX = re.compile(r"^1[3-9]\d{9}$")

# 2. 身份证号校验（中国大陆18位或15位）
ID_CARD_REGEX = re.compile(r"(^\d{15}$)|(^\d{17}[\dXx]$)")

# 3. 邮箱校验
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

# 4. 用户名校验（4-20位，字母、数字、下划线，不能以数字开头）
USERNAME_REGEX = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{3,19}$")

# 5. 密码校验（8-20位，必须包含字母和数字）
PASSWORD_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]{8,20}$")

# 6. 验证码校验（6位数字）
VERIFICATION_CODE_REGEX = re.compile(r"^\d{6}$")

# 7. 金额校验（支持整数和两位小数，正数）
AMOUNT_REGEX = re.compile(r"^(0|[1-9]\d*)(\.\d{1,2})?$")

# 8. 日期校验（yyyy-mm-dd）
DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# 9. 网站地址校验（支持 http/https 和常见域名格式）
URL_REGEX = re.compile(r"^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$")

# 10. 域名校验（不包含协议，仅域名部分）
DOMAIN_REGEX = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")

# 11. IP地址校验（IPv4）
IPV4_REGEX = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")

# 12. 端口号校验（1-65535）
PORT_REGEX = re.compile(r"^(?:[1-9]\d{0,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$")

