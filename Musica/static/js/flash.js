function close_flash(flash_id) {
    var flash = document.querySelector('[flash-id="' + flash_id + '"]');
    if (flash) {
        flash.style.display = 'none';
    }
}