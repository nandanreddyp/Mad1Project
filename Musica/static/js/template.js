
function logout() {
    let confirm = window.confirm('Do you want to logout?');
    if (confirm) {
        window.location.href = '/logout'
    }
}
