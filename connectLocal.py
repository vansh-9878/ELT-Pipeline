from pyngrok import ngrok
import os
from dotenv import load_dotenv
load_dotenv()

ngrok.set_auth_token(os.getenv("AUTH"))

tcp_tunnel = ngrok.connect(5432, "tcp")
print("Public address:", tcp_tunnel.public_url)