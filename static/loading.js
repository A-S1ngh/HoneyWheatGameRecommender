const loginButton = document.getElementById("loginButton");

loginButton.addEventListener('click', () => {
    setTimeout(() => {
        document.getElementById('login-class').innerHTML = ""
        document.getElementById('loading').style.display = "block"
    }, 200)
})