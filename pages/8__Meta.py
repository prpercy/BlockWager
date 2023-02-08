import streamlit as st

# MetaMask JavaScript library
st.html("""
<script src="https://cdn.jsdelivr.net/npm/@metamask/metamask-extension@^5.5.7/dist/metamask.js"></script>
""")
# MetaMask login button
if (typeof window.ethereum !== 'undefined') {
  # Check if the user is logged in
  if (window.ethereum.isMetaMask) {
    st.button('Log in with MetaMask')
  }
} else {
  st.error('MetaMask is not installed.')
}
# Request access to the user's Ethereum account
if st.button('Log in with MetaMask'):
  window.ethereum.enable().then(function (address) {
    # Store the Ethereum address in a variable
    const userAddress = address;
    st.write(`Your Ethereum address is: ${userAddress}`)
  });

Meta_script = """ <script type = 'text/javascript'> 

const initialize = () => {
    const connectButton = document.getElementById('connectWallet');
    const { ethereum } = window;
    const onboardMetaMaskClient = async () => {
        if (!isMetamaskInstalled()) {
            // prompt the user to install it
            console.log("MetaMask is not installed :(");
            connectButton.value = "Click here to install metamask";
            connectButton.onclick = installMetaMask;
        } else {
            console.log("MetaMask is installed Hurray!!!!!");
            connectButton.onclick = connectMetaMask;
        }
    }
    const connectMetaMask = async () => {
        connectButton.disabled = true;
        try {
            const accounts = await ethereum.request({ method: "eth_requestAccounts" });
            connectButton.value = "Connected";
            console.log("accounts: ", accounts);
            connectButton.disabled = false;
        } catch (err) {
            console.error("error occured while connecting to MetaMask: ", err)
        }
    }
    const isMetamaskInstalled = () => {
        return ethereum && ethereum.isMetaMask;
    }
    const installMetaMask = () => {
        const onboarding = new MetaMaskOnboarding({ forwarderOrigin });
        connectButton.value = "Installation in progress";
        connectButton.disabled = true;
        onboarding.startOnboarding();
    }
    onboardMetaMaskClient();
};
window.addEventListener('DOMContentLoaded', initialize);

</script type = text/javascript>
"""

    html(meta_script)








