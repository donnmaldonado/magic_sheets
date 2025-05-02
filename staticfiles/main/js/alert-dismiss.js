// This script is used to dismiss alerts when the close button is clicked
document.addEventListener('DOMContentLoaded', function() {
    // Get all close buttons in alerts
    var closeButtons = document.querySelectorAll('.alert .btn-close');
    
    // Add click handler to each button
    closeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var alert = this.closest('.alert');
            alert.remove();
        });
    });
});