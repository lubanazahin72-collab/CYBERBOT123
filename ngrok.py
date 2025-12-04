from pyngrok import ngrok

# 1. Set new auth token
ngrok.set_auth_token("36BLevuLXUOj3AcgoMqu23YuI0d_XaskVERxfgc4SRwkEXfy")  # <-- paste new token

# 2. Optional: kill any existing tunnels
ngrok.kill()

# 3. Start tunnel
public_url = ngrok.connect(8000)
print("Public URL:", public_url)



