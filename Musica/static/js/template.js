var expand = true
const aside_expand_html = `
<div class="main-side">
<div class="user-section">
    <h1 class="premiumUser-label label">Premium User</h1>
    <h1 class="basicUser-label label">Basic User</h1>
        <nav class="nav-links">
            <ul class="user-links">
                <li  ><a href="/home">Home</a></li>
                <li  ><a href="/songs">Explore</a></li>
                <li id="current-page" ><a href="/albums">Library</a></li>
                <li  ><a href="/playlists">Upgrade</a></li>
            </ul>
        </nav>
</div>
<div class="creator-section">  
    <h1 class="creator-label label">Creator Zone</h1>
        <nav class="nav-links">
            <ul class="creator-links">
                <li  ><a href="/creator/upload">Upload songs</a></li>
                <li  ><a href="/creator/uploads">Uploads</a></li>
                <li  ><a href="/creator/albums">Albums</a></li>
                <li  ><a href="/creato/analytics">Analytics</a></li>
            </ul>
        </nav>
</div>
</div>
<nav class="nav-links">
<ul class="tools">
        <li id="premium"><a href="/premium-apply">Get Premium</a></li>
        <li id="creator"><a href="/creator-apply">Become Creator</a></li>
        <li id='logout' onclick="logout()"><a>Logout</a></li>          
</ul>
</nav>
`;
const aside_contract_html = `
<div class="main-side">

    <a href='/home' > <img src='http://127.0.0.1:3000/Musica/static/images/logos/home.svg'></a>
    <a href='/explore' > <img src='http://127.0.0.1:3000/Musica/static/images/logos/explore.svg'></a>
    <a href='/library' > <img src='http://127.0.0.1:3000/Musica/static/images/logos/library.svg'></a>
    <a href='/upgrade' > <img src='http://127.0.0.1:3000/Musica/static/images/logos/premium.svg'></a>
    <a href='/upload' > <img src='http://127.0.0.1:3000/Musica/static/images/logos/upload.svg'></a>
    <a href='/uploads' > <img src='http://127.0.0.1:3000/Musica/static/images/logos/song.svg'></a>
    <a href='/albums' > <img src='http://127.0.0.1:3000/Musica/static/images/logos/album.svg'></a>
    <a href='/analytics' > <img src='http://127.0.0.1:3000/Musica/static/images/logos/analytics.svg'></a>

<div class="tools-side">

</div>
`;
function open_close_sidebar() {
    expand = !expand;
    const menu = document.getElementById('menu')
    const main = document.getElementById('main')
    if (expand) {
        menu.classList.remove('contract-aside')
        main.classList.remove('expand-main')
        menu.classList.add('expand-aside')
        main.classList.add('contract-menu')

        // changing inner html
        menu.innerHTML = aside_expand_html
        
    }
    else {
        menu.classList.remove('expand-aside')
        main.classList.remove('contract-aside')
        menu.classList.add('contract-aside')
        main.classList.add('expand-main')

        menu.innerHTML = aside_contract_html
    }
}

function logout() {
    let confirm = window.confirm('Do you want to logout?');
    if (confirm) {
        window.location.href = '/logout'
    }
}
