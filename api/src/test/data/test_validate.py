from data.validation import validateEmailAddress, validatePhoneNumberString


def test_emailAddressSuccess():
    assert validateEmailAddress("valid@email.com")


def test_emailAddressFailure():
    assert not validateEmailAddress("noDomain@email")


def test_validUSPhoneNumber():
    assert validatePhoneNumberString("1018679305")


def test_validUSPhoneNumberWithDashes():
    assert validatePhoneNumberString("101-867-9305")
