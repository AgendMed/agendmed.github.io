
document.addEventListener('DOMContentLoaded', function() {

    const detalhesBtns = document.querySelectorAll('.btn-small');
    detalhesBtns.forEach(btn => {
        btn.addEventListener('click', function(event) {
            event.preventDefault();
            alert("Detalhes da consulta!");
        });
    });

    const consultaItems = document.querySelectorAll('.consulta-item');
    consultaItems.forEach(item => {
        item.addEventListener('mouseover', function() {
            item.style.backgroundColor = '#f0f8ff';
        });
        item.addEventListener('mouseout', function() {
            item.style.backgroundColor = '#fff';
        });
    });
});
