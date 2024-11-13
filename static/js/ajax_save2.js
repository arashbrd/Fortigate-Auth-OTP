document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");  // فرم را انتخاب کنید
    const saveButton = document.querySelector('input[name="_save"]');
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    console.log(form);
    console.log(saveButton);  
    console.log(csrfToken);  

    if (saveButton) {
        saveButton.addEventListener("click", function(event) {
            event.preventDefault(); // جلوگیری از ارسال فرم به صورت پیش‌فرض

            const formData = new FormData(form); // جمع‌آوری داده‌های فرم

            // ارسال درخواست AJAX
            fetch(window.location.href, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrfToken // تعیین درخواست به عنوان AJAX
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("داده‌ها با موفقیت ذخیره شدند!");
                    form.submit(); // فرم را به‌طور معمول ارسال کنید
                } else {
                    alert("خطایی رخ داده است!");
                }
            })
            .catch(error => console.error("Error:", error));
        });
    } else {
        console.log("Save button not found. Please check the button's selector.");
    }
});
