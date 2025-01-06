function showPopup() {
    var modal = document.querySelector('.nova-modal');
    modal.style.display = 'block';
}

function accept() {
    // Redirect to the live page
    window.location.href = 'http://127.0.0.1:5500/Frontend/caretaker.html';
}

document.querySelector('.dismissButton').addEventListener('click', function() {
    var modal = document.querySelector('.nova-modal');
    modal.style.display = 'none';
});

window.addEventListener("load", function() {
    var distressSound = document.getElementById("distress-sound");
    distressSound.play().catch(function(error) {
        console.error("Audio play failed:", error);
    });
});