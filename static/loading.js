const loginButton = document.getElementById("loginButton");

loginButton.addEventListener('click', () => {
    setTimeout(() => {
        document.getElementById('loginContainer').innerHTML = ""
        document.getElementById('loading').style.display = "block"
    }, 200)
})