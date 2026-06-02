<?php

function wordcount($text) {
    // Check if input is null or not a string
    if ($text === null || !is_string($text)) {
        throw new InvalidArgumentException("Input must be a string");
    }

    $trimmed_text = trim($text);
    
    
    if (empty($trimmed_text)) {
        throw new InvalidArgumentException("Input string cannot be empty");
    }

    
    $normalized_text = preg_replace('/\s+/', ' ', $trimmed_text);
    
    return str_word_count($normalized_text);
}

function validate_input($text) {
    if ($text === null) {
        return [
            'valid' => false,
            'message' => 'Input cannot be null'
        ];
    }

    if (!is_string($text)) {
        return [
            'valid' => false,
            'message' => 'Input must be a string'
        ];
    }

    if (trim($text) === '') {
        return [
            'valid' => false,
            'message' => 'Input cannot be empty'
        ];
    }

    return [
        'valid' => true,
        'message' => 'Input is valid'
    ];
}