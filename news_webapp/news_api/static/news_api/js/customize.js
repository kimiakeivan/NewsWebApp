// customize.js
console.log("Script is running");
// گرفتن عناصر از DOM
const customizeButton = document.getElementById("customizeButton");
const customizeModal = document.getElementById("customizeModal");
const closeModal = document.getElementById("closeModal");



// نشان دادن مودال هنگام کلیک روی دکمه "Customize"
customizeButton.onclick = function() {
    customizeModal.style.display = "block";
}

// بستن مودال وقتی روی دکمه "×" کلیک می‌شود
closeModal.onclick = function() {
    customizeModal.style.display = "none";
}

// بستن مودال وقتی کاربر خارج از مودال کلیک کند
window.onclick = function(event) {
    if (event.target == customizeModal) {
        customizeModal.style.display = "none";
    }
}

// ارسال فرم با استفاده از جاوا اسکریپت (AJAX)
document.getElementById("customize-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const selectedCategories = Array.from(document.getElementById("categories").selectedOptions).map(option => option.value);
    const selectedCountries = Array.from(document.getElementById("countries").selectedOptions).map(option => option.value);

    // ارسال داده‌ها به سرور (با استفاده از fetch)
    fetch('/save_preferences/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,  // برای جلوگیری از حملات CSRF
        },
        body: JSON.stringify({
            categories: selectedCategories,
            countries: selectedCountries
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Preferences saved successfully!');
            customizeModal.style.display = "none";  // بستن مودال بعد از موفقیت
        } else {
            alert('There was an error saving preferences.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error.');
    });
});
