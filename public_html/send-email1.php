<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Verify reCAPTCHA response
    $recaptcha_secret = "6LdWnqwpAAAAAAVG82kSzR9Pu0ZDalGN8C96VA3O";
    $recaptcha_response = $_POST['g-recaptcha-response'];
    $recaptcha = file_get_contents("https://www.google.com/recaptcha/api/siteverify?secret=$recaptcha_secret&response=$recaptcha_response");
    $recaptcha_result = json_decode($recaptcha);
    
    if (!$recaptcha_result->success) {
        $error_message = "Please complete the CAPTCHA verification.";
    } else {
       // Get form data
    $name = $_POST["name"];
    $phone = $_POST["phone"];
    $email = $_POST["email"];
    $message = $_POST["message"];
    
    // Email details
    $to = "Jennifer_Cunneen@wycliffeassociates.org"; // Change this to your email address
    $subject = "New Contact Form Submission";
    $body = "Name: $name\nPhone: $phone\nEmail: $email\nMessage:\n$message";
    $headers = "From: $email";
    }
    // Send email
    if (mail($to, $subject, $body, $headers)) {
        echo "<p>Thank you for contacting us. We'll get back to you shortly!</p>";
    } else {
        echo "<p>Oops! Something went wrong. Please try again later.</p>";
    }
}
?>