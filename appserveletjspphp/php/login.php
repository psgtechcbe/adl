<?php
// Initialize variables to store error or success messages
$errorMessage = '';
$successMessage = '';

// Check if form was submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Database connection variables
    $host = 'localhost'; // or your host
    $dbname = 'loginservlet';
    $user = 'root'; // your database username
    $pass = '12345'; // your database password

    try {
        $pdo = new PDO("mysql:host=$host;dbname=$dbname", $user, $pass);

        // Always use prepared statements to prevent SQL injection
        $stmt = $pdo->prepare("SELECT * FROM login WHERE username = ? AND password = ?");
        $stmt->execute([$username, $password]);
        $user = $stmt->fetch();

        if ($user) {
            $successMessage = "Login successful!";
        } else {
            $errorMessage = "Login failed: Invalid username or password.";
        }
    } catch (PDOException $e) {
        $errorMessage = "Error connecting to the database: " . $e->getMessage();
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<div class="login-form">
    <form action="login.php" method="post">
        <h2>Login Form</h2>
        <?php
            if ($errorMessage) {
                echo "<p style='color: red;'>$errorMessage</p>";
            }
            if ($successMessage) {
                echo "<p style='color: green;'>$successMessage</p>";
            }
        ?>
        <div class="input-group">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username">
        </div>
        <div class="input-group">
            <label for="password">Password:</label>
            <input type="password" id="password" name="password">
        </div>
        <button type="submit">Login</button>
    </form>
</div>

</body>
</html>
