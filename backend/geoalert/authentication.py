from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
import jwt
import requests

User = get_user_model()

class KeycloakAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            # Busca cabeçalho do token para extrair o 'kid'
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get('kid')

            if not kid:
                raise AuthenticationFailed('Token sem kid.')

            # Busca as chaves públicas do Keycloak (JWKS)
            jwks_url = 'http://keycloak:8080/realms/geoalert/protocol/openid-connect/certs'
            jwks = requests.get(jwks_url).json()

            # Procura a chave que corresponde ao kid
            public_key = None
            for key in jwks['keys']:
                if key['kid'] == kid:
                    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                    break

            if not public_key:
                raise AuthenticationFailed('Chave pública não encontrada para o kid.')

            # Decodifica e valida o token
            decoded = jwt.decode(
                token,
                key=public_key,
                algorithms=['RS256'],
                audience='account',  # ou seu client_id, se configurado
                options={'verify_exp': True}
            )

            username = decoded.get('preferred_username')
            email = decoded.get('email')

            if not username or not email:
                raise AuthenticationFailed('Token inválido.')

            user, _ = User.objects.get_or_create(username=username, defaults={'email': email})
            return (user, None)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expirado.')
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f'Token inválido: {str(e)}')
        except Exception as e:
            raise AuthenticationFailed(f'Erro ao autenticar: {str(e)}')
