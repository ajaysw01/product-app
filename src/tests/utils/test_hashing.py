from passlib.context import CryptContext
from api.utils.hashing import Hash

def test_bcrypt() : 
    password = "test"

    hashed_password = Hash.bcrypt(password)

    assert hashed_password != password

    assert hashed_password.startswith("$2b$")



def test_verify_correct_password() :
    password = "test"
    wrong_password = "wrong"

    hashed_password = Hash.bcrypt(password)

    is_valid = Hash.verify(wrong_password, hashed_password)
    assert is_valid is False