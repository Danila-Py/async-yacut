import string

ALLOWED_AUTO_CHARS = string.ascii_letters + string.digits
ALLOWED_USER_CHARS = '^[a-zA-Z0-9_]*$'
ORIGINAL_LINK_LENGJT = 256
AUTO_LINK_LENGJT = 6
REGEX = fr'^[{ALLOWED_AUTO_CHARS}]*$'
URL_MAX_LEN = 2048
SHORT_MAX_LEN = 16
ADD_TRIES = 10
RESERVED_SHORTS = ('files',)
SHORT_URL_VIEW = 'redirect_view'