<?php

header("Access-Control-Allow-Origin: *");
header("Content-type: application/json");
header("Access-Control-Allow-Methods: GET, OPTIONS");

require('functions.inc.php');

// Initialize output array
$output = array(
    "error" => false,
    "string" => "",
    "answer" => 0,
    "message" => ""
);

try {
    // Check if text parameter exists
    if (!isset($_REQUEST['text'])) {
        throw new InvalidArgumentException("Missing 'text' parameter");
    }

    $text = $_REQUEST['text'];
    
    // Validate input
    $validation = validate_input($text);
    if (!$validation['valid']) {
        throw new InvalidArgumentException($validation['message']);
    }

    // Count words
    $answer = wordcount($text);
    
    $output['string'] = "Contains " . $answer . " words";
    $output['answer'] = $answer;

} catch (InvalidArgumentException $e) {
    http_response_code(400);
    $output['error'] = true;
    $output['message'] = $e->getMessage();
} catch (Exception $e) {
    http_response_code(500);
    $output['error'] = true;
    $output['message'] = "Internal server error";
    error_log($e->getMessage());
}

echo json_encode($output);
exit();