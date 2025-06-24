function checkPasswordMatch() {
    const pwd1 = document.getElementById("password").value;
    const pwd2 = document.getElementById("cnf_password");

    if (pwd2.value !== pwd1){
        pwd2.setCustomValidity("Password doesn't match");
    }else{
        pwd2.setCustomValidity("");
    }
}

function togglePassword1() {
    const password = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon1');

    if (password.type === "password") {
        password.type = 'text'; // Show the password
        toggleIcon.classList.remove("fa-regular","fa-eye-slash");
        toggleIcon.classList.add("fa-regular","fa-eye"); // Change the icon to 'eye-slash'
    } else {
        password.type = 'password'; // Hide the password
        toggleIcon.classList.remove("fa-regular","fa-eye");
        toggleIcon.classList.add("fa-regular","fa-eye-slash"); // Change the icon to 'eye'
    }
}

function togglePassword2() {
    const password = document.getElementById('cnf_password');
    const toggleIcon = document.getElementById('toggleIcon2');

    if (password.type === "password") {
        password.type = 'text'; // Show the password
        toggleIcon.classList.remove("fa-regular","fa-eye-slash");
        toggleIcon.classList.add("fa-regular","fa-eye"); // Change the icon to 'eye-slash'
    } else {
        password.type = 'password'; // Hide the password
        toggleIcon.classList.remove("fa-regular","fa-eye");
        toggleIcon.classList.add("fa-regular","fa-eye-slash"); // Change the icon to 'eye'
    }
}

function togglePassword3() {
    const password = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon3');

    if (password.type === "password") {
        password.type = 'text'; // Show the password
        toggleIcon.classList.remove("fa-regular","fa-eye-slash");
        toggleIcon.classList.add("fa-regular","fa-eye"); // Change the icon to 'eye-slash'
    } else {
        password.type = 'password'; // Hide the password
        toggleIcon.classList.remove("fa-regular","fa-eye");
        toggleIcon.classList.add("fa-regular","fa-eye-slash"); // Change the icon to 'eye'
    }
}
