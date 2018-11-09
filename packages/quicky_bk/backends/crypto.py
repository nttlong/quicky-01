import base64, sys
import Crypto.Cipher.AES
import re
import HTMLParser
from datetime import datetime
import urllib

class TokenResult:
    def __init__(self, is_success, login_account):
        self.is_success = is_success
        self.login_account = login_account

def sso_authenticate(token_key):
    #n9uY3n#l3#v!3T#p76!
    password = base64.b64decode('GN+6pk+Y7o/FOqBtgeblEZZBiLqfBCMk3w8Ag0u6ZYk=')
    #Ps+<LQ#1om<U8iN,~=5OJIOS^@m)#AwI^nJ@vI3FH<Z(#81KyzOZcQNzPHq*asRb')
    public_salt = base64.b64decode('2KyltpPZP2dbPZUkkg0bAw==')
    aes = Crypto.Cipher.AES.new(password, Crypto.Cipher.AES.MODE_CBC, public_salt)

    token_key = urllib.unquote(token_key).decode('utf8') #System.Web.HttpUtility.UrlDecode in C#
    encrypt_text = base64.b64decode(HTMLParser.HTMLParser().unescape(token_key))
    decrypt_text = aes.decrypt(encrypt_text)

    """
    Remove the special characters at the end of the string after decoding 
    (error: ASCII convert to UTF8)
    """
    plain_text = re.sub('[\x00-\x1f]', '', decrypt_text)
    user,time=plain_text.split(";")

    login_account = user.replace("u=", "")
    request_time = datetime.strptime(time.replace("t=", ""), '%Y-%m-%dT%H:%M:%S')

    now = datetime.utcnow()
    #now = datetime.strptime("2018-10-05T07:02:12", '%Y-%m-%dT%H:%M:%S')
    diff_seconds = (now - request_time).total_seconds()
    expired_seconds = 60
    if (diff_seconds > expired_seconds):
        return TokenResult(False, login_account)
    else:
        return TokenResult(True, login_account)



# def sign_on(token_key, return_url):
#     return_url = urllib.unquote(return_url).decode('utf8')
#     res = sso_authenticate(token_key);
#     #print (res.is_success, res.login_account)
#     if res.is_success:
#         #SUCCESS
#         print("Login with user '"+ res.login_account + "'")
#         print ("redirect to " + return_url)
#     else:
#         #FAILURE
#         print("User '"+ res.login_account + "' is expired")
#         print ("redirect to " + "login_page_url")




################DEMO################
#http://localhost:8888/lms?token=72%2fpZFkKgB7vW%2bIc13AntLOt%2b434R%2byOO9MazshMPBg%3d=&retUrl=http%3a%2f%2flocalhost%3a8888%2flms
# req_token = "M13HBRy8Q3GeDTt5r%2fXsOlUtdLyjDbE3ebDDYDcxvTE%3d"
# req_url = "http%3a%2f%2flocalhost%3a8888%2flms"
# sign_on(req_token, req_url)
####################################