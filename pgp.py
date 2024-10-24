import streamlit as st
import gnupg
import random
import string
import os

# Set GNUPGHOME to the current directory
os.environ['GNUPGHOME'] = os.path.abspath('.')

# Initialize GPG
gpg = gnupg.GPG()

# Set Streamlit page configuration
st.set_page_config(page_title="PGP Key Pair Generator", layout="centered")

st.title("PGP Key Pair Generator")

# Input fields for user details
name = st.text_input("Name")
email = st.text_input("Email")
comment = st.text_input("Comment (optional)")
key_type = st.selectbox("Algorithm", ["RSA", "DSA", "ECDSA", "EdDSA"])
key_size = st.selectbox("Key Size", [2048, 3072, 4096])
key_expire = st.number_input("Key Expiration (days)", min_value=0, value=0)
passphrase_length = st.number_input("Passphrase Length (for random generation)", min_value=8, value=16)
passphrase = st.text_input("Passphrase (leave blank to generate randomly)", type="password")

if st.button("Generate PGP Key Pair"):
    if not name or not email:
        st.error("Please fill in all required fields")
    else:
        if not passphrase:
            passphrase = ''.join(random.choices(string.ascii_letters + string.digits, k=passphrase_length))

        # Generate PGP key pair
        input_data = gpg.gen_key_input(
            name_real=name,
            name_email=email,
            name_comment=comment,
            key_type=key_type,
            key_length=key_size,
            expire_date=f"{key_expire}d" if key_expire > 0 else None,
            passphrase=passphrase
        )
        key = gpg.gen_key(input_data)

        # Export keys
        private_key = gpg.export_keys(key.fingerprint, secret=True, passphrase=passphrase)
        public_key = gpg.export_keys(key.fingerprint)

        # Store keys and passphrase in session state
        st.session_state.private_key = private_key
        st.session_state.public_key = public_key
        st.session_state.passphrase = passphrase

        st.success("PGP Key Pair Generated Successfully")

# Display passphrase and download buttons if keys are in session state
if 'private_key' in st.session_state and 'public_key' in st.session_state and 'passphrase' in st.session_state:
    st.write(f"Passphrase: {st.session_state.passphrase}")
    st.download_button("Download Private Key", st.session_state.private_key, file_name="private_key.asc")
    st.download_button("Download Public Key", st.session_state.public_key, file_name="public_key.asc")