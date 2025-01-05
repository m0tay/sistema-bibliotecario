import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.audit import Audit
from models.books import Book
from models.lendings import Lending
from models.users import User


def send_email(email: str, text_body: str, user_id: int) -> None:
	print(f'Para: {email}')
	print(f'Corpo: {text_body}')
	print(f'User: {User.read(user_id)}')
