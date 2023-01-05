import re

US_PHONE_NUMBER_REGEX = r'^\(?\d{3}\)?( |-)?\d{3}( |-)?\d{4}'
INTERNATIONAL_PHONE_NUMBER_REGEX = r'^\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*\d\W*(\d{1,2})'
EMAIL_REGEX = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})'


def validatePhoneNumberString(phoneNumber) -> bool:
    """
    Validate US and International Phone Numbers
    :param: phoneNumber
    :return: bool
    """
    usPhoneNumberMatch = re.match(US_PHONE_NUMBER_REGEX, phoneNumber)
    internationalPhoneNumberMatch = re.match(INTERNATIONAL_PHONE_NUMBER_REGEX, phoneNumber)

    if usPhoneNumberMatch is not None or internationalPhoneNumberMatch is not None:
        return True
    return False


def validateEmailAddress(email) -> bool:
    """
    Validate email address
    :param email:
    :return:
    """
    emailMatch = re.match(EMAIL_REGEX, email)
    if emailMatch is not None:
        return True
    return False
