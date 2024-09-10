from django.core.exceptions import BadRequest
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class TokenService:

    @staticmethod
    def get_invitation_link(base_url, course, email):
        """
        generate verification link with unique token
        """
        token = f"{course}:{email}"
        # Encode the token as base64
        encoded_token = urlsafe_base64_encode(token.encode('utf-8'))
        invitation_link = f"{base_url}/accept_invitation/{encoded_token}/"
        return invitation_link

    @staticmethod
    def decode_token(token):
        decoded_token = urlsafe_base64_decode(token).decode('utf-8')
        token_parts = decoded_token.split(':')
        if len(token_parts) != 2:
            raise BadRequest("Invalid Verification Link!")
        course, user = token_parts
        return course, user
